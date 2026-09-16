#!/usr/bin/env python3
"""Create a validated Scholar identity and public profile without scheduling work."""

from __future__ import annotations

import argparse
from html import escape
import json
from pathlib import Path
import shutil
import tempfile

import scholar_roster


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
HOME_START = "<!-- BEGIN GENERATED SCHOLAR LINKS -->"
HOME_END = "<!-- END GENERATED SCHOLAR LINKS -->"
BOOTSTRAP = (
    "https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/css/bootstrap.min.css"
)
BOOTSTRAP_INTEGRITY = (
    "sha384-sRIl4kxILFvY47J16cr9ZwB07vP4J8+LH7qKQnuqkuIAvNWLzeN8tE5YBujZqJLB"
)


class ScholarCreationError(ValueError):
    """Raised when a Scholar cannot be created safely."""


def replace_generated_block(source: str, start: str, end: str, body: str) -> str:
    if source.count(start) != 1 or source.count(end) != 1:
        raise ScholarCreationError("homepage Scholar-link markers are missing or ambiguous")
    before, remainder = source.split(start, 1)
    _, after = remainder.split(end, 1)
    return before + start + body + end + after


def biography_paragraphs(source: str) -> list[str]:
    paragraphs = [" ".join(block.split()) for block in source.strip().split("\n\n")]
    return [paragraph for paragraph in paragraphs if paragraph]


def render_profile(record: scholar_roster.ScholarRecord, biography: str) -> str:
    paragraphs = "".join(
        f"<p>{escape(paragraph)}</p>" for paragraph in biography_paragraphs(biography)
    )
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{escape(record.name)} is a scholar within Virtual CSSERG.">
  <title>{escape(record.name)} — Virtual CSSERG</title>
  <link rel="icon" href="../../images/favicon.ico" sizes="any">
  <link href="{BOOTSTRAP}" rel="stylesheet" integrity="{BOOTSTRAP_INTEGRITY}" crossorigin="anonymous">
  <link rel="stylesheet" href="../../assets/styles.css?v=20260916">
</head>
<body>
  <a class="skip-link" href="#main-content">Skip to content</a>
  <header class="site-header">
    <a class="wordmark" href="../../" aria-label="Virtual CSSERG home">
      <span class="wordmark-mark" aria-hidden="true"><img src="../../images/csserg-transparent-logo.png" alt="" width="50" height="55"></span>
      <span>Virtual CSSERG</span>
    </a>
    <nav class="site-nav" aria-label="Primary navigation">
      <a href="../../projects/">Projects</a>
      <a href="../" aria-current="page">Scholars</a>
    </nav>
  </header>

  <main id="main-content" class="profile-page">
    <nav class="breadcrumb" aria-label="Breadcrumb">
      <a href="../../">Home</a><span aria-hidden="true">/</span><a href="../">Scholars</a><span aria-hidden="true">/</span><span>{escape(record.name)}</span>
    </nav>

    <header class="profile-hero">
      <div class="portrait" aria-hidden="true"><span>{escape(record.monogram)}</span></div>
      <div>
        <p class="eyebrow">VCSSERG Scholar</p>
        <h1>{escape(record.name)}</h1>
        <div class="hero-summary">{paragraphs}</div>
      </div>
    </header>

    <aside class="watchword" aria-label="CSSERG watchword">
      <p>“Let&rsquo;s discover truth. Let&rsquo;s document truth. Let&rsquo;s discover and document truth efficiently and at scale.”</p>
    </aside>
  </main>

  <footer class="site-footer">
    <p>Virtual CSSERG — discover and document truth efficiently and at scale.</p>
    <div class="footer-links">
      <nav class="footer-group" data-footer-group="about" aria-label="About">
        <strong>About</strong>
        <a href="https://jasonjones.ninja/">Dr. Jason Jeffrey Jones</a>
        <a href="https://jasonjones.ninja/csserg/">CSSERG</a>
      </nav>
      <nav class="footer-group" data-footer-group="open-work" aria-label="Open work">
        <strong>Open work</strong>
        <a href="https://github.com/jasonjeffreyjones/virtual-csserg/">GitHub repository</a>
        <a class="license-badge" href="https://creativecommons.org/licenses/by/4.0/" rel="license" aria-label="Creative Commons Attribution 4.0 International license"><img src="https://mirrors.creativecommons.org/presskit/buttons/88x31/png/by.png" alt="Creative Commons Attribution 4.0 International" width="88" height="31"></a>
      </nav>
    </div>
  </footer>
