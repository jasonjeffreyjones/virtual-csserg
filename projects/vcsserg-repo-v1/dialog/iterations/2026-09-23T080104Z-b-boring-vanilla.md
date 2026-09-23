---
started: 2026-09-23T08:01:04Z
finished: 2026-09-23T08:19:04Z
scholar: "Bee Boring Vanilla"
scholar_slug: b-boring-vanilla
project: vcsserg-repo-v1
---

# Explicit generated table-header scope

## Scope

Audit a deterministic prerequisite of the remaining rendered screen-reader
gate: whether public data-table headers declare their row or column
relationships. Repair the generated-report path and add regression coverage
without treating source markup as observed assistive-technology behavior.

## Work completed

- Audited all public table headers. Hand-authored tables already declared
  scope, while 60 header cells across the three table-bearing generated Quarto
  pages did not.
- Extended the shared, preflight-first post-render normalizer to add
  `scope="col"` only inside table heads, validate every table header against
  the four allowed scope values, and refuse an unrecognized remaining header
  before writing any page.
- Strengthened the whole-site parser to require valid scope on every public
  table header. Added focused generated-page and generic-page fixtures for
  repair, idempotence, accepted row/column scope, and fail-closed behavior.
- Rebuilt all four Quarto report pages through their documented source paths.
  Updated the three report build guides, accessibility protocol, audit,
  recommendations, v1 state, homepage, Projects catalog, and all three v1
  report forms. The Project remains Active because rendered keyboard and
  screen-reader review is still open.
- Recorded the clean outgoing v1 report set under full commit
  `60bcf794fc368495aa7fea7acacfe89c47c5b674` before materially updating the
  report narrative. The generated header markup in the other two Projects is
  accessibility maintenance recoverable through ordinary Git history.

## Evidence and validation

- Before editing, the credential-free production probe found all 158 expected
  website files byte-identical. This describes the incoming release; public
  HTTP still cannot discover extra remote-only paths.
- The pre-change baseline passed all 35 routine v1 tests and all seven Version
  1 promise groups. After adding the stronger generic rule but before rebuilding
  reports, the static-site group failed on exactly the 60 unscoped generated
  headers.
- After repair, all 37 routine v1 tests pass, including five normalizer tests
  and the generic table-header fixture. All seven Version 1 groups pass across
  26 HTML pages and six first-party stylesheets. A second normalizer pass
  changed zero pages.
- Quarto 1.10.18 rendered all four report pages successfully. The existing NFL
  warning about its output directory being outside the Project directory
  recurred, but rendering and validation completed.
- The VCSSERG v1, Predict the Self, and NFL publication verifiers pass. Their
  routine suites pass 37, 33, and 7 tests respectively. The NFL verifier first
  found its project-specific temporary dependency path absent, then passed
  against the already-present v1 build-only `pypdf` path; no package was
  installed.
- Roster and Project registry checks report four Scholars, four Projects, and
  three Published Projects. Python compilation, release-key artifact lookup,
  and repository whitespace validation pass.

## Limitations and decisions

W3C technique H63 treats `scope` as a way to make table-header relationships
explicit and its test procedure checks valid scope values. The new contract is
therefore a deliberately stronger, uniform source convention; absence of
`scope` on a simple first-row header was not represented as a WCAG failure.

No graphical browser or supported screen-reader/browser pairing is installed.
Explicit scope reduces ambiguity but does not establish announcement quality or
row/column navigation in assistive technology. The 44-result review in
`ACCESSIBILITY-REVIEW.md` remains incomplete and is still the sole manual gate.

No credential, `.env`, manual deployment, package or replacement-runtime
installation, PI-owned runner edit, charter edit, earlier iteration edit, PI
blockquote change, or parallel agent was used. Normal host-managed automation
must still commit, push, deploy, and perform authenticated inventory for this
revised release.

## Questions and next steps

No blocking PI question. Execute `ACCESSIBILITY-REVIEW.md` on a
browser/screen-reader-equipped host, verify report table caption and header
navigation along with the other recorded checks, repair and retest any failure,
and only then assess the charter and PI authority before changing lifecycle
state.

Elapsed time: 18 minutes (1,080 seconds).
