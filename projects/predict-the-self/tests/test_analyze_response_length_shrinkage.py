from __future__ import annotations

import importlib.util
import math
import sys
import unittest
from pathlib import Path


ANALYSIS_DIR = Path(__file__).resolve().parents[1] / "analysis"
sys.path.insert(0, str(ANALYSIS_DIR))
MODULE_PATH = ANALYSIS_DIR / "analyze_response_length_shrinkage.py"
SPEC = importlib.util.spec_from_file_location("response_length_shrinkage", MODULE_PATH)
assert SPEC and SPEC.loader
analysis = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(analysis)


class ResponseLengthShrinkageTests(unittest.TestCase):
    def test_ols_slope_includes_intercept_and_handles_constant_source(self) -> None:
        self.assertAlmostEqual(
            analysis.ols_slope([1.0, 2.0, 3.0], [5.0, 7.0, 9.0]), 2.0
        )
        self.assertEqual(
            analysis.ols_slope([4.0, 4.0, 4.0], [1.0, 2.0, 8.0]), 0.0
        )

    def test_cross_fitted_support_excludes_outer_and_support_cases(self) -> None:
        support, slopes = analysis.cross_fitted_linear_support(
            0,
            [1.0, 2.0, 3.0, 4.0],
            [2.0, 4.0, 6.0, 8.0],
        )
        self.assertEqual(slopes, [2.0, 2.0, 2.0])
        self.assertEqual(support, [2.0, 2.0, 2.0])

    def test_zero_slope_reduces_to_raw_support(self) -> None:
        support, slopes = analysis.cross_fitted_linear_support(
            0,
            [3.0, 3.0, 3.0, 3.0],
            [2.0, 5.0, 7.0, 11.0],
        )
        self.assertEqual(slopes, [0.0, 0.0, 0.0])
        self.assertEqual(support, [5.0, 7.0, 11.0])

    def test_support_is_clipped_at_zero(self) -> None:
        support, slopes = analysis.cross_fitted_linear_support(
            0,
            [0.0, 10.0, 20.0, 30.0],
            [0.0, 20.0, 40.0, 60.0],
        )
        self.assertEqual(slopes, [2.0, 2.0, 2.0])
        self.assertEqual(support, [0.0, 0.0, 0.0])

    def test_count_parser_rejects_fractional_and_nonfinite_values(self) -> None:
        self.assertEqual(analysis.parse_count("12.000000", "count", "case"), 12.0)
        for value in ("1.5", "-1", "nan", "inf"):
            with self.assertRaises(ValueError):
                analysis.parse_count(value, "count", "case")

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

    def test_slope_description_is_complete_and_finite(self) -> None:
        description = analysis.describe_slopes([0.1, 0.2, 0.3, 0.4])
        self.assertEqual(description["count"], 4)
        self.assertAlmostEqual(float(description["mean"]), 0.25)
        self.assertTrue(
            all(
                math.isfinite(float(value))
                for key, value in description.items()
                if key != "count"
            )
        )

    def test_locked_plan_and_preceding_artifacts_match(self) -> None:
        project = Path(__file__).resolve().parents[1]
        paths = {
            "EXPECTED_PLAN_SHA256": project
            / "ANALYSIS_PLAN_RESPONSE_LENGTH_SHRINKAGE.md",
            "EXPECTED_PRECEDING_PLAN_SHA256": project
            / "ANALYSIS_PLAN_RESPONSE_LENGTH_DECOMPOSITION.md",
            "EXPECTED_PRECEDING_IMPLEMENTATION_SHA256": project
            / "analysis/analyze_response_length_persistence.py",
            "EXPECTED_PRECEDING_AUDIT_SHA256": project
            / "results/response_length_persistence_train_audit.csv",
        }
        for constant, path in paths.items():
            with self.subTest(path=path.name):
                self.assertEqual(
                    analysis.shared.sha256(path), getattr(analysis, constant)
                )


if __name__ == "__main__":
    unittest.main()
