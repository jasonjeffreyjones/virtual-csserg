# VCSSERG Version 1.0 Audit

This is a point-in-time map from documented promises to observable evidence. It
separates verified behavior from assumptions so “works as documented” remains a
testable goal.

Run the non-destructive automated portion from the repository root:

```bash
python3 projects/vcsserg-repo-v1/verify_v1.py
```

The verifier does not read `.env`, contact remote systems, create commits, or
deploy. It returns nonzero while an automated group fails. A passing run still
does not establish rendered keyboard or assistive-technology usability.

## Evidence matrix

| Documented promise | Evidence or test | Status on September 24, 2026 |
|---|---|---|
| Repository guidance and growth procedure exist | Required top-level files, creation guide, tested Project and Scholar creation, validated identity roster and biographies, and a guarded manual-review record | Automated pass |
| Every Project uses current memory and metadata | `PROJECT.md`, `STATE.md`, bounded `DIALOG.md`, immutable iteration/year indexes, legacy hashes where applicable, plus `title`, `status`, `publication`, `updated`, including `_template` | Automated pass; Active Unpublished work is valid and all five pre-migration dialogs are byte-preserved |
| Public static site is branded, accessible by deterministic checks, and locally connected | First-party HTML/CSS semantics, first-anchor bypass links, named repeated navigation landmarks, scoped table headers, explicit image alternatives, named exposed links/buttons with valid ARIA relationships and safely hidden source-line anchors, local paths/fragments, Bootstrap CDN, logo, grouped required footer | Automated pass across 26 HTML pages, 527 interactive elements, and 6 first-party stylesheets; generated-report bypass order, navigation names, and table-head scope no longer depend on runtime JavaScript or hand-editing; rendered keyboard/assistive-technology QA remains manual |
| Published Projects and Scholars are findable and sourced | `publication` metadata, `scholars.json`, canonical biographies, home, Projects index, Scholar index, and profiles | Automated pass; lifecycle and publication are independent |
| Every Published Project has all three linked report formats | Executive Summary with exactly one figure, Quarto source/book, Full Report, short PDF, cross-links and required phrase | Automated pass |
| Scholar runner fails closed | Inspectable clean tree, known Scholar, Active Project, unchanged PI-owned runner, independent checks, abort behavior, and commit/push/deploy ordering | Automated pass; the separately invoked integration suite witnesses each controlled failure without external effects and is excluded from nested routine validation |
| Deployment safely mirrors `website/` | Mocked guarded transfer plus checksum/inventory dry run; completed normal workflow; public expected-file probe | Pass; the September 15 run reached completion only after exact-inventory verification, all 110 expected files matched production on September 16, 114 matched before the September 18 revision, 128 before the September 19 revision, 134 before the September 20 revision, 142 before the September 21 revision, 150 before the September 22 revision, 158 before the September 23 revision, and 166 before the September 24 revision |

## Current automated result

On September 24, 2026, **all seven groups pass**. The final report-format gap
had closed the previous day when Predict the Self adopted the current
publication structure:

- VCSSERG v1 supplies a Quarto HTML book, linked two-column PDF, and the
  PI-selected evidence-brief Executive Summary with one dense figure.
- Predict the Self now supplies a two-chapter Quarto book, guarded publication
  pipeline, one-figure evidence brief, and linked two-column PDF. Its book and
  short report explicitly allow content-driven chapter/page counts within the
  documented constraints.
- NFL Team Fandom Identities supplies all three forms. Its Quarto footer source
  and rendered report now retain the PI-requested GitHub link.
- `scholars.json` is now the validated identity source for names, slugs, and
  monograms, while `scholars/<slug>/BIOGRAPHY.md` holds each canonical
  PI-authored biography. Public profiles are checked against both. Every footer places its
  required links into the approved About and Open work groups.
- On September 15, the roster and selected public directory gained Disciple Dee
  Duplo with the exact PI-supplied biography and monogram `DDD`. The NFL Project
  was changed to Paused without altering its reports. The dialog runbook specified the
  coordinated canary that completed on September 16.
- On September 16, the first Git-backed superseded-report ledger recorded the
  exact outgoing v1 report commit. The operative archive policy now defines
  material changes, correction/retraction handling, retrieval, and validation
  without copying stale Quarto trees into the live website.
