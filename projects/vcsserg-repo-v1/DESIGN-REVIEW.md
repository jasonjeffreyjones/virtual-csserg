# Website alternatives for PI review

Prepared by Bee Boring Vanilla on September 9, 2026.

## Review artifact

Open `website/projects/vcsserg-repo-v1/designs/index.html`, or follow the design
comparison link in the v1 Executive Summary after automated publication.
The previews are ordinary static pages, publicly publishable but explicitly
unselected. Existing homepage, Scholar pages, and shared production CSS remain
unchanged. Existing destination pages retain their current designs.

| Concept | Visual language | Information architecture | Layout | Principal tradeoff |
|---|---|---|---|---|
| A: Research directory | Spacious, bright, sans-serif, rounded cards | Mission → projects → Scholars | Wide introduction, three project cards, Scholar band | Findings require opening a project |
| B: Evidence observatory | Compact, neutral background, dark status panels, numeric typography | Snapshot → available evidence → pending evidence → Scholars | Left section rail, status panels, evidence table | Snapshot content requires maintenance and can feel dense |
| C: Research journal | Warm paper, serif headlines, editorial rules | Lead finding → notebook entries, with lab context and project links alongside | Asymmetric story/sidebar composition | Editorial prominence may hide less prominent projects |

At narrow widths, cards, rail/content, and editorial columns stack. Navigation
remains visible without JavaScript. Semantic headings, skip links, focus outlines,
textual status descriptions, and table headers are included. The comparison
page's small layout illustrations are decorative CSS, not screenshots.

## Content provenance and boundaries

All three concepts draw on the same three projects. Statements were checked
against `projects/predict-the-self/STATE.md`,
`projects/nfl-team-fandom-identities/STATE.md`, and the v1 verifier/current state.
No new empirical findings were produced. NFL report links are intentionally
absent because no public index exists. Private test performance is not claimed.
The journal's lead story is an illustrative editorial choice, not a PI decision.

The 4/6 measure is explicitly labeled as automated infrastructure check groups;
it is not a completion percentage or a measure of research quality. These pages
are dated static snapshots, not live dashboards.

## Implementation and validation

- Four preview HTML files share a CSS file scoped to their own directory.
- Bootstrap 5.3.8 CSS uses the CDN URL and integrity value in the official
  documentation. This meets the requested Bootstrap approach for the previews
  without adding a build/runtime tool or JavaScript. CDN access is required for
  Bootstrap styling; the local CSS supplies core layouts and typography too.
- `verify_v1.py`: all 12 HTML pages and 3 CSS files pass structural/local-link
  checks. Four of six groups pass overall, with unchanged memory/catalog gaps.
- No browser executable was found for Chromium, Chrome, or Firefox, and no
  browser tool is available. Rendered QA and assistive-technology checks remain
  outstanding. No browser or other infrastructure was installed.
- The previews are homepage prototypes, not full redesigns of every report and
  profile. PI review should select a direction before extending it site-wide.

## Decision requested in the next PI review

Select A, B, C, a combination of named elements, or another direction. No
selection is presumed. Inspect each at desktop and phone widths, follow a project
and Scholar link, and compare how readily evidence limitations can be found.
After selection, extend the chosen system to the remaining page types and perform
rendered QA before replacing the current design.

## Reference

Bootstrap team. (n.d.). *Get started with Bootstrap*. Bootstrap. Retrieved
September 9, 2026, from https://getbootstrap.com/docs/5.3/getting-started/introduction/
