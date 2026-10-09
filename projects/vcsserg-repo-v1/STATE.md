---
title: "Virtual CSSERG Version 1.0"
status: Active
publication: Published
updated: 2026-10-09T08:12:39Z
---

# VCSSERG v1 — Current State

## Status

Active. On October 9, 2026, all seven automated promise groups pass across
39 HTML pages, 160 named navigation landmarks, 97 native images, four exposed ARIA images, 38 named data tables,
204 exposed headings, 846 interactive or keyboard-focusable elements, and
seven first-party stylesheets. All four exposed ARIA images and all 820
exposed interactive elements are named and the other 26 are safely hidden
Quarto source-line anchors. The
static-site group requires
exactly one page-level banner, main, and content-information landmark; the
page to declare one `width=device-width` viewport without disabling scaling or
setting a nonnegative maximum scale below 2; no page to reload or redirect
automatically through `meta http-equiv="refresh"`; the
first anchor itself to be a bypass link targeting `main`; an explicit `alt`
decision for every native image; an accessible name for every exposed
non-native ARIA image; and an accessible name for every navigation landmark
on pages containing more than one. A referenced navigation name must resolve
to nonempty text rather than merely an existing ID, and repeated names are
allowed only when the landmarks contain identical link sets. It requires every exposed heading to
contain text without skipping forward over a rank. It also requires every data table to have a
nonempty caption or valid explicit ARIA name, every table header cell to
declare a valid row or column scope, and every exposed interactive or
keyboard-focusable element to have an accessible name, label/control
references to resolve, expanded states to be boolean, and
assistive-technology-hidden controls to be absent from the tab order. This
includes links, buttons, native form and disclosure controls, interactive ARIA
roles, media controls, and custom nonnegative-`tabindex` targets. A tested
source-order rule also rejects positive `tabindex` values; the public tree uses
ten zero-value scroll targets and 26 negative source anchors without any
author-set positive tab priority. A tested focus-entry rule also rejects every
`autofocus` attribute so page load cannot request focus away from the document
entry and first-link bypass path. A tested
post-render normalizer makes the
bypass link first, names Quarto's repeated navigation regions, and adds column
scope inside generated table heads on all five report pages without runtime
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
gate, while rendered desktop/phone keyboard, reflow, and assistive-technology review
remains open under the explicit `ACCESSIBILITY-REVIEW.md` protocol. Its
13-page, 52-result worksheet and environment record are now machine-checked so
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
- The public homepage and Projects directory link all four Published
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
  three-page, two-column PDF; and the production Executive Summary contains
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
- Ipseity Daily Pulse returned to Published status on September 28 with a
  one-chapter Quarto book, one-figure Executive Summary, linked short PDF, and
  Project-specific verifier. The generic v1 contracts incorporated it without
  special casing: the catalogs now expose four Published Projects and the
  accessibility worksheet derives two additional pages and eight additional
  result cells.
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
  direct HTML, all four Quarto footer sources and five generated report pages,
  and archived design pages; the verifier rejects missing groups and misplaced
  links.
- Every public HTML page now exposes a first-anchor bypass link, and every
  native HTML image has an explicit `alt` attribute (including empty
  alternatives for decorative images). The verifier records the first anchor's
  own target and requires that
  target to identify `main`; it no longer lets an invalid first skip-styled link
  borrow validity from a later bypass. It also requires accessible names on
  repeated navigation landmarks and resolves `aria-labelledby` targets to
  nonempty text. This
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
  September 24 audit then found all exposed links and buttons named with valid
  checked `aria-labelledby`, `aria-controls`, and `aria-expanded`
  relationships. The September 25 coverage audit found that two native
  disclosure summaries and six custom focusable scroll regions fell outside
  that link/button-only implementation; all eight were already named. The
  parser now checks 827 interactive or keyboard-focusable elements: all 801
  exposed elements are named and the other 26 are Quarto source-line anchors
  explicitly hidden and removed from the tab order. Three focused fixtures
  cover unnamed icon-only links, disclosures, custom focus targets and
  placeholder-only inputs; explicit and implicit form labels; input values;
  empty/missing labels; broken control targets; invalid expanded state; and
  hidden-control handling. The verifier no longer accepts runtime
  JavaScript relocation. The two NFL report
  figures retain detailed alternatives after rendering. These static checks do
  not replace rendered keyboard or assistive-technology review.
- A September 26 audit found that 24 of 26 public data tables had scoped
  headers but no table-level accessible name. Full Report sources now generate
  concise captions for every affected table, and the Predict the Self Executive
  Summary carries visually hidden source captions matching its scroll-region
  names. The whole-site parser accepts a nonempty caption, `aria-label`, or
  resolved nonempty `aria-labelledby` reference; one focused fixture rejects
  unnamed, missing-reference, and empty-reference cases. All 26 tables in that
  snapshot passed. Ipseity Daily Pulse subsequently returned to Published status with
  three additional named tables, and later Predict the Self work added more;
  all 35 current tables pass. This source
  contract does not establish rendered announcements or screen-reader table
  navigation.
