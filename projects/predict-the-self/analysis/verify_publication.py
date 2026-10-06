#!/usr/bin/env python3
"""Validate Predict the Self's three-form publication and PDF layout."""

from html.parser import HTMLParser
import json
from pathlib import Path, PureWindowsPath
from urllib.parse import unquote, urlsplit

PROJECT = Path(__file__).resolve().parents[1]
ROOT = PROJECT.parents[1]
PUBLIC = ROOT / "website/projects/predict-the-self"
PUBLIC_PROJECT_URL = (
    "https://jasonjones.ninja/virtual-csserg/projects/predict-the-self/"
)
PUBLIC_REPORT_URL = PUBLIC_PROJECT_URL + "report/"


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


def validate_reciprocal_html_links(
    summary_path: Path,
    summary: Page,
    landing_path: Path,
    landing: Page,
    evidence_path: Path,
    evidence: Page,
    short_path: Path,
) -> None:
    """Require every HTML report surface to link to the other report forms."""
    summary_targets = local_targets(summary_path, summary)
    landing_targets = local_targets(landing_path, landing)
    evidence_targets = local_targets(evidence_path, evidence)
    assert landing_path.resolve() in summary_targets, (
        "Executive Summary omits Full Report landing page"
    )
    assert short_path.resolve() in summary_targets, (
        "Executive Summary omits short report"
    )
    for label, targets in (
        ("Full Report landing page", landing_targets),
        ("Full Report evidence chapter", evidence_targets),
    ):
        assert summary_path.resolve() in targets, f"{label} omits Executive Summary"
        assert short_path.resolve() in targets, f"{label} omits short report"


def pdf_external_uris(pdf) -> set[str]:
    """Collect external URI actions from every annotation in a PDF reader."""
    uris = set()
    for page in pdf.pages:
        for reference in page.get("/Annots", []):
            annotation = reference.get_object()
            action = annotation.get("/A")
            if hasattr(action, "get_object"):
                action = action.get_object()
            uri = action.get("/URI") if action else None
            if uri:
                uris.add(str(uri))
    return uris


def validate_pdf_report_links(pdf) -> None:
    """Require the short PDF to link back to both public HTML report forms."""
    uris = pdf_external_uris(pdf)
    expected = {PUBLIC_PROJECT_URL, PUBLIC_REPORT_URL}
    missing = sorted(expected - uris)
    assert not missing, f"short report omits reciprocal links: {', '.join(missing)}"


def validate_artifact_copy(source: Path, canonical: Path, alias: Path) -> None:
    """Require both public copies to equal the authoritative Project source."""
    expected = source.read_bytes()
    assert canonical.read_bytes() == expected, (
        f"published artifact differs from Project source: {canonical}"
    )
    assert alias.read_bytes() == expected, (
        f"published artifact alias differs from Project source: {alias}"
    )


def validate_scorecard_provenance(scorecard: dict[str, object]) -> None:
    """Reject machine-specific paths from public scorecard provenance."""
    for field in ("predictions", "references"):
        value = scorecard.get(field)
        assert isinstance(value, str) and value, f"scorecard {field} is missing"
        parsed = urlsplit(value)
        assert parsed.scheme != "file", f"scorecard {field} uses a file URI: {value}"
        assert not Path(value).is_absolute(), (
            f"scorecard {field} exposes an absolute host path: {value}"
        )
        assert not PureWindowsPath(value).is_absolute(), (
            f"scorecard {field} exposes an absolute host path: {value}"
        )


