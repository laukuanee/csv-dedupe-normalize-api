from __future__ import annotations

import json
import sys
from http.server import BaseHTTPRequestHandler
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from api_app import DEFAULT_MAX_BYTES, error_payload, handle_clean_csv_json  # noqa: E402


class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self) -> None:
        self.send_response(204)
        self.add_cors_headers()
        self.end_headers()

    def do_POST(self) -> None:
        content_length = int(self.headers.get("Content-Length", "0") or "0")
        if content_length > DEFAULT_MAX_BYTES:
            self.rfile.read(min(content_length, DEFAULT_MAX_BYTES + 1))
            self.write_json(413, error_payload("payload_too_large", f"Request body exceeds {DEFAULT_MAX_BYTES} bytes"))
            return

        body = self.rfile.read(content_length)
        status, payload = handle_clean_csv_json(body, max_bytes=DEFAULT_MAX_BYTES)
        self.write_json(status, payload)

    def do_GET(self) -> None:
        self.write_json(200, {"ok": True, "endpoint": "/api/clean_csv", "method": "POST"})

    def add_cors_headers(self) -> None:
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def write_json(self, status: int, payload: dict) -> None:
        body = json.dumps(payload, indent=2).encode("utf-8")
        self.send_response(status)
        self.add_cors_headers()
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
