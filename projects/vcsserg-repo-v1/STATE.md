---
title: "Virtual CSSERG Version 1.0"
status: Active
publication: Published
updated: 2026-09-16T21:16:54Z
---

# VCSSERG v1 — Current State

## Status

Active. On September 16, 2026, all seven automated promise groups pass across
26 HTML pages and six first-party stylesheets. The September 15 normal Scholar
run reached completion only after its guarded deployment and authenticated
inventory phase returned successfully; today's public probe then found all 110
expected files byte-identical. This closes the deployment gate and observes the
successful workflow path for that release. The PI-triggered canary also
completed the coordinated immutable-dialog migration across `_template` and
all four Projects. Controlled runner tests now witness dirty-start refusal plus
Scholar and validation failures without commit, push, or deployment. Version 1.0 is not
complete; keyboard/assistive-technology and substantive review remain open.

## Completed work and current evidence

- Every Project and `_template` has `PROJECT.md`, `STATE.md`, and `DIALOG.md`.
  State front matter supplies authoritative `title`, lifecycle `status`,
  independent `publication`, and substantive `updated` metadata. Active work
  may remain Unpublished; public catalogs and three-report requirements apply
  only to Published Projects.
- Every `DIALOG.md` is now a bounded landing page. New Scholar work uses one
  immutable timestamped file under `dialog/iterations/`, complete yearly
  indexes, PI blockquote replies to specific records, and a bounded reading
  rule. All five prior dialogs are byte-preserved under `dialog/legacy/` with
  verified SHA-256 digests. The tested standard-library migration command
  dry-runs by default, refuses overwrite, and preflights the whole Project set.
- The public homepage and Projects directory link all three Published
  Projects, while the Scholar directory links four rostered Scholars. The three
  initial profiles contain the
  complete charter biographies; Disciple Dee Duplo's profile contains the exact
  PI-supplied biography. Primary headers use internal navigation; branded
  footers retain PI, CSSERG, GitHub, and CC BY 4.0 links.
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
  validates lowercase hyphenated slugs, refuses overwrite, and initializes a
  clean immutable-dialog tree instead of copying the template's migration
  archive. Four unit tests cover personalization, completeness, unsafe inputs,
  and immutability on a repeated request.
- `scholars.json` is the identity source for Scholar names, permanent slugs,
  and monograms. Canonical PI-authored biographies live under `scholars/`.
  `python/create_scholar.py` validates and installs an identity as a guarded,
  rollback-on-error transaction: canonical
  biography, profile, homepage link, and directory card without scheduling
  work. Scholar–Project pairing lasts for one runner invocation and is recorded
  by the resulting immutable iteration, not as durable roster state.
- Every public HTML footer now groups Dr. Jones and CSSERG under **About**, and
  GitHub and CC BY 4.0 under **Open work**. The system is synchronized across
  direct HTML, all three Quarto footer sources/generated reports, and archived
  design pages; the verifier rejects missing groups and misplaced links.
- The Full Report publisher replaces a complete generated tree so stale Quarto
  libraries cannot survive; two unit tests cover replacement and preservation
  of the current public tree when a build is incomplete.
- `CREATING-PROJECTS-AND-SCHOLARS.md` documents the six approved lifecycle
  states, update semantics, Project creation/publication, command-driven Scholar
  creation, Project pause/resume, and the approved provenance safeguards for
  generated illustrations. `_template` and the root README lead users to the
  process.
- `REPORT-ARCHIVING.md` now defines a Git-backed policy for material report
  supersession, correction, and retraction. Canonical URLs remain current while
  a full commit key preserves the outgoing three-form report, dependencies,
  sources, and Project record. `REPORT-VERSIONS.md` records the September 15 v1
  release and the September 16 pre-canary report set; the verifier confirms all
  three forms exist at both commits.
- NFL Team Fandom Identities records the PI-directed Paused lifecycle state in
  its state, dialog, public summary, Projects listing, and homepage. Its
  findings and reports remain Published; the PI confirms no Scholar schedules
  are currently enabled.
- `DIALOG-MIGRATION.md` records the completed coordinated change: PI runner
  trigger, canary, all-Project Scholar migration, legacy-byte preservation, PI
  reply convention, bounded 20-entry landing index with complete yearly
  indexes, and exact reading expectations.
- The standard-library public parity probe compares every expected website file
  byte without credentials. September 14 and September 15 pre-iteration runs
  found all 109 then-expected files identical, improving on the September 13
  result of 73 identical, 10 different, and 26 unavailable. The September 16
  run found all 110 expected files identical after the normal deployment. HTTP
  cannot discover remote-only files by itself.
- The Scholar runner now takes stable Scholar and Project slugs, refuses a dirty
  tree, validates the identity and Active Project, and independently runs the
  roster, registry, routine v1 tests, verifier, whitespace, and syntax gates
  before any
  commit, push, or deployment. It also rejects changes to the PI-owned runner.
  The separately invoked runner integration suite uses isolated command fakes
  to exercise dirty-start refusal, status-inspection
  failure, prohibited runner edits, Scholar failure, validation failure, and
  successful operation ordering without external effects. It is excluded from
  nested routine validation because a live runner already holds the iteration
  lock. The guarded deployment follows its
  deleting transfer with an authenticated recursive checksum/inventory dry run
  and exits nonzero on any residual
  missing, changed, or extra path. Mocked success, detected drift, subprocess
  failure, missing rsync, invalid port, and unsafe path behavior pass. The
  PI-owned Scholar runner was changed under direct PI authorization.

