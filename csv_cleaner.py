#!/usr/bin/env python3
"""Clean a CSV by normalizing headers, trimming rows, and removing duplicates."""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path
from typing import Any


def normalize_header(value: str) -> str:
    header = value.strip().lower()
    header = re.sub(r"[^a-z0-9]+", "_", header)
    header = re.sub(r"_+", "_", header).strip("_")
    return header or "column"


def unique_headers(raw_headers: list[str]) -> list[str]:
    counts: dict[str, int] = {}
    result: list[str] = []
    for raw in raw_headers:
        base = normalize_header(raw)
        counts[base] = counts.get(base, 0) + 1
        if counts[base] == 1:
            result.append(base)
        else:
            result.append(f"{base}_{counts[base]}")
    return result


def is_empty_row(row: list[str]) -> bool:
    return all(cell.strip() == "" for cell in row)


def normalize_cell(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip())


def read_csv(path: Path) -> tuple[list[str], list[list[str]]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.reader(handle))
    if not rows:
        raise ValueError("CSV is empty")
    return rows[0], rows[1:]


def repair_rows(headers: list[str], rows: list[list[str]]) -> tuple[list[str], list[list[str]], dict[str, int]]:
    repaired_headers = list(headers)
    repaired_rows: list[list[str]] = []
    stats = {"empty_rows_removed": 0, "short_rows_padded": 0, "wide_rows_extended": 0}

    for row in rows:
        if is_empty_row(row):
            stats["empty_rows_removed"] += 1
            continue
        clean_row = [normalize_cell(cell) for cell in row]
        if len(clean_row) < len(repaired_headers):
            clean_row.extend([""] * (len(repaired_headers) - len(clean_row)))
            stats["short_rows_padded"] += 1
        elif len(clean_row) > len(repaired_headers):
            overflow = len(clean_row) - len(repaired_headers)
            for index in range(overflow):
                repaired_headers.append(f"extra_{index + 1}")
            stats["wide_rows_extended"] += 1
            for existing in repaired_rows:
                existing.extend([""] * overflow)
        repaired_rows.append(clean_row)

    return repaired_headers, repaired_rows, stats


def dedupe_rows(headers: list[str], rows: list[list[str]], key_columns: list[str] | None = None) -> tuple[list[list[str]], int]:
    if key_columns:
        missing = [column for column in key_columns if column not in headers]
        if missing:
            raise ValueError(f"Key columns not found: {', '.join(missing)}")
        key_indexes = [headers.index(column) for column in key_columns]
    else:
        key_indexes = list(range(len(headers)))

    seen: set[tuple[str, ...]] = set()
    deduped: list[list[str]] = []
    duplicates = 0
    for row in rows:
        key = tuple(row[index] if index < len(row) else "" for index in key_indexes)
        if key in seen:
            duplicates += 1
            continue
        seen.add(key)
        deduped.append(row)
    return deduped, duplicates


def clean_csv(input_path: Path, output_path: Path, report_path: Path, key_columns: list[str] | None = None) -> dict[str, Any]:
    raw_headers, raw_rows = read_csv(input_path)
    headers = unique_headers(raw_headers)
    repaired_headers, repaired_rows, repair_stats = repair_rows(headers, raw_rows)
    deduped_rows, duplicate_rows_removed = dedupe_rows(repaired_headers, repaired_rows, key_columns)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(repaired_headers)
        writer.writerows(deduped_rows)

    report = {
        "input_file": str(input_path),
        "output_file": str(output_path),
        "input_rows": len(raw_rows),
        "output_rows": len(deduped_rows),
        "input_columns": len(raw_headers),
        "output_columns": len(repaired_headers),
        "columns": repaired_headers,
        "duplicate_rows_removed": duplicate_rows_removed,
        **repair_stats,
    }
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return report


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", help="Input CSV path")
    parser.add_argument("--out", required=True, help="Cleaned output CSV path")
    parser.add_argument("--report", required=True, help="Cleanup report JSON path")
    parser.add_argument("--key", action="append", default=None, help="Column to use for dedupe; repeat for composite keys")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    try:
        report = clean_csv(Path(args.input), Path(args.out), Path(args.report), args.key)
    except Exception as exc:
        print(f"csv-cleaner error: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
