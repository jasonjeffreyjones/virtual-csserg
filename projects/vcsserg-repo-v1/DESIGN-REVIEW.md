# Website design decision and implementation

Prepared by Bee Boring Vanilla on September 9, 2026.

## Review artifact

Open `website/projects/vcsserg-repo-v1/designs/index.html`, or follow the design
comparison link in the v1 Executive Summary after automated publication.
Dr. Jones selected Concept C in DIALOG.md and requested a GitHub repository
link in the footer. On September 11, the homepage adopted C's research lead,
notebook entries, and contextual sidebar. Shared styles extend its warm paper,
serif typography, and editorial rules to Scholar profiles, project summaries,
and the existing report. All current and review-artifact HTML footers link to
the repository.
The three prototypes remain archived comparisons, with their selection labels
updated. The homepage's lead is a Scholar editorial choice grounded in the
current Predict the Self records; the PI selected the design, not a finding.

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
The archived journal lead reflects the same documented development findings now highlighted on the homepage.

The 4/6 measure is explicitly labeled as automated infrastructure check groups;
it is not a completion percentage or a measure of research quality. These pages
are dated static snapshots, not live dashboards.

## Implementation and validation

- Four archived homepage-review files use their scoped preview CSS. Ten
  production pages use the shared journal styling, eight new PI-review pages use
  their own scoped styles, and the generated NFL Full Report retains its Quarto
  styles. All use Bootstrap.
- Bootstrap 5.3.8 CSS uses the CDN URL and integrity value in the official
  documentation. This meets the requested Bootstrap approach for all pages
  without adding a build/runtime tool or JavaScript. CDN access is required for
  Bootstrap styling; the local CSS supplies core layouts and typography too.
- The current `verify_v1.py` audit supersedes these September 9 counts; see
  `V1-AUDIT.md` for the current seven-group result.
- No browser executable was found for Chromium, Chrome, or Firefox, and no
  browser tool is available. Rendered QA and assistive-technology checks remain
  outstanding. No browser or other infrastructure was installed.
- The verifier now requires the GitHub URL within every HTML footer. A temporary
  copied-site fixture confirms removing one footer link causes a failure.
- No browser is installed on the September 11 host; rendered desktop/mobile QA
  remains outstanding. Bootstrap was reused from the reviewed preview asset;
  no new package or system tool was installed.

## Remaining review

Inspect the homepage, a Scholar profile, a project summary, and the Full Report
at desktop and phone widths, including keyboard navigation and table scrolling.
Selection is resolved; rendered QA and future editorial choices remain open.

The September 11 PI review requests are handled in two separate comparison
sets: `website/projects/vcsserg-repo-v1/designs/project-summaries/` and
`website/projects/vcsserg-repo-v1/designs/scholar-directories/`. Their design
recommendations and the requested workflow opinions are recorded in
`V1-RECOMMENDATIONS.md`. These later alternatives do not reopen the selected
homepage system.

## Reference

Bootstrap team. (n.d.). *Get started with Bootstrap*. Bootstrap. Retrieved
September 9, 2026, from https://getbootstrap.com/docs/5.3/getting-started/introduction/
