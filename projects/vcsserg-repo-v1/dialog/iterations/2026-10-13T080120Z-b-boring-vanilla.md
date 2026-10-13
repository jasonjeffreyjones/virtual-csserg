---
started: 2026-10-13T08:01:20Z
finished: 2026-10-13T08:12:36Z
scholar: "Bee Boring Vanilla"
scholar_slug: b-boring-vanilla
project: vcsserg-repo-v1
---

# Conforming document identifier regression contract

## Scope

Close the remaining HTML authoring-conformance gap in the existing document-ID
check. Preserve its duplicate-ID rejection while making empty values and ASCII
whitespace deterministic whole-site failures. Keep rendered behavior and WCAG
conformance outside this narrow source claim.

## Work completed

- Changed the standard-library page parser to retain every `id` attribute,
  including an empty value. Moved identifier validation from an inline
  duplicate-only check into a page-level function requiring every ID to be
  nonempty, contain no ASCII whitespace, and be unique within its document.
- Added one focused fixture covering a valid fragment pair plus empty,
  whitespace-containing, and duplicate ID failures. Routine discovery now
  contains 54 tests.
- Audited all 39 public pages. Their 328 ID attributes already satisfied all
  three constraints, so no published identifier required repair. The stronger
  rule preserves this state for future fragments and ARIA references rather
  than claiming a newly fixed public defect.
- Synchronized the state, audit, accessibility protocol, recommendations,
  build guide, homepage, Projects catalog, Executive Summary, Full Report, and
  short report. Preserved the clean outgoing October 12 report set under full
  commit `87eafc61160ae3684d8fc37b99e807ff40d6258a` in the release ledger.

## Evidence and validation

- Before editing, the credential-free production probe found all 295 expected
  website files byte-identical. Public HTTP still cannot discover extra
  remote-only paths.
- All 54 routine tests pass. The Version 1 verifier passes all seven groups and
  reports 39 atomic English language/title declarations, 328 conforming
  document IDs, 160 named navigation landmarks with distinct labels for
  different link sets, 39 complete landmark frames and responsive viewports,
  no iframes, autofocus, media autoplay, or automatic meta refresh, 97 native
  images with explicit alternatives, four named exposed ARIA images, 38 named
  tables, 204 exposed headings, 826 exposed named interactive or
  keyboard-focusable elements, 26 safely hidden controls, no positive
  `tabindex` overrides, and seven first-party stylesheets.
- Quarto 1.10.18 rebuilt the one-page Full Report, and the post-render
  normalizer validated the fresh output before the guarded publisher replaced
  the complete public report tree. The regenerated three-page, two-column
  short PDF and publication verifier pass reciprocal links, one summary
  figure, the required phrase, both PDF columns, nonempty pages, and the
  ten-page ceiling.
- A supplemental `w3m` 0.5.3 pass returned zero for all 13 selected pages at
  40 and 120 columns; every one of the 26 linearized views began with “Skip to
  content.” Roster, Python compilation, repository whitespace, and local-link
  validation pass.

## Limitations and decisions

The HTML Standard requires an ID value to be nonempty, contain no ASCII
whitespace, and remain unique in its element tree. This Project applies those
authoring constraints page-wide because its fragment, bypass, label, control,
and accessible-name checks rely on unambiguous ID targets. The check is not a
general HTML validator and does not inspect duplicate attribute names,
script-created DOM state, browser fragment selection, or assistive-technology
behavior. A source pass is not a WCAG conformance claim.

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

WHATWG. (2026, October 12). *HTML Standard: Global attributes*.
https://html.spec.whatwg.org/multipage/dom.html#the-id-attribute

Elapsed time: 11 minutes 16 seconds (676 seconds).
