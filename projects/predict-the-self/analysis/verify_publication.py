#!/usr/bin/env python3
"""Validate Predict the Self's three-form publication and PDF layout."""

from html.parser import HTMLParser
import json
from pathlib import Path, PurePosixPath, PureWindowsPath
from urllib.parse import unquote, urlsplit

PROJECT = Path(__file__).resolve().parents[1]
ROOT = PROJECT.parents[1]
PUBLIC = ROOT / "website/projects/predict-the-self"
MANIFEST = PROJECT / "PUBLICATION_ARTIFACTS.json"
PUBLIC_PROJECT_URL = (
    "https://jasonjones.ninja/virtual-csserg/projects/predict-the-self/"
)
PUBLIC_REPORT_URL = PUBLIC_PROJECT_URL + "report/"


class Page(HTMLParser):
    def __init__(self, text: str):
        super().__init__()
        self.figures = 0
        self.ids = set()
        self.links = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == "figure":
            self.figures += 1
        if attributes.get("id"):
            self.ids.add(attributes["id"])
        for name in ("href", "src"):
            if attributes.get(name):
                self.links.append(attributes[name])


def resolve_local(path: Path, link: str) -> tuple[Path | None, str]:
    parsed = urlsplit(link)
    if parsed.scheme or parsed.netloc:
        return None, parsed.fragment
    target = (path.parent / unquote(parsed.path)).resolve() if parsed.path else path
    if target.is_dir():
        target = target / "index.html"
    return target, parsed.fragment


def validate_local_links(path: Path, page: Page) -> None:
    for link in page.links:
        target, fragment = resolve_local(path, link)
        if target is None:
            continue
        assert target.is_file(), f"{path.name}: missing local target {link}"
        if fragment and target.suffix.lower() == ".html":
            target_page = Page(target.read_text(encoding="utf-8"))
            assert fragment in target_page.ids, f"{path.name}: missing fragment {link}"


def local_targets(path: Path, page: Page) -> set[Path]:
    return {
        target
        for link in page.links
        for target, _ in [resolve_local(path, link)]
        if target is not None
    }


def validate_reciprocal_html_links(
    summary_path: Path,
    summary: Page,
    landing_path: Path,
    landing: Page,
    evidence_path: Path,
    evidence: Page,
    short_path: Path,
) -> None:
    """Require every HTML report surface to link to the other report forms."""
    summary_targets = local_targets(summary_path, summary)
    landing_targets = local_targets(landing_path, landing)
    evidence_targets = local_targets(evidence_path, evidence)
    assert landing_path.resolve() in summary_targets, (
        "Executive Summary omits Full Report landing page"
    )
    assert short_path.resolve() in summary_targets, (
        "Executive Summary omits short report"
    )
    for label, targets in (
        ("Full Report landing page", landing_targets),
        ("Full Report evidence chapter", evidence_targets),
    ):
        assert summary_path.resolve() in targets, f"{label} omits Executive Summary"
        assert short_path.resolve() in targets, f"{label} omits short report"


def pdf_external_uris(pdf) -> set[str]:
    """Collect external URI actions from every annotation in a PDF reader."""
    uris = set()
    for page in pdf.pages:
        for reference in page.get("/Annots", []):
            annotation = reference.get_object()
            action = annotation.get("/A")
            if hasattr(action, "get_object"):
                action = action.get_object()
            uri = action.get("/URI") if action else None
            if uri:
                uris.add(str(uri))
    return uris


def validate_pdf_report_links(pdf) -> None:
    """Require the short PDF to link back to both public HTML report forms."""
    uris = pdf_external_uris(pdf)
    expected = {PUBLIC_PROJECT_URL, PUBLIC_REPORT_URL}
    missing = sorted(expected - uris)
    assert not missing, f"short report omits reciprocal links: {', '.join(missing)}"


def validate_artifact_copy(source: Path, canonical: Path, alias: Path) -> None:
    """Require both public copies to equal the authoritative Project source."""
    expected = source.read_bytes()
    assert canonical.read_bytes() == expected, (
        f"published artifact differs from Project source: {canonical}"
    )
    assert alias.read_bytes() == expected, (
        f"published artifact alias differs from Project source: {alias}"
    )


def load_artifact_manifest(path: Path = MANIFEST) -> dict[str, str]:
    """Load the publisher's sole source-to-alias artifact inventory."""
    pairs = json.loads(
        path.read_text(encoding="utf-8"), object_pairs_hook=lambda items: items
    )
    assert isinstance(pairs, list) and pairs, (
        "artifact manifest must be a nonempty JSON object"
    )
    artifacts = {}
    aliases = set()
    for entry in pairs:
        assert isinstance(entry, tuple) and len(entry) == 2, (
            "artifact manifest must be a JSON object"
        )
        source, alias = entry
        assert isinstance(source, str) and isinstance(alias, str), (
            "artifact manifest paths must be strings"
        )
        assert source not in artifacts, f"duplicate artifact source {source}"
        assert alias not in aliases, f"duplicate artifact alias {alias}"
        for label, value in (("source", source), ("alias", alias)):
            relative = PurePosixPath(value)
            assert (
                relative.parts
                and not relative.is_absolute()
                and ".." not in relative.parts
                and "\\" not in value
            ), f"unsafe artifact {label} path {value}"
        assert PurePosixPath(alias).parts[0] == "artifacts", (
            f"artifact alias is outside artifacts/: {alias}"
        )
        assert source != alias, f"artifact source and alias are identical: {source}"
        artifacts[source] = alias
        aliases.add(alias)
    return artifacts


