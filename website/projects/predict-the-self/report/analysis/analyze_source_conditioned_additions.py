#!/usr/bin/env python3
"""Compare marginal and source-conditioned Add rankings in training LOO.

This diagnostic holds out each of the 150 training cases, estimates token Add
events and source-to-Add associations on the other 149, and gives both methods
the held-out case's observed number of novel-token guesses. It tests ranking
information only; the oracle budget makes it unsuitable as a full forecast.
"""

from __future__ import annotations

import argparse
import csv
import json
import random
from collections import Counter, defaultdict
from pathlib import Path
from types import ModuleType

import analyze_dev_diagnostics as shared


EXPECTED_TRAIN_SHA256 = (
    "720aea3c4a9f7ad96ff3960ad6faa36991e1771dc43793c9e16e33b583bd4a48"
)
EXPECTED_PLAN_SHA256 = (
    "e65f04fd9e55843db8ff1a1bb0544acb00ec869eb58f9b312a63d531fc5f4ec9"
)
PRIOR_WEIGHT = 10.0
BOOTSTRAP_SEED = 20260920
BOOTSTRAP_RESAMPLES = 20_000
AUDIT_FIELDS = [
    "id",
    "source_unique_tokens",
    "observed_addition_budget",
    "reachable_observed_additions",
    "reachable_fraction",
    "marginal_hits",
    "marginal_recovered_fraction",
    "source_conditioned_hits",
    "source_conditioned_recovered_fraction",
    "conditioned_minus_marginal",
]


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle, strict=True))


def token_sets(
    rows: list[dict[str, str]], evaluator: ModuleType
) -> tuple[list[set[str]], list[set[str]]]:
    sources: list[set[str]] = []
    additions: list[set[str]] = []
    for row in rows:
        source = set(evaluator.tokenize(row["tst_2024"]))
        follow_up = set(evaluator.tokenize(row["tst_2025"]))
        sources.append(source)
        additions.append(follow_up - source)
    return sources, additions


def build_counts(
    sources: list[set[str]], additions: list[set[str]]
) -> tuple[Counter[str], Counter[str], dict[str, Counter[str]]]:
    """Return source document counts, Add counts, and source-to-Add counts."""
    if len(sources) != len(additions):
        raise ValueError("Source and addition vectors must have equal length")
    source_counts: Counter[str] = Counter()
    addition_counts: Counter[str] = Counter()
    coadd_counts: defaultdict[str, Counter[str]] = defaultdict(Counter)
    for source, added in zip(sources, additions):
        source_counts.update(source)
        addition_counts.update(added)
        for source_token in source:
            coadd_counts[source_token].update(added)
    return source_counts, addition_counts, dict(coadd_counts)


def fold_addition_counts(
    global_counts: Counter[str], held_out_additions: set[str]
) -> Counter[str]:
    """Subtract one held-out case and discard zero-count candidates."""
    return Counter(
        {
            token: count - int(token in held_out_additions)
            for token, count in global_counts.items()
            if count - int(token in held_out_additions) > 0
        }
    )


def eligible_candidates(
    fold_counts: Counter[str], held_out_source: set[str]
) -> list[str]:
    return [token for token in fold_counts if token not in held_out_source]


def marginal_ranking(
    fold_counts: Counter[str], held_out_source: set[str]
) -> list[str]:
    return sorted(
        eligible_candidates(fold_counts, held_out_source),
        key=lambda token: (-fold_counts[token], token),
    )


def conditioned_score(
    candidate: str,
    held_out_source: set[str],
    held_out_additions: set[str],
    source_counts: Counter[str],
    coadd_counts: dict[str, Counter[str]],
    fold_add_count: int,
    fold_size: int,
    prior_weight: float = PRIOR_WEIGHT,
) -> float:
    """Return the strongest smoothed source-token cue for one candidate."""
    if not held_out_source:
        raise ValueError("A held-out source must contain at least one token")
    marginal_rate = fold_add_count / fold_size
    held_out_pair = int(candidate in held_out_additions)
    rates = []
    for source_token in held_out_source:
        fold_source_count = source_counts[source_token] - 1
        fold_coadd_count = coadd_counts.get(source_token, Counter())[candidate]
        fold_coadd_count -= held_out_pair
        if fold_source_count < 0 or fold_coadd_count < 0:
            raise ValueError("Held-out subtraction produced a negative count")
        rates.append(
            (fold_coadd_count + prior_weight * marginal_rate)
            / (fold_source_count + prior_weight)
        )
    return max(rates)


