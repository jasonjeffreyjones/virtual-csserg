#!/usr/bin/env python3
"""Validate Predict the Self's three-form publication and PDF layout."""

from html.parser import HTMLParser
import json
from pathlib import Path, PurePosixPath, PureWindowsPath
import re
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
        self.result_claims = []
        self.result_bars = []
        self.result_labels = []
        self._open_result_claims = []
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
        result_attributes = {
            "id": attributes.get("id"),
            "source": attributes.get("data-result-source"),
            "pointer": attributes.get("data-result-pointer"),
            "format": attributes.get("data-result-format"),
        }
        if any(
            result_attributes[name] is not None
            for name in ("source", "pointer", "format")
        ):
            result_attributes.update({"tag": tag, "text_parts": []})
            self._open_result_claims.append(result_attributes)
        if attributes.get("data-result-bar-for") is not None:
            self.result_bars.append(
                {
                    "result_id": attributes["data-result-bar-for"],
                    "classes": attributes.get("class", "").split(),
                }
            )
        if attributes.get("data-result-label-for") is not None:
            self.result_labels.append(
                {
                    "result_ids": attributes["data-result-label-for"].split(),
                    "aria_label": attributes.get("aria-label"),
                }
            )

    def handle_data(self, data):
        for claim in self._open_result_claims:
            claim["text_parts"].append(data)

    def handle_endtag(self, tag):
        if self._open_result_claims and self._open_result_claims[-1]["tag"] == tag:
            claim = self._open_result_claims.pop()
            claim["text"] = " ".join("".join(claim.pop("text_parts")).split())
            claim.pop("tag")
            self.result_claims.append(claim)


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


def resolve_json_pointer(document: object, pointer: str) -> object:
    """Resolve an RFC 6901 JSON pointer with explicit structural checks."""
    assert pointer == "" or pointer.startswith("/"), (
        f"result claim uses an invalid JSON pointer: {pointer}"
    )
    current = document
    if not pointer:
        return current
    for raw_token in pointer[1:].split("/"):
        token = raw_token.replace("~1", "/").replace("~0", "~")
        if isinstance(current, dict):
            assert token in current, f"result claim JSON pointer is missing: {pointer}"
            current = current[token]
        elif isinstance(current, list):
            assert token.isdigit() and int(token) < len(current), (
                f"result claim JSON pointer is missing: {pointer}"
            )
            current = current[int(token)]
        else:
            raise AssertionError(f"result claim JSON pointer is missing: {pointer}")
    return current


def validate_result_claims(
    page: Page,
    project: Path,
    artifacts: dict[str, str],
    expected_count: int,
) -> dict[str, dict[str, object]]:
    """Require annotated displayed values to equal inventoried JSON results."""
    assert len(page.result_claims) == expected_count, (
        f"Executive Summary result claims: {len(page.result_claims)}"
    )
    documents = {}
    resolved_claims = {}
    for claim in page.result_claims:
        source = claim.get("source")
        pointer = claim.get("pointer")
        format_spec = claim.get("format")
        assert all(isinstance(value, str) and value for value in (
            source,
            pointer,
            format_spec,
        )), "result claim provenance is incomplete"
        assert source in artifacts and source.endswith(".json"), (
            f"result claim source is not an inventoried JSON artifact: {source}"
        )
        assert re.fullmatch(r"\.\d{1,2}f", format_spec), (
            f"result claim format is invalid: {format_spec}"
        )
        if source not in documents:
            documents[source] = json.loads(
                (project / source).read_text(encoding="utf-8")
            )
        value = resolve_json_pointer(documents[source], pointer)
        assert isinstance(value, (int, float)) and not isinstance(value, bool), (
            f"result claim is not numeric: {source}#{pointer}"
        )
        expected = format(value, format_spec)
        actual = claim["text"]
        assert actual == expected, (
            f"displayed result differs from {source}#{pointer}: "
            f"expected {expected}, found {actual}"
        )
        claim_id = claim.get("id")
        if claim_id is not None:
            assert isinstance(claim_id, str) and claim_id, "result claim id is empty"
            assert claim_id not in resolved_claims, f"duplicate result claim id: {claim_id}"
            resolved_claims[claim_id] = {"value": value, "display": actual}
    return resolved_claims


def css_width_for_class(stylesheet: str, css_class: str) -> str:
    """Read one simple class rule's one explicit width declaration."""
    rule_pattern = re.compile(
        rf"(?<![-\w])\.{re.escape(css_class)}\s*\{{([^{{}}]*)\}}", re.DOTALL
    )
    rules = rule_pattern.findall(stylesheet)
    assert len(rules) == 1, f"result bar CSS rule count for .{css_class}: {len(rules)}"
    widths = re.findall(r"(?:^|;)\s*width\s*:\s*([^;]+)\s*;", rules[0])
    assert len(widths) == 1, (
        f"result bar width declaration count for .{css_class}: {len(widths)}"
    )
    return widths[0].strip()


def validate_figure_result_encodings(
    page: Page,
    resolved_claims: dict[str, dict[str, object]],
    stylesheet: str,
    expected_bars: int,
) -> None:
    """Bind chart widths and accessible numeric text to resolved result claims."""
    assert len(page.result_bars) == expected_bars, (
        f"Executive Summary source-verified result bars: {len(page.result_bars)}"
    )
    result_ids = []
    for bar in page.result_bars:
        result_id = bar["result_id"]
        classes = bar["classes"]
        assert isinstance(result_id, str) and result_id in resolved_claims, (
            f"result bar references an unknown claim: {result_id}"
        )
        assert isinstance(classes, list) and len(classes) == 1, (
            f"result bar must have exactly one CSS class: {classes}"
        )
        value = resolved_claims[result_id]["value"]
        assert isinstance(value, (int, float)) and 0 <= value <= 1, (
            f"result bar value is outside the 0-1 scale: {result_id}"
        )
        expected_width = f"{value * 100:.4f}%"
        actual_width = css_width_for_class(stylesheet, classes[0])
        assert actual_width == expected_width, (
            f"result bar differs from {result_id}: expected {expected_width}, "
            f"found {actual_width}"
        )
        result_ids.append(result_id)
    assert len(set(result_ids)) == expected_bars, "result bars repeat a claim"

    assert len(page.result_labels) == 1, (
        f"Executive Summary source-verified accessible result labels: "
        f"{len(page.result_labels)}"
    )
    label = page.result_labels[0]
    assert label["result_ids"] == result_ids, (
        "accessible result label does not reference every bar in display order"
    )
    aria_label = label["aria_label"]
    assert isinstance(aria_label, str) and aria_label, (
        "source-verified result figure has no accessible label"
    )
    actual_values = re.findall(r"[-+]?(?:\d+\.\d+|\d+)", aria_label)
    expected_values = [
        str(resolved_claims[result_id]["display"]) for result_id in result_ids
    ]
    assert actual_values == expected_values, (
        "accessible result values differ from source-verified figure values: "
        f"expected {expected_values}, found {actual_values}"
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
    resolved_claims = validate_result_claims(
        summary, PROJECT, artifacts, expected_count=20
    )
    validate_figure_result_encodings(
        summary,
        resolved_claims,
        (ROOT / "website/assets/styles.css").read_text(encoding="utf-8"),
        expected_bars=5,
    )
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
        "Predict the Self publication: one summary figure with 20 source-verified "
        "headline values, five source-verified bars and accessible values, "
        "two-chapter linked "
        f"Full Report, {len(artifacts)} artifacts, required phrase, and {len(pdf.pages)}-page "
        "two-column PDF passed."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
