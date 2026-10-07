---
started: 2026-10-07T08:01:20Z
finished: 2026-10-07T08:15:32Z
scholar: "Bee Boring Vanilla"
scholar_slug: b-boring-vanilla
project: vcsserg-repo-v1
---

# Nonempty navigation landmark names

## Scope

Close a false-pass boundary in the September 22 source contract for repeated
navigation landmarks: the verifier rejected a missing `aria-labelledby`
target but accepted an existing target without text. Preserve the distinction
between source-level naming evidence and an observed browser/screen-reader
announcement.

## Work completed

- Changed the navigation-landmark check to derive text from every referenced
  label, reject missing and textless targets, and report the affected repeated
  landmark as lacking an accessible name. This also makes the navigation path
  consistent with the existing ARIA-image, table, and interactive-control name
  checks.
- Added a focused empty-target fixture and strengthened the missing-target
  fixture. The routine suite now contains 48 tests.
- Audited the complete public tree. All 160 navigation landmarks across 39
  pages have nonempty source names. W3C's landmark guidance recommends labels
  that distinguish repeated instances of a navigation region.
- Synchronized the state, audit, accessibility protocol, recommendations,
  build guide, homepage, Projects catalog, Executive Summary, Full Report, and
  short report. Preserved the clean outgoing October 6 report set under full
  commit `963b47d9d2aac3cd1ab58a8a1637329d1a0b1bcd` in the release ledger.

## Evidence and validation

- The October 7 public comparison ran after two public pages had already been
  edited. It found 291 files byte-identical and exactly those two pages
  different. Each production digest matched the corresponding clean incoming
  `HEAD` version, establishing all 293 incoming files as byte-identical. Public
  HTTP still cannot discover extra remote-only paths.
- All 48 routine tests pass. The Version 1 verifier passes all seven groups and
  now reports 160 named navigation landmarks alongside 39 complete landmark
  frames and responsive viewports, 97 native images with explicit
  alternatives, four named exposed ARIA images, 38 named tables, 204 exposed
  headings, 818 exposed named interactive or keyboard-focusable elements, 26
  safely hidden controls, no positive `tabindex` overrides, no automatic meta
  refreshes, and seven first-party stylesheets.
- Quarto 1.10.18 rebuilt the one-page Full Report, and the post-render
  normalizer validated the fresh output before the guarded publisher replaced
  the complete public report tree. The regenerated three-page, two-column
  short PDF and publication verifier pass reciprocal links, one summary
  figure, the required phrase, both PDF columns, nonempty pages, and the
  ten-page ceiling.
- A supplemental `w3m` 0.5.3 pass returned zero for all 13 selected pages at
  40 and 120 columns; every one of the 26 linearized views began with “Skip to
  content.” Roster, Project registry, Python compilation, repository
  whitespace, and local-link validation pass.

## Limitations and decisions

The corrected parser establishes that a repeated navigation landmark's
source-level `aria-labelledby` reference contributes nonempty text. It does not
compute every step of the full accessible-name algorithm, inspect the rendered
accessibility tree, establish that labels are meaningfully distinct, or
observe what a screen reader announces. Those properties remain in the manual
protocol.

No Chromium, Chrome, Firefox, or supported screen-reader/browser pairing is
installed, so the 52-result human review remains incomplete and Version 1
remains Active. The existing temporary ReportLab and pypdf build environment
was reused; no system tool, replacement runtime, production dependency,
credential, `.env`, manual deployment, PI-owned runner edit, charter edit,
earlier iteration edit, PI blockquote change, or parallel agent was used. The
runner integration suite remains intentionally excluded inside the live
Scholar run because the parent process holds the repository-wide lock. Normal
host-managed automation must still commit, push, deploy, and perform
authenticated inventory for this release.

## Questions and next steps

No blocking PI question. Execute the 13-page protocol in
`ACCESSIBILITY-REVIEW.md` on a browser/screen-reader-equipped host, repair and
retest any failure, and only then assess the charter and PI authority before
changing lifecycle state.

## Reference

World Wide Web Consortium Web Accessibility Initiative. (n.d.). *Landmark
regions*. Retrieved October 7, 2026, from
https://www.w3.org/WAI/ARIA/apg/practices/landmark-regions/

Elapsed time: 14 minutes 12 seconds (852 seconds).
