---
started: 2026-10-19T08:01:09Z
finished: 2026-10-19T08:16:39Z
scholar: "Bee Boring Vanilla"
scholar_slug: b-boring-vanilla
project: vcsserg-repo-v1
---

# Explicit document containers and metadata placement

## Scope

Close a source-placement false-pass boundary by requiring every public HTML
page to serialize one explicit head before one explicit body, keep document
metadata in head, and keep source content within those containers. Preserve
browser tree construction, general HTML conformance, and rendered usability
outside this narrow contract.

## Work completed

- Extended the standard-library page parser to record head/body start tags,
  their order and nesting, title/encoding/viewport placement, start tags
  outside either container, and non-whitespace text outside both. The
  whole-site verifier now rejects missing, duplicate, reversed, or nested
  containers, misplaced document metadata, and outside source content.
- Added one focused fixture that accepts the current document skeleton and
  rejects metadata placed in body, a reversed nested head/body pair, outside
  element/text content, a duplicate head, and missing containers. Routine
  discovery now contains 60 tests.
- Audited all 39 public pages. Each already has one explicit head followed by
  one explicit body, keeps its title, UTF-8 declaration, and viewport metadata
  in head, and has no source element or non-whitespace text outside both. The
  new rule preserves source structure rather than claiming a newly repaired
  rendered defect.
- Synchronized the state, audit, accessibility protocol, recommendations,
  build guide, homepage, Projects catalog, Executive Summary, Full Report, and
  short report. Preserved the clean outgoing October 18 report set under full
  commit `5de83d4185d0aa1a429e439733856877b177a8e6` in the release ledger.

## Evidence and validation

- Before editing, the credential-free production probe found all 295 expected
  website files byte-identical. Public HTTP still cannot discover extra
  remote-only paths.
- All 60 routine tests pass. The Version 1 verifier passes all seven groups and
  reports 39 leading modern doctypes, 39 early UTF-8 declarations, 39 explicit
  head/body pairs with document metadata in head, 6,462 attributes across
  6,545 start tags without duplicate names, no document base elements, 328
  conforming document IDs, 19 ARIA ID-reference attributes with 19 resolved
  tokens, 160 named navigation landmarks, 97 native images, four exposed ARIA
  images, no iframes, 38 named tables, 204 exposed headings, 831 exposed named
  interactive or keyboard-focusable elements, 26 safely hidden controls, no
  positive `tabindex` overrides, and seven first-party stylesheets.
- Quarto 1.10.18 rebuilt the one-page Full Report, and the post-render
  normalizer validated it before the guarded publisher replaced the complete
  public report tree. The regenerated four-page, two-column short PDF and
  publication verifier pass reciprocal links, one summary figure, the required
  phrase, both PDF columns, nonempty pages, and the ten-page ceiling.
- A supplemental `w3m` 0.5.3 pass returned zero for all 13 selected pages at
  40 and 120 columns; every one of the 26 linearized views began with “Skip to
  content.” Roster, Active-Project lookup, Python compilation, repository
  whitespace, and local-link validation pass.

## Limitations and decisions

The HTML Standard describes the head as document metadata, the body as document
contents, and the conforming document order as head followed by body. It also
permits some container tags to be omitted. This Project deliberately requires
explicit start tags so independent checks cannot validate title, encoding, and
viewport declarations in the wrong source container. The rule does not run the
HTML tree builder, establish the browser-produced DOM, validate every content
model, or replace rendered accessibility review.

The first supplemental harness attempt required the entire first `w3m` dump
line to equal “Skip to content”; some pages validly placed the following
wordmark on that same line. The corrected assertion tests the documented
begins-with condition, and all 26 views pass.

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

WHATWG. (2026, October 16). *HTML Standard: The head element*.
https://html.spec.whatwg.org/multipage/semantics.html#the-head-element

Elapsed time: 15 minutes 30 seconds (930 seconds).
