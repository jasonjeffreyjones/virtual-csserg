from __future__ import annotations

import importlib.util
import math
import sys
import unittest
from pathlib import Path


ANALYSIS_DIR = Path(__file__).resolve().parents[1] / "analysis"
sys.path.insert(0, str(ANALYSIS_DIR))
MODULE_PATH = ANALYSIS_DIR / "analyze_response_length_persistence.py"
SPEC = importlib.util.spec_from_file_location("response_length_persistence", MODULE_PATH)
assert SPEC and SPEC.loader
analysis = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(analysis)


class FakeEvaluator:
    @staticmethod
    def tokenize(text: str) -> list[str]:
        return text.casefold().split()

    @staticmethod
    def line_count(text: str) -> int:
        return sum(bool(line.strip()) for line in text.splitlines())

    @staticmethod
    def rouge_l_f1(left: str, right: str) -> float:
        left_tokens = left.casefold().split()
        right_tokens = right.casefold().split()
        overlap = len(set(left_tokens) & set(right_tokens))
        return 2 * overlap / (len(left_tokens) + len(right_tokens))


def response(length: int, stem: str) -> str:
    return " ".join(f"{stem}{index}" for index in range(length))


def row(case_id: str, source_length: int, future_length: int) -> dict[str, str]:
    return {
        "id": case_id,
        "tst_2024": response(source_length, f"{case_id}s"),
        "tst_2025": response(future_length, f"{case_id}f"),
    }


class ResponseLengthPersistenceTests(unittest.TestCase):
    def test_additive_support_shifts_and_clips_fold_changes(self) -> None:
        self.assertEqual(analysis.additive_support(5.0, [-8.0, -2.0, 3.0]), [0.0, 3.0, 8.0])

    def test_leave_one_out_support_excludes_held_out_future(self) -> None:
        rows = [
            row("a", 10, 12),
            row("b", 20, 24),
            row("c", 30, 36),
        ]
        audits = analysis.leave_one_out_scores(rows, FakeEvaluator)
        first = audits[0]
        self.assertEqual(first["source_word_count"], 10.0)
        self.assertEqual(first["additive_persistence_prediction"], 14.0)
        self.assertEqual(first["raw_marginal_prediction"], 24.0)
        self.assertEqual(first["observed_word_count"], 12.0)

    def test_paired_effect_sign_and_counts_favor_named_method(self) -> None:
        original_resamples = analysis.BOOTSTRAP_RESAMPLES
        analysis.BOOTSTRAP_RESAMPLES = 100
        try:
            summary = analysis.paired_summary(
                [1.0, -0.5, 0.0], "first_minus_second", "second"
            )
        finally:
            analysis.BOOTSTRAP_RESAMPLES = original_resamples
        self.assertAlmostEqual(summary["mean_effect"], 1 / 6)
        self.assertEqual(summary["favored_method_case_wins"], 1)
        self.assertEqual(summary["case_ties"], 1)
        self.assertEqual(summary["favored_method_case_losses"], 1)

    def test_pearson_correlation_has_expected_extremes(self) -> None:
        self.assertAlmostEqual(
            analysis.pearson_correlation([1.0, 2.0, 3.0], [2.0, 4.0, 6.0]),
            1.0,
        )
        self.assertAlmostEqual(
            analysis.pearson_correlation([1.0, 2.0, 3.0], [6.0, 4.0, 2.0]),
            -1.0,
        )

    def test_distribution_scores_are_finite_and_nonnegative(self) -> None:
        audits = analysis.leave_one_out_scores(
            [row("a", 2, 3), row("b", 3, 5), row("c", 4, 7)],
            FakeEvaluator,
        )
        for audit in audits:
            for field in ("raw_marginal_crps", "additive_persistence_crps"):
                self.assertTrue(math.isfinite(float(audit[field])))
                self.assertGreaterEqual(float(audit[field]), 0.0)

    def test_locked_plan_and_inherited_artifacts_match(self) -> None:
        project = Path(__file__).resolve().parents[1]
        self.assertEqual(
            analysis.shared.sha256(
                project / "ANALYSIS_PLAN_RESPONSE_LENGTH_DECOMPOSITION.md"
            ),
            analysis.EXPECTED_PLAN_SHA256,
        )
        self.assertEqual(
            analysis.shared.sha256(
                project / "ANALYSIS_PLAN_RESPONSE_LENGTH_PERSISTENCE.md"
            ),
            analysis.EXPECTED_INITIAL_PLAN_SHA256,
        )
        self.assertEqual(
            analysis.shared.sha256(
                project / "analysis/analyze_source_form_ablation.py"
            ),
            analysis.EXPECTED_SOURCE_FORM_IMPLEMENTATION_SHA256,
        )
        self.assertEqual(
            analysis.shared.sha256(
                project / "results/source_form_ablation_train_audit.csv"
            ),
            analysis.EXPECTED_SOURCE_FORM_AUDIT_SHA256,
        )


if __name__ == "__main__":
    unittest.main()
