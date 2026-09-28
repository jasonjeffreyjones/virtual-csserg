#!/usr/bin/env python3
"""Render every dated outreach source as a static Project blog entry."""

from html import escape
from pathlib import Path
import re
import shutil
import subprocess


PROJECT = Path(__file__).resolve().parents[1]
ROOT = PROJECT.parents[1]
PUBLIC = ROOT / "website/projects/ipseity-daily-pulse"
BLOG = PUBLIC / "blog"

# Historical figures are pinned to the commit that created each dated source.
# The newest entry uses the current output produced in the same iteration.
ENTRIES = [
    {
        "date": "2026-09-26",
        "slug": "2026-09-26-a-leaderboard-is-not-a-discovery",
        "description": "Why none of 704 descriptive trend tests becomes a discovery after either multiplicity screen.",
        "image": "annual-prevalence-growth-histogram.svg",
        "commit": None,
    },
    {
        "date": "2026-09-25",
        "slug": "2026-09-25-adjustment-changes-the-lurch",
        "description": "Adjustment preserves average path concentration but often changes when the largest move appears.",
        "image": "leader-period-adjustment-sensitivity.svg",
        "commit": "d67843135142ac786538ffd718fc733f7ede51ef",
    },
    {
        "date": "2026-09-24",
        "slug": "2026-09-24-linear-trend-can-hide-a-lurch",
        "description": "A linear summary can conceal an uneven four-period trajectory.",
        "image": "leader-period-trajectory.svg",
        "commit": "798752777e9955640468bad1a32c82e2983a9a11",
    },
    {
        "date": "2026-09-23",
        "slug": "2026-09-23-two-period-contrast-after-adjustment",
        "description": "A before-and-after contrast can change when recorded sample composition changes.",
        "image": "leader-early-late-sensitivity.svg",
        "commit": "9d70a922dde140f958a757d75eaf1ce179f1ad0d",
    },
    {
        "date": "2026-09-22",
        "slug": "2026-09-22-seven-checks-one-day-lag",
        "description": "Seven healthy snapshots with one-day data lag are useful monitoring evidence, not an uptime estimate.",
        "image": "monitoring-history.svg",
        "commit": "60bcf794fc368495aa7fea7acacfe89c47c5b674",
    },
    {
        "date": "2026-09-21",
        "slug": "2026-09-21-trend-without-straight-line-assumption",
        "description": "A two-period contrast checks trend direction without requiring a straight-line path.",
        "image": "leader-early-late-sensitivity.svg",
        "commit": "bd7fdad6ef229bbeaf073f1ece8e5aecb175281d",
    },
    {
        "date": "2026-09-20",
        "slug": "2026-09-20-one-trend-three-comparisons",
        "description": "All-response, repeat-sample, and within-person slopes answer different questions.",
        "image": "leader-within-respondent-sensitivity.svg",
        "commit": "5ea9cce438c4dbef96e2855144f8fb6b2161fefd",
    },
    {
        "date": "2026-09-19",
        "slug": "2026-09-19-pooled-trends-are-not-within-person-change",
        "description": "A changing response sample is not the same estimand as change within returning people.",
        "image": "leader-within-respondent-sensitivity.svg",
        "commit": "42328ddcbdaa8b27087c046ab765cf82aa2cbf4b",
    },
    {
        "date": "2026-09-18",
        "slug": "2026-09-18-apparent-trends-soften-after-adjustment",
        "description": "Observed composition and calendar adjustment can soften extreme sample-trend estimates.",
        "image": "leader-adjustment-sensitivity.svg",
        "commit": "188e26853d9f9fa94ea9285d906f1a2ee72d2640",
    },
    {
        "date": "2026-09-16",
        "slug": "2026-09-16-nearly-700k-observations",
        "description": "Nearly 700,000 answers show data scale, not 700,000 people or a population trend.",
        "image": "observation-growth.svg",
        "commit": "026c1d4511fbd99789c8252c552e72f90a799b5a",
    },
]


def section(source: str, name: str, alternatives=()) -> str:
    names = (name,) + tuple(alternatives)
    for candidate in names:
        match = re.search(
            rf"^## {re.escape(candidate)}\s*$\n(.*?)(?=^## |\Z)",
            source,
            flags=re.MULTILINE | re.DOTALL,
        )
        if match:
            return match.group(1).strip()
    raise ValueError(f"missing section {name!r}")


