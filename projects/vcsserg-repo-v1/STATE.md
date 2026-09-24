---
title: "Virtual CSSERG Version 1.0"
status: Active
publication: Published
updated: 2026-09-24T08:15:10Z
---

# VCSSERG v1 — Current State

## Status

Active. On September 24, 2026, all seven automated promise groups pass across
26 HTML pages, 527 links and buttons, and six first-party stylesheets. The
static-site group requires
the first anchor itself to be a bypass link targeting `main`, an explicit `alt`
decision for every image, and an accessible name for every navigation landmark
on pages containing more than one. It also requires every table header cell to
declare a valid row or column scope, every exposed interactive element to have an
accessible name, label/control references to resolve, expanded states to be
boolean, and assistive-technology-hidden controls to be absent from the tab
order. A tested post-render normalizer makes the
bypass link first, names Quarto's repeated navigation regions, and adds column
scope inside generated table heads on all four report pages without runtime
JavaScript or hand-editing. The
September 15 normal Scholar
run reached completion only after its guarded deployment and authenticated
inventory phase returned successfully; the September 16 public probe then found all 110
expected files byte-identical. This closes the deployment gate and observes the
successful workflow path for that release. The PI-triggered canary also
completed the coordinated immutable-dialog migration across `_template` and
all four Projects. Controlled runner tests now witness dirty-start refusal plus
Scholar and validation failures without commit, push, or deployment. Version 1.0 is not
complete: a September 18 claim-to-evidence review closes the substantive report
gate, while rendered desktop/phone keyboard and assistive-technology review
remains open under the explicit `ACCESSIBILITY-REVIEW.md` protocol. Its
11-page, 44-result worksheet and environment record are now machine-checked so
an incomplete record cannot be marked **Closed**; this guards evidence capture
without performing the unavailable human review.

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
- `SUBSTANTIVE-REVIEW.md` maps every charter deliverable and material v1 report
  claim family to current or historical evidence. The internal review found no
  unsupported material claim, explicitly excludes other Projects' empirical
  validity and independent peer review, and leaves rendered accessibility
  open. It also found that the outgoing state timestamp preceded its iteration
  finish by 2 minutes 46 seconds; this iteration restores the documented exact
  finish-time convention in both state and public catalog.
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
- Every public HTML page now exposes a first-anchor bypass link, and every image
  has an explicit `alt` attribute (including empty alternatives for decorative
  images). The verifier records the first anchor's own target and requires that
  target to identify `main`; it no longer lets an invalid first skip-styled link
  borrow validity from a later bypass. It also requires accessible names on
  repeated navigation landmarks and resolves `aria-labelledby` targets. This
  exposed 14 unnamed Quarto navigation regions across the four generated report
  pages. The September 23 rule then exposed 60 unscoped headers in the three
  table-bearing generated report pages. Their shared standard-library
  post-render normalizer now preflights the whole output tree, moves the bypass
  before repeated navigation, validates its `main` target, labels Quarto's
  report/chapter/on-page/previous-next navigation, assigns `scope="col"` inside
  table heads, and refuses unknown navigation or invalid remaining header scope
  before writing. Five focused normalizer tests cover promotion, names, header
  scopes, idempotence, and failure without partial mutation; generic fixtures
  cover missing landmark names, label targets, and invalid header scope. A
  September 24 audit then found all 501 assistive-technology-exposed links and
  buttons named with valid checked `aria-labelledby`, `aria-controls`, and
  `aria-expanded` relationships; the other 26 are Quarto source-line anchors
  explicitly hidden and removed from the tab order. The parser rejects a
  focusable hidden control. Two focused fixtures cover unnamed icon-only
  controls, empty/missing labels, broken control targets, invalid expanded
  state, and hidden-control handling. The verifier no longer accepts runtime
  JavaScript relocation. The two NFL report
  figures retain detailed alternatives after rendering. These static checks do
  not replace rendered keyboard or assistive-technology review.
