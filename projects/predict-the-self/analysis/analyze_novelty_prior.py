#!/usr/bin/env python3
"""Test whether retrieval beats a marginal prior on novel-token content.

The matched-trajectory baseline emits approximately the observed amount of
lexical novelty, but volume alone can inflate the number of correct novel
tokens. This post hoc diagnostic gives a training-only marginal-addition prior
exactly the same novel-token budget as retrieval on every development case.
It then compares which method recovers the observed novel token types.
"""

from __future__ import annotations

import argparse
import csv
import json
import random
from collections import Counter
from pathlib import Path
from types import ModuleType

import analyze_dev_diagnostics as shared


EXPECTED_TRAIN_SHA256 = (
    "720aea3c4a9f7ad96ff3960ad6faa36991e1771dc43793c9e16e33b583bd4a48"
)
EXPECTED_RETRIEVAL_SHA256 = (
    "f061d6658bb89359cee12313d426225d1ace601a01e51a8751662570b4345d60"
)
BOOTSTRAP_SEED = 20260919
BOOTSTRAP_RESAMPLES = 20_000
AUDIT_FIELDS = [
    "rank",
    "token",
    "training_add_cases",
    "training_add_rate",
    "development_observed_add_cases",
    "marginal_predicted_cases",
    "marginal_correct_cases",
    "retrieval_predicted_cases",
    "retrieval_correct_cases",
]


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle, strict=True))


def training_addition_counts(
    rows: list[dict[str, str]], evaluator: ModuleType
) -> Counter[str]:
    """Count documents in which each token is added at follow-up."""
    counts: Counter[str] = Counter()
    for row in rows:
        source = set(evaluator.tokenize(row["tst_2024"]))
        follow_up = set(evaluator.tokenize(row["tst_2025"]))
        counts.update(follow_up - source)
    return counts


def ranked_additions(counts: Counter[str]) -> list[str]:
    """Rank by training document frequency, then Unicode token order."""
    return sorted(counts, key=lambda token: (-counts[token], token))


def marginal_prediction(
    ranked: list[str], source_tokens: set[str], budget: int
) -> set[str]:
    """Return the most frequent training additions absent from this source."""
    if budget < 0:
        raise ValueError("Novel-token budget cannot be negative")
    prediction: set[str] = set()
    for token in ranked:
        if token not in source_tokens:
            prediction.add(token)
            if len(prediction) == budget:
                break
    if len(prediction) != budget:
        raise ValueError(
            f"Only {len(prediction)} eligible marginal tokens for budget {budget}"
        )
    return prediction


def recovery_scores(
    predicted: set[str], observed: set[str], evaluator: ModuleType
) -> tuple[float, float, float]:
    overlap = len(predicted & observed)
    precision = overlap / len(predicted) if predicted else 0.0
    recall = overlap / len(observed) if observed else 0.0
    return precision, recall, evaluator.f1(precision, recall)


def summarize_pair(
    marginal_values: list[float],
    retrieval_values: list[float],
    rng: random.Random,
    resamples: int,
) -> dict[str, object]:
    if len(marginal_values) != len(retrieval_values) or not marginal_values:
        raise ValueError("Paired vectors must have the same nonzero length")
    differences = [
        marginal - retrieval
        for marginal, retrieval in zip(marginal_values, retrieval_values)
    ]
    low, high = shared.bootstrap_mean_interval(differences, resamples, rng)
    tolerance = 1e-12
    return {
        "marginal_prior_mean": sum(marginal_values) / len(marginal_values),
        "trajectory_retrieval_mean": sum(retrieval_values) / len(retrieval_values),
        "effect_definition": "marginal_prior_minus_trajectory_retrieval",
        "mean_effect_positive_favors_marginal_prior": sum(differences)
        / len(differences),
        "paired_case_bootstrap_95_ci_low": low,
        "paired_case_bootstrap_95_ci_high": high,
        "marginal_prior_case_wins": sum(
            value > tolerance for value in differences
        ),
        "case_ties": sum(abs(value) <= tolerance for value in differences),
        "marginal_prior_case_losses": sum(
            value < -tolerance for value in differences
        ),
    }


