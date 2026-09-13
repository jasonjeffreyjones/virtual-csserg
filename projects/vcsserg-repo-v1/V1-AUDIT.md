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

| Documented promise | Evidence or test | Status on September 13, 2026 |
|---|---|---|
| Repository guidance and growth procedure exist | Required top-level files, creation guide, tested Project scaffold, validated Scholar roster | Automated pass |
| Every Project uses current memory and metadata | `PROJECT.md`, `STATE.md`, `DIALOG.md`, plus `title`, `status`, `updated`, including `_template` | Automated pass; Predict the Self migration preserves legacy records |
| Public static site is branded and locally connected | First-party HTML/CSS semantics, local paths/fragments, Bootstrap CDN, logo, grouped required footer | Automated pass across 25 HTML pages and 6 first-party stylesheets |
| Projects and Scholars are findable and correctly assigned | `scholars.json`, home, Projects index, Scholar index, profiles, assignment links, charter biographies | Automated pass |
| Every Project has all three linked report formats | Executive Summary with exactly one figure, Quarto source/book, Full Report, short PDF, cross-links and required phrase | Automated pass |
| Scholar runner wires the documented lifecycle | Syntax and static command/path checks | Automated pass; not executed end to end |
| Deployment safely mirrors `website/` | Mocked guarded, shell-free `rsync`, deletion and error propagation | Automated pass; live parity unverified |

## Current automated result

On September 13, 2026, **all seven groups pass**. The final report-format gap
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

- Confirm production file inventory and bytes exactly match `website/` after
  the normal commit, push, and deploy sequence.
- Observe one complete successful Scholar workflow, including logging and
  failure behavior.
- Inspect the selected layouts at desktop and phone widths with keyboard and
  assistive-technology checks.
- Review substantive report completeness and research validity. File existence
  and links cannot establish either.
- Confirm short reports use two columns and remain at or under 10 pages. The
  generic v1 verifier checks only the PDF signature; project publication tests
  may enforce stronger PDF properties.

The September 13 pre-iteration expected-file probe found production was not
current with the repository checkout: of 109 expected files, 73 were
byte-identical, 10 differed, and 26 returned HTTP 404. The unavailable files
were the newly published Predict the Self short PDF and most of its Quarto book
tree; several v1 files also differed. This observation does not establish why
deployment lagged. Re-run
`analysis/check_production_parity.py` after this iteration's normal deployment.
The probe compares all expected bytes without credentials but cannot discover
extra stale production files, so complete remote inventory remains open.

## Other current requirements

- The Project directory exists at `website/projects/index.html` and is ordered
  by authoritative `STATE.md` metadata: VCSSERG v1, NFL Team Fandom Identities,
  then Predict the Self. The verifier rejects stale timestamps or order.
- Homepage copy now reads “Research Updates from Virtual CSSERG.” Primary
  headers contain internal Home/Projects/Scholars navigation; external CSSERG,
  PI, GitHub, and license links remain in footers.
- Executive Summary A and Scholar-directory A are production defaults by PI
  decision. Their two three-way comparison sets remain dated decision archives.
- All three initial Scholar profiles now contain the complete biographies
  supplied in the charter. `scholars.json` separately governs the operational
  roster and assignments.
- `_template` provides the three required memory files plus setup, reporting,
  branding, publication, lifecycle, and update-metadata guidance. A tested
  command creates a personalized no-overwrite scaffold without publishing it;
  the creation guide also documents the review-led Scholar procedure.
