#!/usr/bin/env python3
"""Evaluate one locked full-text synthesis rule in training leave-one-out.

The rule combines fold-fit stable source units, prospective word and Add-count
targets, and common fold-only novel response units. It never reads development
or private-test rows and never changes an existing prediction artifact.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import random
from collections import Counter
from pathlib import Path
from types import ModuleType

import analyze_change_volume as volume
import analyze_dev_diagnostics as shared
import analyze_source_conditioned_additions as source_conditioned
import analyze_source_form_ablation as source_form
import stable_signifier_projection as stable


EXPECTED_PLAN_SHA256 = (
    "ae0594e0f95f4131416be0bab4c3bfa913010dc6380d65c39966849c3a9f7253"
)
EXPECTED_STABLE_SHA256 = (
    "ae1eb8b653cd704fcc411790b39f83109e0f92c9af3bfe4fc347d5fb0e04b8c3"
)
EXPECTED_VOLUME_SHA256 = (
    "59b1a48b9b4e7194bbe260b497c5463cb1e4ce984c544e58a404f913046d6c09"
)
EXPECTED_SOURCE_FORM_SHA256 = (
    "721815303644b0da611732496207609f26cd421ae28f9f00d1563d3fe473195f"
)
EXPECTED_SOURCE_CONDITIONED_SHA256 = (
    "3fbe44d591c028f05541877b246f4fdfc9c53bc2d5ac940111142d00c75e9480"
)
EXPECTED_RETRIEVAL_SHA256 = (
    "05f64bb95440dcea8125358441878612e71ba19b898a791a0d3a200511a5077e"
)
PRIOR_STRENGTH = 10.0
MINIMUM_NOVEL_UNIT_CASES = 2
BOOTSTRAP_SEED = 20260930
BOOTSTRAP_RESAMPLES = 20_000
METHODS = ("calibrated_synthesis", "stable_projection", "repeat_2024")
METRICS = (
    "normalized_exact_match_rate",
    "normalized_edit_similarity",
    "token_jaccard_similarity",
    "token_overlap_f1",
    "rouge_l_f1",
    "character_ngram_f1",
    "word_count_mae",
    "line_count_mae",
    "source_similarity_mae",
)
HIGHER_IS_BETTER = {metric: not metric.endswith("_mae") for metric in METRICS}

BASE_AUDIT_FIELDS = [
    "id",
    "source_unit_count",
    "retained_source_unit_count",
    "eligible_common_novel_unit_count",
    "appended_unit_count",
    "target_word_count",
    "predicted_word_count",
    "observed_word_count",
    "target_add_count",
    "predicted_add_count",
    "observed_add_count",
]
CONTENT_AUDIT_FIELDS = [
    f"{method}_novel_type_{metric}"
    for method in ("calibrated_synthesis", "volume_matched_marginal")
    for metric in ("precision", "recall", "f1")
]
AUDIT_FIELDS = BASE_AUDIT_FIELDS + [
    f"{method}_{metric}" for method in METHODS for metric in METRICS
] + CONTENT_AUDIT_FIELDS


def normalize_unit(text: str) -> str:
    """Normalize a response unit exactly as the evaluator normalizes text."""
    return " ".join(text.casefold().split())


def common_novel_units(
    fold_rows: list[dict[str, str]], minimum_cases: int = MINIMUM_NOVEL_UNIT_CASES
) -> list[str]:
    """Rank fold follow-up units that are exact-unit additions in >= N cases."""
    if minimum_cases < 1:
        raise ValueError("Minimum novel-unit case count must be positive")
    counts: Counter[str] = Counter()
    first_surface: dict[str, str] = {}
    for row in fold_rows:
        source_units = {
            normalize_unit(unit) for unit in stable.response_units(row["tst_2024"])
        }
        seen: set[str] = set()
        for surface in stable.response_units(row["tst_2025"]):
            normalized = normalize_unit(surface)
            if not normalized or normalized in source_units or normalized in seen:
                continue
            seen.add(normalized)
            counts[normalized] += 1
            first_surface.setdefault(normalized, surface.strip())
    ranked = sorted(
        (normalized for normalized, count in counts.items() if count >= minimum_cases),
        key=lambda normalized: (-counts[normalized], normalized),
    )
    return [first_surface[normalized] for normalized in ranked]


def source_quantities(source: str, evaluator: ModuleType) -> dict[str, object]:
    """Return only source-observable quantities required for inverse scaling."""
    tokens = evaluator.tokenize(source)
    lines = evaluator.line_count(source)
    if not tokens or lines < 1:
        raise ValueError("Held-out source must contain a token and nonblank line")
    return {
        "source_unique_tokens": len(set(tokens)),
        "source_word_count": len(tokens),
        "source_line_count": lines,
    }


def forecast_targets(
    query: dict[str, str],
    fold_rows: list[dict[str, str]],
    evaluator: ModuleType,
    neighbor_count: int = volume.NEIGHBOR_COUNT,
) -> tuple[int, int]:
    """Forecast word and distinct-Add counts without querying the held-out future."""
    if len(fold_rows) < neighbor_count:
        raise ValueError("Fold is too small for the fixed neighborhood")
    quantities = [volume.case_quantities(row, evaluator) for row in fold_rows]
    held_out = source_quantities(query["tst_2024"], evaluator)
    prior_case_weight = volume.PRIOR_WEIGHT / len(fold_rows)

    word_indices, word_similarities = source_form.select_source_form_neighbors(
        query, fold_rows, neighbor_count, evaluator
    )
    word_neighbor_weights = volume.normalized_neighbor_weights(word_similarities)
    word_values = [float(item["modeled"]["word_count"]) for item in quantities]
    word_change = volume.weighted_median(
        word_values + [word_values[index] for index in word_indices],
        [prior_case_weight] * len(word_values) + word_neighbor_weights,
    )
    target_words = max(
        1,
        round(volume.outcome_scale("word_count", word_change, held_out)),
    )

    add_indices, add_similarities = volume.select_neighbors(
        query, fold_rows, neighbor_count
    )
    add_neighbor_weights = volume.normalized_neighbor_weights(add_similarities)
    add_values = [float(item["modeled"]["add_count"]) for item in quantities]
    add_count = volume.weighted_median(
        add_values + [add_values[index] for index in add_indices],
        [prior_case_weight] * len(add_values) + add_neighbor_weights,
    )
    return target_words, max(0, round(add_count))


def ranked_source_units(
    source: str, fold_rows: list[dict[str, str]]
) -> tuple[list[str], list[int]]:
    """Return source units and their fold-fit stable ranking."""
    probabilities, prior = stable.fit_token_retention(fold_rows, PRIOR_STRENGTH)
    units = stable.response_units(source)
    ranking = sorted(
        range(len(units)),
        key=lambda index: (
            stable.unit_score(units[index], probabilities, prior),
            -index,
        ),
        reverse=True,
    )
    return units, ranking


def synthesize_response(
    query: dict[str, str],
    fold_rows: list[dict[str, str]],
    evaluator: ModuleType,
    target_words: int,
    target_adds: int,
) -> tuple[str, dict[str, int]]:
    """Search the two fixed ranked-prefix dimensions and emit the best response."""
    if target_words < 1 or target_adds < 0:
        raise ValueError("Targets must be a positive word count and nonnegative Add count")
    source = query["tst_2024"]
    source_tokens = set(evaluator.tokenize(source))
    source_unit_norms = {
        normalize_unit(unit) for unit in stable.response_units(source)
    }
    units, source_ranking = ranked_source_units(source, fold_rows)
    common_units = [
        unit
        for unit in common_novel_units(fold_rows)
        if normalize_unit(unit) not in source_unit_norms
    ]

    source_prefixes: list[tuple[list[str], int]] = []
    for count in range(1, len(source_ranking) + 1):
        chosen_indices = sorted(source_ranking[:count])
        chosen_units = [units[index] for index in chosen_indices]
        source_prefixes.append(
            (chosen_units, sum(len(evaluator.tokenize(unit)) for unit in chosen_units))
        )

    addition_prefixes: list[tuple[list[str], int, int]] = [([], 0, 0)]
    surfaces: list[str] = []
    word_count = 0
    token_types: set[str] = set()
    for unit in common_units:
        surfaces.append(unit)
        tokens = evaluator.tokenize(unit)
        word_count += len(tokens)
        token_types.update(tokens)
        addition_prefixes.append(
            (list(surfaces), word_count, len(token_types - source_tokens))
        )

    best_key: tuple[float, int, int, int, int, int, int] | None = None
    best_response = ""
    best_counts = (0, 0)
    for source_count, (source_surfaces, source_words) in enumerate(
        source_prefixes, start=1
    ):
        for addition_count, (addition_surfaces, addition_words, novel_types) in enumerate(
            addition_prefixes
        ):
            candidate_words = source_words + addition_words
            word_error = abs(candidate_words - target_words)
            add_error = abs(novel_types - target_adds)
            objective = (
                word_error / target_words
                + add_error / max(1, target_adds)
            )
            key = (
                objective,
                word_error,
                add_error,
                -source_count,
                addition_count,
                source_count,
                addition_count,
            )
            if best_key is None or key < best_key:
                best_key = key
                best_response = "\n".join(source_surfaces + addition_surfaces)
                best_counts = (source_count, addition_count)
    if not best_response.strip():
        raise ValueError("Synthesis produced a blank response")
    return best_response, {
        "source_unit_count": len(units),
        "retained_source_unit_count": best_counts[0],
        "eligible_common_novel_unit_count": len(common_units),
        "appended_unit_count": best_counts[1],
    }


def metric_vectors(
    sources: list[str], references: list[str], predictions: list[str], evaluator: ModuleType
) -> dict[str, list[float]]:
    """Return all nine official scored metrics as complete case vectors."""
    vectors = shared.case_metric_vectors(sources, references, predictions, evaluator)
    return {name: values[0] for name, values in vectors.items()}


def paired_metric_summary(
    first: list[float],
    second: list[float],
    higher_is_better: bool,
    first_name: str,
    second_name: str,
    resamples: int,
) -> dict[str, object]:
    """Summarize a paired utility difference; positive always favors first."""
    if len(first) != len(second) or not first:
        raise ValueError("Paired metric vectors must align and be nonempty")
    raw = [left - right for left, right in zip(first, second)]
    effects = raw if higher_is_better else [-value for value in raw]
    low, high = shared.bootstrap_mean_interval(
        effects, resamples, random.Random(BOOTSTRAP_SEED)
    )
    tolerance = 1e-12
    return {
        f"{first_name}_mean": sum(first) / len(first),
        f"{second_name}_mean": sum(second) / len(second),
        "effect_definition": (
            f"{first_name}_minus_{second_name}"
            if higher_is_better
            else f"{second_name}_error_minus_{first_name}_error"
        ),
        f"mean_effect_positive_favors_{first_name}": sum(effects) / len(effects),
        "paired_case_bootstrap_95_ci_low": low,
        "paired_case_bootstrap_95_ci_high": high,
        f"{first_name}_case_wins": sum(value > tolerance for value in effects),
        "case_ties": sum(abs(value) <= tolerance for value in effects),
        f"{first_name}_case_losses": sum(value < -tolerance for value in effects),
    }


def content_scores(predicted: set[str], observed: set[str]) -> tuple[float, float, float]:
    """Return set precision, recall, and F1 with the locked zero-size rule."""
    if not predicted:
        return 0.0, 0.0, 0.0
    hits = len(predicted & observed)
    precision = hits / len(predicted)
    recall = hits / len(observed) if observed else 0.0
    return precision, recall, 0.0 if precision + recall == 0 else (
        2 * precision * recall / (precision + recall)
    )


def case_metrics(
    source: str, reference: str, prediction: str, evaluator: ModuleType
) -> dict[str, float]:
    """Calculate the nine official scored metrics for one case."""
    observed_similarity = evaluator.rouge_l_f1(reference, source)
    return {
        "normalized_exact_match_rate": float(
            evaluator.normalize(prediction) == evaluator.normalize(reference)
        ),
        "normalized_edit_similarity": evaluator.normalized_edit_similarity(
            prediction, reference
        ),
        "token_jaccard_similarity": evaluator.token_jaccard_similarity(
            prediction, reference
        ),
        "token_overlap_f1": evaluator.token_overlap_f1(prediction, reference),
        "rouge_l_f1": evaluator.rouge_l_f1(prediction, reference),
        "character_ngram_f1": evaluator.character_ngram_f1(prediction, reference),
        "word_count_mae": abs(
            len(evaluator.tokenize(prediction)) - len(evaluator.tokenize(reference))
        ),
        "line_count_mae": abs(
            evaluator.line_count(prediction) - evaluator.line_count(reference)
        ),
        "source_similarity_mae": abs(
            evaluator.rouge_l_f1(prediction, source) - observed_similarity
        ),
    }


def analyze(
    benchmark_dir: Path,
    plan_path: Path,
    stable_path: Path,
    volume_path: Path,
    source_form_path: Path,
    source_conditioned_path: Path,
    retrieval_path: Path,
    resamples: int = BOOTSTRAP_RESAMPLES,
) -> tuple[dict[str, object], list[dict[str, object]], list[dict[str, str]]]:
    """Run the locked fold analysis and return result, audit, and predictions."""
    training_path = benchmark_dir / "data/train.csv"
    evaluator_path = benchmark_dir / "scripts/evaluate_predictions.py"
    shared.require_hash(training_path, volume.EXPECTED_TRAIN_SHA256)
    shared.require_hash(evaluator_path, shared.EXPECTED_EVALUATOR_SHA256)
    for path, expected in (
        (plan_path, EXPECTED_PLAN_SHA256),
        (stable_path, EXPECTED_STABLE_SHA256),
        (volume_path, EXPECTED_VOLUME_SHA256),
        (source_form_path, EXPECTED_SOURCE_FORM_SHA256),
        (source_conditioned_path, EXPECTED_SOURCE_CONDITIONED_SHA256),
        (retrieval_path, EXPECTED_RETRIEVAL_SHA256),
    ):
        shared.require_hash(path, expected)
    evaluator = shared.load_evaluator(evaluator_path)
    _, rows = evaluator.read_csv(training_path)
    volume.validate_rows(rows, volume.NEIGHBOR_COUNT)

    sources: list[str] = []
    references: list[str] = []
    synthesis_predictions: list[str] = []
    stable_predictions: list[str] = []
    audits: list[dict[str, object]] = []
    prediction_rows: list[dict[str, str]] = []

    for held_out_index, row in enumerate(rows):
        fold = rows[:held_out_index] + rows[held_out_index + 1 :]
        target_words, target_adds = forecast_targets(row, fold, evaluator)
        synthesis, structure = synthesize_response(
            row, fold, evaluator, target_words, target_adds
        )
        stable_prediction = stable.make_predictions(
            [row], fold, PRIOR_STRENGTH
        )[0]["predicted_tst_2025"]
        source = row["tst_2024"]
        reference = row["tst_2025"]
        source_tokens = set(evaluator.tokenize(source))
        observed_adds = set(evaluator.tokenize(reference)) - source_tokens
        synthesis_adds = set(evaluator.tokenize(synthesis)) - source_tokens

        fold_addition_counts: Counter[str] = Counter()
        for candidate in fold:
            candidate_source = set(evaluator.tokenize(candidate["tst_2024"]))
            candidate_follow_up = set(evaluator.tokenize(candidate["tst_2025"]))
            fold_addition_counts.update(candidate_follow_up - candidate_source)
        marginal_ranking = source_conditioned.marginal_ranking(
            fold_addition_counts, source_tokens
        )
        marginal_adds = source_conditioned.top_set(
            marginal_ranking, len(synthesis_adds)
        )
        synthesis_content = content_scores(synthesis_adds, observed_adds)
        marginal_content = content_scores(marginal_adds, observed_adds)

        method_predictions = {
            "calibrated_synthesis": synthesis,
            "stable_projection": stable_prediction,
            "repeat_2024": source,
        }
        audit: dict[str, object] = {
            "id": row["id"],
            **structure,
            "target_word_count": target_words,
            "predicted_word_count": len(evaluator.tokenize(synthesis)),
            "observed_word_count": len(evaluator.tokenize(reference)),
            "target_add_count": target_adds,
            "predicted_add_count": len(synthesis_adds),
            "observed_add_count": len(observed_adds),
        }
        for method, prediction in method_predictions.items():
            for metric, value in case_metrics(
                source, reference, prediction, evaluator
            ).items():
                audit[f"{method}_{metric}"] = f"{value:.6f}"
        for method, scores in (
            ("calibrated_synthesis", synthesis_content),
            ("volume_matched_marginal", marginal_content),
        ):
            for metric, value in zip(("precision", "recall", "f1"), scores):
                audit[f"{method}_novel_type_{metric}"] = f"{value:.6f}"
        audits.append(audit)
        prediction_rows.append(
            {"id": row["id"], "predicted_tst_2025": synthesis}
        )
        sources.append(source)
        references.append(reference)
        synthesis_predictions.append(synthesis)
        stable_predictions.append(stable_prediction)

    synthesis_vectors = metric_vectors(
        sources, references, synthesis_predictions, evaluator
    )
    stable_vectors = metric_vectors(sources, references, stable_predictions, evaluator)
    repeat_vectors = metric_vectors(sources, references, sources, evaluator)
    official_comparisons: dict[str, object] = {}
    for comparator_name, comparator_vectors in (
        ("repeat_2024", repeat_vectors),
        ("stable_projection", stable_vectors),
    ):
        official_comparisons[
            f"calibrated_synthesis_vs_{comparator_name}"
        ] = {
            metric: paired_metric_summary(
                synthesis_vectors[metric],
                comparator_vectors[metric],
                HIGHER_IS_BETTER[metric],
                "calibrated_synthesis",
                comparator_name,
                resamples,
            )
            for metric in METRICS
        }

    synthesis_content_vectors = {
        metric: [float(row[f"calibrated_synthesis_novel_type_{metric}"]) for row in audits]
        for metric in ("precision", "recall", "f1")
    }
    marginal_content_vectors = {
        metric: [float(row[f"volume_matched_marginal_novel_type_{metric}"]) for row in audits]
        for metric in ("precision", "recall", "f1")
    }
    content_comparison = {
        metric: paired_metric_summary(
            synthesis_content_vectors[metric],
            marginal_content_vectors[metric],
            True,
            "calibrated_synthesis",
            "volume_matched_marginal",
            resamples,
        )
        for metric in ("precision", "recall", "f1")
    }

    edit_gate = official_comparisons["calibrated_synthesis_vs_repeat_2024"][
        "normalized_edit_similarity"
    ]
    word_gate = official_comparisons["calibrated_synthesis_vs_repeat_2024"][
        "word_count_mae"
    ]
    content_gate = content_comparison["f1"]
    gate_summaries = [edit_gate, word_gate, content_gate]
    gate_effects = [
        float(summary["mean_effect_positive_favors_calibrated_synthesis"])
        for summary in gate_summaries
    ]
    gate_lows = [
        float(summary["paired_case_bootstrap_95_ci_low"])
        for summary in gate_summaries
    ]
    advancement_passed = all(value > 0 for value in gate_effects + gate_lows)

    result = shared.round_floats(
        {
            "schema_version": 1,
            "analysis": "training_leave_one_out_calibrated_full_text_synthesis",
            "cases": len(rows),
            "benchmark": {
                "commit": "9b6a766712583fec8d3182957260b1123fbfa146",
                "training_sha256": volume.EXPECTED_TRAIN_SHA256,
                "evaluator_sha256": shared.EXPECTED_EVALUATOR_SHA256,
                "analysis_plan_sha256": EXPECTED_PLAN_SHA256,
                "stable_implementation_sha256": EXPECTED_STABLE_SHA256,
                "change_volume_implementation_sha256": EXPECTED_VOLUME_SHA256,
                "source_form_implementation_sha256": EXPECTED_SOURCE_FORM_SHA256,
                "marginal_ranking_implementation_sha256": (
                    EXPECTED_SOURCE_CONDITIONED_SHA256
                ),
                "retrieval_feature_implementation_sha256": EXPECTED_RETRIEVAL_SHA256,
            },
            "design": {
                "training_cases_per_fold": len(rows) - 1,
                "stable_retention_prior_strength": PRIOR_STRENGTH,
                "minimum_fold_cases_per_common_novel_unit": (
                    MINIMUM_NOVEL_UNIT_CASES
                ),
                "word_count_representation": "source word, distinct-token, and line counts",
                "add_count_representation": (
                    "surface text and field-qualified 2024 demographics"
                ),
                "neighbor_count": volume.NEIGHBOR_COUNT,
                "neighbor_effective_weight": volume.NEIGHBOR_EFFECTIVE_WEIGHT,
                "fold_prior_effective_weight": volume.PRIOR_WEIGHT,
                "held_out_future_information_used_for_prediction": "none",
            },
            "paired_official_metric_comparisons": official_comparisons,
            "volume_matched_novel_type_comparison": content_comparison,
            "advancement_gate": {
                "requires_all_three_means_and_ci_lows_above_zero": True,
                "normalized_edit_similarity_vs_repeat_2024": edit_gate,
                "word_count_error_vs_repeat_2024": word_gate,
                "novel_type_f1_vs_volume_matched_marginal": content_gate,
                "passed": advancement_passed,
                "development_comparison_permitted_by_plan": advancement_passed,
            },
            "bootstrap": {
                "unit": "paired training case",
                "resamples": resamples,
                "seed_restarted_for_each_contrast": BOOTSTRAP_SEED,
                "interval": "percentile",
                "confidence_level": shared.CONFIDENCE_LEVEL,
                "interpretation": (
                    "Describes sensitivity to this training cohort's case composition; "
                    "it is not multiplicity-adjusted or a population interval."
                ),
            },
            "claim_boundary": (
                "This dependent training-only analysis integrates components selected "
                "after earlier results. It is not untouched confirmation or private-test "
                "performance, and transferred fold text is a benchmark-data adaptation."
            ),
        }
    )
    return result, audits, prediction_rows


def write_audit(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=AUDIT_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def parse_args() -> argparse.Namespace:
    project = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--benchmark-dir", required=True, type=Path)
    parser.add_argument(
        "--analysis-plan",
        type=Path,
        default=project / "ANALYSIS_PLAN_CALIBRATED_SYNTHESIS.md",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=project / "results/calibrated_synthesis_train_analysis.json",
    )
    parser.add_argument(
        "--audit-output",
        type=Path,
        default=project / "results/calibrated_synthesis_train_audit.csv",
    )
    parser.add_argument(
        "--predictions-output",
        type=Path,
        default=project / "results/calibrated_synthesis_train_predictions.csv",
    )
    parser.add_argument("--bootstrap-resamples", type=int, default=BOOTSTRAP_RESAMPLES)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.bootstrap_resamples < 1:
        raise SystemExit("--bootstrap-resamples must be positive")
    project = Path(__file__).resolve().parents[1]
    try:
        result, audit, predictions = analyze(
            args.benchmark_dir,
            args.analysis_plan,
            project / "analysis/stable_signifier_projection.py",
            project / "analysis/analyze_change_volume.py",
            project / "analysis/analyze_source_form_ablation.py",
            project / "analysis/analyze_source_conditioned_additions.py",
            project / "analysis/trajectory_retrieval.py",
            args.bootstrap_resamples,
        )
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        write_audit(args.audit_output, audit)
        stable.write_predictions(args.predictions_output, predictions)
    except (OSError, csv.Error, KeyError, ValueError, ImportError) as error:
        raise SystemExit(f"analyze_calibrated_synthesis: {error}") from error
    print(f"Wrote calibrated synthesis analysis for {result['cases']} cases to {args.output}")
    print(f"Wrote {len(audit)} case audit rows to {args.audit_output}")
    print(f"Wrote {len(predictions)} fold predictions to {args.predictions_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