- A September 30 audit found all 196 exposed headings nonempty and free of
  forward rank skips. The page parser now records `h1` through `h6`, rejects an
  empty heading and a jump such as `h2` to `h4`, and permits multiple
  first-level headings and returns to higher ranks in the Quarto book
  structure. One focused fixture covers both failures. This source contract
  does not establish rendered heading order or announced names.
- An October 1 audit found exactly one page-level banner, main region, and
  content-information landmark on all 39 public pages. The parser follows the
  native HTML context rule, so headers and footers nested within a main,
  article, aside, navigation, or section region are not counted as page
  landmarks. One focused fixture accepts valid nesting and rejects missing or
  duplicate landmarks, including duplicates supplied with explicit ARIA roles.
  Later Predict the Self work brings the current inventory to 35 named tables,
  200 exposed headings, and 827 interactive or keyboard-focusable elements:
  all 801 exposed elements are named and 26 source-line anchors remain safely
  hidden. This source contract does not establish the browser accessibility
  tree or observed screen-reader navigation.
- An October 2 coverage audit found that the native-image `alt` rule did not
  inspect composite figures exposed with `role="img"`, including the Version 1
  Executive Summary's dense promise map. All four current exposed ARIA images
  already have explicit names. The parser now accepts a nonempty `aria-label`
  or a resolvable, nonempty `aria-labelledby` reference and rejects missing,
  broken, and empty names. One focused fixture covers those failures and an
  assistive-technology-hidden graphic. WAI-ARIA 1.2 requires author-supplied
  names for this role. This source contract does not establish the rendered
  announcement in a browser and screen-reader pairing.
- An October 3 focus-order coverage audit found that the parser inventoried
  nonnegative `tabindex` targets but did not reject positive values, which
  would move those elements ahead of the default DOM-order tab sequence. The
  current public tree has ten `tabindex="0"` custom scroll regions, 26
  `tabindex="-1"` source anchors, and no positive value. A focused fixture now
  rejects positive values while accepting both current patterns. W3C strongly
  advises against using positive values for tab priority. After the current
  report rebuild, all 836 interactive or keyboard-focusable elements pass: 810
  are exposed and named, and 26 are safely hidden. This source contract does
  not establish rendered focus order, visibility, or operation.
- An October 4 viewport audit found exactly one responsive
  `width=device-width` declaration on each of the 39 public pages, with none
  disabling user scaling or setting a nonnegative maximum scale below 2. A
  focused fixture rejects missing and duplicate declarations, fixed widths,
  `user-scalable=no`, insufficient numeric ceilings, and ambiguous maximum
  scales. W3C's ACT rule maps its zoom restrictions to Resize Text and says a
  passed rule still needs further testing. The current tree also has 38 named
  tables, 204 exposed headings, and 843 interactive or keyboard-focusable
  elements: all 817 exposed elements are named and 26 source anchors remain
  safely hidden. This source contract preserves a narrow-layout and 200%-text
  prerequisite; it does not establish rendered reflow or text resizing.
- An October 6 timing audit found no `meta http-equiv="refresh"` declaration
  on any of the 39 public pages. The parser now records those declarations and
  a focused fixture rejects both a delayed reload and a zero-delay redirect.
  W3C identifies timed meta redirects and page reloads as failures of Timing
  Adjustable; this Project applies the stricter rule that its static pages need
  no meta refresh at all. The source check does not inspect script- or
  server-driven updates or establish the absence of rendered interruptions.
- An October 7 navigation-name coverage audit found that an existing but empty
  `aria-labelledby` target could pass the September 22 repeated-landmark rule.
  The parser now derives the referenced text, rejects missing and textless
  targets, and reports the affected repeated landmark as unnamed. A separate
  focused fixture preserves the empty-target failure. All 160 navigation
  landmarks in the current 39-page tree pass the corrected source rule. W3C
  recommends labels that distinguish repeated navigation regions; only the
  open screen-reader protocol can establish the browser-exposed and announced
  names.
- An October 8 navigation-distinction audit found that the nonempty-name rule
  could still accept the same name on landmarks containing different links.
  The parser now retains each navigation region's link targets and rejects a
  repeated source-derived name when those link sets differ. It permits the
  W3C-documented exception for identical link sets. A focused fixture covers
  both the failure and exception; all 160 current navigation landmarks pass.
  This exact-link comparison does not establish that labels are semantically
  useful or that a browser and screen reader expose and announce them as
  intended.
- An October 9 focus-entry audit found no `autofocus` attribute on any current
  public page, but the verifier did not preserve that source condition. The
  HTML Standard defines the attribute as a request to focus an element on page
  load and runs focusing steps for an eligible candidate. The parser now
  rejects every occurrence, including the boolean form `autofocus="false"`;
  one focused fixture covers the failure. This strict static-site rule does
  not establish the initial focus observed in a browser.
