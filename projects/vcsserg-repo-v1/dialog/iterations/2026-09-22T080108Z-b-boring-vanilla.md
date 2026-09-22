---
started: 2026-09-22T08:01:08Z
finished: 2026-09-22T08:18:42Z
scholar: "Bee Boring Vanilla"
scholar_slug: b-boring-vanilla
project: vcsserg-repo-v1
---

# Named Quarto navigation landmarks

## Scope

Audit another deterministic prerequisite of the sole remaining rendered
accessibility gate: whether repeated navigation landmarks on public pages have
names that let screen-reader users distinguish their purposes. Repair any
source-controlled defect without claiming unavailable assistive-technology
evidence.

## Work completed

- Strengthened the whole-site parser to require an accessible name on every
  navigation landmark when a page contains more than one and to reject any
  `aria-labelledby` reference whose target is absent.
- The new rule exposed 14 unnamed landmarks across all four generated Quarto
  pages: mobile report navigation, chapter sidebars, on-page contents, and the
  previous/next chapter regions present in Predict the Self.
- Extended the shared, preflight-first post-render normalizer to assign stable
  names to those Quarto regions, validate every report `nav`, and refuse an
  unknown unnamed navigation region before writing any page. Added focused
  fixtures for generated labels, idempotence, fail-closed handling, generic
  repeated-navigation names, and label-target resolution.
- Rebuilt all three Quarto Full Reports through their documented source paths;
  the VCSSERG v1 and Predict the Self guarded publishers replaced their public
  report trees, while the NFL build wrote its configured public output. A
  second normalizer pass changed zero pages.
- Updated the accessibility protocol, build documentation for all three
  reports, audit, recommendations, current state, public homepage notebook, and
  metadata-derived Projects catalog. The Project remains Active because the
  rendered keyboard and screen-reader review is still open.

## Evidence and validation

- Before editing, the credential-free production probe found all 150 expected
  website files byte-identical. This describes the incoming release; public
  HTTP still cannot discover extra remote-only paths.
- The pre-change baseline passed all 33 routine v1 tests and all seven Version
  1 promise groups. After adding the stronger generic rule but before repairing
  generated HTML, the Version 1 verifier failed only the static-site group and
  identified all 14 unnamed landmarks.
- After repair, all 35 routine v1 tests pass, including four normalizer tests
  and the generic navigation-landmark fixture. All seven Version 1 groups pass
  across 26 HTML pages and six first-party stylesheets.
- Quarto 1.10.18 rendered all four report pages successfully, and the shared
  post-render step normalized each output. The existing NFL warning about its
  output directory being outside the Project directory recurred, but rendering
  and validation completed.
- The VCSSERG v1, Predict the Self, and NFL publication verifiers pass. Their
  routine suites pass 35, 28, and 7 tests respectively. Roster and Project
  registry checks report four Scholars, four Projects, and three Published
  Projects; Python compilation and repository whitespace validation pass. An
  initial final check correctly rejected the Projects catalog because its old
  order placed a September 21 update before this September 22 update; the
  catalog was reordered from state metadata and the complete required checks
  then passed.

## Limitations and decisions

No graphical browser or supported screen-reader/browser pairing is installed,
so named source landmarks reduce a known risk but do not establish their
rendered announcement or usability. The 44-result review in
`ACCESSIBILITY-REVIEW.md` remains incomplete and is still the sole manual gate.

The public Full Report changes only add accessible names to generated
navigation; they do not change a claim, method, result, interpretation,
limitation, or report structure. Under `REPORT-ARCHIVING.md`, this is navigation
maintenance recoverable through ordinary Git history, so no material report
supersession was recorded. No package, credential, `.env`, manual deployment,
replacement runtime, PI-owned runner edit, charter edit, earlier iteration
edit, or PI blockquote change occurred. Normal host-managed automation must
still commit, push, deploy, and perform authenticated inventory for this
revised release.

## Questions and next steps

No blocking PI question. Execute `ACCESSIBILITY-REVIEW.md` on a
browser/screen-reader-equipped host, record the environment and all 44 results,
repair and retest any failure, and only then assess the charter and PI authority
before changing the Project lifecycle state.

Elapsed time: 17 minutes 34 seconds (1,054 seconds).