def source_conditioned_ranking(
    fold_counts: Counter[str],
    held_out_source: set[str],
    held_out_additions: set[str],
    source_counts: Counter[str],
    coadd_counts: dict[str, Counter[str]],
    fold_size: int,
) -> list[str]:
    scored = [
        (
            conditioned_score(
                token,
                held_out_source,
                held_out_additions,
                source_counts,
                coadd_counts,
                fold_counts[token],
                fold_size,
            ),
            fold_counts[token],
            token,
        )
        for token in eligible_candidates(fold_counts, held_out_source)
    ]
    return [
        token
        for _, _, token in sorted(
            scored, key=lambda item: (-item[0], -item[1], item[2])
        )
    ]


def top_set(ranking: list[str], budget: int) -> set[str]:
    if budget < 0:
        raise ValueError("Novel-token budget cannot be negative")
    if len(ranking) < budget:
        raise ValueError(
            f"Only {len(ranking)} eligible candidates for budget {budget}"
        )
    return set(ranking[:budget])


def descriptive(values: list[float]) -> dict[str, float]:
    if not values:
        raise ValueError("Cannot summarize an empty vector")
    ordered = sorted(values)
    return {
        "mean": sum(values) / len(values),
        "median": shared.percentile(ordered, 0.5),
        "minimum": ordered[0],
        "maximum": ordered[-1],
    }


def paired_summary(
    conditioned: list[float],
    marginal: list[float],
    resamples: int,
) -> dict[str, object]:
    if len(conditioned) != len(marginal) or not conditioned:
        raise ValueError("Paired vectors must have the same nonzero length")
    differences = [
        personalized - baseline
        for personalized, baseline in zip(conditioned, marginal)
    ]
    low, high = shared.bootstrap_mean_interval(
        differences, resamples, random.Random(BOOTSTRAP_SEED)
    )
    tolerance = 1e-12
    return {
        "effect_definition": "source_conditioned_minus_marginal",
        "mean_effect_positive_favors_source_conditioned": sum(differences)
        / len(differences),
        "paired_case_bootstrap_95_ci_low": low,
        "paired_case_bootstrap_95_ci_high": high,
        "source_conditioned_case_wins": sum(
            difference > tolerance for difference in differences
        ),
        "case_ties": sum(abs(difference) <= tolerance for difference in differences),
        "source_conditioned_case_losses": sum(
            difference < -tolerance for difference in differences
        ),
    }


