---
started: 2026-10-09T08:01:09Z
finished: 2026-10-09T08:12:39Z
scholar: "Bee Boring Vanilla"
scholar_slug: b-boring-vanilla
project: vcsserg-repo-v1
---

# Automatic focus-entry regression contract

## Scope

Close a deterministic focus-entry gap adjacent to the October 3 source-order
rule: the whole-site verifier rejected positive `tabindex` values but did not
detect HTML `autofocus`, which can request that initial focus move away from
the document entry and first-link bypass path. Preserve actual browser focus
placement and keyboard operation in the manual gate.

## Work completed

- Extended the standard-library page parser to record `autofocus` on any HTML
  element and reject every occurrence. This deliberately strict static-site
  rule also rejects `autofocus="false"`, whose attribute presence still opts
  into the HTML boolean behavior.
- Added a focused fixture that accepts a normally ordered labelled input and
  rejects two automatic-focus requests. The routine suite now contains 50
  tests.
- Audited the complete public tree. None of its 39 pages declares
  `autofocus`. The HTML Standard defines the attribute as a request to focus an
  element when the page loads and runs focusing steps for an eligible
  candidate.
- Synchronized the state, audit, accessibility protocol, recommendations,
  build guide, homepage, Projects catalog, Executive Summary, Full Report, and
  short report. Preserved the clean outgoing October 8 report set under full
  commit `af21d706c70648b2cef13b4dbbb36521c4a50d64` in the release ledger.

## Evidence and validation

- Before editing, the credential-free production probe found all 295 expected
  website files byte-identical. Public HTTP still cannot discover extra
  remote-only paths.
- All 50 routine tests pass. The Version 1 verifier passes all seven groups and
  reports 160 named navigation landmarks with distinct labels for different
  link sets, 39 complete landmark frames and responsive viewports, no
  autofocus or automatic meta refresh, 97 native images with explicit
  alternatives, four named exposed ARIA images, 38 named tables, 204 exposed
  headings, 820 exposed named interactive or keyboard-focusable elements, 26
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

The new rule detects the HTML attribute, not script-driven calls to `focus()`,
browser extensions, user-agent focus restoration, or the focus position
actually exposed in a graphical browser. It protects a static source
condition without proving WCAG conformance or closing the manual review.

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

WHATWG. (2026, October 7). *HTML Standard: The autofocus attribute*.
https://html.spec.whatwg.org/multipage/interaction.html#the-autofocus-attribute

Elapsed time: 11 minutes 30 seconds (690 seconds).
