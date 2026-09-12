#!/usr/bin/env python3
"""Create a validated, unpublished Virtual CSSERG Project scaffold."""

from __future__ import annotations

import argparse
from pathlib import Path
import re
import shutil
import tempfile


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PROJECTS_ROOT = REPOSITORY_ROOT / "projects"
SLUG_PATTERN = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")
REQUIRED_TEMPLATE_FILES = {"PROJECT.md", "STATE.md", "DIALOG.md", "README.md"}


class ScaffoldError(ValueError):
    """Raised when a requested scaffold would be invalid or unsafe."""


def validate_slug(slug: str) -> str:
    if not SLUG_PATTERN.fullmatch(slug) or len(slug) > 80:
        raise ScaffoldError(
            "slug must be 1-80 lowercase letters/digits separated by single hyphens"
        )
    return slug


def validate_title(title: str) -> str:
    normalized = " ".join(title.split())
    if (
        not normalized
        or len(normalized) > 160
        or any(ord(char) < 32 for char in title)
    ):
        raise ScaffoldError("title must be 1-160 printable characters on one line")
    return normalized


def yaml_double_quoted(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def replace_once(path: Path, old: str, new: str) -> None:
    source = path.read_text(encoding="utf-8")
    if source.count(old) != 1:
        raise ScaffoldError(f"template marker {old!r} is not unique in {path.name}")
    path.write_text(source.replace(old, new, 1), encoding="utf-8")


def create_project(
    slug: str,
    title: str,
    projects_root: Path = DEFAULT_PROJECTS_ROOT,
    template_root: Path | None = None,
) -> Path:
    """Create a personalized scaffold atomically and return its path."""
    slug = validate_slug(slug)
    title = validate_title(title)
    projects_root = Path(projects_root).resolve()
    template_root = Path(
        template_root or DEFAULT_PROJECTS_ROOT / "_template"
    ).resolve()
    destination = projects_root / slug

    if destination.exists():
        raise ScaffoldError(f"refusing to overwrite existing path: {destination}")
    missing = sorted(
        name for name in REQUIRED_TEMPLATE_FILES if not (template_root / name).is_file()
    )
    if missing:
        raise ScaffoldError(f"template is missing required files: {', '.join(missing)}")

    projects_root.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix=".create-project-", dir=projects_root))
    try:
        shutil.copytree(template_root, staging, dirs_exist_ok=True)
        replace_once(staging / "PROJECT.md", "# Title of Project", f"# {title}")
        replace_once(
            staging / "STATE.md",
            'title: "Project title"',
            f"title: {yaml_double_quoted(title)}",
        )
        replace_once(
            staging / "STATE.md",
            "# Project title — Current state",
            f"# {title} — Current state",
        )
        replace_once(
            staging / "DIALOG.md",
            "# Project title — Dialog",
            f"# {title} — Dialog",
        )
        staging.rename(destination)
    except Exception:
        if staging.exists():
            shutil.rmtree(staging)
        raise

    return destination


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a private Project scaffold; no website page is published."
    )
    parser.add_argument("slug", help="permanent lowercase hyphenated identifier")
    parser.add_argument("title", help="public Project title")
    parser.add_argument(
        "--projects-root",
        type=Path,
        default=DEFAULT_PROJECTS_ROOT,
        help=argparse.SUPPRESS,
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        destination = create_project(args.slug, args.title, args.projects_root)
    except ScaffoldError as error:
        raise SystemExit(f"create_project: {error}") from error

    relative = (
        destination.relative_to(REPOSITORY_ROOT)
        if destination.is_relative_to(REPOSITORY_ROOT)
        else destination
    )
    print(f"Created {relative}")
    print(
        f"Next: Dr. Jones completes {relative / 'PROJECT.md'}; "
        "do not publish an empty Project."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
