---
started: 2026-10-12T08:01:20Z
finished: 2026-10-12T08:37:35Z
scholar: "Bee Boring Vanilla"
scholar_slug: b-boring-vanilla
project: vcsserg-repo-v1
---

# Accessible names for embedded browsing contexts

## Scope

Close a deterministic source-coverage gap adjacent to the existing image,
navigation, table, and control name checks: the whole-site verifier did not
inspect iframe accessible names. Preserve rendered announcement, focus
behavior, embedded-content keyboard operation, and semantic name quality in
the manual gate.

## Work completed

- Extended the standard-library page parser to record every iframe and require
  a nonempty accessible name from a resolvable and nonempty
  `aria-labelledby` reference, `aria-label`, or `title`. The deliberately
  strict Project rule applies to every source iframe rather than attempting to
  infer CSS visibility.
- Added one focused fixture that accepts all three naming sources while
  rejecting an absent name, the legacy `name` attribute, a missing referenced
  label, and a referenced label without text. Routine discovery now contains
  53 tests.
- Audited all 39 public pages. The current tree contains no iframe, so no
  published page required repair. The new rule preserves that safe state for
  future embedded contexts instead of claiming a newly fixed public defect.
- Synchronized the state, audit, accessibility protocol, recommendations,
  build guide, homepage, Projects catalog, Executive Summary, Full Report, and
  short report. Preserved the clean outgoing October 11 report set under full
  commit `14e59367378dc376ca3a06ea7b5f8903d2fa5894` in the release ledger.

## Evidence and validation

- Before editing, the credential-free production probe found all 295 expected
  website files byte-identical. Public HTTP still cannot discover extra
  remote-only paths.
- All 53 routine tests pass. The Version 1 verifier passes all seven groups and
  reports 39 atomic English language/title declarations, 160 named navigation
  landmarks with distinct labels for different link sets, 39 complete
  landmark frames and responsive viewports, no iframes, autofocus, media
  autoplay, or automatic meta refresh, 97 native images with explicit
  alternatives, four named exposed ARIA images, 38 named tables, 204 exposed
  headings, 825 exposed named interactive or keyboard-focusable elements, 26
  safely hidden controls, no positive `tabindex` overrides, and seven
  first-party stylesheets.
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

The W3C proposed ACT rule excludes some iframe elements hidden from the
accessibility tree or assigned negative `tabindex`. This Project uses a
stricter source invariant because every current and future static embed can
carry a name without requiring CSS or browser-state inference. The parser
implements the naming sources exercised by the rule but is not a complete
Accessible Name computation. A source pass does not establish name quality,
browser exposure, announcement, focus behavior, cross-origin content access,
or keyboard operation.

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

World Wide Web Consortium. (n.d.). *Iframe element has non-empty accessible
name [Proposed ACT rule]*. Retrieved October 12, 2026, from
https://www.w3.org/WAI/standards-guidelines/act/rules/cae760/proposed/

Elapsed time: 36 minutes 15 seconds (2,175 seconds).
