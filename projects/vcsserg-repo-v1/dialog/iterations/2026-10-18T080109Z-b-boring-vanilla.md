---
started: 2026-10-18T08:01:09Z
finished: 2026-10-18T08:12:38Z
scholar: "Bee Boring Vanilla"
scholar_slug: b-boring-vanilla
project: vcsserg-repo-v1
---

# All-ARIA ID-reference integrity

## Scope

Close an element-coverage gap by requiring every WAI-ARIA ID-reference
attribute in the public static tree to be nonempty and resolve within its
document. Preserve semantic relationship evaluation and observed browser or
assistive-technology behavior outside this narrow source contract.

## Work completed

- Extended the standard-library page parser to inventory
  `aria-activedescendant`, `aria-controls`, `aria-describedby`, `aria-details`,
  `aria-errormessage`, `aria-flowto`, `aria-labelledby`, and `aria-owns` on
  every element. The whole-site verifier now rejects an empty attribute or any
  token without a matching in-document ID, including relationships on generic
  regions outside the existing element-specific name and control paths.
- Added one focused fixture that exercises all eight attributes and rejects an
  empty `aria-labelledby` value plus two missing `aria-controls` targets.
  Routine discovery now contains 59 tests.
- Audited all 39 public pages. All 19 current ARIA ID-reference attributes
  resolve their 19 tokens, so no public relationship required repair. The new
  rule preserves referential integrity rather than claiming a newly fixed
  rendered defect.
- Synchronized the state, audit, accessibility protocol, recommendations,
  build guide, homepage, Projects catalog, Executive Summary, Full Report, and
  short report. Preserved the clean outgoing October 17 report set under full
  commit `e0a17209c6dafda70cf3c0a47caa79787a1d4deb` in the release ledger.

## Evidence and validation

- Before editing, the credential-free production probe found all 295 expected
  website files byte-identical. Public HTTP still cannot discover extra
  remote-only paths.
- All 59 routine tests pass. The Version 1 verifier passes all seven groups and
  reports 39 leading modern doctypes, 39 early UTF-8 declarations, 6,409
  attributes across 6,523 start tags without duplicate names, no document base
  elements, 328 conforming document IDs, 19 ARIA ID-reference attributes with
  19 resolved tokens, 160 named navigation landmarks, 97 native images with
  explicit alternatives, four named exposed ARIA images, no iframes, 38 named
  tables, 204 exposed headings, 830 exposed named interactive or
  keyboard-focusable elements, 26 safely hidden controls, no positive
  `tabindex` overrides, and seven first-party stylesheets.
- Quarto 1.10.18 rebuilt the one-page Full Report, and the post-render
  normalizer validated it before the guarded publisher replaced the complete
  public report tree. The regenerated four-page, two-column short PDF and
  publication verifier pass reciprocal links, one summary figure, the required
  phrase, both PDF columns, nonempty pages, and the ten-page ceiling.
- A supplemental `w3m` 0.5.3 pass returned zero for all 13 selected pages at
  40 and 120 columns; every one of the 26 linearized views began with “Skip to
  content.” Scholar roster, Active-Project lookup, Python compilation,
  repository whitespace, and local-link validation pass.

## Limitations and decisions

WAI-ARIA 1.2 defines ID references as same-document element identifiers and
directs user agents to ignore unmatched references. This Project applies the
stricter fail-closed source rule to prevent a relationship from disappearing
silently. The rule does not validate role support, single-reference versus
list cardinality, ownership constraints, relationship meaning, dynamic DOM
changes, accessible-name computation, or accessibility-tree exposure.

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

World Wide Web Consortium. (2023, June 6). *Accessible Rich Internet
Applications (WAI-ARIA) 1.2*. https://www.w3.org/TR/wai-aria-1.2/

Elapsed time: 11 minutes 29 seconds (689 seconds).