def fragment(markdown: str) -> str:
    normalized = markdown.replace("../CURRENT-FINDINGS.md", "../report/")
    normalized = normalized.replace(
        "../data/monitoring-history.csv", "../artifacts/monitoring-history.csv"
    )
    normalized = re.sub(
        r"\.\./outputs/([^/)]+\.(?:csv|json))", r"../artifacts/\1", normalized
    )
    result = subprocess.run(
        ["pandoc", "--from=gfm", "--to=html"],
        input=normalized,
        text=True,
        capture_output=True,
        check=True,
    )
    return result.stdout.strip()


def title_from(source: str) -> str:
    match = re.match(r"^# (.+)$", source, flags=re.MULTILINE)
    if not match:
        raise ValueError("outreach source has no title")
    return match.group(1).strip()


def alt_from(source: str) -> str:
    visual = section(source, "Visual")
    match = re.search(r"Suggested alt text:\s*[“\"](.*)[”\"]\s*$", visual, re.DOTALL)
    if not match:
        raise ValueError("outreach source has no suggested alt text")
    return " ".join(match.group(1).split())


def page(entry, source: str) -> str:
    title = title_from(source)
    body = fragment(section(source, "Post", alternatives=("Suggested post",)))
    evidence = fragment(section(source, "Evidence note"))
    alt = alt_from(source)
    historical_note = ""
    if entry["commit"]:
        historical_note = (
            '<p class="muted"><strong>Snapshot note:</strong> This dated entry and figure '
            "are preserved from the stated check. Links to the cumulative report and aggregate "
            "tables may show newer data.</p>"
        )
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{escape(entry['description'], quote=True)}">
  <title>{escape(title)} — Ipseity Daily Pulse</title>
  <link rel="icon" href="../../../images/favicon.ico" sizes="any">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-sRIl4kxILFvY47J16cr9ZwB07vP4J8+LH7qKQnuqkuIAvNWLzeN8tE5YBujZqJLB" crossorigin="anonymous">
  <link rel="stylesheet" href="../../../assets/styles.css?v=20260926">
</head>
<body>
  <a class="skip-link" href="#main-content">Skip to content</a>
  <header class="site-header">
    <a class="wordmark" href="../../../" aria-label="Virtual CSSERG home"><span class="wordmark-mark" aria-hidden="true"><img src="../../../images/csserg-transparent-logo.png" alt="" width="50" height="55"></span><span>Virtual CSSERG</span></a>
    <nav class="site-nav" aria-label="Primary navigation"><a href="../../">Projects</a><a href="../../../scholars/">Scholars</a></nav>
  </header>
  <main id="main-content" class="profile-page">
    <nav class="breadcrumb" aria-label="Breadcrumb"><a href="../../../">Home</a><span aria-hidden="true">/</span><a href="../">Ipseity Daily Pulse</a><span aria-hidden="true">/</span><a href="./">Blog</a><span aria-hidden="true">/</span><span>{escape(title)}</span></nav>
    <article>
      <header class="profile-hero"><div><p class="eyebrow">Ipseity Daily Pulse · {entry['date']}</p><h1>{escape(title)}</h1><p class="hero-summary">{escape(entry['description'])}</p><p>By Ceetown · 3 minute read</p></div></header>
      {body}
      <figure><img src="images/{entry['slug']}.svg" alt="{escape(alt, quote=True)}" style="width:100%;height:auto"><figcaption>Dated visualization for the observation snapshot described in this entry.</figcaption></figure>
      <h2>Evidence note</h2>
      {evidence}
      {historical_note}
      <p><a href="../report/">Read the cumulative Full Report</a> · <a href="./">Browse every Pulse entry</a></p>
    </article>
  </main>
  <footer class="site-footer">
    <p>Virtual CSSERG — discover and document truth efficiently and at scale.</p>
    <div class="footer-links"><nav class="footer-group" data-footer-group="about" aria-label="About"><strong>About</strong><a href="https://jasonjones.ninja/">Dr. Jason Jeffrey Jones</a><a href="https://jasonjones.ninja/csserg/">CSSERG</a></nav><nav class="footer-group" data-footer-group="open-work" aria-label="Open work"><strong>Open work</strong><a href="https://github.com/jasonjeffreyjones/virtual-csserg/">GitHub repository</a><a class="license-badge" href="https://creativecommons.org/licenses/by/4.0/" rel="license" aria-label="Creative Commons Attribution 4.0 International license"><img src="https://mirrors.creativecommons.org/presskit/buttons/88x31/png/by.png" alt="Creative Commons Attribution 4.0 International" width="88" height="31"></a></nav></div>
  </footer>
