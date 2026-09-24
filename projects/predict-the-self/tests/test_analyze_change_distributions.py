from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


ANALYSIS_DIR = Path(__file__).resolve().parents[1] / "analysis"
sys.path.insert(0, str(ANALYSIS_DIR))
MODULE_PATH = ANALYSIS_DIR / "analyze_change_distributions.py"
SPEC = importlib.util.spec_from_file_location("change_distributions", MODULE_PATH)
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


def row(case_id: str, source: str, future: str) -> dict[str, str]:
    return {"id": case_id, "tst_2024": source, "tst_2025": future}


class ChangeDistributionTests(unittest.TestCase):
    def test_normalize_distribution_rejects_invalid_weights(self) -> None:
        support, weights = analysis.normalize_distribution([1, 2], [1, 3])
        self.assertEqual(support, [1, 2])
        self.assertEqual(weights, [0.25, 0.75])
        with self.assertRaises(ValueError):
            analysis.normalize_distribution([1], [-1])

    def test_empirical_crps_matches_point_and_two_point_examples(self) -> None:
        self.assertEqual(analysis.empirical_crps([2], [1], 5), 3)
        self.assertAlmostEqual(
            analysis.empirical_crps([0, 2], [0.5, 0.5], 1), 0.5
        )

    def test_weighted_quantile_uses_inverse_empirical_cdf(self) -> None:
        support = [5, 1, 3]
        weights = [0.6, 0.2, 0.2]
        self.assertEqual(analysis.weighted_quantile(support, weights, 0), 1)
        self.assertEqual(analysis.weighted_quantile(support, weights, 0.2), 1)
        self.assertEqual(analysis.weighted_quantile(support, weights, 0.21), 3)
        self.assertEqual(analysis.weighted_quantile(support, weights, 0.9), 5)

    def test_interval_score_penalizes_misses(self) -> None:
        self.assertEqual(analysis.interval_score(2, 1, 3, 0.2), 2)
        self.assertEqual(analysis.interval_score(5, 1, 3, 0.2), 22)

    def test_held_out_future_cannot_change_its_own_intervals(self) -> None:
        rows = [
            row("a", "alpha source", "alpha later"),
            row("b", "beta source", "beta later"),
            row("c", "gamma source", "gamma later"),
            row("d", "delta source", "delta later"),
        ]
        original = analysis.leave_one_out_distributions(
            rows, FakeEvaluator, neighbor_count=2
        )[0]
        rows[0]["tst_2025"] = "entirely different future response words"
        changed = analysis.leave_one_out_distributions(
            rows, FakeEvaluator, neighbor_count=2
        )[0]
        for outcome in analysis.OUTCOMES:
            for method in ("marginal", "neighborhood"):
                for bound in ("lower_80", "upper_80"):
                    self.assertEqual(
                        original[f"{outcome}_{method}_{bound}"],
                        changed[f"{outcome}_{method}_{bound}"],
                    )
        self.assertNotEqual(original["add_count_observed"], changed["add_count_observed"])

    def test_paired_effect_sign_favors_lower_neighborhood_score(self) -> None:
        original_resamples = analysis.BOOTSTRAP_RESAMPLES
        analysis.BOOTSTRAP_RESAMPLES = 100
        try:
            summary = analysis.paired_summary([1.0, 0.5, -0.25], "test")
        finally:
            analysis.BOOTSTRAP_RESAMPLES = original_resamples
        self.assertGreater(summary["mean_effect_positive_favors_neighborhood"], 0)
        self.assertEqual(summary["neighborhood_case_wins"], 2)
        self.assertEqual(summary["neighborhood_case_losses"], 1)

    def test_locked_plan_and_implementation_hashes_match(self) -> None:
        project = Path(__file__).resolve().parents[1]
        self.assertEqual(
            analysis.shared.sha256(project / "ANALYSIS_PLAN_CHANGE_DISTRIBUTIONS.md"),
            analysis.EXPECTED_PLAN_SHA256,
        )
        self.assertEqual(
            analysis.shared.sha256(project / "analysis/analyze_change_volume.py"),
            analysis.EXPECTED_CHANGE_VOLUME_SHA256,
        )


if __name__ == "__main__":
    unittest.main()
