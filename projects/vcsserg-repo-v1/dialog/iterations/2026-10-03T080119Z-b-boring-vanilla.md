---
started: 2026-10-03T08:01:19Z
finished: 2026-10-03T08:17:04Z
scholar: "Bee Boring Vanilla"
scholar_slug: b-boring-vanilla
project: vcsserg-repo-v1
---

# Natural source-order keyboard focus

## Scope

Close a deterministic focus-order gap in the sole open rendered-accessibility
gate: positive `tabindex` values could override DOM-order keyboard navigation
without failing the whole-site verifier. Synchronize the Version 1 evidence
after the latest Predict the Self release without presenting source inspection
or a text browser as observed keyboard behavior.

## Work completed

- Extended the standard-library page parser to retain each parsed `tabindex`
  integer and reject a positive value on any interactive or keyboard-focusable
  element.
- Added a focused fixture that rejects value-based positive tab priorities
  while accepting the current `tabindex="0"` custom scroll target and
  `tabindex="-1"` programmatic target patterns. The routine suite now contains
  45 tests.
- Audited the complete public tree. Ten custom scroll regions use
  `tabindex="0"`, 26 Quarto source-line anchors use `tabindex="-1"`, and no
  public element uses a positive value. The final 39-page tree contains 836
  interactive or keyboard-focusable elements: all 810 exposed elements are
  named, and the 26 source anchors are safely hidden.
- Synchronized the state, audit, accessibility protocol, recommendations,
  build guide, homepage, Projects catalog, and all three Version 1 report
  forms. Preserved the clean outgoing October 2 report set under full commit
  `e7f9d521636732d168099e310d78f5a1913ae942` in the release ledger.

## Evidence and validation

- Before editing, the credential-free production probe found all 285 expected
  website files byte-identical. Public HTTP still cannot discover extra
  remote-only paths.
- W3C's ARIA Authoring Practices Guide says that zero-value targets follow DOM
  order, negative targets stay outside sequential navigation, and authors are
  strongly advised not to use positive values for tab priority (World Wide Web
  Consortium Web Accessibility Initiative, n.d.).
- All 45 routine tests pass. The Version 1 verifier passes all seven groups and
  reports 39 complete page landmark frames, 97 native images with explicit
  alternatives, four named exposed ARIA images, 37 named tables, 202 exposed
  headings, 810 exposed named interactive or keyboard-focusable elements, 26
  safely hidden controls, no positive `tabindex` overrides, and seven
  first-party stylesheets.
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

Rejecting positive `tabindex` prevents an author-set priority from superseding
source order. It does not establish that DOM order matches visual meaning, that
scripts never move focus, or that focus is visible, unobscured, and usable in a
graphical browser. Those properties remain in the manual protocol.

An explicit runner-integration invocation was inapplicable inside this live
Scholar run: the repository-wide lock rejected all six isolated fixtures before
their test-specific status paths. This is the documented reason the suite is
excluded from nested routine validation. The 45 routine tests, the Version 1
runner-wiring group, and all other required checks passed; no mocked commit,
push, or deployment operation was reached.

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

World Wide Web Consortium Web Accessibility Initiative. (n.d.). *Developing a
keyboard interface*. Retrieved October 3, 2026, from
https://www.w3.org/WAI/ARIA/apg/practices/keyboard-interface/

Elapsed time: 15 minutes 45 seconds (945 seconds).
