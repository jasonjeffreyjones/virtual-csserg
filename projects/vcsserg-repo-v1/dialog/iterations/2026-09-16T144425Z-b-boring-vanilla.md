---
started: 2026-09-16T14:44:25Z
finished: 2026-09-16T14:57:00Z
scholar: "Bee Boring Vanilla"
scholar_slug: b-boring-vanilla
project: vcsserg-repo-v1
---

# Immutable-dialog migration canary

## Scope

Execute the PI-triggered, repository-wide immutable-dialog migration as one
coordinated VCSSERG v1 canary. Preserve every legacy `DIALOG.md` byte-for-byte,
update the governing workflow and Project handoffs, make the protocol
reproducibly verifiable, and keep all three v1 report forms synchronized.

## Work completed

- Added `python/migrate_dialogs.py`, a standard-library migration command that
  dry-runs by default, validates every target before mutation, stages all
  outputs, refuses overwrite, and rolls back installed outputs if an apply step
  raises an exception. Three fixture tests cover dry-run immutability, exact
  byte preservation/repeat refusal, and whole-set preflight failure.
- Migrated `_template` and all four existing Projects. Each now has a bounded
  `DIALOG.md`, `dialog/iterations/`, `dialog/indexes/2026.md`, and a byte-exact
  archive under `dialog/legacy/`. The five landing pages record the archive
  SHA-256 digests.
- Updated `RESEARCHER-ORIENTATION.md`, template/project guidance and states,
  Project creation, growth and archive procedures, the migration runbook,
  audit/recommendations, and public v1 reporting. New Project scaffolds receive
  a fresh dialog tree rather than inheriting `_template`'s migration archive.
- Extended `verify_v1.py` to validate the protocol marker, required landing
  sections, archive paths and recomputed hashes, iteration filename/metadata
  agreement, required record sections, a newest-first 20-record landing window,
  and exactly one yearly-index link per iteration. Biography provenance now
  resolves Disciple Dee Duplo's PI-authored text from the preserved archive.
- Recorded the clean pre-canary report commit in `REPORT-VERSIONS.md`, rendered
  and safely published the updated Quarto Full Report, rebuilt the short PDF,
  and refreshed the Executive Summary and homepage account.

## Evidence and validation

- The real dry run identified exactly five targets and reported the same five
  hashes later recomputed from both the archived files and the pre-iteration
  Git blobs. A repeat real-repository migration refused before mutation.
- All 15 VCSSERG v1 unit tests pass, including the three migration tests. The
  Version 1 verifier passes all seven groups across five Project/template
  memory layouts, 26 HTML pages, six first-party stylesheets, all three
  publication-eligible report sets, runner wiring, and guarded deployment.
- The v1 publication verifier passes one Executive Summary figure, reciprocal
  links, the required phrase, and a linked two-page, two-column PDF. Quarto
  1.10.18 rendered cleanly; Ghostscript rasterization and page inspection found
  no clipping or overlap.
- Predict the Self's five unit tests and publication verifier pass. NFL Team
  Fandom Identities' seven unit tests and publication verifier pass. Python
  compilation, runner shell syntax through the v1 verifier, and
  `git diff --check` pass.

## Limitations and decisions

The migration does not rewrite the older `PI.md` or `LOG.md` files that remain
as additional history in two Projects. The HTTP production probe was not rerun
against this changed checkout because normal automation has not deployed it
yet. No credential, `.env`, manual deployment, package installation,
replacement runtime, PI-owned runner edit, charter edit, or parallel agent was
used. No installed graphical browser is available, so HTML desktop/phone,
keyboard, and assistive-technology inspection remains open.

The operative design is one record per iteration, not per day. Scholar text is
immutable after creation; only Dr. Jones may append dated blockquote feedback.
The landing page retains at most 20 recent records, while complete yearly
indexes and the hashed legacy archive preserve discovery and provenance.

## Questions and next steps

No blocking PI question. Dr. Jones still needs to disable the external NFL
schedule if that host-side pause step remains outstanding. For VCSSERG v1,
witness the safe workflow failure path and complete rendered
keyboard/assistive-technology and substantive review. After normal deployment,
the public parity probe can confirm the changed website bytes.

Elapsed time: 12 minutes 35 seconds (755 seconds).
