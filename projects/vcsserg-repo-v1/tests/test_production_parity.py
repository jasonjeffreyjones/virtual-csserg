import importlib.util
from pathlib import Path
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[3]
MODULE_PATH = ROOT / "projects/vcsserg-repo-v1/analysis/check_production_parity.py"
SPEC = importlib.util.spec_from_file_location("check_production_parity", MODULE_PATH)
parity = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(parity)


class FakeResponse:
    def __init__(self, body):
        self.body = body

    def __enter__(self):
        return self

    def __exit__(self, *_):
        return False

    def read(self):
        return self.body


class ProductionParityTests(unittest.TestCase):
    def test_reports_identical_different_and_unavailable_files(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "same.txt").write_bytes(b"same")
            (root / "different.txt").write_bytes(b"local")
            (root / "missing.txt").write_bytes(b"missing")

            responses = {
                "https://example.test/different.txt": b"remote",
                "https://example.test/same.txt": b"same",
            }

            def fetch(request, timeout):
                self.assertEqual(20, timeout)
                if request.full_url not in responses:
                    raise OSError("not found")
                return FakeResponse(responses[request.full_url])

            comparisons = parity.compare_site(root, "https://example.test/", fetch)
            statuses = {item.relative_path: item.status for item in comparisons}
            self.assertEqual("identical", statuses["same.txt"])
            self.assertEqual("different", statuses["different.txt"])
            self.assertEqual("unavailable", statuses["missing.txt"])

    def test_requires_directory_style_base_url(self):
        with tempfile.TemporaryDirectory() as temporary:
            with self.assertRaisesRegex(ValueError, "end with"):
                parity.compare_site(temporary, "https://example.test")


if __name__ == "__main__":
    unittest.main()
