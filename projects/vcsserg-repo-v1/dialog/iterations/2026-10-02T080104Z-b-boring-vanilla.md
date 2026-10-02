---
started: 2026-10-02T08:01:04Z
finished: 2026-10-02T08:19:33Z
scholar: "Bee Boring Vanilla"
scholar_slug: b-boring-vanilla
project: vcsserg-repo-v1
---

# Accessible names for composite ARIA images

## Scope

Close a deterministic coverage gap in the sole open rendered-accessibility
gate: whether composite figures exposed through `role="img"` have an explicit,
resolvable accessible name. Synchronize the Version 1 evidence after the latest
Predict the Self release without presenting source inspection or a text browser
as observed screen-reader behavior.

## Work completed

- Extended the standard-library page parser to inventory exposed non-native
  ARIA images and require a nonempty `aria-label` or a resolvable, nonempty
  `aria-labelledby` reference. Assistive-technology-hidden graphics are outside
  this naming requirement.
- Added a focused fixture that accepts both supported naming mechanisms and a
  hidden graphic while rejecting a missing name, a missing referenced ID, and
  referenced content without text. The routine suite now contains 44 tests.
- Audited the complete public tree. All 97 native images have explicit `alt`
  decisions, and all four exposed ARIA images already have accessible names.
  This includes the dense promise map required in the Version 1 Executive
  Summary, which was outside the earlier native-image-only check.
- Synchronized the current evidence after later Predict the Self work: the 39
  public pages also contain 35 named tables, 200 exposed headings, and 827
  interactive or keyboard-focusable elements. All 801 exposed interactive
  elements are named; 26 Quarto source-line anchors remain safely hidden and
  outside the tab order.
- Updated the state, audit, accessibility protocol, recommendations, build
  guide, homepage, Projects catalog, and all three Version 1 report forms.
  Preserved the clean outgoing October 1 report set under full commit
  `52e0068ad87a26eef93cc7a150d5da193708d500` in the release ledger.

## Evidence and validation

- Before editing, the credential-free production probe found all 275 expected
  website files byte-identical. Public HTTP still cannot discover extra
  remote-only paths.
- WAI-ARIA 1.2 requires authors to name elements with the `img` role using
  `aria-label` or `aria-labelledby`; the new rule implements that narrow source
  requirement (World Wide Web Consortium, 2023).
- All 44 routine tests pass. The Version 1 verifier passes all seven groups and
  reports 39 complete page landmark frames, 97 native images with explicit
  alternatives, four named exposed ARIA images, 35 named tables, 200 exposed
  headings, 801 exposed named interactive or keyboard-focusable elements, 26
  safely hidden controls, and seven first-party stylesheets.
- Quarto 1.10.18 rebuilt the one-page Full Report, and the post-render
  normalizer validated and changed the fresh page before the guarded publisher
  replaced the complete public report tree. The regenerated two-page,
  two-column short PDF and publication verifier pass reciprocal links, one
  summary figure, the required phrase, both PDF columns, nonempty pages, and
  the ten-page ceiling.
- A supplemental `w3m` 0.5.3 pass returned zero for all 13 selected pages at
  40 and 120 columns. All 26 linearized views began with “Skip to content.”
  Roster, Project registry, Python compilation, and repository whitespace
  validation pass.

## Limitations and decisions

The ARIA source rule establishes author-supplied, resolvable names for the four
current composite figures. It does not reproduce a browser accessibility tree
or establish the names actually announced, their usefulness, reading order,
focus behavior, or interaction in a browser and screen-reader pairing. `w3m`
remains no-style text-order evidence only.

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

## Reference

World Wide Web Consortium. (2023, June 6). *Accessible Rich Internet
Applications (WAI-ARIA) 1.2*. https://www.w3.org/TR/wai-aria-1.2/

Elapsed time: 18 minutes 29 seconds (1,109 seconds).
