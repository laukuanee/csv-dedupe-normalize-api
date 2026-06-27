import csv
import importlib.util
import json
import pathlib
import sys
import tempfile
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("csv_cleaner", ROOT / "csv_cleaner.py")
cleaner = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules["csv_cleaner"] = cleaner
SPEC.loader.exec_module(cleaner)


class CsvCleanerTests(unittest.TestCase):
    def test_normalizes_headers_and_makes_them_unique(self):
        self.assertEqual(
            cleaner.unique_headers([" Full Name ", "Email Address", "Email Address"]),
            ["full_name", "email_address", "email_address_2"],
        )

    def test_cleans_rows_and_writes_report(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = pathlib.Path(temp_dir)
            source = root / "messy.csv"
            output = root / "cleaned.csv"
            report = root / "report.json"
            source.write_text(
                "Full Name, Email Address, Email Address, Signup Date\n"
                " Alice Example , alice@example.com , alice@example.com, 2026-06-01\n"
                "Alice Example,alice@example.com,alice@example.com,2026-06-01\n"
                ",,,\n"
                "Charlie Example,charlie@example.com,charlie@example.com,2026-06-03,overflow\n",
                encoding="utf-8",
            )

            summary = cleaner.clean_csv(source, output, report)

            with output.open("r", encoding="utf-8", newline="") as handle:
                rows = list(csv.reader(handle))
            saved_report = json.loads(report.read_text(encoding="utf-8"))

            self.assertEqual(rows[0], ["full_name", "email_address", "email_address_2", "signup_date", "extra_1"])
            self.assertEqual(summary["duplicate_rows_removed"], 1)
            self.assertEqual(saved_report["empty_rows_removed"], 1)
            self.assertEqual(saved_report["wide_rows_extended"], 1)
            self.assertEqual(saved_report["output_rows"], 2)


if __name__ == "__main__":
    unittest.main()