def validate_artifact_links(
    report_root: Path,
    evidence_targets: set[Path],
    artifacts: dict[str, str],
) -> None:
    """Require the report's canonical artifact links to equal the inventory."""
    report_root = report_root.resolve()
    expected = {(report_root / source).resolve() for source in artifacts}
    linked = set()
    for target in evidence_targets:
        try:
            relative = target.resolve().relative_to(report_root)
        except ValueError:
            continue
        if relative.parts and (
            relative.parts[0] in {"analysis", "results", "submissions"}
            or relative.name == "BENCHMARK_PROVENANCE.md"
            or relative.name == "PUBLICATION_ARTIFACTS.json"
            or relative.name.startswith("ANALYSIS_PLAN_")
        ):
            linked.add(target.resolve())
    missing = sorted(str(path.relative_to(report_root)) for path in expected - linked)
    unlisted = sorted(str(path.relative_to(report_root)) for path in linked - expected)
    assert not missing, f"Full Report omits inventoried artifacts: {', '.join(missing)}"
    assert not unlisted, (
        f"Full Report links unlisted research artifacts: {', '.join(unlisted)}"
    )


def validate_scorecard_provenance(scorecard: dict[str, object]) -> None:
    """Reject machine-specific paths from public scorecard provenance."""
    for field in ("predictions", "references"):
        value = scorecard.get(field)
        assert isinstance(value, str) and value, f"scorecard {field} is missing"
        parsed = urlsplit(value)
        assert parsed.scheme != "file", f"scorecard {field} uses a file URI: {value}"
        assert not Path(value).is_absolute(), (
            f"scorecard {field} exposes an absolute host path: {value}"
        )
        assert not PureWindowsPath(value).is_absolute(), (
            f"scorecard {field} exposes an absolute host path: {value}"
        )


def main() -> int:
    from pypdf import PdfReader

    summary_path = PUBLIC / "index.html"
    landing_path = PUBLIC / "report/index.html"
    evidence_path = PUBLIC / "report/report.html"
    short_path = PUBLIC / "short-report.pdf"
    for required in (summary_path, landing_path, evidence_path, short_path):
        assert required.is_file(), f"missing publication artifact {required}"

    summary = Page(summary_path.read_text(encoding="utf-8"))
    landing_source = landing_path.read_text(encoding="utf-8")
    evidence_source = evidence_path.read_text(encoding="utf-8")
    landing = Page(landing_source)
    evidence = Page(evidence_source)

    assert summary.figures == 1, f"Executive Summary figures: {summary.figures}"
    phrase_count = (landing_source + evidence_source).lower().count("far beyond")
    assert phrase_count == 1, f"Full Report phrase count: {phrase_count}"
    for path, page in (
        (summary_path, summary),
        (landing_path, landing),
        (evidence_path, evidence),
    ):
        validate_local_links(path, page)

    validate_reciprocal_html_links(
        summary_path,
        summary,
        landing_path,
        landing,
        evidence_path,
        evidence,
        short_path,
    )

    artifacts = load_artifact_manifest()
    for scorecard_name in (
        "stable_signifier_dev_scorecard.json",
        "trajectory_retrieval_dev_scorecard.json",
    ):
        with (PROJECT / "results" / scorecard_name).open(encoding="utf-8") as handle:
            validate_scorecard_provenance(json.load(handle))
    evidence_targets = local_targets(evidence_path, evidence)
    validate_artifact_links(PUBLIC / "report", evidence_targets, artifacts)
    for source, alias in artifacts.items():
        validate_artifact_copy(
            PROJECT / source,
            PUBLIC / "report" / source,
            PUBLIC / "report" / alias,
        )

    pdf = PdfReader(short_path)
    assert 1 <= len(pdf.pages) <= 10, f"PDF pages: {len(pdf.pages)}"
    columns = set()
    annotations = 0
    for page in pdf.pages:
        assert page.extract_text().strip(), "empty PDF page"
        annotations += len(page.get("/Annots", []))

        def visit(text, cm, tm, _font, _size):
            x = cm[4] + tm[4]
            y = cm[5] + tm[5]
            if text.strip() and y > 40:
                if 35 <= x < 295:
                    columns.add("left")
                elif 295 <= x <= 570:
                    columns.add("right")

        page.extract_text(visitor_text=visit)
    assert columns == {"left", "right"}, f"PDF body columns found: {columns}"
    assert annotations >= 5, f"PDF link annotations found: {annotations}"
    validate_pdf_report_links(pdf)

    print(
        "Predict the Self publication: one summary figure, two-chapter linked "
        f"Full Report, {len(artifacts)} artifacts, required phrase, and {len(pdf.pages)}-page "
        "two-column PDF passed."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
