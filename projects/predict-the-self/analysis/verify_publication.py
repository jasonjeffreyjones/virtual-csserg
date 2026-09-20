#!/usr/bin/env python3
"""Validate Predict the Self's three-form publication and PDF layout."""

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

from pypdf import PdfReader


PROJECT = Path(__file__).resolve().parents[1]
ROOT = PROJECT.parents[1]
PUBLIC = ROOT / "website/projects/predict-the-self"


class Page(HTMLParser):
    def __init__(self, text: str):
        super().__init__()
        self.figures = 0
        self.ids = set()
        self.links = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == "figure":
            self.figures += 1
        if attributes.get("id"):
            self.ids.add(attributes["id"])
        for name in ("href", "src"):
            if attributes.get(name):
                self.links.append(attributes[name])


def resolve_local(path: Path, link: str) -> tuple[Path | None, str]:
    parsed = urlsplit(link)
    if parsed.scheme or parsed.netloc:
        return None, parsed.fragment
    target = (path.parent / unquote(parsed.path)).resolve() if parsed.path else path
    if target.is_dir():
        target = target / "index.html"
    return target, parsed.fragment


def validate_local_links(path: Path, page: Page) -> None:
    for link in page.links:
        target, fragment = resolve_local(path, link)
        if target is None:
            continue
        assert target.is_file(), f"{path.name}: missing local target {link}"
        if fragment and target.suffix.lower() == ".html":
            target_page = Page(target.read_text(encoding="utf-8"))
            assert fragment in target_page.ids, f"{path.name}: missing fragment {link}"


def local_targets(path: Path, page: Page) -> set[Path]:
    return {
        target
        for link in page.links
        for target, _ in [resolve_local(path, link)]
        if target is not None
    }


