from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


ANALYSIS_DIR = Path(__file__).resolve().parents[1] / "analysis"
sys.path.insert(0, str(ANALYSIS_DIR))
MODULE_PATH = ANALYSIS_DIR / "analyze_change_volume.py"
SPEC = importlib.util.spec_from_file_location("change_volume", MODULE_PATH)
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


class ChangeVolumeTests(unittest.TestCase):
    def test_weighted_median_handles_exact_half_and_dominant_weight(self) -> None:
        self.assertEqual(analysis.weighted_median([1, 3], [1, 1]), 2)
        self.assertEqual(analysis.weighted_median([1, 3, 8], [1, 5, 1]), 3)

    def test_case_quantities_use_add_delete_and_source_calibration(self) -> None:
        quantities = analysis.case_quantities(
            row("a", "old keep\nthird", "keep new new"), FakeEvaluator
        )
        self.assertEqual(quantities["source_unique_tokens"], 3)
        self.assertEqual(quantities["observed"]["add_count"], 1)
        self.assertEqual(quantities["observed"]["delete_count"], 2)
        self.assertAlmostEqual(quantities["modeled"]["delete_count"], 2 / 3)
        self.assertEqual(quantities["modeled"]["word_count"], 0)
        self.assertEqual(quantities["modeled"]["line_count"], -1)

    def test_outcome_scale_clips_to_possible_ranges(self) -> None:
        quantities = {
            "source_unique_tokens": 4,
            "source_word_count": 5,
            "source_line_count": 2,
        }
        self.assertEqual(analysis.outcome_scale("delete_count", 2, quantities), 4)
        self.assertEqual(analysis.outcome_scale("word_count", -8, quantities), 0)
        self.assertEqual(analysis.outcome_scale("line_count", -8, quantities), 1)
        self.assertEqual(
            analysis.outcome_scale("source_similarity", 1.5, quantities), 1
        )

    def test_held_out_future_cannot_change_its_own_forecasts(self) -> None:
        rows = [
            row("a", "alpha source", "alpha later"),
            row("b", "beta source", "beta later"),
            row("c", "gamma source", "gamma later"),
            row("d", "delta source", "delta later"),
        ]
        original = analysis.leave_one_out_forecasts(
            rows, FakeEvaluator, neighbor_count=2
        )[0]
        rows[0]["tst_2025"] = "entirely different future response words"
        changed = analysis.leave_one_out_forecasts(
            rows, FakeEvaluator, neighbor_count=2
        )[0]
        for outcome in analysis.OUTCOMES:
            self.assertEqual(
                original[f"{outcome}_marginal_prediction"],
                changed[f"{outcome}_marginal_prediction"],
            )
            self.assertEqual(
                original[f"{outcome}_neighborhood_prediction"],
                changed[f"{outcome}_neighborhood_prediction"],
            )
        self.assertNotEqual(original["add_count_observed"], changed["add_count_observed"])

    def test_paired_effect_sign_favors_lower_neighborhood_error(self) -> None:
        summary = analysis.paired_summary([1.0, 0.5, -0.25], 100)
        self.assertGreater(summary["mean_effect_positive_favors_neighborhood"], 0)
        self.assertEqual(summary["neighborhood_case_wins"], 2)
        self.assertEqual(summary["neighborhood_case_losses"], 1)

    def test_locked_plan_and_feature_hashes_match(self) -> None:
        project = Path(__file__).resolve().parents[1]
        self.assertEqual(
            analysis.shared.sha256(project / "ANALYSIS_PLAN_CHANGE_VOLUME.md"),
            analysis.EXPECTED_PLAN_SHA256,
        )
        self.assertEqual(
            analysis.shared.sha256(project / "analysis/trajectory_retrieval.py"),
            analysis.EXPECTED_RETRIEVAL_SHA256,
        )


if __name__ == "__main__":
    unittest.main()
