# VCSSERG Version 1.0 Audit

This is a point-in-time map from documented promises to observable evidence. It
separates verified behavior from assumptions so “works as documented” remains a
testable goal.

Run the non-destructive automated portion from the repository root:

```bash
python3 projects/vcsserg-repo-v1/verify_v1.py
```

The verifier does not read `.env`, contact remote systems, create commits, or
deploy. It returns nonzero while an automated group fails. A passing run would
still not establish the manual gates below.

## Evidence matrix

| Documented promise | Evidence or test | Status on September 16, 2026 |
|---|---|---|
| Repository guidance and growth procedure exist | Required top-level files, creation guide, tested Project scaffold, validated Scholar roster | Automated pass |
| Every Project uses current memory and metadata | `PROJECT.md`, `STATE.md`, bounded `DIALOG.md`, immutable iteration/year indexes, legacy hashes where applicable, plus `title`, `status`, `updated`, including `_template` | Automated pass; all five pre-migration dialogs are byte-preserved |
| Public static site is branded and locally connected | First-party HTML/CSS semantics, local paths/fragments, Bootstrap CDN, logo, grouped required footer | Automated pass across 26 HTML pages and 6 first-party stylesheets |
| Publication-eligible Projects and Scholars are findable and correctly assigned | `scholars.json`, home, Projects index, Scholar index, profiles, assignment links, PI-authored biographies | Automated pass; Proposed scaffolds remain private |
| Every publication-eligible Project has all three linked report formats | Executive Summary with exactly one figure, Quarto source/book, Full Report, short PDF, cross-links and required phrase | Automated pass |
| Scholar runner wires the documented lifecycle | Syntax and static command/path checks | Automated pass; not executed end to end |
| Deployment safely mirrors `website/` | Mocked guarded transfer plus checksum/inventory dry run; completed normal workflow; public expected-file probe | Pass; the September 15 run reached completion only after exact-inventory verification, and all 110 expected files matched production on September 16 |

## Current automated result

On September 16, 2026, **all seven groups pass**. The final report-format gap
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
- On September 13, `scholars.json` became the validated operational source for
  roster, slug, monogram, and current-assignment data. Public profiles are
  checked against it and Project title metadata. Every footer now places its
  required links into the approved About and Open work groups.
- On September 15, the roster and selected public directory gained Disciple Dee
  Duplo with the exact PI-supplied biography, monogram `DDD`, and no invented
  Project assignment. The NFL Project was changed to Paused without altering
  its reports or Aleph's assignment. The dialog runbook specified the
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

This is a count of automated promise groups, not a Version 1 completion
declaration or a measure of research quality. The manual gates remain open.

## Verifier validity

The earlier six-group script was a useful regression check, but it did not
accurately certify Version 1. It omitted report formats, full biographies, and
the Projects directory. It also produced false failures by applying CSSERG
palette and motion rules to vendored Quarto libraries and by requiring exactly
one H1 on a multi-level Quarto book page.

The current verifier:

- adds a dedicated three-format report group;
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

## Manual gates

- Exercise and witness the Scholar workflow's safe failure path. The September
  15 normal run records start and completion; by control flow, completion occurs
  only after commit, push, deployment, and an empty authenticated inventory
  check all succeed.
- Inspect the selected layouts at desktop and phone widths with keyboard and
  assistive-technology checks.
- Review substantive report completeness and research validity. File existence
  and links cannot establish either.

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
phase.

## Other current requirements

- The Project directory exists at `website/projects/index.html` and is ordered
  by authoritative `STATE.md` metadata. The verifier rejects stale timestamps,
  status labels, or order.
- Homepage copy now reads “Research Updates from Virtual CSSERG.” Primary
  headers contain internal Home/Projects/Scholars navigation; external CSSERG,
  PI, GitHub, and license links remain in footers.
- Executive Summary A and Scholar-directory A are production defaults by PI
  decision. Their two three-way comparison sets remain dated decision archives.
- All three initial Scholar profiles contain the complete charter biographies,
  and Disciple Dee Duplo's profile contains the complete biography supplied in
  PI dialog. `scholars.json` separately governs the four-member operational
  roster and three assignments.
- `_template` provides the three required memory files plus setup, reporting,
  branding, publication, lifecycle, and update-metadata guidance. A tested
  command creates a personalized no-overwrite scaffold without publishing it;
  the creation guide also documents the review-led Scholar procedure. New
  scaffolds receive a fresh immutable-dialog tree rather than inheriting the
  template's migration archive.
- `REPORT-ARCHIVING.md` keeps canonical URLs current while preserving material
  supersessions by full public commit key. `REPORT-VERSIONS.md` applies it to
  the outgoing September 15 v1 release, whose three report forms are verified
  to exist at the recorded commit.
