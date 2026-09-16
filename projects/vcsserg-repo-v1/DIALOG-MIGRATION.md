# Immutable dialog migration runbook

Status: completed September 16, 2026. The immutable-per-iteration protocol is
now authoritative across `_template` and every existing Project. The trigger
and execution steps below are retained as the migration record.

## Migration completion evidence

The PI-owned runner contained the approved trigger language before the canary
began. `python/migrate_dialogs.py` then dry-ran and migrated all five Project
directories together. It refuses overwrite, preflights every target before
mutation, stages every output, and restores prior landings if installation
raises an exception. Fixture tests cover read-only dry run, exact legacy-byte
preservation, repeat refusal, and whole-set preflight failure.

The source `DIALOG.md` SHA-256 digests, now recorded in each landing page, are:

- `_template`: `4c96151dfd236ea13dad31a64a8efd9a5a1812d1ea036e0dffbd3c99c2041abd`
- `ipseity-daily-pulse`: `9d6b28e3dc60686f318397a9c398f1219febc1b6855c9fca3bd0f7744b855321`
- `nfl-team-fandom-identities`: `316cbcf943e6a9bfec21123e6d1c3f67976a3164ebdb301658fb2ba9c8402428`
- `predict-the-self`: `f618ab88bfac5da80e62f31119839bd054b9b590febf4cdf8b4103fdc9ced741`
- `vcsserg-repo-v1`: `8b5d890175d767048ec77f1b191a49d773cbfcfb6a895b8115dd170fd2a6d685`

## Target layout

Each Project will use this structure:

```text
projects/<project-slug>/
├── DIALOG.md
└── dialog/
    ├── iterations/
    │   └── 2026-09-15T080104Z-bee-boring-vanilla.md
    ├── indexes/
    │   └── 2026.md
    └── legacy/
        └── DIALOG-through-2026-09-15.md
```

`DIALOG.md` becomes a bounded landing page, not the conversation store. It
contains active PI guidance and unresolved questions, then newest-first links
to at most the 20 most recent iteration records. Complete yearly indexes retain
older links. The pre-migration dialog is copied byte-for-byte into `legacy/`
and recorded with a SHA-256 digest before the original path becomes the index.
Legacy `PI.md` and `LOG.md` files remain unchanged where they already exist.

An iteration filename uses its UTC start time and permanent Scholar slug:
`YYYY-MM-DDTHHMMSSZ-<scholar-slug>.md`. Creation must refuse overwrite. The
file records start and finish times, scope, work, evidence, validation,
limitations, decisions, questions, and likely next steps. After its commit, a
Scholar never edits that record or any earlier iteration record.

## Steps Dr. Jones must take to begin

1. Let the September 15 VCSSERG v1 iteration finish its normal commit, push,
   and deployment. Then temporarily pause all Scholar schedules so two protocol
   versions cannot run concurrently.
2. Edit the PI-owned `run-scholar.sh` prompt. Replace the instruction to read all
   of `DIALOG.md` with an instruction to read `PROJECT.md`, `STATE.md`, the
   bounded `DIALOG.md` index, the records marked as active PI guidance, and the
   bounded recent set defined below. Replace the instruction to append to
   `DIALOG.md` with an instruction to create exactly one timestamped file under
   `dialog/iterations/` and update the index and `STATE.md`.
3. Add these safeguards to the prompt: never alter an earlier Scholar record;
   never create or modify PI blockquotes; refuse to reuse an iteration filename;
   and follow the legacy procedure if the Project has not yet been migrated.
   The last clause makes the trigger safe while the canary migration is running.
4. Commit and push that runner-only trigger change. Do not resume the full
   schedule yet. Invoke Bee Boring Vanilla once on VCSSERG v1 as the migration
   canary and inspect whether the run commits, pushes, and deploys successfully.
5. After the canary's checks pass, resume schedules for Active Projects only.
   Keep NFL Team Fandom Identities disabled while its lifecycle state is Paused.

The runner edit is the required PI action because Scholars are explicitly
forbidden to edit `run-scholar.sh`. No repository migration should precede it.

## Steps the migration Scholar will take next

1. Confirm the runner prompt contains the trigger language and record the
   pre-migration SHA-256 digest of every Project's existing `DIALOG.md`.
2. Add a standard-library migration command with dry-run, no-overwrite, and
   all-or-nothing behavior. Exercise it first on temporary fixtures.
3. Migrate `_template` and every existing Project, including Paused Projects,
   in one commit: preserve each legacy dialog byte-for-byte, create the current
   and yearly indexes, and do not alter historical blockquotes.
4. Update `RESEARCHER-ORIENTATION.md`, `_template`, Project-creation code, growth
   documentation, all Project states, and `verify_v1.py` together. The verifier
   will require the new layout, filename/metadata consistency, legacy hashes,
   a bounded current index, and unique links to all iteration records.
5. Write the canary iteration itself in the new format, update the v1 state and
   index, run all Project and Version 1 checks, and verify that existing report
   publication is unchanged.
6. Record any Project-specific anomaly instead of silently rewriting history.
   If migration or validation fails, leave the old layout operative and report
   the failure; do not publish a mixed protocol.

## PI–Scholar exchange after migration

- A Scholar creates one new iteration record and adds its link at the top of the
  bounded `DIALOG.md` list. Operative decisions and open questions are also
  summarized in `STATE.md`; the index is navigation, while state remains the
  concise handoff.
- Dr. Jones provides feedback by opening the specific linked iteration record
  and appending dated Markdown blockquotes at its end. He does not rewrite the
  Scholar's text. For new Project-wide guidance that is not a reply, he appends
  it to the newest relevant iteration record and identifies it as new guidance.
- PI additions are the sole exception to byte immutability: Scholar-authored
  text is immutable, while PI feedback remains append-only. The next Scholar
  preserves every blockquote, promotes currently operative guidance to
  `STATE.md`, and points the new iteration record back to the file containing
  the response. The most recent applicable, unambiguous PI statement still
  governs.
- If a response arrives after a topic has moved on, Dr. Jones replies to the
  record whose question he is answering. The active-guidance section of the
  index links that response until a Scholar has incorporated or resolved it.

## How much history Scholars read

Scholars will not be expected to reread the entire historical corpus on every
iteration. They must read:

1. all of `PROJECT.md`, `STATE.md`, and the bounded `DIALOG.md` landing page;
2. every record linked under active PI guidance or unresolved questions;
3. the three newest iteration records;
4. their own most recent record on that Project, if it is not among those three;
5. any older record directly cited by the charter, state, current analysis, or
   a newer dialog record as necessary to understand provenance or a decision.

The current index retains 20 entries so browsing remains useful without making
20 the reading requirement. Yearly indexes and immutable records preserve the
complete audit trail. `STATE.md` must be refreshed every iteration so the
bounded reading rule is safe; when state is stale, contradictory, or missing
provenance, the Scholar expands the historical review until the issue is
resolved.
