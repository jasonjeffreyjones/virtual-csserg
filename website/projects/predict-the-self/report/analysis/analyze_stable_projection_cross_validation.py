#!/usr/bin/env python3
"""Cross-validate the frozen stable-signifier projection on training cases.

Each training trajectory is held out before fitting the unchanged projection
on the other 149 cases. The resulting prediction is compared case by case with
repeat-2024 using the pinned benchmark evaluator. This is a training-cohort
diagnostic, not an untouched confirmatory estimate or a private-test result.
"""

from __future__ import annotations

import argparse
import csv
import json
import random
from pathlib import Path
from types import ModuleType

import analyze_dev_diagnostics as shared
import stable_signifier_projection as stable


EXPECTED_TRAIN_SHA256 = (
    "720aea3c4a9f7ad96ff3960ad6faa36991e1771dc43793c9e16e33b583bd4a48"
)
EXPECTED_PLAN_SHA256 = (
    "2929b1fb8111c42170d23e725c08f6167135d9a703a1b61e87ed59af5f97c5d8"
)
EXPECTED_GENERATOR_SHA256 = (
    "ae1eb8b653cd704fcc411790b39f83109e0f92c9af3bfe4fc347d5fb0e04b8c3"
)
PRIOR_STRENGTH = 10.0
BOOTSTRAP_SEED = 20260922
BOOTSTRAP_RESAMPLES = 20_000
REQUIRED_FIELDS = {"id", "tst_2024", "tst_2025"}


def validate_training_rows(rows: list[dict[str, str]]) -> None:
    """Require a usable longitudinal training table with unique IDs."""
    if len(rows) < 2:
        raise ValueError("Cross-validation requires at least two training cases")
    missing = REQUIRED_FIELDS - set(rows[0])
    if missing:
        raise ValueError(f"Training data is missing fields: {sorted(missing)}")
    case_ids = [row["id"] for row in rows]
    if any(not case_id for case_id in case_ids):
        raise ValueError("Training data contains a blank ID")
    if len(set(case_ids)) != len(case_ids):
        raise ValueError("Training data contains duplicate IDs")
    if any(not row["tst_2024"].strip() or not row["tst_2025"].strip() for row in rows):
        raise ValueError("Training source and follow-up responses must be nonblank")


def leave_one_out_predictions(
    rows: list[dict[str, str]], prior_strength: float = PRIOR_STRENGTH
) -> list[dict[str, str]]:
    """Refit the frozen generator without each case and predict that case."""
    validate_training_rows(rows)
    predictions = []
    for held_out_index, held_out in enumerate(rows):
        fold = rows[:held_out_index] + rows[held_out_index + 1 :]
        predictions.extend(stable.make_predictions([held_out], fold, prior_strength))
    return predictions


def descriptive_scorecard(
    sources: list[str],
    references: list[str],
    predictions: list[str],
    evaluator: ModuleType,
) -> dict[str, float]:
    """Return the official scorecard's six descriptive form/change measures."""
    count = len(sources)
    if count == 0 or len(references) != count or len(predictions) != count:
        raise ValueError("Source, reference, and prediction vectors must align")
    prediction_source_similarity = [
        evaluator.rouge_l_f1(prediction, source)
        for prediction, source in zip(predictions, sources)
    ]
    observed_source_similarity = [
        evaluator.rouge_l_f1(reference, source)
        for reference, source in zip(references, sources)
    ]
    return {
        "prediction_word_count_mean": sum(
            len(evaluator.tokenize(text)) for text in predictions
        )
        / count,
        "reference_word_count_mean": sum(
            len(evaluator.tokenize(text)) for text in references
        )
        / count,
        "prediction_repeat_2024_rate": sum(
            evaluator.normalize(prediction) == evaluator.normalize(source)
            for prediction, source in zip(predictions, sources)
        )
        / count,
        "observed_repeat_2024_rate": sum(
            evaluator.normalize(reference) == evaluator.normalize(source)
            for reference, source in zip(references, sources)
        )
        / count,
        "prediction_source_similarity_mean": sum(prediction_source_similarity)
        / count,
        "observed_source_similarity_mean": sum(observed_source_similarity) / count,
    }


