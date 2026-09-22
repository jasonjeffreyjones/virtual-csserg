from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch


ANALYSIS_DIR = Path(__file__).resolve().parents[1] / "analysis"
sys.path.insert(0, str(ANALYSIS_DIR))
MODULE_PATH = ANALYSIS_DIR / "analyze_stable_projection_cross_validation.py"
SPEC = importlib.util.spec_from_file_location("stable_projection_cv", MODULE_PATH)
assert SPEC and SPEC.loader
cv = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(cv)


def sample_rows() -> list[dict[str, str]]:
    return [
        {"id": "a", "tst_2024": "alpha one", "tst_2025": "alpha later"},
        {"id": "b", "tst_2024": "beta two", "tst_2025": "beta later"},
        {"id": "c", "tst_2024": "gamma three", "tst_2025": "gamma later"},
    ]


class StableProjectionCrossValidationTests(unittest.TestCase):
    def test_leave_one_out_never_trains_on_held_out_case(self) -> None:
        rows = sample_rows()
        calls: list[tuple[str, list[str], float]] = []

        def fake_predict(inputs, training, prior_strength):
            calls.append(
                (inputs[0]["id"], [row["id"] for row in training], prior_strength)
            )
            return [
                {
                    "id": inputs[0]["id"],
                    "predicted_tst_2025": inputs[0]["tst_2024"],
                }
            ]

        with patch.object(cv.stable, "make_predictions", side_effect=fake_predict):
            predictions = cv.leave_one_out_predictions(rows)

        self.assertEqual([row["id"] for row in predictions], ["a", "b", "c"])
        self.assertEqual(
            calls,
            [
                ("a", ["b", "c"], 10.0),
                ("b", ["a", "c"], 10.0),
                ("c", ["a", "b"], 10.0),
            ],
        )

    def test_validation_rejects_duplicate_ids(self) -> None:
        rows = sample_rows()
        rows[1]["id"] = "a"
        with self.assertRaisesRegex(ValueError, "duplicate"):
            cv.validate_training_rows(rows)

    def test_validation_rejects_blank_response(self) -> None:
        rows = sample_rows()
        rows[1]["tst_2025"] = " "
        with self.assertRaisesRegex(ValueError, "nonblank"):
            cv.validate_training_rows(rows)

    def test_descriptive_scorecard_uses_aligned_cases(self) -> None:
        evaluator = SimpleNamespace(
            tokenize=lambda text: text.split(),
            normalize=lambda text: " ".join(text.lower().split()),
            rouge_l_f1=lambda left, right: 1.0 if left == right else 0.25,
        )
        scorecard = cv.descriptive_scorecard(
            ["one two", "three"],
            ["one two", "later words"],
            ["one", "three"],
            evaluator,
        )
        self.assertEqual(scorecard["prediction_word_count_mean"], 1.0)
        self.assertEqual(scorecard["reference_word_count_mean"], 2.0)
        self.assertEqual(scorecard["prediction_repeat_2024_rate"], 0.5)
        self.assertEqual(scorecard["observed_repeat_2024_rate"], 0.5)
        self.assertEqual(scorecard["prediction_source_similarity_mean"], 0.625)
        self.assertEqual(scorecard["observed_source_similarity_mean"], 0.625)

    def test_locked_plan_and_generator_hashes_match(self) -> None:
        project = Path(__file__).resolve().parents[1]
        self.assertEqual(
            cv.shared.sha256(
                project / "ANALYSIS_PLAN_STABLE_PROJECTION_CROSS_VALIDATION.md"
            ),
            cv.EXPECTED_PLAN_SHA256,
        )
        self.assertEqual(
            cv.shared.sha256(project / "analysis/stable_signifier_projection.py"),
            cv.EXPECTED_GENERATOR_SHA256,
        )


if __name__ == "__main__":
    unittest.main()