- `ACCESSIBILITY-REVIEW.md` defines the last manual gate's 11 production pages,
  desktop and 320-CSS-pixel conditions, keyboard/focus, reflow, screen-reader
  checks, structured environment record, 44 result cells, and passing rule.
  The verifier derives the sample from current Published summaries and Full
  Reports, rejects missing/duplicate rows and unknown result words, and refuses
  closed records with placeholders or non-passing cells. Three tests cover
  current coverage, malformed rows, and incomplete versus complete closure. A
  supplemental `w3m` 0.5.3 pass
  returned zero at 40 and 120 columns for every selected page and showed “Skip
  to content” first. It is linearized text evidence, not a graphical-browser or
  screen-reader pass.
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
  sources, and Project record. `REPORT-VERSIONS.md` records material outgoing
  releases from September 15 through the clean September 22 report set; the
  verifier confirms all three forms exist at each recorded commit.
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
  run found all 110 expected files identical after the normal deployment. The
  September 18 pre-change probe found all 114 incoming files byte-identical, and
  the September 19 pre-change probe found all 128 incoming files byte-identical,
  the September 20 pre-change probe found all 134 incoming files byte-identical,
  and the September 21 pre-change probe found all 142 incoming files
  byte-identical. The September 22 pre-change probe found all 150 incoming files
  byte-identical, and the September 23 pre-change probe found all 158 incoming
  files byte-identical. The September 24 pre-change probe found all 166 incoming
  files byte-identical.
  HTTP cannot discover remote-only files by itself, and the latest result does
  not substitute for deploying and inventorying this revised release.
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

All seven groups and all 39 routine tests pass across 26 HTML pages, 527 links
and buttons, and six first-party stylesheets on September 24.
The checks now include validated identity/biography data, independent Project
lifecycle/publication state, footer-link group placement,
iteration filename/metadata agreement, bounded recent links, complete yearly
indexes, legacy-dialog digests, first-anchor bypass mechanisms, explicit image
alternatives, repeated navigation names, resolved landmark-label references,
valid table-header scopes, interactive names and ARIA relationships, and the
manual-review worksheet's sample and closure boundary. One focused negative
test guards the first-anchor/target conjunction, five tests cover the build-time
Quarto normalizer, one covers the generic navigation-name rule, one covers the
generic table-header rule, two cover interactive names and ARIA relationships,
and three cover the manual-review record.
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
The verifier also enforces state-to-catalog timestamp agreement but cannot
infer whether a human correctly classified an iteration as substantive; the
September 18 review found and corrected one such timestamp decision.

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

- Follow `ACCESSIBILITY-REVIEW.md` on a browser-equipped host: inspect all 11
  selected production pages at desktop and phone widths with keyboard and a
  recorded screen-reader pairing, complete all 44 result cells and environment
  fields, and close the record only after every result passes. No installed
  Chromium, Chrome, or Firefox executable or supported screen-reader/browser
  pairing is available on this host.
- Dr. Jones reported that the production pages and PDFs look acceptable. The
  keyboard/assistive-technology pass remains the sole open manual gate.

## Resources and limitations

September 24 preflight: 2 logical CPUs, 3.7 GiB RAM, 4.0 GiB swap, and 65 GiB
free disk. Installed Python 3.12.3, R 4.3.3, Quarto 1.10.18, Pandoc, and
rsync 3.2.7 are available. `w3m` 0.5.3 is available; no Chromium, Chrome, or
Firefox executable or supported screen-reader/browser pairing was found.
ReportLab/pypdf are not installed in the base Python environment; any PDF build
uses the existing documented temporary build-only packages, not production
dependencies. No package or replacement runtime was installed in this iteration.

## Important files

- `V1-AUDIT.md`: current promise/evidence matrix and manual gates.
- `ACCESSIBILITY-REVIEW.md`: derived selected-page worksheet, environment
  record, keyboard/reflow/screen-reader procedure, and guarded passing rule for
  the open gate.
- `SUBSTANTIVE-REVIEW.md`: charter coverage, material claim-to-evidence matrix,
  review boundaries, the timestamp correction, and reproduction evidence.
- `V1-RECOMMENDATIONS.md`: approved design/governance decisions and rollout.
- `DIALOG-MIGRATION.md`: exact PI trigger, Scholar migration plan, reply
  protocol, legacy hashes, completion evidence, and bounded-reading rule.
- `python/migrate_dialogs.py`: dry-run-first, no-overwrite, whole-set migration
  command; fixture tests cover preservation and preflight failure.
- `CREATING-PROJECTS-AND-SCHOLARS.md`: growth and image-policy procedure.
- `REPORT-ARCHIVING.md` and `REPORT-VERSIONS.md`: supersession policy and the
  v1 release ledger, including the clean September 23 report set superseded by
  this interactive-element contract.
- `verify_v1.py`: non-destructive promise regression suite.
- `python/promote_report_skip_links.py`: tested, preflight-first Quarto
  post-render normalizer that makes bypass links first and names repeated
  navigation landmarks and scopes table-head cells in static HTML.
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
Next execute `ACCESSIBILITY-REVIEW.md` on a browser/screen-reader-equipped host,
record the environment and all 44 page-level results, repair and retest any
failure, and then assess the charter and PI authority before changing lifecycle
state.