def main() -> int:
    from pypdf import PdfReader

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

    validate_reciprocal_html_links(
        summary_path,
        summary,
        landing_path,
        landing,
        evidence_path,
        evidence,
        short_path,
    )

    expected_artifacts = {
        PUBLIC / "report/ANALYSIS_PLAN_CALIBRATED_SYNTHESIS.md",
        PUBLIC / "report/ANALYSIS_PLAN_SEMANTIC_NEIGHBORHOOD_ADDITIONS.md",
        PUBLIC / "report/ANALYSIS_PLAN_RESPONSE_LENGTH_PERSISTENCE.md",
        PUBLIC / "report/ANALYSIS_PLAN_RESPONSE_LENGTH_DECOMPOSITION.md",
        PUBLIC / "report/ANALYSIS_PLAN_RESPONSE_LENGTH_SHRINKAGE.md",
        PUBLIC / "report/ANALYSIS_PLAN_CHANGE_DISTRIBUTIONS.md",
        PUBLIC / "report/ANALYSIS_PLAN_CHANGE_VOLUME.md",
        PUBLIC / "report/ANALYSIS_PLAN_FEATURE_ABLATION.md",
        PUBLIC / "report/ANALYSIS_PLAN_MULTIPLICITY_STRESS_TEST.md",
        PUBLIC / "report/ANALYSIS_PLAN_SOURCE_FORM_ABLATION.md",
        PUBLIC / "report/ANALYSIS_PLAN_NEIGHBORHOOD_ADDITIONS.md",
        PUBLIC / "report/ANALYSIS_PLAN_SOURCE_CONDITIONED_ADDITIONS.md",
        PUBLIC / "report/ANALYSIS_PLAN_STABLE_PROJECTION_CROSS_VALIDATION.md",
        PUBLIC / "report/ANALYSIS_PLAN_TRAJECTORY_RETRIEVAL.md",
        PUBLIC / "report/BENCHMARK_PROVENANCE.md",
        PUBLIC / "report/analysis/analyze_change_distributions.py",
        PUBLIC / "report/analysis/analyze_calibrated_synthesis.py",
        PUBLIC / "report/analysis/analyze_semantic_neighborhood_additions.py",
        PUBLIC / "report/analysis/analyze_response_length_persistence.py",
        PUBLIC / "report/analysis/analyze_response_length_shrinkage.py",
        PUBLIC / "report/analysis/analyze_change_volume.py",
        PUBLIC / "report/analysis/analyze_feature_ablation.py",
        PUBLIC / "report/analysis/analyze_multiplicity_stress_test.py",
        PUBLIC / "report/analysis/analyze_source_form_ablation.py",
        PUBLIC / "report/analysis/analyze_dev_diagnostics.py",
        PUBLIC / "report/analysis/analyze_neighborhood_additions.py",
        PUBLIC / "report/analysis/analyze_novelty_prior.py",
        PUBLIC / "report/analysis/analyze_source_conditioned_additions.py",
        PUBLIC / "report/analysis/analyze_stable_projection_cross_validation.py",
        PUBLIC / "report/analysis/analyze_trajectory_retrieval.py",
        PUBLIC / "report/analysis/stable_signifier_projection.py",
        PUBLIC / "report/analysis/trajectory_retrieval.py",
        PUBLIC / "report/results/change_distributions_train_analysis.json",
        PUBLIC / "report/results/change_distributions_train_audit.csv",
        PUBLIC / "report/results/calibrated_synthesis_train_analysis.json",
        PUBLIC / "report/results/calibrated_synthesis_train_audit.csv",
        PUBLIC / "report/results/calibrated_synthesis_train_predictions.csv",
        PUBLIC / "report/results/change_volume_train_analysis.json",
        PUBLIC / "report/results/change_volume_train_audit.csv",
        PUBLIC / "report/results/feature_ablation_train_analysis.json",
        PUBLIC / "report/results/feature_ablation_train_audit.csv",
        PUBLIC / "report/results/multiplicity_stress_test_train_analysis.json",
        PUBLIC / "report/results/multiplicity_stress_test_train_audit.csv",
        PUBLIC / "report/results/source_form_ablation_train_analysis.json",
        PUBLIC / "report/results/source_form_ablation_train_audit.csv",
        PUBLIC / "report/results/semantic_neighborhood_additions_train_analysis.json",
        PUBLIC / "report/results/semantic_neighborhood_additions_train_audit.csv",
        PUBLIC / "report/results/response_length_persistence_train_analysis.json",
        PUBLIC / "report/results/response_length_persistence_train_audit.csv",
        PUBLIC / "report/results/response_length_shrinkage_train_analysis.json",
        PUBLIC / "report/results/response_length_shrinkage_train_audit.csv",
        PUBLIC / "report/results/neighborhood_additions_train_analysis.json",
        PUBLIC / "report/results/neighborhood_additions_train_audit.csv",
        PUBLIC / "report/results/novelty_prior_dev_analysis.json",
        PUBLIC / "report/results/novelty_prior_token_audit.csv",
        PUBLIC / "report/results/source_conditioned_additions_train_analysis.json",
        PUBLIC / "report/results/source_conditioned_additions_train_audit.csv",
        PUBLIC / "report/results/stable_signifier_dev_diagnostics.json",
        PUBLIC / "report/results/stable_signifier_dev_predictions.csv",
        PUBLIC / "report/results/stable_signifier_dev_scorecard.json",
        PUBLIC / "report/results/stable_projection_train_cv_analysis.json",
        PUBLIC / "report/results/stable_projection_train_cv_predictions.csv",
        PUBLIC / "report/results/trajectory_retrieval_dev_analysis.json",
        PUBLIC / "report/results/trajectory_retrieval_dev_audit.csv",
        PUBLIC / "report/results/trajectory_retrieval_dev_predictions.csv",
        PUBLIC / "report/results/trajectory_retrieval_dev_scorecard.json",
        PUBLIC / "report/submissions/aleph_initial_alpha_submission.csv",
        PUBLIC / "report/submissions/aleph_initial_alpha_method.md",
    }
    for scorecard_name in (
        "stable_signifier_dev_scorecard.json",
        "trajectory_retrieval_dev_scorecard.json",
    ):
        with (PROJECT / "results" / scorecard_name).open(encoding="utf-8") as handle:
            validate_scorecard_provenance(json.load(handle))
    evidence_targets = local_targets(evidence_path, evidence)
    assert expected_artifacts <= evidence_targets, "Full Report omits public artifacts"
    for source, legacy in (
        ("ANALYSIS_PLAN_CALIBRATED_SYNTHESIS.md", "artifacts/ANALYSIS_PLAN_CALIBRATED_SYNTHESIS.md"),
        ("ANALYSIS_PLAN_SEMANTIC_NEIGHBORHOOD_ADDITIONS.md", "artifacts/ANALYSIS_PLAN_SEMANTIC_NEIGHBORHOOD_ADDITIONS.md"),
        ("ANALYSIS_PLAN_RESPONSE_LENGTH_PERSISTENCE.md", "artifacts/ANALYSIS_PLAN_RESPONSE_LENGTH_PERSISTENCE.md"),
        ("ANALYSIS_PLAN_RESPONSE_LENGTH_DECOMPOSITION.md", "artifacts/ANALYSIS_PLAN_RESPONSE_LENGTH_DECOMPOSITION.md"),
        ("ANALYSIS_PLAN_RESPONSE_LENGTH_SHRINKAGE.md", "artifacts/ANALYSIS_PLAN_RESPONSE_LENGTH_SHRINKAGE.md"),
        ("ANALYSIS_PLAN_CHANGE_DISTRIBUTIONS.md", "artifacts/ANALYSIS_PLAN_CHANGE_DISTRIBUTIONS.md"),
        ("ANALYSIS_PLAN_CHANGE_VOLUME.md", "artifacts/ANALYSIS_PLAN_CHANGE_VOLUME.md"),
        ("ANALYSIS_PLAN_FEATURE_ABLATION.md", "artifacts/ANALYSIS_PLAN_FEATURE_ABLATION.md"),
        ("ANALYSIS_PLAN_MULTIPLICITY_STRESS_TEST.md", "artifacts/ANALYSIS_PLAN_MULTIPLICITY_STRESS_TEST.md"),
        ("ANALYSIS_PLAN_SOURCE_FORM_ABLATION.md", "artifacts/ANALYSIS_PLAN_SOURCE_FORM_ABLATION.md"),
        ("ANALYSIS_PLAN_NEIGHBORHOOD_ADDITIONS.md", "artifacts/ANALYSIS_PLAN_NEIGHBORHOOD_ADDITIONS.md"),
        ("ANALYSIS_PLAN_SOURCE_CONDITIONED_ADDITIONS.md", "artifacts/ANALYSIS_PLAN_SOURCE_CONDITIONED_ADDITIONS.md"),
        ("ANALYSIS_PLAN_STABLE_PROJECTION_CROSS_VALIDATION.md", "artifacts/ANALYSIS_PLAN_STABLE_PROJECTION_CROSS_VALIDATION.md"),
        ("ANALYSIS_PLAN_TRAJECTORY_RETRIEVAL.md", "artifacts/ANALYSIS_PLAN_TRAJECTORY_RETRIEVAL.md"),
        ("BENCHMARK_PROVENANCE.md", "artifacts/BENCHMARK_PROVENANCE.md"),
        ("analysis/analyze_change_distributions.py", "artifacts/analyze_change_distributions.py"),
        ("analysis/analyze_calibrated_synthesis.py", "artifacts/analyze_calibrated_synthesis.py"),
        ("analysis/analyze_semantic_neighborhood_additions.py", "artifacts/analyze_semantic_neighborhood_additions.py"),
        ("analysis/analyze_response_length_persistence.py", "artifacts/analyze_response_length_persistence.py"),
        ("analysis/analyze_response_length_shrinkage.py", "artifacts/analyze_response_length_shrinkage.py"),
        ("analysis/analyze_change_volume.py", "artifacts/analyze_change_volume.py"),
        ("analysis/analyze_feature_ablation.py", "artifacts/analyze_feature_ablation.py"),
        ("analysis/analyze_multiplicity_stress_test.py", "artifacts/analyze_multiplicity_stress_test.py"),
        ("analysis/analyze_source_form_ablation.py", "artifacts/analyze_source_form_ablation.py"),
        ("analysis/analyze_dev_diagnostics.py", "artifacts/analyze_dev_diagnostics.py"),
        ("analysis/analyze_neighborhood_additions.py", "artifacts/analyze_neighborhood_additions.py"),
        ("analysis/analyze_novelty_prior.py", "artifacts/analyze_novelty_prior.py"),
        ("analysis/analyze_source_conditioned_additions.py", "artifacts/analyze_source_conditioned_additions.py"),
        ("analysis/analyze_stable_projection_cross_validation.py", "artifacts/analyze_stable_projection_cross_validation.py"),
        ("analysis/analyze_trajectory_retrieval.py", "artifacts/analyze_trajectory_retrieval.py"),
        ("analysis/stable_signifier_projection.py", "artifacts/stable_signifier_projection.py"),
        ("analysis/trajectory_retrieval.py", "artifacts/trajectory_retrieval.py"),
        ("results/change_distributions_train_analysis.json", "artifacts/change_distributions_train_analysis.json"),
        ("results/change_distributions_train_audit.csv", "artifacts/change_distributions_train_audit.csv"),
        ("results/calibrated_synthesis_train_analysis.json", "artifacts/calibrated_synthesis_train_analysis.json"),
        ("results/calibrated_synthesis_train_audit.csv", "artifacts/calibrated_synthesis_train_audit.csv"),
        ("results/calibrated_synthesis_train_predictions.csv", "artifacts/calibrated_synthesis_train_predictions.csv"),
        ("results/change_volume_train_analysis.json", "artifacts/change_volume_train_analysis.json"),
        ("results/change_volume_train_audit.csv", "artifacts/change_volume_train_audit.csv"),
        ("results/feature_ablation_train_analysis.json", "artifacts/feature_ablation_train_analysis.json"),
        ("results/feature_ablation_train_audit.csv", "artifacts/feature_ablation_train_audit.csv"),
        ("results/multiplicity_stress_test_train_analysis.json", "artifacts/multiplicity_stress_test_train_analysis.json"),
        ("results/multiplicity_stress_test_train_audit.csv", "artifacts/multiplicity_stress_test_train_audit.csv"),
        ("results/source_form_ablation_train_analysis.json", "artifacts/source_form_ablation_train_analysis.json"),
        ("results/source_form_ablation_train_audit.csv", "artifacts/source_form_ablation_train_audit.csv"),
        ("results/semantic_neighborhood_additions_train_analysis.json", "artifacts/semantic_neighborhood_additions_train_analysis.json"),
        ("results/semantic_neighborhood_additions_train_audit.csv", "artifacts/semantic_neighborhood_additions_train_audit.csv"),
        ("results/response_length_persistence_train_analysis.json", "artifacts/response_length_persistence_train_analysis.json"),
        ("results/response_length_persistence_train_audit.csv", "artifacts/response_length_persistence_train_audit.csv"),
        ("results/response_length_shrinkage_train_analysis.json", "artifacts/response_length_shrinkage_train_analysis.json"),
        ("results/response_length_shrinkage_train_audit.csv", "artifacts/response_length_shrinkage_train_audit.csv"),
        ("results/neighborhood_additions_train_analysis.json", "artifacts/neighborhood_additions_train_analysis.json"),
        ("results/neighborhood_additions_train_audit.csv", "artifacts/neighborhood_additions_train_audit.csv"),
        ("results/novelty_prior_dev_analysis.json", "artifacts/novelty_prior_dev_analysis.json"),
        ("results/novelty_prior_token_audit.csv", "artifacts/novelty_prior_token_audit.csv"),
        ("results/source_conditioned_additions_train_analysis.json", "artifacts/source_conditioned_additions_train_analysis.json"),
        ("results/source_conditioned_additions_train_audit.csv", "artifacts/source_conditioned_additions_train_audit.csv"),
        ("results/stable_signifier_dev_diagnostics.json", "artifacts/stable_signifier_dev_diagnostics.json"),
        ("results/stable_signifier_dev_predictions.csv", "artifacts/stable_signifier_dev_predictions.csv"),
        ("results/stable_signifier_dev_scorecard.json", "artifacts/stable_signifier_dev_scorecard.json"),
        ("results/stable_projection_train_cv_analysis.json", "artifacts/stable_projection_train_cv_analysis.json"),
        ("results/stable_projection_train_cv_predictions.csv", "artifacts/stable_projection_train_cv_predictions.csv"),
        ("results/trajectory_retrieval_dev_analysis.json", "artifacts/trajectory_retrieval_dev_analysis.json"),
        ("results/trajectory_retrieval_dev_audit.csv", "artifacts/trajectory_retrieval_dev_audit.csv"),
        ("results/trajectory_retrieval_dev_predictions.csv", "artifacts/trajectory_retrieval_dev_predictions.csv"),
        ("results/trajectory_retrieval_dev_scorecard.json", "artifacts/trajectory_retrieval_dev_scorecard.json"),
        ("submissions/aleph_initial_alpha_submission.csv", "artifacts/aleph_initial_alpha_submission.csv"),
        ("submissions/aleph_initial_alpha_method.md", "artifacts/aleph_initial_alpha_method.md"),
    ):
        validate_artifact_copy(
            PROJECT / source,
            PUBLIC / "report" / source,
            PUBLIC / "report" / legacy,
        )

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
    validate_pdf_report_links(pdf)

    print(
        "Predict the Self publication: one summary figure, two-chapter linked "
        f"Full Report, {len(expected_artifacts)} artifacts, required phrase, and {len(pdf.pages)}-page "
        "two-column PDF passed."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