</body>
</html>
'''


def index_page(rendered):
    cards = []
    for entry, title in rendered:
        display_date = entry["date"]
        cards.append(
            f'''<article class="project-listing"><p class="card-meta"><time datetime="{display_date}">{display_date}</time> · 3 minute read</p><h3><a href="{entry['slug']}.html">{escape(title)}</a></h3><p>{escape(entry['description'])}</p></article>'''
        )
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="Accessible research updates from the Ipseity Daily Pulse project.">
  <title>Ipseity Daily Pulse Blog — Virtual CSSERG</title>
  <link rel="icon" href="../../../images/favicon.ico" sizes="any">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-sRIl4kxILFvY47J16cr9ZwB07vP4J8+LH7qKQnuqkuIAvNWLzeN8tE5YBujZqJLB" crossorigin="anonymous">
  <link rel="stylesheet" href="../../../assets/styles.css?v=20260926">
</head>
<body>
  <a class="skip-link" href="#main-content">Skip to content</a>
  <header class="site-header"><a class="wordmark" href="../../../" aria-label="Virtual CSSERG home"><span class="wordmark-mark" aria-hidden="true"><img src="../../../images/csserg-transparent-logo.png" alt="" width="50" height="55"></span><span>Virtual CSSERG</span></a><nav class="site-nav" aria-label="Primary navigation"><a href="../../">Projects</a><a href="../../../scholars/">Scholars</a></nav></header>
  <main id="main-content" class="directory-page">
    <nav class="breadcrumb" aria-label="Breadcrumb"><a href="../../../">Home</a><span aria-hidden="true">/</span><a href="../">Ipseity Daily Pulse</a><span aria-hidden="true">/</span><span>Blog</span></nav>
    <header class="project-hero"><div><p class="eyebrow">Project blog</p><h1>Short reads from<br><em>Ipseity Daily Pulse</em></h1></div><p class="hero-summary">One evidence-linked idea at a time, written for curious readers and bounded by what each dated snapshot can support.</p></header>
    <section class="project-directory ruled-section" aria-labelledby="entries-title"><div class="section-heading"><div><p class="section-number">01 / Entries</p><h2 id="entries-title">Newest first</h2></div><p>Public entries supplement the cumulative reports; they do not replace them.</p></div><div class="project-list">{''.join(cards)}</div></section>
  </main>
  <footer class="site-footer"><p>Virtual CSSERG — discover and document truth efficiently and at scale.</p><div class="footer-links"><nav class="footer-group" data-footer-group="about" aria-label="About"><strong>About</strong><a href="https://jasonjones.ninja/">Dr. Jason Jeffrey Jones</a><a href="https://jasonjones.ninja/csserg/">CSSERG</a></nav><nav class="footer-group" data-footer-group="open-work" aria-label="Open work"><strong>Open work</strong><a href="https://github.com/jasonjeffreyjones/virtual-csserg/">GitHub repository</a><a class="license-badge" href="https://creativecommons.org/licenses/by/4.0/" rel="license" aria-label="Creative Commons Attribution 4.0 International license"><img src="https://mirrors.creativecommons.org/presskit/buttons/88x31/png/by.png" alt="Creative Commons Attribution 4.0 International" width="88" height="31"></a></nav></div></footer>
</body>
</html>
'''


def copy_figure(entry):
    destination = BLOG / "images" / f"{entry['slug']}.svg"
    if entry["commit"] is None:
        shutil.copyfile(PROJECT / "outputs" / entry["image"], destination)
        return
    repository_path = f"projects/ipseity-daily-pulse/outputs/{entry['image']}"
    result = subprocess.run(
        ["git", "show", f"{entry['commit']}:{repository_path}"],
        cwd=ROOT,
        capture_output=True,
        check=True,
    )
    destination.write_bytes(result.stdout)


def main() -> int:
    (BLOG / "images").mkdir(parents=True, exist_ok=True)
    rendered = []
    for entry in ENTRIES:
        source_path = PROJECT / "outreach" / f"{entry['slug']}.md"
        source = source_path.read_text(encoding="utf-8")
        title = title_from(source)
        copy_figure(entry)
        (BLOG / f"{entry['slug']}.html").write_text(page(entry, source), encoding="utf-8")
        rendered.append((entry, title))
    (BLOG / "index.html").write_text(index_page(rendered), encoding="utf-8")
    print(f"Rendered {len(rendered)} blog entries with pinned dated figures.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
