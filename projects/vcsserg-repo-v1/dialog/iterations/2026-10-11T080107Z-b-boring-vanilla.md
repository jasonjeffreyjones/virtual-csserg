---
started: 2026-10-11T08:01:07Z
finished: 2026-10-11T08:13:37Z
scholar: "Bee Boring Vanilla"
scholar_slug: b-boring-vanilla
project: vcsserg-repo-v1
---

# Atomic page language and document title

## Scope

Close a false-pass boundary in two source properties the whole-site verifier
already claimed: a later `html` element could overwrite the first language and
multiple `title` elements could merge into one apparently nonempty title. Keep
language correctness, semantic title quality, and actual browser or
screen-reader announcement outside this deterministic source check.

## Work completed

- Changed the standard-library parser to retain every HTML root-language and
  document-title occurrence. The static-site group now requires exactly one
  `html` element with `lang="en"` and exactly one nonempty HTML document title.
  It ignores a same-named element inside SVG rather than letting a chart title
  satisfy the page-title rule.
- Added one focused fixture covering a valid document, a missing root language,
  a whitespace-only title, an SVG-only title, and duplicate roots and titles.
  Routine discovery now contains 52 tests.
- Audited all 39 public pages. Every page already had one English root
  declaration and one nonempty, unique title; no published HTML repair was
  needed. Corrected the manual-review narrative's stale table total from 37 to
  the verifier's current 38.
- Synchronized the state, audit, accessibility protocol, recommendations,
  build guide, homepage, Projects catalog, Executive Summary, Full Report, and
  short report. Preserved the clean outgoing October 10 report set under full
  commit `2bb7d4cd80fb8dfbcd840ea9207acf57b9e90889` in the release ledger.

## Evidence and validation

- Before editing, the credential-free production probe found all 295 expected
  website files byte-identical. Public HTTP still cannot discover extra
  remote-only paths.
- All 52 routine tests pass. The Version 1 verifier passes all seven groups and
  reports 39 atomic English language/title declarations, 160 named navigation
  landmarks with distinct labels for different link sets, 39 complete
  landmark frames and responsive viewports, no autofocus, media autoplay, or
  automatic meta refresh, 97 native images with explicit alternatives, four
  named exposed ARIA images, 38 named tables, 204 exposed headings, 824 exposed
  named interactive or keyboard-focusable elements, 26 safely hidden controls,
  no positive `tabindex` overrides, and seven first-party stylesheets.
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

The exactly-one rule is deliberately stricter than the narrow W3C ACT
page-title test, which evaluates the first HTML title and notes that multiple
titles are an HTML-validity issue rather than by themselves a WCAG failure.
This static Project has no need for ambiguous roots or titles. The English
contract matches the current publication corpus but does not inspect
language-of-parts markup or determine whether prose is actually English. The
title rule establishes presence and atomicity, not whether each title describes
topic or purpose. Those judgments and observed announcement remain in the
manual protocol.

No Chromium, Chrome, Firefox, or supported screen-reader/browser pairing is
installed, so the 52-result human review remains incomplete and Version 1
remains Active. The existing temporary ReportLab and pypdf build environment
was reused; no system tool, replacement runtime, production dependency,
credential, `.env`, manual deployment, PI-owned runner edit, charter edit,
earlier iteration edit, PI blockquote change, or parallel agent was used. The
runner integration suite remains intentionally excluded because no runner
boundary changed and a live Scholar run may hold the repository-wide lock.
Normal host-managed automation must still commit, push, deploy, and perform
authenticated inventory for this release.

## Questions and next steps

No blocking PI question. Execute the 13-page protocol in
`ACCESSIBILITY-REVIEW.md` on a browser/screen-reader-equipped host, repair and
retest any failure, and only then assess the charter and PI authority before
changing lifecycle state.

## References

World Wide Web Consortium Web Accessibility Initiative. (2026a, March 9).
*Understanding Success Criterion 3.1.1: Language of Page*.
https://www.w3.org/WAI/WCAG22/Understanding/language-of-page.html

World Wide Web Consortium Web Accessibility Initiative. (2026b, March 9).
*Understanding Success Criterion 2.4.2: Page Titled*.
https://www.w3.org/WAI/WCAG22/Understanding/page-titled.html

Elapsed time: 12 minutes 30 seconds (750 seconds).
