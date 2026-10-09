from __future__ import annotations

import importlib.util
from pathlib import Path
from types import SimpleNamespace
import tempfile
import unittest


MODULE_PATH = (
    Path(__file__).resolve().parents[1] / "analysis/verify_publication.py"
)
SPEC = importlib.util.spec_from_file_location("predict_verify_publication", MODULE_PATH)
assert SPEC and SPEC.loader
verify_publication = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(verify_publication)


class FakeAnnotation:
    def __init__(self, uri: str):
        self.uri = uri

    def get_object(self):
        return {"/A": {"/URI": self.uri}}


def fake_pdf(*uris: str):
    return SimpleNamespace(
        pages=[{"/Annots": [FakeAnnotation(uri) for uri in uris]}]
    )


class ArtifactCopyTests(unittest.TestCase):
    def test_matching_canonical_and_alias_copies_pass(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "source.txt"
            canonical = root / "canonical.txt"
            alias = root / "alias.txt"
            for path in (source, canonical, alias):
                path.write_bytes(b"authoritative research artifact\n")

            verify_publication.validate_artifact_copy(source, canonical, alias)

    def test_stale_canonical_copy_fails_even_when_public_copies_match(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "source.txt"
            canonical = root / "canonical.txt"
            alias = root / "alias.txt"
            source.write_bytes(b"current\n")
            canonical.write_bytes(b"stale\n")
            alias.write_bytes(b"stale\n")

            with self.assertRaisesRegex(
                AssertionError, "published artifact differs from Project source"
            ):
                verify_publication.validate_artifact_copy(source, canonical, alias)

    def test_stale_alias_copy_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "source.txt"
            canonical = root / "canonical.txt"
            alias = root / "alias.txt"
            source.write_bytes(b"current\n")
            canonical.write_bytes(b"current\n")
            alias.write_bytes(b"stale\n")

            with self.assertRaisesRegex(
                AssertionError,
                "published artifact alias differs from Project source",
            ):
                verify_publication.validate_artifact_copy(source, canonical, alias)


class ArtifactInventoryLinkTests(unittest.TestCase):
    def test_project_manifest_loads_with_unique_paths(self) -> None:
        artifacts = verify_publication.load_artifact_manifest()

        self.assertEqual(len(artifacts), 69)
        self.assertEqual(len(set(artifacts.values())), 69)
        self.assertEqual(
            artifacts["PUBLICATION_ARTIFACTS.json"],
            "artifacts/PUBLICATION_ARTIFACTS.json",
        )

    def test_exact_inventory_links_pass(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            report = Path(temporary) / "report"
            artifacts = {
                "results/a.csv": "artifacts/a.csv",
                "analysis/a.py": "artifacts/a.py",
            }
            targets = {report / source for source in artifacts}

            verify_publication.validate_artifact_links(report, targets, artifacts)

    def test_missing_inventoried_link_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            report = Path(temporary) / "report"
            artifacts = {
                "results/a.csv": "artifacts/a.csv",
                "results/b.csv": "artifacts/b.csv",
            }

            with self.assertRaisesRegex(
                AssertionError, "Full Report omits inventoried artifacts"
            ):
                verify_publication.validate_artifact_links(
                    report, {report / "results/a.csv"}, artifacts
                )

    def test_unlisted_research_link_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            report = Path(temporary) / "report"
            artifacts = {"results/a.csv": "artifacts/a.csv"}

            with self.assertRaisesRegex(
                AssertionError, "Full Report links unlisted research artifacts"
            ):
                verify_publication.validate_artifact_links(
                    report,
                    {report / "results/a.csv", report / "results/unlisted.csv"},
                    artifacts,
                )


class DisplayedResultClaimTests(unittest.TestCase):
    def make_claim_page(self, displayed: str = "0.125000"):
        return verify_publication.Page(
            '<strong data-result-source="results/score.json" '
            'data-result-pointer="/metrics/agreement/value" '
            f'data-result-format=".6f">{displayed}</strong>'
        )

    def test_displayed_value_matches_inventoried_json_result(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary)
            result = project / "results/score.json"
            result.parent.mkdir()
            result.write_text(
                '{"metrics":{"agreement":{"value":0.125}}}', encoding="utf-8"
            )

            verify_publication.validate_result_claims(
                self.make_claim_page(),
                project,
                {"results/score.json": "artifacts/score.json"},
                expected_count=1,
            )

    def test_stale_displayed_value_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary)
            result = project / "results/score.json"
            result.parent.mkdir()
            result.write_text(
                '{"metrics":{"agreement":{"value":0.125}}}', encoding="utf-8"
            )

            with self.assertRaisesRegex(
                AssertionError, "displayed result differs"
            ):
                verify_publication.validate_result_claims(
                    self.make_claim_page("0.250000"),
                    project,
                    {"results/score.json": "artifacts/score.json"},
                    expected_count=1,
                )

    def test_uninventoried_result_source_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            with self.assertRaisesRegex(
                AssertionError, "not an inventoried JSON artifact"
            ):
                verify_publication.validate_result_claims(
                    self.make_claim_page(),
                    Path(temporary),
                    {},
                    expected_count=1,
                )

    def test_missing_headline_claim_fails(self) -> None:
        with self.assertRaisesRegex(
            AssertionError, "Executive Summary result claims: 0"
        ):
            verify_publication.validate_result_claims(
                verify_publication.Page("<strong>0.125000</strong>"),
                Path("."),
                {},
                expected_count=1,
            )


class ScorecardProvenanceTests(unittest.TestCase):
    def test_logical_relative_paths_pass(self) -> None:
        verify_publication.validate_scorecard_provenance(
            {
                "predictions": "projects/predict-the-self/results/predictions.csv",
                "references": "benchmark@commit/data/dev.csv",
            }
        )

    def test_posix_absolute_path_fails(self) -> None:
        with self.assertRaisesRegex(AssertionError, "absolute host path"):
            verify_publication.validate_scorecard_provenance(
                {
                    "predictions": "/home/researcher/predictions.csv",
                    "references": "benchmark@commit/data/dev.csv",
                }
            )

    def test_windows_absolute_path_fails(self) -> None:
        with self.assertRaisesRegex(AssertionError, "absolute host path"):
            verify_publication.validate_scorecard_provenance(
                {
                    "predictions": "projects/predictions.csv",
                    "references": "C:\\Users\\researcher\\dev.csv",
                }
            )

    def test_file_uri_fails(self) -> None:
        with self.assertRaisesRegex(AssertionError, "file URI"):
            verify_publication.validate_scorecard_provenance(
                {
                    "predictions": "projects/predictions.csv",
                    "references": "file:///tmp/dev.csv",
                }
            )


class ReciprocalReportLinkTests(unittest.TestCase):
    def test_all_html_report_surfaces_link_to_other_forms(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            summary_path = root / "index.html"
            landing_path = root / "report/index.html"
            evidence_path = root / "report/report.html"
            short_path = root / "short-report.pdf"

            summary = verify_publication.Page(
                '<a href="report/index.html">Full</a>'
                '<a href="short-report.pdf">Short</a>'
            )
            report_links = (
                '<a href="../index.html">Summary</a>'
                '<a href="../short-report.pdf">Short</a>'
            )
            landing = verify_publication.Page(report_links)
            evidence = verify_publication.Page(report_links)

            verify_publication.validate_reciprocal_html_links(
                summary_path,
                summary,
                landing_path,
                landing,
                evidence_path,
                evidence,
                short_path,
            )

    def test_evidence_chapter_without_short_report_link_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            summary_path = root / "index.html"
            landing_path = root / "report/index.html"
            evidence_path = root / "report/report.html"
            short_path = root / "short-report.pdf"

            with self.assertRaisesRegex(
                AssertionError, "Full Report evidence chapter omits short report"
            ):
                verify_publication.validate_reciprocal_html_links(
                    summary_path,
                    verify_publication.Page(
                        '<a href="report/index.html">Full</a>'
                        '<a href="short-report.pdf">Short</a>'
                    ),
                    landing_path,
                    verify_publication.Page(
                        '<a href="../index.html">Summary</a>'
                        '<a href="../short-report.pdf">Short</a>'
                    ),
                    evidence_path,
                    verify_publication.Page(
                        '<a href="../index.html">Summary</a>'
                    ),
                    short_path,
                )

    def test_pdf_links_to_both_html_report_forms(self) -> None:
        verify_publication.validate_pdf_report_links(
            fake_pdf(
                verify_publication.PUBLIC_PROJECT_URL,
                verify_publication.PUBLIC_REPORT_URL,
            )
        )

    def test_unrelated_pdf_annotations_do_not_satisfy_reciprocity(self) -> None:
        with self.assertRaisesRegex(AssertionError, "short report omits reciprocal"):
            verify_publication.validate_pdf_report_links(
                fake_pdf(
                    "https://example.com/one",
                    "https://example.com/two",
                    "https://example.com/three",
                    "https://example.com/four",
                    "https://example.com/five",
                )
            )

if __name__ == "__main__":
    unittest.main()
