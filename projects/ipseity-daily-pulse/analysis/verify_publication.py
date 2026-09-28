#!/usr/bin/env python3
"""Verify current Ipseity Daily Pulse publication derivatives."""

from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys

from pypdf import PdfReader


PROJECT = Path(__file__).resolve().parents[1]
ROOT = PROJECT.parents[1]
PUBLIC = ROOT / "website/projects/ipseity-daily-pulse"


class SummaryParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.figures = 0
        self.references = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == "figure":
            self.figures += 1
        elif tag == "a":
            self.references.append(attributes.get("href", ""))


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def column_coverage(page):
    widths = []
    for item in page.get_text("dict").get("blocks", []):
        if "bbox" not in item:
            continue
        text = "".join(
            span.get("text", "")
            for line in item.get("lines", [])
            for span in line.get("spans", [])
        ).strip()
        if text:
            widths.append((item["bbox"], text))
    left = any(box[0] < 280 and box[2] < 330 and len(text) > 20 for box, text in widths)
    right = any(box[0] > 300 and len(text) > 20 for box, text in widths)
    return left and right


def main() -> int:
    summary_path = PUBLIC / "index.html"
    report_path = PUBLIC / "report/index.html"
    pdf_path = PUBLIC / "short-report.pdf"
    blog_path = PUBLIC / "blog/2026-09-26-a-leaderboard-is-not-a-discovery.html"
    blog_index_path = PUBLIC / "blog/index.html"
    artifact_path = PUBLIC / "artifacts/current-summary.json"
    for path in (
        summary_path,
        report_path,
        pdf_path,
        blog_path,
        blog_index_path,
        artifact_path,
    ):
        require(path.is_file(), f"missing publication artifact: {path}")

    summary = summary_path.read_text(encoding="utf-8")
    parsed = SummaryParser()
    parsed.feed(summary)
    require(parsed.figures == 1, "Executive Summary must contain exactly one figure")
    require("report/" in parsed.references, "Executive Summary must link Full Report")
    require("short-report.pdf" in parsed.references, "Executive Summary must link PDF")

    report = report_path.read_text(encoding="utf-8")
    require(report.lower().count("far beyond") == 1, "Full Report phrase count differs from one")
    for text in ("716,237", "704", "0e3558ecb76f84cb33ca1fa878f81cb82159457987bd384edad13c34b2cd2354"):
        require(text in report, f"Full Report missing current value {text}")

    current = json.loads((PROJECT / "outputs/current-summary.json").read_text(encoding="utf-8"))
    public_current = json.loads(artifact_path.read_text(encoding="utf-8"))
    require(public_current == current, "published current summary differs from analysis output")
    require(current["dataset"]["observations"] == 716237, "unexpected observation count")
    require(current["trend_method"]["eligible_signifiers"] == 704, "unexpected eligible count")
    require(current["trend_method"]["fdr_05_discoveries"] == 0, "unexpected FDR discoveries")
    require(current["trend_method"]["bonferroni_05_discoveries"] == 0, "unexpected Bonferroni discoveries")

    reader = PdfReader(pdf_path)
    require(1 <= len(reader.pages) <= 10, "short PDF must have 1-10 pages")
    require(all(page.extract_text().strip() for page in reader.pages), "short PDF has empty page")
    try:
        import fitz
    except ImportError:
        fitz = None
    if fitz is not None:
        document = fitz.open(pdf_path)
        require(all(column_coverage(page) for page in document), "short PDF does not occupy both columns")

    blog = blog_path.read_text(encoding="utf-8")
    require("none" in blog.lower() and "704" in blog, "blog omits central multiplicity result")
    entries = sorted((PUBLIC / "blog").glob("20*.html"))
    require(len(entries) == 10, f"expected 10 blog entries; found {len(entries)}")
    blog_index = blog_index_path.read_text(encoding="utf-8")
    for entry in entries:
        require(entry.name in blog_index, f"blog index omits {entry.name}")
        pinned_figure = PUBLIC / "blog/images" / f"{entry.stem}.svg"
        require(pinned_figure.is_file(), f"blog entry has no pinned figure: {entry.stem}")
    home = (ROOT / "website/index.html").read_text(encoding="utf-8")
    require(
        "projects/ipseity-daily-pulse/blog/2026-09-26-a-leaderboard-is-not-a-discovery.html" in home,
        "home page does not link latest outreach entry",
    )
    print(
        "PASS: publication derivatives, current values, 10-entry blog, "
        f"home-page link, and {len(reader.pages)}-page PDF"
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as error:
        print(f"FAIL: {error}", file=sys.stderr)
        raise SystemExit(1)