def main() -> int:
    summary_path = PUBLIC / "index.html"
    landing_path = PUBLIC / "report/index.html"
    evidence_path = PUBLIC / "report/report.html"
    short_path = PUBLIC / "short-report.pdf"
    for required in (summary_path, landing_path, evidence_path, short_path):
        assert required.is_file(), f"missing publication artifact {required}"

    summary = Page(summary_path.read_text(encoding="utf-8"))
    landing_source = landing_path.read_text(encoding="utf-8")
    evidence_source = evidence_path.read_text(encoding="utf-8")
    landing = Page(landing_source)
    evidence = Page(evidence_source)

    assert summary.figures == 1, f"Executive Summary figures: {summary.figures}"
    phrase_count = (landing_source + evidence_source).lower().count("far beyond")
    assert phrase_count == 1, f"Full Report phrase count: {phrase_count}"
    for path, page in (
        (summary_path, summary),
        (landing_path, landing),
        (evidence_path, evidence),
    ):
        validate_local_links(path, page)

    assert landing_path.resolve() in local_targets(summary_path, summary)
    assert short_path.resolve() in local_targets(summary_path, summary)
    assert summary_path.resolve() in local_targets(landing_path, landing)
    assert short_path.resolve() in local_targets(landing_path, landing)

    expected_artifacts = {
        PUBLIC / "report/ANALYSIS_PLAN_SOURCE_CONDITIONED_ADDITIONS.md",
        PUBLIC / "report/ANALYSIS_PLAN_TRAJECTORY_RETRIEVAL.md",
        PUBLIC / "report/BENCHMARK_PROVENANCE.md",
        PUBLIC / "report/analysis/analyze_dev_diagnostics.py",
        PUBLIC / "report/analysis/analyze_novelty_prior.py",
        PUBLIC / "report/analysis/analyze_source_conditioned_additions.py",
        PUBLIC / "report/analysis/analyze_trajectory_retrieval.py",
        PUBLIC / "report/analysis/stable_signifier_projection.py",
        PUBLIC / "report/analysis/trajectory_retrieval.py",
        PUBLIC / "report/results/novelty_prior_dev_analysis.json",
        PUBLIC / "report/results/novelty_prior_token_audit.csv",
        PUBLIC / "report/results/source_conditioned_additions_train_analysis.json",
        PUBLIC / "report/results/source_conditioned_additions_train_audit.csv",
        PUBLIC / "report/results/stable_signifier_dev_diagnostics.json",
        PUBLIC / "report/results/stable_signifier_dev_predictions.csv",
        PUBLIC / "report/results/stable_signifier_dev_scorecard.json",
        PUBLIC / "report/results/trajectory_retrieval_dev_analysis.json",
        PUBLIC / "report/results/trajectory_retrieval_dev_audit.csv",
        PUBLIC / "report/results/trajectory_retrieval_dev_predictions.csv",
        PUBLIC / "report/results/trajectory_retrieval_dev_scorecard.json",
        PUBLIC / "report/submissions/aleph_initial_alpha_submission.csv",
        PUBLIC / "report/submissions/aleph_initial_alpha_method.md",
    }
    evidence_targets = local_targets(evidence_path, evidence)
    assert expected_artifacts <= evidence_targets, "Full Report omits public artifacts"
    for source, legacy in (
        ("ANALYSIS_PLAN_SOURCE_CONDITIONED_ADDITIONS.md", "artifacts/ANALYSIS_PLAN_SOURCE_CONDITIONED_ADDITIONS.md"),
        ("ANALYSIS_PLAN_TRAJECTORY_RETRIEVAL.md", "artifacts/ANALYSIS_PLAN_TRAJECTORY_RETRIEVAL.md"),
        ("BENCHMARK_PROVENANCE.md", "artifacts/BENCHMARK_PROVENANCE.md"),
        ("analysis/analyze_dev_diagnostics.py", "artifacts/analyze_dev_diagnostics.py"),
        ("analysis/analyze_novelty_prior.py", "artifacts/analyze_novelty_prior.py"),
        ("analysis/analyze_source_conditioned_additions.py", "artifacts/analyze_source_conditioned_additions.py"),
        ("analysis/analyze_trajectory_retrieval.py", "artifacts/analyze_trajectory_retrieval.py"),
        ("analysis/stable_signifier_projection.py", "artifacts/stable_signifier_projection.py"),
        ("analysis/trajectory_retrieval.py", "artifacts/trajectory_retrieval.py"),
        ("results/novelty_prior_dev_analysis.json", "artifacts/novelty_prior_dev_analysis.json"),
        ("results/novelty_prior_token_audit.csv", "artifacts/novelty_prior_token_audit.csv"),
        ("results/source_conditioned_additions_train_analysis.json", "artifacts/source_conditioned_additions_train_analysis.json"),
        ("results/source_conditioned_additions_train_audit.csv", "artifacts/source_conditioned_additions_train_audit.csv"),
        ("results/stable_signifier_dev_diagnostics.json", "artifacts/stable_signifier_dev_diagnostics.json"),
        ("results/stable_signifier_dev_predictions.csv", "artifacts/stable_signifier_dev_predictions.csv"),
        ("results/stable_signifier_dev_scorecard.json", "artifacts/stable_signifier_dev_scorecard.json"),
        ("results/trajectory_retrieval_dev_analysis.json", "artifacts/trajectory_retrieval_dev_analysis.json"),
        ("results/trajectory_retrieval_dev_audit.csv", "artifacts/trajectory_retrieval_dev_audit.csv"),
        ("results/trajectory_retrieval_dev_predictions.csv", "artifacts/trajectory_retrieval_dev_predictions.csv"),
        ("results/trajectory_retrieval_dev_scorecard.json", "artifacts/trajectory_retrieval_dev_scorecard.json"),
        ("submissions/aleph_initial_alpha_submission.csv", "artifacts/aleph_initial_alpha_submission.csv"),
        ("submissions/aleph_initial_alpha_method.md", "artifacts/aleph_initial_alpha_method.md"),
    ):
        assert (PUBLIC / "report" / source).read_bytes() == (
            PUBLIC / "report" / legacy
        ).read_bytes(), f"legacy artifact alias differs: {legacy}"

    pdf = PdfReader(short_path)
    assert 1 <= len(pdf.pages) <= 10, f"PDF pages: {len(pdf.pages)}"
    columns = set()
    annotations = 0
    for page in pdf.pages:
        assert page.extract_text().strip(), "empty PDF page"
        annotations += len(page.get("/Annots", []))

        def visit(text, cm, tm, _font, _size):
            x = cm[4] + tm[4]
            y = cm[5] + tm[5]
            if text.strip() and y > 40:
                if 35 <= x < 295:
                    columns.add("left")
                elif 295 <= x <= 570:
                    columns.add("right")

        page.extract_text(visitor_text=visit)
    assert columns == {"left", "right"}, f"PDF body columns found: {columns}"
    assert annotations >= 5, f"PDF link annotations found: {annotations}"

    print(
        "Predict the Self publication: one summary figure, two-chapter linked "
        f"Full Report, artifacts, required phrase, and {len(pdf.pages)}-page "
        "two-column PDF passed."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