- Also on September 16, the immutable-dialog canary migrated `_template` and
  every existing Project together. The verifier checks filename/metadata
  agreement, bounded newest-first links, complete yearly indexes, and each
  recorded legacy SHA-256 digest. The ledger preserves the clean pre-canary
  report commit as a second superseded release.
- On September 17, the static-site group gained negative fixtures for missing
  or late bypass links and missing image `alt` attributes. All four generated
  Quarto report pages now use a source-controlled, runtime-relocated skip link
  at the start of the live document, and both NFL Full Report figures carry explicit
  alternatives. This is deterministic coverage, not a rendered accessibility
  certification.
- On September 18, `SUBSTANTIVE-REVIEW.md` traced the charter and each material
  v1 report-claim family to current or historical evidence. The internal review
  found no unsupported material claim, corrected a state timestamp that
  preceded its iteration finish, and leaves rendered accessibility as the sole
  open manual gate.
- On September 19, a text-browser review showed that Quarto report bypass links
  followed repeated navigation without JavaScript. All three report builds now
  use a tested, preflight-first post-render normalizer that makes the bypass link
  the first anchor in all four generated pages. The verifier rejects runtime
  relocation as a substitute, and `ACCESSIBILITY-REVIEW.md` defines the 11-page
  environment, procedure, evidence record, and passing rule for the open gate.
- On September 20, that evidence record became a structured 44-result worksheet.
  The verifier derives its required sample from current Published summaries
  and Full Report pages, rejects missing or duplicate rows and unknown result
  words, and prevents a **Closed** record with placeholders or non-passing
  cells. Three negative and positive fixtures guard the contract. This validates
  the record boundary, not rendered usability.
- On September 21, a negative fixture exposed a conjunction error in the static
  bypass check: an invalid first skip-styled anchor and a later valid bypass
  could previously satisfy two separately evaluated conditions. The parser now
  records the first anchor's target and requires that same anchor to target
  `main`. All current pages continue to pass; the rendered manual gate remains
  open.
- On September 22, the strengthened static check exposed 14 unnamed navigation
  landmarks across all four generated Quarto pages. The shared post-render
  normalizer now assigns stable names to the mobile report navigation, chapter
  sidebar, on-page contents, and previous/next chapter navigation. It validates
  every report `nav` before writing, and the whole-site verifier now rejects
  unnamed repeated navigation landmarks and missing `aria-labelledby` targets.
  Focused fixtures cover both the generated normalizer and generic page rule;
  rendered screen-reader review remains open.
- On September 23, the whole-site check exposed 60 generated report table
  headers without explicit scope. The shared post-render normalizer now adds
  column scope inside table heads and refuses any remaining missing or invalid
  header scope. The generic verifier enforces valid row or column scope across
  all public HTML. Two focused fixtures cover the generated and generic rules;
  rendered table navigation remains part of the open screen-reader review.
- On September 24, a whole-site interactive-element audit found all 501 exposed
  links and buttons named and all checked `aria-labelledby`, `aria-controls`,
  and `aria-expanded` relationships valid. The other 26 controls are Quarto
  source-line anchors hidden from assistive technology and explicitly removed
  from the tab order; the parser rejects a focusable hidden control. Two focused fixtures guard
  unnamed icon-only controls, empty or missing label targets, missing controlled
  targets, invalid expanded states, and hidden-control handling. Rendered name,
  role, state, focus order, and operation remain in the manual review.

This is a count of automated promise groups, not a Version 1 completion
declaration or a measure of research quality. Rendered keyboard and
assistive-technology review remains open.

## Verifier validity

The earlier six-group script was a useful regression check, but it did not
accurately certify Version 1. It omitted report formats, full biographies, and
the Projects directory. It also produced false failures by applying CSSERG
palette and motion rules to vendored Quarto libraries and by requiring exactly
one H1 on a multi-level Quarto book page.

The current verifier:

- adds a dedicated three-format report group;
- requires every page's first anchor itself to target `main` as a bypass and
  every image to carry an explicit `alt` attribute, and requires accessible
  names on repeated navigation landmarks and interactive elements, valid ARIA
  label/control/state relationships, and valid scope on table header cells,
  with negative fixtures for missing,
  late, wrong-target, misleading-first, and runtime-relocated bypasses, a
  missing image alternative, unnamed navigation or control, missing or empty
  label targets, missing controlled targets, invalid expanded state, unsafe
  hidden controls, and missing table-header scope;