- `ACCESSIBILITY-REVIEW.md` defines the last manual gate's 13 production pages,
  desktop and 320-CSS-pixel conditions, keyboard/focus, reflow, screen-reader
  checks, structured environment record, 52 result cells, and passing rule.
  The verifier derives the sample from current Published summaries and Full
  Reports, rejects missing/duplicate rows and unknown result words, and refuses
  closed records with placeholders or non-passing cells. Three tests cover
  current coverage, malformed rows, and incomplete versus complete closure. A
  supplemental `w3m` 0.5.3 pass on October 9 returned zero at 40 and 120
  columns for all 13 current pages; each of the 26 linearized views began with
  “Skip to content.” It is text-order evidence, not a graphical-browser or
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
  releases from September 15 through the clean October 1 report set; the
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
  files byte-identical, and the September 25 pre-change probe found all 174
  incoming files byte-identical. The September 26 pre-change probe found all
  182 incoming files byte-identical.
  The September 29 pre-change probe found all 249 incoming files
  byte-identical after Ipseity Daily Pulse returned to the public catalog.
  The September 30 pre-change probe found all 257 incoming files byte-identical
  after later Predict the Self publication work. The October 1 pre-change
  probe found all 267 incoming files byte-identical after the next Predict the
  Self iteration. The October 2 pre-change probe found all 275 incoming files
  byte-identical after the next Predict the Self iteration. The October 3
  pre-change probe found all 285 incoming files byte-identical after the latest
  Predict the Self iteration.
  The October 4 pre-change probe found all 293 incoming files byte-identical
  after the next Predict the Self iteration.
  The October 6 pre-change probe again found all 293 incoming files
  byte-identical. The October 7 worktree probe found 291 files byte-identical
  and the two already-edited public pages different; their production digests
  exactly matched the clean incoming `HEAD` versions, establishing all 293
  incoming files as byte-identical.
  The October 8 pre-change probe found all 295 incoming files byte-identical.
  The October 9 pre-change probe again found all 295 incoming files
  byte-identical.
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

All seven groups and all 50 routine tests pass across 39 HTML pages, 160 named
navigation landmarks, 97 native
images, four exposed ARIA images, 38 named data tables, 204 exposed headings,
846 interactive or keyboard-focusable elements, and seven first-party
stylesheets on October 9. Every page has
exactly one page-level banner, main, and content-information landmark. The verifier's success detail now
reports the navigation-landmark count, responsive zoom-permitting viewport contract, plus exposed and
safely hidden control counts directly, rather than leaving that coverage
implicit.
The checks now include validated identity/biography data, independent Project
lifecycle/publication state, footer-link group placement,
iteration filename/metadata agreement, bounded recent links, complete yearly
indexes, legacy-dialog digests, first-anchor bypass mechanisms, explicit image
alternatives, exposed ARIA image names, exact top-level landmark frames,
nonempty unskipped heading ranks, repeated navigation names,
resolved nonempty landmark-label references, distinct navigation names for
different link sets,
accessible data-table names, valid table-header scopes, interactive and keyboard-focusable element names,
ARIA relationships, no positive `tabindex` overrides, one responsive viewport
without a sub-200% zoom ceiling, no autofocus, no automatic meta refresh or
redirect, and the
manual-review worksheet's sample and closure boundary. One focused table-name
test covers captions and valid explicit labels while rejecting absent, broken,
or empty names. One focused negative
test guards the first-anchor/target conjunction, one covers missing and
duplicate top-level landmarks with native context, five tests cover the build-time
Quarto normalizer, three cover the generic navigation-name rule (including
textless referenced labels and repeated names on different link sets), one covers the
generic table-header rule, one covers heading text and rank, one covers
missing, broken, and empty ARIA image names, three cover
interactive names and ARIA relationships
across links, buttons, forms, disclosures, roles, media, and custom focus
targets, one rejects positive `tabindex` values while accepting zero and
negative patterns, one rejects autofocus, one covers responsive and zoom-permitting viewport
metadata, one rejects automatic meta refreshes and redirects, and three cover
the manual-review record.
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

- Follow `ACCESSIBILITY-REVIEW.md` on a browser-equipped host: inspect all 13
  selected production pages at desktop and phone widths with keyboard and a
  recorded screen-reader pairing, complete all 52 result cells and environment
  fields, and close the record only after every result passes. No installed
  Chromium, Chrome, or Firefox executable or supported screen-reader/browser
  pairing is available on this host.
- Dr. Jones reported that the production pages and PDFs look acceptable. The
  keyboard/reflow/assistive-technology pass remains the sole open manual gate.

## Resources and limitations

October 9 preflight: 2 logical CPUs, 3.7 GiB RAM, 4.0 GiB swap, and 61 GiB
free disk. Installed Python 3.12.3, R 4.3.3, Quarto 1.10.18, Pandoc, and
rsync 3.2.7 are available. `w3m` 0.5.3 is available; no Chromium, Chrome, or
Firefox executable or supported screen-reader/browser pairing was found.
ReportLab/pypdf are not installed in the base Python environment; any PDF build
uses the existing documented temporary build-only packages, not production
dependencies. The pinned PDF packages were installed under `/tmp` for this
build; no system package, replacement runtime, or production dependency was
installed.

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
  v1 release ledger, including the clean October 7 report set superseded by
  the current navigation-label distinction revision.
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
record the environment and all 52 page-level results, repair and retest any
failure, and then assess the charter and PI authority before changing lifecycle
state.