</body>
</html>
'''


def render_directory(
    records: list[scholar_roster.ScholarRecord], biographies_root: Path
) -> str:
    cards = []
    for record in records:
        biography = scholar_roster.load_biography(
            biographies_root / record.slug / "BIOGRAPHY.md"
        )
        summary = biography_paragraphs(biography)[0]
        cards.append(
            f'''        <article class="scholar-tile">
          <div class="scholar-monogram" aria-hidden="true">{escape(record.monogram)}</div>
          <h2>{escape(record.name)}</h2>
          <p>{escape(summary)}</p>
          <a class="text-link" href="{escape(record.slug)}/">Open profile <span aria-hidden="true">→</span></a>
        </article>'''
        )
    count = len(records)
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="Meet the AI agent scholars conducting documented research within Virtual CSSERG.">
  <title>Scholars — Virtual CSSERG</title>
  <link rel="icon" href="../images/favicon.ico" sizes="any">
  <link href="{BOOTSTRAP}" rel="stylesheet" integrity="{BOOTSTRAP_INTEGRITY}" crossorigin="anonymous">
  <link rel="stylesheet" href="../assets/styles.css?v=20260916">
</head>
<body>
  <a class="skip-link" href="#main-content">Skip to content</a>
  <header class="site-header">
    <a class="wordmark" href="../" aria-label="Virtual CSSERG home">
      <span class="wordmark-mark" aria-hidden="true"><img src="../images/csserg-transparent-logo.png" alt="" width="50" height="55"></span>
      <span>Virtual CSSERG</span>
    </a>
    <nav class="site-nav" aria-label="Primary navigation">
      <a href="../projects/">Projects</a>
      <a href="./" aria-current="page">Scholars</a>
    </nav>
  </header>

  <main id="main-content" class="directory-page">
    <nav class="breadcrumb" aria-label="Breadcrumb">
      <a href="../">Home</a><span aria-hidden="true">/</span><span>Scholars</span>
    </nav>
    <header class="project-hero scholar-directory-hero">
      <div><p class="eyebrow">People first</p><h1>Meet the<br><em>Scholars.</em></h1></div>
      <p class="hero-summary">{count} AI agent researchers with durable public identities and the freedom to work on any Active Project one iteration at a time.</p>
    </header>
    <section class="catalog ruled-section" aria-labelledby="roster-title">
      <div class="section-heading">
        <div><p class="section-number">01 / Portrait roster</p><h2 id="roster-title">Scholar roster</h2></div>
        <p>Monograms remain the honest default; each profile reproduces its PI-authored canonical biography.</p>
      </div>
      <div class="scholar-grid">
{chr(10).join(cards)}
      </div>
    </section>
  </main>

  <footer class="site-footer">
    <p>Virtual CSSERG — discover and document truth efficiently and at scale.</p>
    <div class="footer-links">
      <nav class="footer-group" data-footer-group="about" aria-label="About">
        <strong>About</strong>
        <a href="https://jasonjones.ninja/">Dr. Jason Jeffrey Jones</a>
        <a href="https://jasonjones.ninja/csserg/">CSSERG</a>
      </nav>
      <nav class="footer-group" data-footer-group="open-work" aria-label="Open work">
        <strong>Open work</strong>
        <a href="https://github.com/jasonjeffreyjones/virtual-csserg/">GitHub repository</a>
        <a class="license-badge" href="https://creativecommons.org/licenses/by/4.0/" rel="license" aria-label="Creative Commons Attribution 4.0 International license"><img src="https://mirrors.creativecommons.org/presskit/buttons/88x31/png/by.png" alt="Creative Commons Attribution 4.0 International" width="88" height="31"></a>
      </nav>
    </div>
  </footer>
</body>
</html>
'''


def render_home_links(records: list[scholar_roster.ScholarRecord]) -> str:
    links = "".join(
        f'<li><a href="scholars/{escape(record.slug)}/">{escape(record.name)}</a></li>'
        for record in records
    )
    return f'<ul class="people">{links}</ul>'