def analyze(
    benchmark_dir: Path,
    plan_path: Path,
    resamples: int = BOOTSTRAP_RESAMPLES,
) -> tuple[dict[str, object], list[dict[str, object]]]:
    training_path = benchmark_dir / "data/train.csv"
    evaluator_path = benchmark_dir / "scripts/evaluate_predictions.py"
    shared.require_hash(training_path, EXPECTED_TRAIN_SHA256)
    shared.require_hash(evaluator_path, shared.EXPECTED_EVALUATOR_SHA256)
    shared.require_hash(plan_path, EXPECTED_PLAN_SHA256)
    evaluator = shared.load_evaluator(evaluator_path)

    rows = read_rows(training_path)
    sources, additions = token_sets(rows, evaluator)
    source_counts, addition_counts, coadd_counts = build_counts(sources, additions)
    fold_size = len(rows) - 1
    if fold_size < 1:
        raise ValueError("Leave-one-out analysis requires at least two cases")

    audit: list[dict[str, object]] = []
    marginal_scores: list[float] = []
    conditioned_scores: list[float] = []
    reachable_fractions: list[float] = []
    budgets: list[int] = []
    for row, source, observed in zip(rows, sources, additions):
        fold_counts = fold_addition_counts(addition_counts, observed)
        marginal = marginal_ranking(fold_counts, source)
        conditioned = source_conditioned_ranking(
            fold_counts,
            source,
            observed,
            source_counts,
            coadd_counts,
            fold_size,
        )
        budget = len(observed)
        reachable = len(observed & set(fold_counts))
        marginal_hits = len(top_set(marginal, budget) & observed)
        conditioned_hits = len(top_set(conditioned, budget) & observed)
        if budget:
            reachable_fraction = reachable / budget
            marginal_score = marginal_hits / budget
            conditioned_score_value = conditioned_hits / budget
            reachable_fractions.append(reachable_fraction)
            marginal_scores.append(marginal_score)
            conditioned_scores.append(conditioned_score_value)
            difference = conditioned_score_value - marginal_score
        else:
            reachable_fraction = marginal_score = conditioned_score_value = difference = 0.0
        budgets.append(budget)
        audit.append(
            {
                "id": row["id"],
                "source_unique_tokens": len(source),
                "observed_addition_budget": budget,
                "reachable_observed_additions": reachable,
                "reachable_fraction": f"{reachable_fraction:.6f}",
                "marginal_hits": marginal_hits,
                "marginal_recovered_fraction": f"{marginal_score:.6f}",
                "source_conditioned_hits": conditioned_hits,
                "source_conditioned_recovered_fraction": f"{conditioned_score_value:.6f}",
                "conditioned_minus_marginal": f"{difference:.6f}",
            }
        )

    scored_cases = len(marginal_scores)
    result = shared.round_floats(
        {
            "schema_version": 1,
            "analysis": "training_leave_one_out_source_conditioned_additions",
            "cases": len(rows),
            "scored_cases_with_positive_budget": scored_cases,
            "zero_budget_cases": len(rows) - scored_cases,
            "benchmark": {
                "commit": "9b6a766712583fec8d3182957260b1123fbfa146",
                "training_sha256": EXPECTED_TRAIN_SHA256,
                "evaluator_sha256": shared.EXPECTED_EVALUATOR_SHA256,
                "analysis_plan_sha256": EXPECTED_PLAN_SHA256,
            },
            "design": {
                "training_cases_per_fold": fold_size,
                "prior_weight": PRIOR_WEIGHT,
                "budget": "observed held-out novel-token-type count",
                "warning": (
                    "The oracle budget uses each held-out follow-up and isolates "
                    "ranking quality; neither method is a standalone forecast."
                ),
                "score_identity": (
                    "Predicted and observed sets have equal size, so case-level "
                    "novel-type precision, recall, and F1 are identical."
                ),
            },
            "observed_addition_budget": descriptive([float(value) for value in budgets]),
            "candidate_vocabulary_reachable_fraction": descriptive(
                reachable_fractions
            ),
            "novel_type_recovered_fraction": {
                "marginal_addition": descriptive(marginal_scores),
                "source_conditioned": descriptive(conditioned_scores),
            },
            "paired_comparison": paired_summary(
                conditioned_scores, marginal_scores, resamples
            ),
            "bootstrap": {
                "unit": "paired scored training case",
                "resamples": resamples,
                "seed": BOOTSTRAP_SEED,
                "interval": "percentile",
                "confidence_level": shared.CONFIDENCE_LEVEL,
                "interpretation": (
                    "Describes sensitivity to training-case composition; it is "
                    "not a population-generalization interval."
                ),
            },
            "interpretation_limits": (
                "This training-only leave-one-out diagnostic uses an oracle token "
                "budget. Lexical tokens include function words and need not be "
                "semantic identity signifiers. It is not development or private-test "
                "performance."
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
        "--analysis-plan",
        type=Path,
        default=project / "ANALYSIS_PLAN_SOURCE_CONDITIONED_ADDITIONS.md",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=project / "results/source_conditioned_additions_train_analysis.json",
    )
    parser.add_argument(
        "--audit-output",
        type=Path,
        default=project / "results/source_conditioned_additions_train_audit.csv",
    )
    parser.add_argument("--bootstrap-resamples", type=int, default=BOOTSTRAP_RESAMPLES)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.bootstrap_resamples < 1:
        raise SystemExit("--bootstrap-resamples must be positive")
    try:
        result, audit = analyze(
            args.benchmark_dir, args.analysis_plan, args.bootstrap_resamples
        )
    except (OSError, csv.Error, ValueError, ImportError) as error:
        raise SystemExit(f"analyze_source_conditioned_additions: {error}") from error
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    write_audit(args.audit_output, audit)
    print(
        "Wrote source-conditioned Add analysis for "
        f"{result['cases']} cases to {args.output}"
    )
    print(f"Wrote {len(audit)} case audit rows to {args.audit_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
