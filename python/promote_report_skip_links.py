#!/usr/bin/env python3
"""Normalize generated Quarto bypass links and navigation landmarks."""

import argparse
from html.parser import HTMLParser
from pathlib import Path
import re


SKIP_LINK = (
    '<a class="report-skip" href="#quarto-document-content">Skip to content</a>'
)
BODY_PATTERN = re.compile(r"<body(?:\s[^>]*)?>", flags=re.IGNORECASE)
NAV_PATTERN = re.compile(r"<nav(?:\s[^>]*)?>", flags=re.IGNORECASE)
NAVIGATION_CLASS_LABELS = {
    "quarto-secondary-nav": "Report navigation",
    "sidebar-navigation": "Report chapters",
    "toc-active": "On this page",
    "page-navigation": "Previous and next chapters",
}


class PromotionError(ValueError):
    """Raised when a generated report cannot be normalized safely."""


class ReportParser(HTMLParser):
    """Collect the structure needed to validate a normalized report page."""

    def __init__(self):
        super().__init__()
        self.body_count = 0
        self.main_ids = set()
        self.anchor_classes = []
        self.anchor_references = []
        self.ids = set()
        self.navigation_landmarks = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if attributes.get("id"):
            self.ids.add(attributes["id"])
        if tag == "body":
            self.body_count += 1
        elif tag == "main" and attributes.get("id"):
            self.main_ids.add(attributes["id"])
        elif tag == "a":
            self.anchor_classes.append(set(attributes.get("class", "").split()))
            self.anchor_references.append(attributes.get("href", ""))
        if tag == "nav":
            self.navigation_landmarks.append(
                (
                    set(attributes.get("class", "").split()),
                    attributes.get("aria-label", "").strip(),
                    attributes.get("aria-labelledby", "").split(),
                )
            )


class StartTagParser(HTMLParser):
    """Parse one generated start tag without rewriting unrelated markup."""

    def __init__(self):
        super().__init__()
        self.attributes = {}

    def handle_starttag(self, _tag, attrs):
        self.attributes = dict(attrs)


def label_navigation_landmarks(source: str, label: str) -> tuple[str, bool]:
    """Add stable names to Quarto navigation landmarks that omit them."""

    changed = False

    def replacement(match):
        nonlocal changed
        tag_source = match.group(0)
        parser = StartTagParser()
        parser.feed(tag_source)
        attributes = parser.attributes
        classes = set(attributes.get("class", "").split())
        matched_labels = {
            accessible_name
            for class_name, accessible_name in NAVIGATION_CLASS_LABELS.items()
            if class_name in classes
        }
        if not matched_labels:
            return tag_source
        if len(matched_labels) != 1:
            raise PromotionError(
                f"{label}: navigation landmark matches conflicting label rules"
            )
        if attributes.get("aria-label", "").strip() or attributes.get(
            "aria-labelledby", ""
        ).strip():
            return tag_source
        changed = True
        accessible_name = matched_labels.pop()
        return tag_source[:-1] + f' aria-label="{accessible_name}">'

    return NAV_PATTERN.sub(replacement, source), changed


def normalized_page(source: str, label: str) -> tuple[str, bool]:
    """Return public HTML with an early bypass and named navigation landmarks."""
    if source.count(SKIP_LINK) != 1:
        raise PromotionError(f"{label}: expected exactly one report bypass link")

    bodies = list(BODY_PATTERN.finditer(source))
    if len(bodies) != 1:
        raise PromotionError(f"{label}: expected exactly one body element")

    body = bodies[0]
    first_anchor = re.search(r"<a(?:\s|>)", source, flags=re.IGNORECASE)
    skip_start = source.index(SKIP_LINK)
    already_promoted = (
        first_anchor
        and first_anchor.start() == skip_start
        and not source[body.end() : skip_start].strip()
    )
    if already_promoted:
        candidate = source
        bypass_changed = False
    else:
        without_skip = source[:skip_start] + source[skip_start + len(SKIP_LINK) :]
        body = BODY_PATTERN.search(without_skip)
        candidate = (
            without_skip[: body.end()]
            + "\n"
            + SKIP_LINK
            + without_skip[body.end() :]
        )
        bypass_changed = True

    candidate, navigation_changed = label_navigation_landmarks(candidate, label)

    parsed = ReportParser()
    parsed.feed(candidate)
    if parsed.body_count != 1:
        raise PromotionError(f"{label}: promotion did not preserve one body element")
    if "quarto-document-content" not in parsed.main_ids:
        raise PromotionError(f"{label}: bypass target is not a main element")
    promoted_body = BODY_PATTERN.search(candidate)
    promoted_skip = candidate.index(SKIP_LINK)
    if candidate[promoted_body.end() : promoted_skip].strip():
        raise PromotionError(f"{label}: bypass link is not first in the body")
    if not parsed.anchor_classes or "report-skip" not in parsed.anchor_classes[0]:
        raise PromotionError(f"{label}: bypass link is not the first anchor")
    if parsed.anchor_references[0] != "#quarto-document-content":
        raise PromotionError(f"{label}: bypass link has the wrong target")
    for classes, accessible_name, labelled_by in parsed.navigation_landmarks:
        if not accessible_name and not labelled_by:
            description = " ".join(sorted(classes)) or "unclassified"
            raise PromotionError(
                f"{label}: navigation landmark has no accessible name: {description}"
            )
        missing_ids = sorted(set(labelled_by) - parsed.ids)
        if missing_ids:
            raise PromotionError(
                f"{label}: navigation landmark references missing label ids: "
                + ", ".join(missing_ids)
            )
    return candidate, bypass_changed or navigation_changed


def promote_tree(tree: Path) -> tuple[int, int]:
    """Preflight and normalize every generated HTML page carrying the marker."""
    tree = Path(tree).resolve()
    if not tree.is_dir():
        raise PromotionError(f"report tree is not a directory: {tree}")

    planned = []
    for path in sorted(tree.rglob("*.html")):
        source = path.read_text(encoding="utf-8")
        if "report-skip" not in source:
            continue
        normalized, changed = normalized_page(source, str(path))
        planned.append((path, normalized, changed))

    if not planned:
        raise PromotionError(f"no report bypass link found under {tree}")

    for path, normalized, changed in planned:
        if changed:
            path.write_text(normalized, encoding="utf-8")
    return len(planned), sum(changed for _, _, changed in planned)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Normalize Quarto report accessibility in generated HTML."
    )
    parser.add_argument("tree", type=Path, help="generated report directory")
    args = parser.parse_args()
    try:
        pages, changed = promote_tree(args.tree)
    except PromotionError as error:
        raise SystemExit(f"promote_report_skip_links: {error}") from error
    print(f"Validated {pages} report page(s); normalized {changed} page(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