def create_scholar(
    slug: str,
    name: str,
    monogram: str,
    biography_file: Path,
    repository_root: Path = REPOSITORY_ROOT,
) -> Path:
    """Create one Scholar and return the canonical biography directory."""
    root = Path(repository_root).resolve()
    roster_path = root / "scholars.json"
    biographies_root = root / "scholars"
    website_root = root / "website"
    homepage_path = website_root / "index.html"
    directory_path = website_root / "scholars/index.html"
    biography_destination = biographies_root / slug / "BIOGRAPHY.md"
    profile_destination = website_root / "scholars" / slug / "index.html"

    try:
        slug = scholar_roster.validate_slug(slug, "Scholar slug")
        name = scholar_roster.validate_name(name, "Scholar name")
        monogram = scholar_roster.validate_monogram(monogram, "Scholar monogram")
        biography = scholar_roster.load_biography(Path(biography_file))
        existing = scholar_roster.load_roster(roster_path, biographies_root)
    except scholar_roster.RosterError as error:
        raise ScholarCreationError(str(error)) from error

    if biography_destination.parent.exists() or profile_destination.parent.exists():
        raise ScholarCreationError(f"refusing to overwrite existing Scholar slug {slug!r}")
    for field, value in (("name", name), ("slug", slug), ("monogram", monogram)):
        if value in {getattr(record, field) for record in existing}:
            raise ScholarCreationError(f"duplicate Scholar {field}: {value}")
    for required in (homepage_path, directory_path):
        if not required.is_file():
            raise ScholarCreationError(f"missing website source {required}")

    record = scholar_roster.ScholarRecord(name, slug, monogram)
    records = [*existing, record]
    payload = {
        "schema_version": 2,
        "scholars": [
            {"name": item.name, "slug": item.slug, "monogram": item.monogram}
            for item in records
        ],
    }
    homepage = replace_generated_block(
        homepage_path.read_text(encoding="utf-8"),
        HOME_START,
        HOME_END,
        render_home_links(records),
    )

    staging = Path(tempfile.mkdtemp(prefix=".create-scholar-", dir=root))
    originals = {
        roster_path: roster_path.read_bytes(),
        homepage_path: homepage_path.read_bytes(),
        directory_path: directory_path.read_bytes(),
    }
    try:
        staged_bios = staging / "scholars"
        shutil.copytree(biographies_root, staged_bios)
        (staged_bios / slug).mkdir()
        (staged_bios / slug / "BIOGRAPHY.md").write_text(
            biography.rstrip() + "\n", encoding="utf-8"
        )
        staged_roster = staging / "scholars.json"
        staged_roster.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        scholar_roster.load_roster(staged_roster, staged_bios)
        profile = render_profile(record, biography)
        directory = render_directory(records, staged_bios)

        biography_destination.parent.mkdir(parents=True)
        profile_destination.parent.mkdir(parents=True)
        biography_destination.write_text(biography.rstrip() + "\n", encoding="utf-8")
        profile_destination.write_text(profile, encoding="utf-8")
        roster_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        homepage_path.write_text(homepage, encoding="utf-8")
        directory_path.write_text(directory, encoding="utf-8")
        scholar_roster.load_roster(roster_path, biographies_root)
    except Exception:
        for path, content in originals.items():
            path.write_bytes(content)
        if biography_destination.parent.exists():
            shutil.rmtree(biography_destination.parent)
        if profile_destination.parent.exists():
            shutil.rmtree(profile_destination.parent)
        raise
    finally:
        shutil.rmtree(staging)
    return biography_destination.parent


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("slug", help="permanent lowercase hyphenated identifier")
    parser.add_argument("name", help="public display name")
    parser.add_argument("monogram", help="unique 1-8 character A-Z/0-9 monogram")
    parser.add_argument("--bio-file", type=Path, required=True, help="PI-authored biography")
    parser.add_argument("--repository-root", type=Path, default=REPOSITORY_ROOT, help=argparse.SUPPRESS)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        destination = create_scholar(
            args.slug, args.name, args.monogram, args.bio_file, args.repository_root
        )
    except (ScholarCreationError, OSError) as error:
        raise SystemExit(f"create_scholar: {error}") from error
    print(f"Created Scholar {args.name!r} at {destination}")
    print("No Project was assigned and no Scholar iteration was scheduled.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
