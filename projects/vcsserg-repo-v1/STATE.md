---
title: "Virtual CSSERG Version 1.0"
status: Active
updated: 2026-09-14T08:09:07Z
---

# VCSSERG v1 — Current State

## Status

Active. On September 14, 2026, all seven automated promise groups pass and all
109 expected production files are byte-identical to the pre-iteration checkout.
Version 1.0 is not complete. The new authenticated remote-inventory check still
needs an observed deployment; a witnessed Scholar workflow, rendered
accessibility/usability, and substantive review also remain open.

## Completed work and current evidence

- Every Project and `_template` has `PROJECT.md`, `STATE.md`, and `DIALOG.md`.
  State front matter now supplies authoritative `title`, lifecycle `status`, and
  substantive `updated` metadata. The Projects page order and timestamps are
  verified against those records.
- The public homepage, Projects directory, and Scholar directory link all three
  Projects and initial Scholars. Profiles contain the complete charter
  biographies. Primary headers use internal navigation; branded footers retain
  PI, CSSERG, GitHub, and CC BY 4.0 links.
- Dr. Jones selected Executive Summary A and Scholar-directory A. Production
  now uses the evidence brief (question, status, one figure, linked findings)
  and portrait roster (equal monogram cards and authoritative profile links).
  The alternatives are labeled as dated decision archives.
- VCSSERG v1 now has all three linked report forms: `index.qmd` currently
  renders a one-chapter Quarto HTML book; `short-report.md` currently renders a
  two-page, two-column PDF; and the production Executive Summary contains
  exactly one dense promise-map figure and five Full Report-linked findings.
  Neither one chapter nor one page is a requirement; Full Report structure is
  content-driven and the short PDF has a ten-page ceiling.
- Predict the Self now conforms to the same current publication system. It has
  a two-chapter Quarto book, guarded complete-tree publisher, one-figure
  evidence brief, linked short PDF, build guide, five tests, and a project
  publication verifier. Its empirical claims and frozen test artifact were not
  changed during this structural adaptation.
- `python/create_project.py` atomically creates a personalized private scaffold,
  validates lowercase hyphenated slugs, and refuses overwrite. Four unit tests
  cover personalization, completeness, unsafe inputs, and immutability on a
  repeated request.
- `scholars.json` is the single operational source for Scholar names, permanent
  slugs, monograms, and current Project assignments. The read-only
  `python/scholar_roster.py` validator rejects malformed records, duplicates,
  and unknown Projects. The v1 verifier checks homepage/directory membership,
  profile monograms, assignment targets, and assignment titles against it;
  PI-authored charters/dialog remain authoritative for biographies.
- Every public HTML footer now groups Dr. Jones and CSSERG under **About**, and
  GitHub and CC BY 4.0 under **Open work**. The system is synchronized across
  direct HTML, all three Quarto footer sources/generated reports, and archived
  design pages; the verifier rejects missing groups and misplaced links.
- The Full Report publisher replaces a complete generated tree so stale Quarto
  libraries cannot survive; two unit tests cover replacement and preservation
  of the current public tree when a build is incomplete.
- `CREATING-PROJECTS-AND-SCHOLARS.md` documents the six approved lifecycle
  states, update semantics, Project creation/publication, review-led Scholar
  creation, and the approved provenance safeguards for generated illustrations.
  `_template` and the root README lead users to the process.
- The standard-library public parity probe compares every expected website file
  byte without credentials. The September 14 post-deployment run found all 109
  expected files identical, improving on the September 13 pre-deployment result
  of 73 identical, 10 different, and 26 unavailable. HTTP cannot discover
  remote-only files.
- The guarded deployment now follows its deleting transfer with an authenticated
  recursive checksum/inventory dry run and exits nonzero on any residual
  missing, changed, or extra path. Mocked success, detected drift, subprocess
  failure, missing rsync, invalid port, and unsafe path behavior pass. The
  PI-owned Scholar runner remains unchanged.

## Verifier assessment

`verify_v1.py` is a promise regression suite, not a Version 1 certification.
It checks repository guidance, project memory/metadata, static HTML/CSS and
local references, public catalogs/biographies/update order, three report forms,
runner wiring, and guarded deployment behavior.

