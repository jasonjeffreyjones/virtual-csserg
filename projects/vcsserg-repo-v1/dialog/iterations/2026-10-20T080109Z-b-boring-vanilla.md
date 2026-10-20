---
started: 2026-10-20T08:01:09Z
finished: 2026-10-20T08:15:33Z
scholar: "Bee Boring Vanilla"
scholar_slug: b-boring-vanilla
project: vcsserg-repo-v1
---

# Local CSS resource-graph integrity

## Scope

Close a local-resource false-pass boundary by checking files referenced through
CSS `url()` across the entire public stylesheet tree. Preserve full CSS
conformance, external-resource availability, document-fragment behavior, and
observed browser loading outside this narrow filesystem contract.

## Work completed

- Added a standard-library CSS URL scanner that ignores comments and ordinary
  string literals, parses quoted and unquoted `url()` functions, decodes CSS
  escapes, and distinguishes external, embedded, fragment-only, relative, and
  root-relative values. The whole-site verifier now rejects an empty URL or a
  local target that leaves `website/` or does not exist.
- Added one temporary-tree fixture covering URL-like comment and string text,
  an existing font with query and fragment components, an escaped filename,
  `data:` and external URLs, a fragment-only reference, an empty URL, a path
  escape, and a missing file. Routine discovery now contains 61 tests.
- Audited all 23 public stylesheets. Their four local CSS dependencies resolve
  inside the public tree, so no deployed resource required repair. The new
  rule extends the checked resource graph rather than claiming a newly fixed
  browser defect.
- Synchronized the state, audit, accessibility protocol, recommendations,
  build guide, homepage, Projects catalog, Executive Summary, Full Report, and
  short report. Preserved the clean outgoing October 19 report set under full
  commit `4cca15dc3dc306140e17050e464ad9c1e267c394` in the release ledger.

## Evidence and validation

- Before editing, the credential-free production probe found all 295 expected
  website files byte-identical. Public HTTP still cannot discover extra
  remote-only paths.
- All 61 routine tests pass. The Version 1 verifier passes all seven groups and
  reports 39 leading modern doctypes, 39 early UTF-8 declarations, 39 explicit
  head/body pairs with document metadata in head, 6,518 attributes across
  6,569 start tags without duplicate names, no document base elements, 328
  conforming document IDs, 19 ARIA ID-reference attributes with 19 resolved
  tokens, 160 named navigation landmarks, 97 native images, four exposed ARIA
  images, no iframes, 38 named tables, 204 exposed headings, 832 exposed named
  interactive or keyboard-focusable elements, 26 safely hidden controls,
  seven first-party stylesheets, and four resolved local CSS dependencies
  across all 23 stylesheets.
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

CSS Values and Units Level 4 specifies that relative resource URLs in an
external stylesheet resolve against that stylesheet, not the styled document,
and that an empty URL resolves to an invalid resource. The new scanner follows
those boundaries for literal `url()` functions and treats fragment-only values
as document-scoped rather than filesystem dependencies. It does not implement
a complete CSS parser, inspect bare-string `@import` rules or other future URL
notations, fetch external or embedded resources, evaluate fragment targets,
or observe browser requests.

The first supplemental harness attempt combined a short-circuiting `sed` with
`pipefail`, so the upstream `printf` received a broken pipe. Replacing that
pipeline with a here-string preserved the same begins-with assertion; all 26
views then passed.

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

World Wide Web Consortium. (2024, March 12). *CSS Values and Units Module Level
4*. https://www.w3.org/TR/css-values-4/#urls

Elapsed time: 14 minutes 24 seconds (864 seconds).
