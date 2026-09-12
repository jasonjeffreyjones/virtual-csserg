---
title: "Virtual CSSERG Version 1.0"
status: Active
updated: 2026-09-12T21:06:55Z
---

# VCSSERG v1 — Current State

## Status

Active. On September 12, 2026, all seven automated promise groups pass.
Version 1.0 is not complete because production parity, an observed Scholar
workflow, rendered accessibility/usability, and substantive review remain
manual gates.

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
  one-page, two-column PDF; and the production Executive Summary contains
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
- The Full Report publisher replaces a complete generated tree so stale Quarto
  libraries cannot survive; two unit tests cover replacement and preservation
  of the current public tree when a build is incomplete.
- `CREATING-PROJECTS-AND-SCHOLARS.md` documents the six approved lifecycle
  states, update semantics, Project creation/publication, review-led Scholar
  creation, and the approved provenance safeguards for generated illustrations.
  `_template` and the root README lead users to the process.
- The guarded deployment component and PI-owned Scholar runner pass structural
  and mocked checks. No credential, live deployment, commit, or push was used
  during this iteration; automation performs those after the Scholar finishes.

## Verifier assessment

`verify_v1.py` is a promise regression suite, not a Version 1 certification.
It checks repository guidance, project memory/metadata, static HTML/CSS and
local references, public catalogs/biographies/update order, three report forms,
runner wiring, and guarded deployment behavior.

All seven groups pass across 25 HTML pages and six first-party stylesheets.
The generic check does not validate PDF page layout, research quality,
production parity, rendered usability, or an observed automation run.
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
- The single append-only `DIALOG.md` remains operative until the approved
  immutable-per-iteration migration can update orientation, template, runner,
  active Projects, and verifier together.

## Current problems and manual gates

- Confirm production inventory and bytes equal `website/` after the normal
  commit/push/deploy sequence; witness one complete Scholar workflow.
- Inspect the selected layouts at desktop and phone widths with keyboard and
  assistive technology. No installed Chromium, Chrome, or Firefox executable is
  available on this host.
- Group footer links conceptually into About and Open work, define one durable
  Scholar roster/assignment source, and specify superseded-report archiving.
- Migrate dialog storage only as one coordinated workflow change.

## Resources and limitations

September 12 preflight: 2 logical CPUs, 3.7 GiB RAM, 4.0 GiB swap, and 65 GiB
free disk. Installed Python 3.12.3, R 4.3.3, Quarto 1.10.18, Pandoc, and
Ghostscript were usable. No TeX PDF engine or browser was installed. Existing
temporary build-only ReportLab/pypdf packages rendered and validated the PDFs;
they are not production dependencies. No package or system runtime was
installed or replaced in this iteration.

## Important files

- `V1-AUDIT.md`: current promise/evidence matrix and manual gates.
- `V1-RECOMMENDATIONS.md`: approved design/governance decisions and rollout.
- `CREATING-PROJECTS-AND-SCHOLARS.md`: growth and image-policy procedure.
- `verify_v1.py`: non-destructive promise regression suite.
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
- `python/vcsserg_deploy.py`: guarded deployment component.
- `run-scholar.sh`: PI-owned automation; Scholars must not edit it.

## Unresolved PI questions and likely next steps

No blocking PI question. The PI's chapter/page question is resolved: the
orientation specifies no exact count. Next, coordinate immutable dialog
storage, footer grouping, and Scholar assignment metadata, and complete the
production, workflow, browser, keyboard, accessibility, and substantive manual
gates before marking Version 1 Completed.
