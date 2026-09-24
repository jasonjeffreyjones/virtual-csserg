#!/usr/bin/env python3
"""Replace the public Full Report with the complete local Quarto build."""

from pathlib import Path
import shutil
import tempfile
import uuid


PROJECT = Path(__file__).resolve().parents[1]
ROOT = PROJECT.parents[1]
SOURCE = PROJECT / "_book"
PUBLIC = ROOT / "website/projects/predict-the-self/report"
COMPATIBILITY_ARTIFACTS = {
    "ANALYSIS_PLAN_CHANGE_DISTRIBUTIONS.md": "artifacts/ANALYSIS_PLAN_CHANGE_DISTRIBUTIONS.md",
    "ANALYSIS_PLAN_CHANGE_VOLUME.md": "artifacts/ANALYSIS_PLAN_CHANGE_VOLUME.md",
    "ANALYSIS_PLAN_NEIGHBORHOOD_ADDITIONS.md": "artifacts/ANALYSIS_PLAN_NEIGHBORHOOD_ADDITIONS.md",
    "ANALYSIS_PLAN_SOURCE_CONDITIONED_ADDITIONS.md": "artifacts/ANALYSIS_PLAN_SOURCE_CONDITIONED_ADDITIONS.md",
    "ANALYSIS_PLAN_STABLE_PROJECTION_CROSS_VALIDATION.md": "artifacts/ANALYSIS_PLAN_STABLE_PROJECTION_CROSS_VALIDATION.md",
    "ANALYSIS_PLAN_TRAJECTORY_RETRIEVAL.md": "artifacts/ANALYSIS_PLAN_TRAJECTORY_RETRIEVAL.md",
    "BENCHMARK_PROVENANCE.md": "artifacts/BENCHMARK_PROVENANCE.md",
    "analysis/analyze_change_distributions.py": "artifacts/analyze_change_distributions.py",
    "analysis/analyze_change_volume.py": "artifacts/analyze_change_volume.py",
    "analysis/analyze_dev_diagnostics.py": "artifacts/analyze_dev_diagnostics.py",
    "analysis/analyze_neighborhood_additions.py": "artifacts/analyze_neighborhood_additions.py",
    "analysis/analyze_novelty_prior.py": "artifacts/analyze_novelty_prior.py",
    "analysis/analyze_source_conditioned_additions.py": "artifacts/analyze_source_conditioned_additions.py",
    "analysis/analyze_stable_projection_cross_validation.py": "artifacts/analyze_stable_projection_cross_validation.py",
    "analysis/analyze_trajectory_retrieval.py": "artifacts/analyze_trajectory_retrieval.py",
    "analysis/stable_signifier_projection.py": "artifacts/stable_signifier_projection.py",
    "analysis/trajectory_retrieval.py": "artifacts/trajectory_retrieval.py",
    "results/change_distributions_train_analysis.json": "artifacts/change_distributions_train_analysis.json",
    "results/change_distributions_train_audit.csv": "artifacts/change_distributions_train_audit.csv",
    "results/change_volume_train_analysis.json": "artifacts/change_volume_train_analysis.json",
    "results/change_volume_train_audit.csv": "artifacts/change_volume_train_audit.csv",
    "results/neighborhood_additions_train_analysis.json": "artifacts/neighborhood_additions_train_analysis.json",
    "results/neighborhood_additions_train_audit.csv": "artifacts/neighborhood_additions_train_audit.csv",
    "results/novelty_prior_dev_analysis.json": "artifacts/novelty_prior_dev_analysis.json",
    "results/novelty_prior_token_audit.csv": "artifacts/novelty_prior_token_audit.csv",
    "results/source_conditioned_additions_train_analysis.json": "artifacts/source_conditioned_additions_train_analysis.json",
    "results/source_conditioned_additions_train_audit.csv": "artifacts/source_conditioned_additions_train_audit.csv",
    "results/stable_signifier_dev_diagnostics.json": "artifacts/stable_signifier_dev_diagnostics.json",
    "results/stable_signifier_dev_predictions.csv": "artifacts/stable_signifier_dev_predictions.csv",
    "results/stable_signifier_dev_scorecard.json": "artifacts/stable_signifier_dev_scorecard.json",
    "results/stable_projection_train_cv_analysis.json": "artifacts/stable_projection_train_cv_analysis.json",
    "results/stable_projection_train_cv_predictions.csv": "artifacts/stable_projection_train_cv_predictions.csv",
    "results/trajectory_retrieval_dev_analysis.json": "artifacts/trajectory_retrieval_dev_analysis.json",
    "results/trajectory_retrieval_dev_audit.csv": "artifacts/trajectory_retrieval_dev_audit.csv",
    "results/trajectory_retrieval_dev_predictions.csv": "artifacts/trajectory_retrieval_dev_predictions.csv",
    "results/trajectory_retrieval_dev_scorecard.json": "artifacts/trajectory_retrieval_dev_scorecard.json",
    "submissions/aleph_initial_alpha_submission.csv": "artifacts/aleph_initial_alpha_submission.csv",
    "submissions/aleph_initial_alpha_method.md": "artifacts/aleph_initial_alpha_method.md",
}


class PublicationError(ValueError):
    """Raised when the completed local report cannot be safely published."""


def normalize_generated_html(tree: Path) -> None:
    """Remove generator-introduced line-end whitespace from public HTML."""
    for path in tree.rglob("*.html"):
        source = path.read_text(encoding="utf-8")
        normalized = "\n".join(line.rstrip() for line in source.splitlines())
        if source.endswith(("\n", "\r")):
            normalized += "\n"
        path.write_text(normalized, encoding="utf-8")


def publish(source: Path = SOURCE, public: Path = PUBLIC) -> None:
    source = Path(source).resolve()
    public = Path(public).resolve()
    required = (source / "index.html", source / "report.html", source / "report.css")
    required += tuple(source / path for path in COMPATIBILITY_ARTIFACTS)
    for artifact in required:
        if not artifact.is_file():
            raise PublicationError(f"missing build artifact {artifact}")

    public.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix=".predict-report-stage-", dir=public.parent))
    backup = public.parent / f".predict-report-backup-{uuid.uuid4().hex}"
    moved_existing = False
    try:
        shutil.copytree(source, staging, dirs_exist_ok=True)
        for current, legacy in COMPATIBILITY_ARTIFACTS.items():
            alias = staging / legacy
            alias.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(staging / current, alias)
        normalize_generated_html(staging)
        if public.exists():
            public.rename(backup)
            moved_existing = True
        staging.rename(public)
    except Exception:
        if not public.exists() and moved_existing and backup.exists():
            backup.rename(public)
        if staging.exists():
            shutil.rmtree(staging)
        raise
    else:
        if backup.exists():
            shutil.rmtree(backup)


def main() -> int:
    try:
        publish()
    except PublicationError as error:
        raise SystemExit(f"publish_full_report: {error}") from error
    print(f"Published {SOURCE.relative_to(ROOT)} to {PUBLIC.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
