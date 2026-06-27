import importlib.util
import pathlib
import sys
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("vercel_clean_csv", ROOT / "api" / "clean_csv.py")
vercel_clean_csv = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules["vercel_clean_csv"] = vercel_clean_csv
SPEC.loader.exec_module(vercel_clean_csv)


class VercelFunctionTests(unittest.TestCase):
    def test_vercel_clean_csv_exports_request_handler(self):
        self.assertTrue(hasattr(vercel_clean_csv, "handler"))
        self.assertTrue(hasattr(vercel_clean_csv.handler, "do_POST"))
        self.assertTrue(hasattr(vercel_clean_csv.handler, "do_OPTIONS"))


if __name__ == "__main__":
    unittest.main()
