import importlib.util
from pathlib import Path
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[3]
MODULE_PATH = ROOT / "projects/vcsserg-repo-v1/analysis/publish_full_report.py"
SPEC = importlib.util.spec_from_file_location("publish_full_report", MODULE_PATH)
publish_full_report = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(publish_full_report)


class PublishFullReportTests(unittest.TestCase):
    def test_complete_build_replaces_public_tree_and_stale_files(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "book"
            public = root / "public/report"
            source.mkdir()
            public.mkdir(parents=True)
            (source / "index.html").write_text("new report", encoding="utf-8")
            (source / "report.css").write_text("new styles", encoding="utf-8")
            (source / "library.js").write_text("new library", encoding="utf-8")
            (public / "index.html").write_text("old report", encoding="utf-8")
            (public / "stale.js").write_text("stale", encoding="utf-8")

            publish_full_report.publish(source, public)

            self.assertEqual((public / "index.html").read_text(), "new report")
            self.assertTrue((public / "library.js").is_file())
            self.assertFalse((public / "stale.js").exists())

    def test_incomplete_build_leaves_existing_public_tree_unchanged(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "book"
            public = root / "public/report"
            source.mkdir()
            public.mkdir(parents=True)
            (source / "index.html").write_text("incomplete", encoding="utf-8")
            (public / "index.html").write_text("published", encoding="utf-8")

            with self.assertRaises(publish_full_report.PublicationError):
                publish_full_report.publish(source, public)

            self.assertEqual((public / "index.html").read_text(), "published")


if __name__ == "__main__":
    unittest.main()
