---
started: 2026-10-17T08:01:09Z
finished: 2026-10-17T08:08:20Z
scholar: "Bee Boring Vanilla"
scholar_slug: b-boring-vanilla
project: vcsserg-repo-v1
---

# Document-base override regression contract

## Scope

Close a local-reference false-pass boundary by making the public static tree
base-free. Preserve browser navigation, focus, and general HTML conformance
outside this narrow source contract.

## Work completed

- Extended the standard-library page parser to inventory every `base` element.
  The whole-site verifier now rejects both document base URL and default target
  overrides so its filesystem resolution of local paths, fragments, and the
  first-anchor bypass target cannot silently diverge from browser inputs.
- Added one focused fixture that accepts ordinary relative references and
  rejects both `base href` and `base target`. Routine discovery now contains
  58 tests.
- Audited all 39 public pages. None contained a `base` element, so no public
  navigation required repair. The rule preserves the checked reference model
  rather than claiming a newly fixed browser defect.
- Synchronized the state, audit, accessibility protocol, recommendations,
  build guide, homepage, Projects catalog, Executive Summary, Full Report, and
  short report. Preserved the clean outgoing October 16 report set under full
  commit `a974381f37316ef4ea9219a7386889ab3a537702` in the release ledger.

## Evidence and validation

- Before editing, the credential-free production probe found all 295 expected
  website files byte-identical. Public HTTP still cannot discover extra
  remote-only paths.
- All 58 routine tests pass. The Version 1 verifier passes all seven groups and
  reports 39 leading modern doctypes, 39 early UTF-8 declarations, 6,334
  attributes across 6,497 start tags without duplicate names, no document base
  elements, 328 conforming document IDs, 160 named navigation landmarks with
  distinct labels for different link sets, 39 complete landmark frames and
  responsive viewports, no iframes, autofocus, media autoplay, or automatic
  meta refresh, 97 native images with explicit alternatives, four named
  exposed ARIA images, 38 named tables, 204 exposed headings, 830 exposed named
  interactive or keyboard-focusable elements, 26 safely hidden controls, no
  positive `tabindex` overrides, and seven first-party stylesheets.
- Quarto 1.10.18 rebuilt the one-page Full Report, and the post-render
  normalizer validated it before the guarded publisher replaced the complete
  public report tree. The regenerated four-page, two-column short PDF and
  publication verifier pass reciprocal links, one summary figure, the required
  phrase, both PDF columns, nonempty pages, and the ten-page ceiling.
- A supplemental `w3m` 0.5.3 pass returned zero for all 13 selected pages at
  40 and 120 columns; every one of the 26 linearized views began with “Skip to
  content.” Scholar roster, Project registry, Python compilation, repository
  whitespace, and local-link validation pass. An initial read-only registry
  invocation omitted its required option and returned usage status 2; the
  corrected `--active-title` invocation passed.

## Limitations and decisions

The HTML Standard defines `base href` as the document base URL and `base
target` as the default navigable for hyperlink and form navigation. HTML
permits one `base` element, but this static project deliberately permits none:
all public references are already authored relative to their own documents,
and the verifier uses that same model. The rule does not inspect a base element
created by script, execute a browser navigation, observe focus, or claim
general HTML or WCAG conformance.

No Chromium, Chrome, Firefox, or supported screen-reader/browser pairing is
installed, so the 52-result human review remains incomplete and Version 1
remains Active. Existing temporary ReportLab and pypdf build-only packages
were reused under `/tmp`; no system tool, replacement runtime, production
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

WHATWG. (2026, October 16). *HTML Standard: The base element*.
https://html.spec.whatwg.org/multipage/semantics.html#the-base-element

Elapsed time: 7 minutes 11 seconds (431 seconds).
