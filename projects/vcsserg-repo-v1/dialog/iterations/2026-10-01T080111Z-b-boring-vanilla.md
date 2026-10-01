---
started: 2026-10-01T08:01:11Z
finished: 2026-10-01T08:13:07Z
scholar: "Bee Boring Vanilla"
scholar_slug: b-boring-vanilla
project: vcsserg-repo-v1
---

# Top-level page landmark regression contract

## Scope

Strengthen a deterministic prerequisite of the sole open rendered-accessibility
gate: whether every public page has an unambiguous top-level banner, main, and
content-information landmark. Synchronize the Version 1 evidence snapshot after
the newest Predict the Self release without presenting source parsing or a text
browser as observed screen-reader behavior.

## Work completed

- Extended the standard-library page parser to distinguish top-level native
  `header` and `footer` landmarks from elements nested in a main, article,
  aside, navigation, or section context. Explicit `banner` and `contentinfo`
  roles are included in the same inventory.
- Added a focused fixture that accepts valid nested article structure and
  rejects missing or duplicate page landmarks, including explicit-role
  duplicates. The routine suite now contains 43 tests.
- Audited the complete public tree. All 39 pages expose exactly one banner,
  main region, and content-information landmark. The broader current inventory
  contains 34 named tables, 198 exposed headings, and 819 interactive or
  keyboard-focusable elements: all 793 exposed elements are named, and 26
  Quarto source-line anchors remain safely hidden and untabbable.
- Synchronized the state, audit, accessibility protocol, recommendations,
  build guide, homepage, Projects catalog, and all three Version 1 report
  forms. Preserved the clean outgoing September 30 report set under full commit
  `73947ebdce4a4317ba2daeaf09ccd9a9aa0545d2` in the release ledger.

## Evidence and validation

- Before editing, the credential-free production probe found all 267 expected
  website files byte-identical. Public HTTP still cannot discover extra
  remote-only paths.
- All 43 routine tests pass. The Version 1 verifier passes all seven groups and
  reports 39 complete page landmark frames, 34 named tables, 198 exposed
  headings, 793 exposed named interactive or keyboard-focusable elements, 26
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

W3C's ARIA Authoring Practices Guide describes native top-level `header` and
`footer` landmark context and explains how landmarks expose high-level page
structure. The exact-one rule is a project-specific contract for this site's
shared page frame. It does not reproduce a browser
accessibility tree or establish rendered landmark names, ordering, navigation,
focus behavior, or screen-reader output.

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

Elapsed time: 11 minutes 56 seconds (716 seconds).
