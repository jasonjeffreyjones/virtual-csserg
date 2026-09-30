---
started: 2026-09-30T08:01:11Z
finished: 2026-09-30T08:27:31Z
scholar: "Bee Boring Vanilla"
scholar_slug: b-boring-vanilla
project: vcsserg-repo-v1
---

# Heading structure regression contract

## Scope

Strengthen a deterministic precursor to the sole open rendered-accessibility
gate: whether public headings contain intelligible source text and avoid
forward rank skips. Synchronize the Version 1 evidence snapshot after the
newest Predict the Self release, without presenting source inspection or a text
browser as observed screen-reader behavior.

## Work completed

- Extended the standard-library page parser to record exposed `h1` through
  `h6`, including visible descendant text and image alternatives. The static
  contract now rejects empty headings and forward jumps such as `h2` to `h4`,
  while permitting multiple `h1` elements and returns to higher ranks in a
  Quarto book structure.
- Added a focused fixture that rejects both failure modes and accepts a valid
  nested outline. Updated an existing empty-label fixture to acknowledge that
  its deliberately empty heading now violates both the heading and label
  contracts. The routine suite now contains 42 tests.
- Audited the complete public tree. All 196 exposed headings on 39 pages pass.
  Later Predict the Self work and this report's source citation bring the
  current inventory to 31 named tables and 809 interactive or
  keyboard-focusable elements: all 783 exposed interactive elements are named,
  and 26 Quarto source-line anchors remain safely hidden and untabbable.
- Synchronized the state, audit, accessibility protocol, recommendations,
  build guide, homepage, Projects catalog, and all three Version 1 report
  forms. Preserved the clean outgoing September 29 report set under full commit
  `7e4fb40f0309540a251ba7148987de97279d2751` in the release ledger.

## Evidence and validation

- Before editing, the credential-free production probe found all 257 expected
  website files byte-identical. Public HTTP still cannot discover extra
  remote-only paths.
- All 42 routine tests pass. The Version 1 verifier passes all seven groups and
  reports 39 HTML pages, 31 named tables, 196 exposed headings, 783 exposed
  named interactive or keyboard-focusable elements, 26 safely hidden controls,
  and seven first-party stylesheets.
- Quarto 1.10.18 rebuilt the one-page Full Report, the post-render normalizer
  validated and changed the fresh page, and the guarded publisher replaced the
  complete public report tree. The regenerated two-page, two-column short PDF
  and the publication verifier pass reciprocal links, one summary figure, the
  required phrase, both PDF columns, nonempty pages, and the ten-page ceiling.
- A supplemental `w3m` 0.5.3 pass returned zero for all 13 selected pages at
  40 and 120 columns. All 26 linearized views began with “Skip to content.”
  Python compilation and repository whitespace validation pass.

## Limitations and decisions

W3C's page-structure guidance says headings support in-page navigation and
recommends nesting ranks without forward skips. The new check implements that
narrow source contract. It does not reproduce a browser accessibility tree or
establish rendered heading order, announced names, focus behavior, or
screen-reader navigation. `w3m` remains no-style text-order evidence only.

No Chromium, Chrome, Firefox, or supported screen-reader/browser pairing is
installed, so the 52-result human review remains incomplete and Version 1
remains Active. The existing temporary ReportLab and pypdf build environment
was reused; no system tool, replacement runtime, production dependency,
credential, `.env`, manual deployment, PI-owned runner edit, charter edit,
earlier iteration edit, PI blockquote change, or parallel agent was used.
Normal host-managed automation must still commit, push, deploy, and perform
authenticated inventory for this release.

## Questions and next steps

No blocking PI question. Execute the 13-page protocol in
`ACCESSIBILITY-REVIEW.md` on a browser/screen-reader-equipped host, repair and
retest any failure, and only then assess the charter and PI authority before
changing lifecycle state.

Elapsed time: 26 minutes 20 seconds (1,580 seconds).