def make_token_audit(
    ranked: list[str],
    training_counts: Counter[str],
    training_case_count: int,
    observed_sets: list[set[str]],
    marginal_sets: list[set[str]],
    retrieval_sets: list[set[str]],
) -> list[dict[str, object]]:
    observed_counts: Counter[str] = Counter()
    marginal_counts: Counter[str] = Counter()
    marginal_correct: Counter[str] = Counter()
    retrieval_counts: Counter[str] = Counter()
    retrieval_correct: Counter[str] = Counter()
    for observed, marginal, retrieval in zip(
        observed_sets, marginal_sets, retrieval_sets
    ):
        observed_counts.update(observed)
        marginal_counts.update(marginal)
        marginal_correct.update(marginal & observed)
        retrieval_counts.update(retrieval)
        retrieval_correct.update(retrieval & observed)

    tokens = set(ranked) | set(observed_counts) | set(retrieval_counts)
    rank_by_token = {token: index for index, token in enumerate(ranked, start=1)}
    unranked = len(ranked) + 1
    ordered = sorted(tokens, key=lambda token: (rank_by_token.get(token, unranked), token))
    return [
        {
            "rank": rank_by_token.get(token, ""),
            "token": token,
            "training_add_cases": training_counts[token],
            "training_add_rate": f"{training_counts[token] / training_case_count:.6f}",
            "development_observed_add_cases": observed_counts[token],
            "marginal_predicted_cases": marginal_counts[token],
            "marginal_correct_cases": marginal_correct[token],
            "retrieval_predicted_cases": retrieval_counts[token],
            "retrieval_correct_cases": retrieval_correct[token],
        }
        for token in ordered
    ]