def analyze(
    benchmark_dir: Path,
    plan_path: Path,
    generator_path: Path,
    resamples: int = BOOTSTRAP_RESAMPLES,
) -> tuple[dict[str, object], list[dict[str, str]]]:
    """Generate all fold predictions and their paired scorecard."""
    training_path = benchmark_dir / "data/train.csv"
    evaluator_path = benchmark_dir / "scripts/evaluate_predictions.py"
    shared.require_hash(training_path, EXPECTED_TRAIN_SHA256)
    shared.require_hash(evaluator_path, shared.EXPECTED_EVALUATOR_SHA256)
    shared.require_hash(plan_path, EXPECTED_PLAN_SHA256)
    shared.require_hash(generator_path, EXPECTED_GENERATOR_SHA256)

    evaluator = shared.load_evaluator(evaluator_path)
    _, rows = evaluator.read_csv(training_path)
    validate_training_rows(rows)
    prediction_rows = leave_one_out_predictions(rows)
    case_ids = [row["id"] for row in rows]
    if [row["id"] for row in prediction_rows] != case_ids:
        raise ValueError("Fold predictions must preserve training case order")

    sources = [row["tst_2024"] for row in rows]
    references = [row["tst_2025"] for row in rows]
    predictions = [row["predicted_tst_2025"] for row in prediction_rows]
    rng = random.Random(BOOTSTRAP_SEED)
    comparisons = {
        name: shared.summarize_comparison(
            stable_values, repeat_values, direction, resamples, rng
        )
        for name, (stable_values, repeat_values, direction) in shared.case_metric_vectors(
            sources, references, predictions, evaluator
        ).items()
    }

    result = {
        "schema_version": 1,
        "analysis": "leave_one_out_cross_validation_of_frozen_stable_projection",
        "cases": len(rows),
        "benchmark": {
            "commit": "9b6a766712583fec8d3182957260b1123fbfa146",
            "training_sha256": EXPECTED_TRAIN_SHA256,
            "evaluator_sha256": shared.EXPECTED_EVALUATOR_SHA256,
            "analysis_plan_sha256": EXPECTED_PLAN_SHA256,
            "stable_generator_sha256": EXPECTED_GENERATOR_SHA256,
        },
        "model": {
            "training_cases_per_fold": len(rows) - 1,
            "token_retention_prior_strength": PRIOR_STRENGTH,
            "held_out_information_used_for_prediction": "tst_2024 only",
        },
        "bootstrap": {
            "unit": "paired training case",
            "resamples": resamples,
            "seed": BOOTSTRAP_SEED,
            "interval": "percentile",
            "confidence_level": shared.CONFIDENCE_LEVEL,
            "interpretation": (
                "Describes sensitivity to training-cohort case composition; it is "
                "not a population-generalization interval."
            ),
        },
        "paired_comparisons": comparisons,
        "descriptive_scorecard": descriptive_scorecard(
            sources, references, predictions, evaluator
        ),
        "claim_boundary": (
            "The method and data informed earlier Project work. Leave-one-out fitting "
            "withholds each case's own follow-up, but this is not untouched confirmation "
            "or private-test performance."
        ),
    }
    return shared.round_floats(result), prediction_rows


def parse_args() -> argparse.Namespace:
    project = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--benchmark-dir", required=True, type=Path)
    parser.add_argument(
        "--plan",
        type=Path,
        default=project / "ANALYSIS_PLAN_STABLE_PROJECTION_CROSS_VALIDATION.md",
    )
    parser.add_argument(
        "--generator",
        type=Path,
        default=project / "analysis/stable_signifier_projection.py",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=project / "results/stable_projection_train_cv_analysis.json",
    )
    parser.add_argument(
        "--predictions-output",
        type=Path,
        default=project / "results/stable_projection_train_cv_predictions.csv",
    )
    parser.add_argument("--bootstrap-resamples", type=int, default=BOOTSTRAP_RESAMPLES)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.bootstrap_resamples < 1:
        raise SystemExit("--bootstrap-resamples must be positive")
    try:
        result, predictions = analyze(
            args.benchmark_dir,
            args.plan,
            args.generator,
            args.bootstrap_resamples,
        )
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        stable.write_predictions(args.predictions_output, predictions)
    except (OSError, csv.Error, ValueError, ImportError) as error:
        raise SystemExit(f"analyze_stable_projection_cross_validation: {error}") from error
    print(f"Wrote cross-validation analysis for {result['cases']} cases to {args.output}")
    print(f"Wrote {len(predictions)} fold predictions to {args.predictions_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