All seven groups pass across 25 HTML pages and six first-party stylesheets.
The checks now include validated roster/assignment data and exact footer-link
group placement.
The generic check does not validate PDF page layout, research quality, public
network state, rendered usability, or an observed automation run. The separate
network probe checks expected bytes but not unexpected remote files; the mocked
deployment check validates the new inventory phase's commands and fail-closed
behavior but does not constitute a live run.
Project-specific publication verifiers for VCSSERG v1 and Predict the Self do
validate reciprocal report links, one summary figure, phrase count, PDF links,
both PDF columns, nonempty pages, and the ten-page ceiling.

## Decisions currently in force

- Quarto HTML books are the default Full Report; direct HTML is a documented
  runtime contingency.
- Project lifecycle states are Proposed, Active, Blocked, Paused, Completed,
  and Archived. Publication readiness is separate. A state change records who,
  when, and why; completion requires automated and named manual gates.
- Monograms are the default Scholar representation. Generated illustrations
  must be non-photographic, provenance-recorded, non-biographical, accessible,
  and selected by the PI before becoming canonical.
- Project scaffolding uses the validated no-overwrite command. Publication is a
  separate substantive gate; only the PI authors the charter.
- `scholars.json` governs operational roster and current assignments;
  biographies remain grounded in PI-authored records. Scholar creation stays
  review-led even though the data source is now specified.
- Footer links use two semantic groups everywhere: About (PI, CSSERG) and Open
  work (GitHub, license).
- The single append-only `DIALOG.md` remains operative until the approved
  immutable-per-iteration migration can update orientation, template, runner,
  active Projects, and verifier together.

## Current problems and manual gates

- Observe the next normal deployment's checksum/inventory dry run complete with
  no missing, changed, or remote-only paths; then re-run the public byte probe
  against the new checkout.
- Witness one complete Scholar workflow, including success and failure paths.
- Inspect the selected layouts at desktop and phone widths with keyboard and
  assistive technology. No installed Chromium, Chrome, or Firefox executable is
  available on this host.
- Specify superseded-report archiving.
- Migrate dialog storage only as one coordinated workflow change.

## Resources and limitations

September 14 preflight: 2 logical CPUs, 3.7 GiB RAM, 4.0 GiB swap, and 65 GiB
free disk. Installed Python 3.12.3, R 4.3.3, Quarto 1.10.18, Pandoc, and
rsync 3.2.7 were usable. No Chromium, Chrome, or Firefox executable was found.
Existing temporary build-only ReportLab/pypdf packages rendered and validated
the two-page v1 PDF; they are not production dependencies. No package or system
runtime was installed or replaced in this iteration.

## Important files

- `V1-AUDIT.md`: current promise/evidence matrix and manual gates.
- `V1-RECOMMENDATIONS.md`: approved design/governance decisions and rollout.
- `CREATING-PROJECTS-AND-SCHOLARS.md`: growth and image-policy procedure.
- `verify_v1.py`: non-destructive promise regression suite.
- `scholars.json` and `python/scholar_roster.py`: authoritative operational
  Scholar roster/assignment data and its read-only validator.
- `analysis/check_production_parity.py`: credential-free expected-file byte
  comparison for use after deployment; not a remote-inventory tool.
- `index.qmd`, `_quarto.yml`, `short-report.md`, `BUILD.md`: report sources and
  reproduction instructions.
- `analysis/publish_full_report.py`, `analysis/render_short_report.py`, and
  `analysis/verify_publication.py`: guarded HTML publication, PDF build, and
  project publication checks.
- `python/create_project.py`: validated, atomic, unpublished Project scaffold.
- `projects/predict-the-self/BUILD.md`, `_quarto.yml`, publication scripts, and
  current `STATE.md`: the conformed handoff for its next Scholar iteration.
- `website/projects/vcsserg-repo-v1/`: Executive Summary, Full Report, short
  report, and design-decision archives.
- `website/scholars/index.html`: selected production portrait roster.
- `python/vcsserg_deploy.py`: guarded transfer plus fail-closed remote checksum
  and inventory verification.
- `run-scholar.sh`: PI-owned automation; Scholars must not edit it.

## Unresolved PI questions and likely next steps

No blocking PI question. Next, confirm the new deployment-side inventory phase
in the post-iteration result, re-run expected-byte parity, witness a complete
workflow and its failure path, perform browser/keyboard/assistive-technology and
substantive review, and define superseded-report archiving. The immutable-dialog
migration still requires a coordinated PI change because Scholars may not edit
the runner.
