---
started: 2026-10-08T08:01:05Z
finished: 2026-10-08T08:12:38Z
scholar: "Bee Boring Vanilla"
scholar_slug: b-boring-vanilla
project: vcsserg-repo-v1
---

# Distinct navigation labels for different link sets

## Scope

Close a false-pass boundary adjacent to the October 7 nonempty-name rule: the
whole-site verifier could accept the same source-derived accessible name on
repeated navigation regions containing different links. Preserve W3C's narrow
exception for repeated navigation regions with identical link sets and keep
label meaning and screen-reader announcement in the manual gate.

## Work completed

- Extended the standard-library page parser to retain link targets within each
  navigation landmark. Repeated source-derived names now fail when their link
  multisets differ; comparison is whitespace-normalized and case-insensitive.
- Added a focused fixture that rejects duplicate names on different link sets
  and accepts the same name when the link sets are identical, including a
  different source order. The routine suite now contains 49 tests.
- Audited the complete public tree. All 160 navigation landmarks across 39
  pages pass the new distinction rule. W3C recommends unique labels for
  repeated navigation landmarks and documents the identical-link-set
  exception.
- Synchronized the state, audit, accessibility protocol, recommendations,
  build guide, homepage, Projects catalog, Executive Summary, Full Report, and
  short report. Preserved the clean outgoing October 7 report set under full
  commit `28c71d77d6567c086b54d1ef239095743fb74dbd` in the release ledger.

## Evidence and validation

- Before editing, the credential-free production probe found all 295 expected
  website files byte-identical. Public HTTP still cannot discover extra
  remote-only paths.
- All 49 routine tests pass. The Version 1 verifier passes all seven groups and
  reports 160 named navigation landmarks with distinct labels for different
  link sets, 39 complete landmark frames and responsive viewports, no automatic
  meta refreshes, 97 native images with explicit alternatives, four named
  exposed ARIA images, 38 named tables, 204 exposed headings, 819 exposed named
  interactive or keyboard-focusable elements, 26 safely hidden controls, no
  positive `tabindex` overrides, and seven first-party stylesheets.
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

The new rule compares literal normalized source names and exact link-target
multisets. That is a deterministic safeguard, not an assessment that the names
are meaningful, that apparently identical targets serve the same purpose, or
that a browser and screen reader expose and announce the regions correctly.
Those properties remain in the manual protocol.

No Chromium, Chrome, Firefox, or supported screen-reader/browser pairing is
installed, so the 52-result human review remains incomplete and Version 1
remains Active. The existing temporary ReportLab and pypdf build environment
was reused; no system tool, replacement runtime, production dependency,
credential, `.env`, manual deployment, PI-owned runner edit, charter edit,
earlier iteration edit, PI blockquote change, or parallel agent was used. The
runner integration suite remains intentionally excluded inside the live
Scholar run because the parent process holds the repository-wide lock and no
runner boundary changed. Normal host-managed automation must still commit,
push, deploy, and perform authenticated inventory for this release.

## Questions and next steps

No blocking PI question. Execute the 13-page protocol in
`ACCESSIBILITY-REVIEW.md` on a browser/screen-reader-equipped host, repair and
retest any failure, and only then assess the charter and PI authority before
changing lifecycle state.

## Reference

World Wide Web Consortium Web Accessibility Initiative. (n.d.). *Landmark
regions*. Retrieved October 8, 2026, from
https://www.w3.org/WAI/ARIA/apg/practices/landmark-regions/

Elapsed time: 11 minutes 33 seconds (693 seconds).
