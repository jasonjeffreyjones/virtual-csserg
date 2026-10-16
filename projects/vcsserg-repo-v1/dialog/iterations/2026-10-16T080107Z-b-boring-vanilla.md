---
started: 2026-10-16T08:01:07Z
finished: 2026-10-16T08:11:28Z
scholar: "Bee Boring Vanilla"
scholar_slug: b-boring-vanilla
project: vcsserg-repo-v1
---

# Unique start-tag attribute names

## Scope

Close a parser false-pass boundary by making unique attribute names within each
HTML start tag a deterministic whole-site invariant. Preserve rendered DOM
behavior and general HTML conformance outside this narrow source contract.

## Work completed

- Extended the standard-library page parser to retain raw attribute names
  before converting them to the mapping used by downstream checks. It now
  reports the actual source-order start-tag number, element name, and every
  repeated name using an ASCII case-insensitive comparison.
- Added one focused fixture that accepts distinct names and rejects mixed-case
  duplicate `id`, `alt`, and `aria-label` declarations. Routine discovery now
  contains 57 tests.
- Audited all 39 public pages. Their 6,263 attributes across 6,474 start tags
  already had unique names, so no public attribute required repair. The new
  rule prevents a later duplicate from overwriting a value inspected by the
  verifier without claiming a newly fixed browser defect.
- Synchronized the state, audit, accessibility protocol, recommendations,
  build guide, homepage, Projects catalog, Executive Summary, Full Report, and
  short report. Preserved the clean outgoing October 15 report set under full
  commit `b92fce6fc7d29255afb200ff703d8c35fdd27c0c` in the release ledger.

## Evidence and validation

- Before editing, the credential-free production probe found all 295 expected
  website files byte-identical. Public HTTP still cannot discover extra
  remote-only paths.
- All 57 routine tests pass. The Version 1 verifier passes all seven groups and
  reports 39 leading modern doctypes, 39 early UTF-8 declarations, 6,263
  attributes across 6,474 start tags without duplicate names, 328 conforming
  document IDs, 160 named navigation landmarks with distinct labels for
  different link sets, 39 complete landmark frames and responsive viewports,
  no iframes, autofocus, media autoplay, or automatic meta refresh, 97 native
  images with explicit alternatives, four named exposed ARIA images, 38 named
  tables, 204 exposed headings, 829 exposed named interactive or
  keyboard-focusable elements, 26 safely hidden controls, no positive
  `tabindex` overrides, and seven first-party stylesheets.
- Quarto 1.10.18 rebuilt the one-page Full Report, and the post-render
  normalizer validated the fresh output before the guarded publisher replaced
  the complete public report tree. The regenerated four-page, two-column short
  PDF and publication verifier pass reciprocal links, one summary figure, the
  required phrase, both PDF columns, nonempty pages, and the ten-page ceiling.
- A supplemental `w3m` 0.5.3 pass returned zero for all 13 selected pages at
  40 and 120 columns; every one of the 26 linearized views began with “Skip to
  content.” Scholar roster, Python compilation, repository whitespace, and
  local-link validation pass.

## Limitations and decisions

The HTML Standard prohibits two attributes on the same start tag whose names
are an ASCII case-insensitive match. This Project records raw names because
collapsing them first can hide ambiguity in critical `id`, `alt`, ARIA,
metadata, and reference values. The rule is not a general HTML validator and
does not inspect duplicate names created by script, malformed tokenization, the
DOM chosen by a browser, or assistive-technology behavior.

No Chromium, Chrome, Firefox, or supported screen-reader/browser pairing is
installed, so the 52-result human review remains incomplete and Version 1
remains Active. The pinned ReportLab and pypdf build-only packages were
recreated under `/tmp`; no system tool, replacement runtime, production
dependency, credential, `.env`, manual deployment, PI-owned runner edit,
charter edit, earlier iteration edit, PI blockquote change, or parallel agent
was used. The runner integration suite remains intentionally excluded because
no runner boundary changed and a live Scholar run may hold the repository-wide
lock. Normal host-managed automation must still commit, push, deploy, and
perform authenticated inventory for this release.

## Questions and next steps

No blocking PI question. Execute the 13-page protocol in
`ACCESSIBILITY-REVIEW.md` on a browser/screen-reader-equipped host, repair and
retest any failure, and only then assess the charter and PI authority before
changing lifecycle state.

## Reference

WHATWG. (2026, October 16). *HTML Standard: Attributes*.
https://html.spec.whatwg.org/multipage/syntax.html#attributes-2

Elapsed time: 10 minutes 21 seconds (621 seconds).