def analyze(
    benchmark_dir: Path,
    retrieval_path: Path,
    resamples: int = BOOTSTRAP_RESAMPLES,
) -> tuple[dict[str, object], list[dict[str, object]]]:
    training_path = benchmark_dir / "data/train.csv"
    development_path = benchmark_dir / "data/dev.csv"
    evaluator_path = benchmark_dir / "scripts/evaluate_predictions.py"
    shared.require_hash(training_path, EXPECTED_TRAIN_SHA256)
    shared.require_hash(development_path, shared.EXPECTED_DEV_SHA256)
    shared.require_hash(evaluator_path, shared.EXPECTED_EVALUATOR_SHA256)
    shared.require_hash(retrieval_path, EXPECTED_RETRIEVAL_SHA256)
    evaluator = shared.load_evaluator(evaluator_path)

    training_rows = read_rows(training_path)
    development_rows = read_rows(development_path)
    prediction_rows = shared.read_prediction_rows(retrieval_path)
    case_ids = [row["id"] for row in development_rows]
    retrieval_by_id = {
        row["id"]: row["predicted_tst_2025"] for row in prediction_rows
    }
    if list(retrieval_by_id) != case_ids:
        raise ValueError("Retrieval predictions must follow development ID order")

    addition_counts = training_addition_counts(training_rows, evaluator)
    ranked = ranked_additions(addition_counts)
    observed_sets: list[set[str]] = []
    retrieval_sets: list[set[str]] = []
    marginal_sets: list[set[str]] = []
    for row in development_rows:
        source = set(evaluator.tokenize(row["tst_2024"]))
        observed = set(evaluator.tokenize(row["tst_2025"])) - source
        retrieval = set(evaluator.tokenize(retrieval_by_id[row["id"]])) - source
        marginal = marginal_prediction(ranked, source, len(retrieval))
        observed_sets.append(observed)
        retrieval_sets.append(retrieval)
        marginal_sets.append(marginal)

    score_vectors: dict[str, dict[str, list[float]]] = {
        method: {"precision": [], "recall": [], "f1": []}
        for method in ("marginal_prior", "trajectory_retrieval")
    }
    for observed, marginal, retrieval in zip(
        observed_sets, marginal_sets, retrieval_sets
    ):
        for method, predicted in (
            ("marginal_prior", marginal),
            ("trajectory_retrieval", retrieval),
        ):
            precision, recall, f1 = recovery_scores(predicted, observed, evaluator)
            score_vectors[method]["precision"].append(precision)
            score_vectors[method]["recall"].append(recall)
            score_vectors[method]["f1"].append(f1)

    rng = random.Random(BOOTSTRAP_SEED)
    summaries = {
        method: {
            metric: shared.summarize_values(values, resamples, rng)
            for metric, values in metrics.items()
        }
        for method, metrics in score_vectors.items()
    }
    comparisons = {
        metric: summarize_pair(
            score_vectors["marginal_prior"][metric],
            score_vectors["trajectory_retrieval"][metric],
            rng,
            resamples,
        )
        for metric in ("precision", "recall", "f1")
    }
    budgets = [len(tokens) for tokens in retrieval_sets]
    audit = make_token_audit(
        ranked,
        addition_counts,
        len(training_rows),
        observed_sets,
        marginal_sets,
        retrieval_sets,
    )
    result = shared.round_floats(
        {
            "schema_version": 1,
            "analysis": "post_hoc_volume_matched_marginal_novelty_prior",
            "cases": len(development_rows),
            "benchmark": {
                "commit": "9b6a766712583fec8d3182957260b1123fbfa146",
                "training_sha256": EXPECTED_TRAIN_SHA256,
                "development_sha256": shared.EXPECTED_DEV_SHA256,
                "evaluator_sha256": shared.EXPECTED_EVALUATOR_SHA256,
                "retrieval_prediction_sha256": EXPECTED_RETRIEVAL_SHA256,
            },
            "diagnostic_control": {
                "description": (
                    "For each case, rank token types by the number of training "
                    "documents in which they were added, exclude tokens already "
                    "present in the focal source, and select exactly as many types "
                    "as trajectory retrieval introduced."
                ),
                "mean_novel_token_budget": sum(budgets) / len(budgets),
                "minimum_novel_token_budget": min(budgets),
                "maximum_novel_token_budget": max(budgets),
                "all_case_budgets_equal": all(
                    len(marginal) == len(retrieval)
                    for marginal, retrieval in zip(marginal_sets, retrieval_sets)
                ),
                "warning": (
                    "The marginal prior borrows retrieval's per-case token budget. "
                    "It is a volume-matched token-set diagnostic, not a standalone "
                    "full-text forecast."
                ),
            },
            "bootstrap": {
                "unit": "paired development case",
                "resamples": resamples,
                "seed": BOOTSTRAP_SEED,
                "interval": "percentile",
                "confidence_level": shared.CONFIDENCE_LEVEL,
                "interpretation": (
                    "Describes sensitivity to development-case composition; it is "
                    "not a population-generalization interval."
                ),
            },
            "novel_token_recovery": summaries,
            "paired_comparisons": comparisons,
            "interpretation_limits": (
                "The evaluator's lexical tokens include function words and other "
                "language that may not be identity signifiers. Development labels "
                "were already inspected, so this comparison is post hoc and not a "
                "private-test result."
            ),
        }
    )
    return result, audit


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
        "--retrieval-predictions",
        type=Path,
        default=project / "results/trajectory_retrieval_dev_predictions.csv",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=project / "results/novelty_prior_dev_analysis.json",
    )
    parser.add_argument(
        "--audit-output",
        type=Path,
        default=project / "results/novelty_prior_token_audit.csv",
    )
    parser.add_argument("--bootstrap-resamples", type=int, default=BOOTSTRAP_RESAMPLES)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.bootstrap_resamples < 1:
        raise SystemExit("--bootstrap-resamples must be positive")
    try:
        result, audit = analyze(
            args.benchmark_dir,
            args.retrieval_predictions,
            args.bootstrap_resamples,
        )
    except (OSError, csv.Error, ValueError, ImportError) as error:
        raise SystemExit(f"analyze_novelty_prior: {error}") from error
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    write_audit(args.audit_output, audit)
    print(f"Wrote novelty-prior analysis for {result['cases']} cases to {args.output}")
    print(f"Wrote {len(audit)} token audit rows to {args.audit_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
