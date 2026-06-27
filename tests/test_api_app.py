import csv
import importlib.util
import json
import pathlib
import sys
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("api_app", ROOT / "api_app.py")
api_app = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules["api_app"] = api_app
SPEC.loader.exec_module(api_app)


class ApiAppTests(unittest.TestCase):
    def test_clean_csv_json_returns_cleaned_csv_and_report(self):
        body = json.dumps(
            {
                "csv_text": "Full Name,Email\n Alice , alice@example.com\nAlice,alice@example.com\n",
                "key_columns": ["full_name", "email"],
            }
        ).encode("utf-8")

        status, payload = api_app.handle_clean_csv_json(body, max_bytes=10_000)

        self.assertEqual(status, 200)
        self.assertIn("cleaned_csv", payload)
        self.assertIn("report", payload)
        rows = list(csv.reader(payload["cleaned_csv"].splitlines()))
        self.assertEqual(rows, [["full_name", "email"], ["Alice", "alice@example.com"]])
        self.assertEqual(payload["report"]["duplicate_rows_removed"], 1)

    def test_clean_csv_json_rejects_missing_csv_text(self):
        status, payload = api_app.handle_clean_csv_json(b"{}", max_bytes=10_000)

        self.assertEqual(status, 400)
        self.assertEqual(payload["error"]["code"], "missing_csv_text")

    def test_clean_csv_json_rejects_unknown_key_column(self):
        body = json.dumps(
            {
                "csv_text": "Full Name,Email\nAlice,alice@example.com\n",
                "key_columns": ["not_a_column"],
            }
        ).encode("utf-8")

        status, payload = api_app.handle_clean_csv_json(body, max_bytes=10_000)

        self.assertEqual(status, 400)
        self.assertEqual(payload["error"]["code"], "invalid_key_columns")
        self.assertIn("not_a_column", payload["error"]["message"])

    def test_clean_csv_json_rejects_oversized_payload(self):
        status, payload = api_app.handle_clean_csv_json(b"x" * 20, max_bytes=10)

        self.assertEqual(status, 413)
        self.assertEqual(payload["error"]["code"], "payload_too_large")


if __name__ == "__main__":
    unittest.main()
