from __future__ import annotations

import sys
import unittest
from pathlib import Path


ANALYSIS = Path(__file__).resolve().parents[1] / "analysis"
sys.path.insert(0, str(ANALYSIS))

import stable_signifier_projection as model  # noqa: E402


class StableSignifierProjectionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.training = [
            {
                "id": "train_1",
                "tst_2024": "I am a gardener.\nI am tired.\nI love music.",
                "tst_2025": "I am a gardener. I love music.",
            },
            {
                "id": "train_2",
                "tst_2024": "I am a reader.\nI love music.\nI feel hungry.",
                "tst_2025": "I am a reader. I love music. I am curious.",
            },
        ]

    def test_tokenizer_matches_evaluator_normalization(self) -> None:
        self.assertEqual(
            model.tokenize("  I’m HERE, and  I'm ready. "),
            ["i’m", "here", "and", "i'm", "ready"],
        )

    def test_predictions_are_deterministic_nonblank_and_extractive(self) -> None:
        inputs = [
            {
                "id": "test_1",
                "tst_2024": "I am a gardener.\nI feel worried.\nI love music.",
            }
        ]
        first = model.make_predictions(inputs, self.training, 10.0)
        second = model.make_predictions(inputs, self.training, 10.0)
        self.assertEqual(first, second)
        self.assertEqual(first[0]["id"], "test_1")
        prediction = first[0]["predicted_tst_2025"]
        self.assertTrue(prediction.strip())
        self.assertLessEqual(set(model.tokenize(prediction)), set(model.tokenize(inputs[0]["tst_2024"])))

    def test_response_units_prefer_existing_lines(self) -> None:
        self.assertEqual(
            model.response_units("first line\nsecond line\nthird line"),
            ["first line", "second line", "third line"],
        )


if __name__ == "__main__":
    unittest.main()
