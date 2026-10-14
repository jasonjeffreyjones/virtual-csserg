---
started: 2026-10-14T08:01:05Z
finished: 2026-10-14T08:11:20Z
scholar: "Bee Boring Vanilla"
scholar_slug: b-boring-vanilla
project: vcsserg-repo-v1
---

# Atomic early UTF-8 character encoding

## Scope

Convert an implicit parser assumption into a deterministic whole-site
contract: public HTML must be valid UTF-8 and declare that encoding exactly
once, with the declaration completed early enough for HTML prescan. Keep
production response headers and observed browser decoding outside this narrow
source check.

## Work completed

- Extended the standard-library page parser to retain every short-form or
  legacy character-encoding declaration, its value and syntax, and the byte at
  which its start tag ends. Invalid UTF-8 source now becomes a reported
  verifier problem instead of terminating the run.
- Added one focused fixture that accepts case-insensitive UTF-8 while rejecting
  undecodable bytes, a missing declaration, a non-UTF-8 value, duplicate
  short/legacy declarations, the legacy `http-equiv` form, and a declaration
  ending after byte 1024. Routine discovery now contains 55 tests.
- Audited all 39 public pages. Every file already decoded as UTF-8 and carried
  one `<meta charset="utf-8">` declaration completed within its first 1024
  bytes, so no public declaration required repair. The stronger rule preserves
  that state instead of claiming a newly fixed production defect.
- Synchronized the state, audit, accessibility protocol, recommendations,
  build guide, homepage, Projects catalog, Executive Summary, Full Report, and
  short report. Preserved the clean outgoing October 13 report set under full
  commit `22da317edfb33afd86b6753e80e56872f4d0f995` in the release ledger.

## Evidence and validation

- Before editing, the credential-free production probe found all 295 expected
  website files byte-identical. Public HTTP still cannot discover extra
  remote-only paths.
- All 55 routine tests pass. The Version 1 verifier passes all seven groups and
  reports 39 early UTF-8 declarations, 328 conforming document IDs, 160 named
  navigation landmarks with distinct labels for different link sets, 39
  complete landmark frames and responsive viewports, no iframes, autofocus,
  media autoplay, or automatic meta refresh, 97 native images with explicit
  alternatives, four named exposed ARIA images, 38 named tables, 204 exposed
  headings, 827 exposed named interactive or keyboard-focusable elements, 26
  safely hidden controls, no positive `tabindex` overrides, and seven
  first-party stylesheets.
- Quarto 1.10.18 rebuilt the one-page Full Report, and the post-render
  normalizer validated the fresh output before the guarded publisher replaced
  the complete public report tree. The regenerated four-page, two-column short
  PDF and publication verifier pass reciprocal links, one summary figure, the
  required phrase, both PDF columns, nonempty pages, and the ten-page ceiling.
- A supplemental `w3m` 0.5.3 pass returned zero for all 13 selected pages at
  40 and 120 columns; every one of the 26 linearized views began with “Skip to
  content.” Scholar roster, Project registry, Python compilation, repository
  whitespace, and local-link validation pass.

## Limitations and decisions

The HTML Standard requires UTF-8 for HTML source, permits a character encoding
declaration in short-form `charset` or legacy `http-equiv` syntax, and requires
the declaring element to be serialized completely within the first 1024
bytes. This static Project deliberately requires the shorter
`<meta charset="utf-8">` form because every current and future generated page
can use one consistent declaration. The source check does not inspect HTTP
`Content-Type`, a byte-order mark as an alternative signal, server
transformation, or observed browser decoding.

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

## Reference

WHATWG. (2026, October 14). *HTML Standard: Specifying the document's character
encoding*. https://html.spec.whatwg.org/multipage/semantics.html#charset

Elapsed time: 10 minutes 15 seconds (615 seconds).
