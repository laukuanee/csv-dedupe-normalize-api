#!/usr/bin/env python3
"""Small HTTP API wrapper for the CSV cleaner MVP."""

from __future__ import annotations

import argparse
import json
import sys
import tempfile
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from csv_cleaner import clean_csv  # noqa: E402


DEFAULT_MAX_BYTES = 1_000_000


def error_payload(code: str, message: str) -> dict[str, Any]:
    return {"error": {"code": code, "message": message}}


def success_report(report: dict[str, Any]) -> dict[str, Any]:
    return {
        "input_rows": report["input_rows"],
        "output_rows": report["output_rows"],
        "input_columns": report["input_columns"],
        "output_columns": report["output_columns"],
        "columns": report["columns"],
        "duplicate_rows_removed": report["duplicate_rows_removed"],
        "empty_rows_removed": report["empty_rows_removed"],
        "short_rows_padded": report["short_rows_padded"],
        "wide_rows_extended": report["wide_rows_extended"],
    }


def validate_key_columns(value: Any) -> list[str] | None:
    if value is None:
        return None
    if not isinstance(value, list) or not all(isinstance(item, str) and item.strip() for item in value):
        raise ValueError("key_columns must be an array of non-empty column names")
    return [item.strip() for item in value]


def clean_csv_text(csv_text: str, key_columns: list[str] | None = None) -> tuple[str, dict[str, Any]]:
    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        source = root / "input.csv"
        output = root / "cleaned.csv"
        report_path = root / "report.json"
        source.write_text(csv_text, encoding="utf-8")
        report = clean_csv(source, output, report_path, key_columns)
        return output.read_text(encoding="utf-8"), success_report(report)


def handle_clean_csv_json(body: bytes, max_bytes: int = DEFAULT_MAX_BYTES) -> tuple[int, dict[str, Any]]:
    if len(body) > max_bytes:
        return 413, error_payload("payload_too_large", f"Request body exceeds {max_bytes} bytes")

    try:
        data = json.loads(body.decode("utf-8"))
    except UnicodeDecodeError:
        return 400, error_payload("invalid_encoding", "Request body must be UTF-8 encoded")
    except json.JSONDecodeError as exc:
        return 400, error_payload("invalid_json", f"Request body is not valid JSON: {exc.msg}")

    csv_text = data.get("csv_text") if isinstance(data, dict) else None
    if not isinstance(csv_text, str) or not csv_text.strip():
        return 400, error_payload("missing_csv_text", "Provide a non-empty csv_text field")

    try:
        key_columns = validate_key_columns(data.get("key_columns"))
        cleaned_csv, report = clean_csv_text(csv_text, key_columns)
    except ValueError as exc:
        message = str(exc)
        if message.startswith("Key columns not found"):
            return 400, error_payload("invalid_key_columns", message)
        return 400, error_payload("invalid_csv", message)

    return 200, {"cleaned_csv": cleaned_csv, "report": report}


class CsvCleanerHandler(BaseHTTPRequestHandler):
    server_version = "CsvCleanerApi/0.1"

    def do_GET(self) -> None:
        if self.path == "/healthz":
            self.write_json(200, {"ok": True, "service": "csv-dedupe-normalize-api"})
            return
        self.write_json(404, error_payload("not_found", "Endpoint not found"))

    def do_POST(self) -> None:
        if self.path != "/clean-csv":
            self.write_json(404, error_payload("not_found", "Endpoint not found"))
            return

        content_type = self.headers.get("Content-Type", "")
        if "application/json" not in content_type:
            self.write_json(400, error_payload("unsupported_content_type", "Use application/json with csv_text"))
            return

        content_length = int(self.headers.get("Content-Length", "0") or "0")
        max_bytes = getattr(self.server, "max_bytes", DEFAULT_MAX_BYTES)
        if content_length > max_bytes:
            self.rfile.read(min(content_length, max_bytes + 1))
            self.write_json(413, error_payload("payload_too_large", f"Request body exceeds {max_bytes} bytes"))
            return

        body = self.rfile.read(content_length)
        status, payload = handle_clean_csv_json(body, max_bytes=max_bytes)
        self.write_json(status, payload)

    def write_json(self, status: int, payload: dict[str, Any]) -> None:
        body = json.dumps(payload, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="127.0.0.1", help="Host interface to bind")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind")
    parser.add_argument("--max-bytes", type=int, default=DEFAULT_MAX_BYTES, help="Maximum JSON request body size")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    server = ThreadingHTTPServer((args.host, args.port), CsvCleanerHandler)
    server.max_bytes = args.max_bytes
    print(f"csv-cleaner API listening on http://{args.host}:{args.port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nshutting down")
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
