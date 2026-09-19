#!/usr/bin/env python3
"""Move Quarto report bypass links to the start of each generated body."""

import argparse
from html.parser import HTMLParser
from pathlib import Path
import re


SKIP_LINK = (
    '<a class="report-skip" href="#quarto-document-content">Skip to content</a>'
)
BODY_PATTERN = re.compile(r"<body(?:\s[^>]*)?>", flags=re.IGNORECASE)


class PromotionError(ValueError):
    """Raised when a generated report cannot be normalized safely."""


class BypassParser(HTMLParser):
    """Collect the minimum structure needed to validate a promoted page."""

    def __init__(self):
        super().__init__()
        self.body_count = 0
        self.main_ids = set()
        self.anchor_classes = []
        self.anchor_references = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == "body":
            self.body_count += 1
        elif tag == "main" and attributes.get("id"):
            self.main_ids.add(attributes["id"])
        elif tag == "a":
            self.anchor_classes.append(set(attributes.get("class", "").split()))
            self.anchor_references.append(attributes.get("href", ""))


def normalized_page(source: str, label: str) -> tuple[str, bool]:
    """Return public HTML whose report bypass link is the first anchor."""
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
        changed = False
    else:
        without_skip = source[:skip_start] + source[skip_start + len(SKIP_LINK) :]
        body = BODY_PATTERN.search(without_skip)
        candidate = (
            without_skip[: body.end()]
            + "\n"
            + SKIP_LINK
            + without_skip[body.end() :]
        )
        changed = True

    parsed = BypassParser()
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
    return candidate, changed


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
        description="Promote Quarto report bypass links in generated HTML."
    )
    parser.add_argument("tree", type=Path, help="generated report directory")
    args = parser.parse_args()
    try:
        pages, changed = promote_tree(args.tree)
    except PromotionError as error:
        raise SystemExit(f"promote_report_skip_links: {error}") from error
    print(f"Validated {pages} report page(s); promoted {changed} bypass link(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
