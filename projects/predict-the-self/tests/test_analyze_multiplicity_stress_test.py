from __future__ import annotations

import importlib.util
import math
import sys
import unittest
from pathlib import Path


ANALYSIS_DIR = Path(__file__).resolve().parents[1] / "analysis"
sys.path.insert(0, str(ANALYSIS_DIR))
MODULE_PATH = ANALYSIS_DIR / "analyze_multiplicity_stress_test.py"
SPEC = importlib.util.spec_from_file_location("multiplicity_stress_test", MODULE_PATH)
assert SPEC and SPEC.loader
analysis = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(analysis)


class MultiplicityStressTestTests(unittest.TestCase):
    def test_nearest_rank_uses_locked_definition(self) -> None:
        self.assertEqual(analysis.nearest_rank([4.0, 1.0, 3.0, 2.0], 0.75), 3.0)
        with self.assertRaises(ValueError):
            analysis.nearest_rank([], 0.95)

    def test_synchronized_maximum_yields_common_wider_interval(self) -> None:
        contrasts = {
            "a": [1.0, 2.0, 3.0, 4.0],
            "b": [4.0, 1.0, 5.0, 2.0],
            "constant": [0.0, 0.0, 0.0, 0.0],
        }
        critical, summaries = analysis.simultaneous_summary(
            contrasts, resamples=500, seed=42
        )
        self.assertGreater(critical, 0)
        self.assertEqual(summaries["constant"]["simultaneous_status"], "exact_zero")
        self.assertEqual(summaries["constant"]["simultaneous_95_ci_low"], 0.0)
        half_width_a = (
            summaries["a"]["simultaneous_95_ci_high"]
            - summaries["a"]["simultaneous_95_ci_low"]
        ) / 2
        self.assertTrue(
            math.isclose(
                half_width_a,
                critical * summaries["a"]["standard_error"],
                rel_tol=1e-12,
            )
        )

    def test_direction_classification_does_not_call_zero_stable(self) -> None:
        contrasts = {
            "positive": [9.0, 10.0, 11.0, 10.0, 10.0],
            "negative": [-9.0, -10.0, -11.0, -10.0, -10.0],
            "unclear": [-2.0, -1.0, 0.0, 1.0, 2.0],
            "zero": [0.0] * 5,
        }
        _, summaries = analysis.simultaneous_summary(
            contrasts, resamples=1_000, seed=10
        )
        self.assertEqual(summaries["positive"]["simultaneous_status"], "positive")
        self.assertEqual(summaries["negative"]["simultaneous_status"], "negative")
        self.assertEqual(summaries["unclear"]["simultaneous_status"], "includes_zero")
        self.assertEqual(summaries["zero"]["simultaneous_status"], "exact_zero")

    def test_algebraic_difference_rejects_changed_effect(self) -> None:
        row = {"direct": "0.3", "first": "1.0", "second": "0.5"}
        with self.assertRaises(ValueError):
            analysis.require_algebraic_difference(
                row, "direct", "first", "second"
            )

    def test_locked_plan_and_inputs_match(self) -> None:
        project = Path(__file__).resolve().parents[1]
        self.assertEqual(
            analysis.sha256(project / "ANALYSIS_PLAN_MULTIPLICITY_STRESS_TEST.md"),
            analysis.EXPECTED_PLAN_SHA256,
        )
        input_paths = {
            "change_volume": project / "results/change_volume_train_audit.csv",
            "change_distributions": (
                project / "results/change_distributions_train_audit.csv"
            ),
            "feature_ablation": (
                project / "results/feature_ablation_train_audit.csv"
            ),
            "source_form_ablation": (
                project / "results/source_form_ablation_train_audit.csv"
            ),
        }
        for name, path in input_paths.items():
            self.assertEqual(
                analysis.sha256(path), analysis.EXPECTED_INPUT_SHA256[name]
            )

    def test_complete_inputs_produce_locked_family(self) -> None:
        project = Path(__file__).resolve().parents[1]
        paths = {
            "change_volume": project / "results/change_volume_train_audit.csv",
            "change_distributions": (
                project / "results/change_distributions_train_audit.csv"
            ),
            "feature_ablation": (
                project / "results/feature_ablation_train_audit.csv"
            ),
            "source_form_ablation": (
                project / "results/source_form_ablation_train_audit.csv"
            ),
        }
        audits = {name: analysis.read_audit(path) for name, path in paths.items()}
        contrasts = analysis.extract_contrasts(audits)
        self.assertEqual(len(contrasts), 16)
        self.assertEqual(list(contrasts), list(analysis.CONTRAST_METADATA))
        for name, values in contrasts.items():
            self.assertEqual(len(values), 150)
            self.assertEqual(round(sum(values) / len(values), 6), analysis.EXPECTED_MEANS[name])


if __name__ == "__main__":
    unittest.main()
