#!/usr/bin/env python3
"""Validate the VCSSERG v1 three-form publication and PDF layout."""

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

from pypdf import PdfReader


PROJECT = Path(__file__).resolve().parents[1]
ROOT = PROJECT.parents[1]
PUBLIC = ROOT / "website/projects/vcsserg-repo-v1"


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


def main() -> int:
    summary_path = PUBLIC / "index.html"
    full_path = PUBLIC / "report/index.html"
    short_path = PUBLIC / "short-report.pdf"
    summary = Page(summary_path.read_text(encoding="utf-8"))
    full_source = full_path.read_text(encoding="utf-8")
    full = Page(full_source)

    assert summary.figures == 1, f"Executive Summary figures: {summary.figures}"
    assert full_source.lower().count("far beyond") == 1
    validate_local_links(summary_path, summary)
    validate_local_links(full_path, full)
    assert full_path.resolve() in local_targets(summary_path, summary)
    assert short_path.resolve() in local_targets(summary_path, summary)
    assert summary_path.resolve() in local_targets(full_path, full)
    assert short_path.resolve() in local_targets(full_path, full)

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

    print(
        "VCSSERG v1 publication: one summary figure, reciprocal HTML links, "
        f"required phrase, and {len(pdf.pages)}-page linked two-column PDF passed."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
