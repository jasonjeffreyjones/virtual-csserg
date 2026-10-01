from __future__ import annotations

import gzip
import sys
import tempfile
import unittest
from pathlib import Path


ANALYSIS = Path(__file__).resolve().parents[1] / "analysis"
sys.path.insert(0, str(ANALYSIS))

import analyze_semantic_neighborhood_additions as semantic  # noqa: E402


class SemanticNeighborhoodAdditionTests(unittest.TestCase):
    def test_embedding_loader_filters_and_validates_fixture(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "vectors.gz"
            with gzip.open(path, "wt", encoding="utf-8", newline="") as handle:
                handle.write("3 2\n")
                handle.write("reader 1 0\n")
                handle.write("music 0 1\n")
                handle.write("unused -1 0\n")
            vectors = semantic.load_embeddings(
                path, {"reader", "music"}, expected_count=3, dimension=2
            )
        self.assertEqual(vectors, {"reader": (1.0, 0.0), "music": (0.0, 1.0)})

    def test_embedding_loader_rejects_wrong_dimension(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "vectors.gz"
            with gzip.open(path, "wt", encoding="utf-8", newline="") as handle:
                handle.write("1 2\n")
                handle.write("reader 1\n")
            with self.assertRaises(ValueError):
                semantic.load_embeddings(
                    path, {"reader"}, expected_count=1, dimension=2
                )

    def test_centroid_uses_distinct_idf_weighted_tokens(self) -> None:
        vector, norm = semantic.centroid(
            {"reader", "music"},
            {"reader": (1.0, 0.0), "music": (0.0, 1.0)},
            {"reader": 3.0, "music": 1.0},
            dimension=2,
        )
        self.assertEqual(vector, (0.75, 0.25))
        self.assertAlmostEqual(norm, (0.75**2 + 0.25**2) ** 0.5)

    def test_semantic_neighbors_use_cosine_then_fold_order(self) -> None:
        indices, similarities = semantic.select_semantic_neighbors(
            {"book"},
            [{"book"}, {"read"}, {"music"}],
            {
                "book": (1.0, 0.0),
                "read": (1.0, 0.0),
                "music": (0.0, 1.0),
            },
            count=2,
            dimension=2,
        )
        self.assertEqual(indices, [0, 1])
        self.assertAlmostEqual(similarities[0], 1.0)
        self.assertAlmostEqual(similarities[1], 1.0)

    def test_zero_vector_has_zero_cosine(self) -> None:
        self.assertEqual(semantic.dense_cosine((0.0, 0.0), 0.0, (1.0, 0.0), 1.0), 0.0)

    def test_inherited_reproduction_rejects_changed_hits(self) -> None:
        inherited = {
            "id": "case",
            "source_unique_tokens": "4",
            "observed_addition_budget": "2",
            "marginal_hits": "1",
            "neighborhood_hits": "0",
        }
        semantic.require_inherited_reproduction(inherited, "case", 4, 2, 1, 0)
        with self.assertRaises(ValueError):
            semantic.require_inherited_reproduction(inherited, "case", 4, 2, 1, 1)

    def test_paired_summary_orients_positive_toward_semantic(self) -> None:
        summary = semantic.paired_summary(
            [0.5, 0.2], [0.1, 0.2], "semantic", "marginal", 100
        )
        self.assertAlmostEqual(summary["mean_effect_positive_favors_semantic"], 0.2)
        self.assertEqual(summary["semantic_case_wins"], 1)
        self.assertEqual(summary["case_ties"], 1)
        self.assertEqual(summary["semantic_case_losses"], 0)


if __name__ == "__main__":
    unittest.main()