- checks the Executive Summary figure count, report cross-links, Quarto source,
  PDF signature, and the required “far beyond” phrase;
- checks the Projects index and exact normalized charter biographies;
- checks lifecycle/update metadata, metadata-derived public order, the guarded
  Project scaffold, and the two selected production patterns;
- limits style assertions to first-party CSS and accepts one or more H1s;
- continues to verify local resources and required shared footer links on every
  HTML page, including generated reports.

These changes make the automated claims narrower and more valid. The script is
still a **promise regression report**, not a Version 1 completion oracle. See
`V1-RECOMMENDATIONS.md` for the full assessment.

## Manual review

- Execute `ACCESSIBILITY-REVIEW.md` across its 11 selected production pages at
  desktop and phone widths with keyboard and a recorded screen-reader pairing;
  complete all 44 page-level results and the environment record in place.

The substantive report review is complete. On September 18, a documented
internal review mapped the charter and material report claims to current or
historical evidence and found no unsupported material claim. It corrected a
state timestamp that preceded its iteration finish and explicitly limits the
finding to this infrastructure report—not the empirical validity of other
Projects or independent peer review. See `SUBSTANTIVE-REVIEW.md`.

The generic v1 verifier checks only each PDF signature. All three
Project-specific publication tests separately confirm nonempty pages, two-column
format, links, and the ten-page ceiling; visual legibility remains part of the
rendered review.

The September 13 pre-iteration expected-file probe found 73 of 109 production
files byte-identical, 10 different, and 26 unavailable. After the normal
automation published that iteration, the September 14 probe found all 109
expected files byte-identical, with none different or unavailable. The
September 15 pre-iteration probe reproduced that 109-of-109 result. That
iteration created a 110th file and changed public pages. Its runner log records
an iteration start and completion; inspection of the runner establishes that
completion is written only after the guarded deployment returns zero, while the
deployment can return zero only after its authenticated checksum dry run
reports no residual path. On September 16 the public probe then found all 110
expected files byte-identical, with none different or unavailable. Together
these observations close the deployment inventory and expected-byte gate for
the September 15 release. HTTP alone still cannot discover remote-only files,
so every new deployment must continue to pass the authenticated inventory
phase. Before the September 18 material revision, a new public probe found all
114 incoming files byte-identical. Before the September 19 revision, another
probe found all 128 incoming files byte-identical. Before the September 20
revision, all 134 incoming files were byte-identical. Before the September 21
revision, all 142 incoming files were byte-identical. Before the September 22
revision, all 150 incoming files were byte-identical. Before the September 23
revision, all 158 incoming files were byte-identical. Before the September 24
revision, all 166 incoming files were byte-identical; normal automation must
still deploy and inventory this revised release.

## Other current requirements

- The Project directory exists at `website/projects/index.html` and is ordered
  by authoritative `STATE.md` metadata. The verifier rejects stale timestamps,
  status labels, or order.
- Homepage copy now reads “Research Updates from Virtual CSSERG.” Primary
  headers contain internal Home/Projects/Scholars navigation; external CSSERG,
  PI, GitHub, and license links remain in footers.
- Executive Summary A and Scholar-directory A are production defaults by PI
  decision. Their two three-way comparison sets remain dated decision archives.
- All four Scholar profiles contain the complete canonical PI-authored
  biographies. `scholars.json` governs identity only; Project pairing is the
  runner invocation for one iteration.
- `_template` provides the three required memory files plus setup, reporting,
  branding, publication, lifecycle, and update-metadata guidance. A tested
  command creates a personalized no-overwrite scaffold without publishing it;
  the tested Scholar command creates identity, biography, and public catalog
  files as a guarded, rollback-on-error transaction without scheduling work. New
  scaffolds receive a fresh immutable-dialog tree rather than inheriting the
  template's migration archive.
- `REPORT-ARCHIVING.md` keeps canonical URLs current while preserving material
  supersessions by full public commit key. `REPORT-VERSIONS.md` applies it to
  the outgoing September 15 v1 release, whose three report forms are verified
  to exist at the recorded commit.
