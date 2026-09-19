import importlib.util
from pathlib import Path
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[3]
MODULE_PATH = ROOT / "projects/predict-the-self/analysis/publish_full_report.py"
SPEC = importlib.util.spec_from_file_location("predict_publish_full_report", MODULE_PATH)
publish_full_report = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(publish_full_report)


def make_complete_build(source: Path) -> None:
    files = (
        "index.html",
        "report.html",
        "report.css",
        "ANALYSIS_PLAN_TRAJECTORY_RETRIEVAL.md",
        "BENCHMARK_PROVENANCE.md",
        "analysis/analyze_dev_diagnostics.py",
        "analysis/analyze_novelty_prior.py",
        "analysis/analyze_trajectory_retrieval.py",
        "analysis/stable_signifier_projection.py",
        "analysis/trajectory_retrieval.py",
        "results/novelty_prior_dev_analysis.json",
        "results/novelty_prior_token_audit.csv",
        "results/stable_signifier_dev_diagnostics.json",
        "results/stable_signifier_dev_predictions.csv",
        "results/stable_signifier_dev_scorecard.json",
        "results/trajectory_retrieval_dev_analysis.json",
        "results/trajectory_retrieval_dev_audit.csv",
        "results/trajectory_retrieval_dev_predictions.csv",
        "results/trajectory_retrieval_dev_scorecard.json",
        "submissions/aleph_initial_alpha_submission.csv",
        "submissions/aleph_initial_alpha_method.md",
    )
    for relative in files:
        path = source / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"new {relative}", encoding="utf-8")


class PublishFullReportTests(unittest.TestCase):
    def test_complete_build_replaces_public_tree_and_stale_files(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "book"
            public = root / "public/report"
            source.mkdir()
            public.mkdir(parents=True)
            make_complete_build(source)
            (source / "index.html").write_text("new index.html  \n", encoding="utf-8")
            (public / "index.html").write_text("old report", encoding="utf-8")
            (public / "stale.js").write_text("stale", encoding="utf-8")

            publish_full_report.publish(source, public)

            self.assertEqual((public / "index.html").read_text(), "new index.html\n")
            self.assertTrue((public / "report.html").is_file())
            self.assertEqual(
                (public / "artifacts/aleph_initial_alpha_submission.csv").read_text(),
                "new submissions/aleph_initial_alpha_submission.csv",
            )
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