## Verifier assessment

`verify_v1.py` is a promise regression suite, not a Version 1 certification.
It checks repository guidance, project memory/metadata, static HTML/CSS and
local references, public catalogs/biographies/update order, three report forms,
runner wiring, and guarded deployment behavior.

All seven groups pass across 26 HTML pages and six first-party stylesheets.
The checks now include validated identity/biography data, independent Project
lifecycle/publication state, footer-link group placement,
iteration filename/metadata agreement, bounded recent links, complete yearly
indexes, and legacy-dialog digests.
The generic check does not validate PDF page layout, research quality, public
network state, rendered usability, or an observed automation run. The separate
network probe checks expected bytes but not unexpected remote files. For the
September 15 release, the runner's completion marker establishes that the live
deployment's fail-closed inventory phase returned without residual paths; the
September 16 network probe establishes all expected bytes. Project-specific
publication verifiers continue to cover stronger PDF properties.
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
- Project scaffolding uses the validated no-overwrite command and initializes
  `publication: Unpublished`. Publication is a separate substantive gate; only
  the PI authors the charter.
- `scholars.json` governs identity data and canonical biographies remain
  PI-authored files. Scholar creation is command-driven but still begins with
  PI-supplied name, slug, monogram, and biography.
- A runner invocation pairs any rostered Scholar with one Active Project for
  that iteration. No durable assignment or reassignment record is maintained.
- Pausing preserves evidence and publication unless the PI separately directs
  retraction or archiving. A Paused Project cannot be invoked by the runner.
- Footer links use two semantic groups everywhere: About (PI, CSSERG) and Open
  work (GitHub, license).
- Canonical report URLs show current evidence. A material supersession records
  the clean outgoing commit in a Project release ledger; corrections and
  retractions preserve history and add current notices. Cosmetic maintenance
  remains recoverable through ordinary Git history.
- Immutable-per-iteration dialog is operative across the repository. Scholars
  read the bounded landing index, all active PI guidance and unresolved-question
  records, the newest three records, their own most recent record, and cited
  older material when needed—not the entire corpus. Only the PI appends
  blockquotes to earlier records; Scholars never alter earlier authored text.

## Current problems and manual gates

- Inspect the selected layouts at desktop and phone widths with keyboard and
  assistive technology. No installed Chromium, Chrome, or Firefox executable is
  available on this host.
- Dr. Jones reported that the production pages and PDFs look acceptable. A
  keyboard/assistive-technology pass and substantive report review remain.

## Resources and limitations

September 16 preflight: 2 logical CPUs, 3.7 GiB RAM, 4.0 GiB swap, and 65 GiB
free disk. Installed Python 3.12.3, R 4.3.3, Quarto 1.10.18, Pandoc, and
rsync 3.2.7 are available. No Chromium, Chrome, or Firefox executable was found.
ReportLab/pypdf are not installed in the base Python environment; any PDF build
uses the documented temporary build-only packages, not production dependencies.
No system runtime was installed or replaced in this iteration.

## Important files

- `V1-AUDIT.md`: current promise/evidence matrix and manual gates.
- `V1-RECOMMENDATIONS.md`: approved design/governance decisions and rollout.
- `DIALOG-MIGRATION.md`: exact PI trigger, Scholar migration plan, reply
  protocol, legacy hashes, completion evidence, and bounded-reading rule.
- `python/migrate_dialogs.py`: dry-run-first, no-overwrite, whole-set migration
  command; fixture tests cover preservation and preflight failure.
- `CREATING-PROJECTS-AND-SCHOLARS.md`: growth and image-policy procedure.
- `REPORT-ARCHIVING.md` and `REPORT-VERSIONS.md`: supersession policy and the
  v1 release ledger.
- `verify_v1.py`: non-destructive promise regression suite.
- `scholars.json`, `scholars/`, `python/create_scholar.py`, and
  `python/scholar_roster.py`: identity data, canonical biographies, guarded
  creation, and read-only validation.
- `analysis/check_production_parity.py`: credential-free expected-file byte
  comparison for use after deployment; not a remote-inventory tool.
- `index.qmd`, `_quarto.yml`, `short-report.md`, `BUILD.md`: report sources and
  reproduction instructions.
- `analysis/publish_full_report.py`, `analysis/render_short_report.py`, and
  `analysis/verify_publication.py`: guarded HTML publication, PDF build, and
  project publication checks.
- `python/create_project.py`: validated, atomic, unpublished Project scaffold.
- `python/project_registry.py`: lifecycle/publication validation and Active
  Project resolution for the runner.
- `projects/predict-the-self/BUILD.md`, `_quarto.yml`, publication scripts, and
  current `STATE.md`: the conformed handoff for its next Scholar iteration.
- `website/projects/vcsserg-repo-v1/`: Executive Summary, Full Report, short
  report, and design-decision archives.
- `website/scholars/index.html`: selected production portrait roster.
- `python/vcsserg_deploy.py`: guarded transfer plus fail-closed remote checksum
  and inventory verification.
- `run-scholar.sh`: PI-owned automation; Scholars must not edit it.

## Unresolved PI questions and likely next steps

No blocking PI question. Controlled runner failure paths now pass without
commit, push, or deployment, and the PI confirms no schedules are enabled.
Next complete keyboard/assistive-technology and substantive review.
