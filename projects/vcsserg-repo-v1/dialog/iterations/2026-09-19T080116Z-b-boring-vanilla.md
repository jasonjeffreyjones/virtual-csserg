---
started: 2026-09-19T08:01:16Z
finished: 2026-09-19T08:21:29Z
scholar: "Bee Boring Vanilla"
scholar_slug: b-boring-vanilla
project: vcsserg-repo-v1
---

# Static-first report bypass and manual review protocol

## Scope

Advance the sole remaining Version 1 manual gate without claiming unavailable
graphical-browser or screen-reader evidence. Examine the selected public pages
in the host's text browser, repair any deterministic accessibility weakness it
reveals, make the rendered review reproducible, and synchronize the three v1
report forms and Project records.

## Work completed

- Found that all four generated Quarto pages placed “Skip to content” after
  repeated book navigation in raw HTML and depended on inline JavaScript to move
  it first at runtime. Replaced that exception with
  `python/promote_report_skip_links.py`, a standard-library, preflight-first
  post-render normalizer used by all three published Quarto builds.
- Removed runtime relocation from each source-owned skip-link fragment. The
  generated public HTML now contains the bypass link as its first anchor and
  targets the report `main` before any navigation. The Version 1 verifier now
  rejects runtime-only relocation.
- Added three normalizer tests covering promotion plus idempotence, duplicate
  refusal before any write, and a missing main target. Updated the existing
  negative fixture to reject a late link even when a script would relocate it.
- Added `ACCESSIBILITY-REVIEW.md`, grounded in WCAG 2.2 and W3C evaluation
  guidance. It defines 11 selected production pages, desktop and 320-CSS-pixel
  conditions, keyboard/focus, reflow and screen-reader checks, an environment
  record, and an explicit passing rule.
- Updated all three report sources/forms, build guides, audit, recommendations,
  state, homepage, public Project catalog, and release ledger. The ledger
  preserves the clean outgoing report set under full commit
  `188e26853d9f9fa94ea9285d906f1a2ee72d2640`.

## Evidence and validation

- Before editing, the credential-free production probe found all 128 expected
  website files byte-identical. The archived commit contains the outgoing
  Executive Summary, Full Report, and short PDF.
- `w3m` 0.5.3 returned zero for all 11 selected production pages at 40 and 120
  columns. After the repair, every linearized view began with “Skip to content,”
  including all four Quarto pages.
- All 29 routine v1 unit tests pass, including the three new normalizer tests.
  All seven Version 1 promise groups pass across 26 HTML pages and six
  first-party stylesheets.
- The v1 publication verifier passes exactly one Executive Summary figure,
  reciprocal links, the required phrase, and a linked two-page, two-column PDF.
  All three Quarto projects rendered successfully and their post-render command
  promoted four bypass links.
- Ghostscript rasterization and page-by-page inspection found the rebuilt
  two-page short report legible, with no clipping or overlap.
- Roster and Project-registry validation, both other Projects' test/publication
  suites, Python compilation, repository whitespace, and final repository
  validation pass.

## Limitations and decisions

The text browser supplies useful no-style linearization evidence but cannot
show graphical focus, responsive overlap, browser scripting behavior, or
screen-reader output. No installed Chromium, Chrome, or Firefox executable or
supported screen-reader/browser pairing is available, so the manual gate
remains open. The new protocol is a bounded Project acceptance procedure, not a
WCAG conformance claim.

The NFL Quarto build repeated its existing warning about an output directory
outside the main Project directory but completed and passed validation. No
credential, `.env`, manual deployment, package or replacement runtime
installation, PI-owned runner edit, charter edit, earlier iteration edit, PI
blockquote change, or parallel agent was used.

## Sources

World Wide Web Consortium. (2024, December 12). *Web Content Accessibility
Guidelines (WCAG) 2.2*. https://www.w3.org/TR/WCAG22/

World Wide Web Consortium Web Accessibility Initiative. (n.d.). *Easy checks:
A first review of web accessibility*. Retrieved September 19, 2026, from
https://www.w3.org/WAI/test-evaluate/preliminary/

## Questions and next steps

No blocking PI question. Execute `ACCESSIBILITY-REVIEW.md` on a
browser/screen-reader-equipped host, record the environment and all page
results, fix and retest any failure, and only then assess the charter and PI
authority before changing the Project lifecycle state.

Elapsed time: 20 minutes 13 seconds (1,213 seconds).
