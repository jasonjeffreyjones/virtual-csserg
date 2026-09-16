# Creating Projects and Scholars

This is the Version 1 procedure for Dr. Jones. It separates private research
setup from public publication, preserves PI authority over charters and
biographies, and makes the mechanical parts reviewable.

The versioned `scholars.json` file is the source of truth for Scholar names,
permanent slugs, and monograms. Canonical PI-authored biographies live at
`scholars/<scholar-slug>/BIOGRAPHY.md`. A Scholar–Project pairing lasts for one
runner invocation; there is no durable assignment record. Validate identities
and biographies from the repository root with:

```bash
python3 python/scholar_roster.py
```

## Project lifecycle and update metadata

Every `STATE.md` begins with these machine-readable fields:

```yaml
---
title: "Project title"
status: Proposed
publication: Unpublished
updated: null
---
```

Use exactly one lifecycle state:

- **Proposed:** a charter is being prepared; research has not begun.
- **Active:** work is authorized and useful next work exists.
- **Blocked:** progress genuinely depends on unavailable input or infrastructure.
- **Paused:** the PI has intentionally deprioritized otherwise feasible work.
- **Completed:** the charter and required publication are complete.
- **Archived:** a closed Project is retained but superseded or retired.

`publication` is either **Unpublished** or **Published** and is independent of
lifecycle state. An Active Project may remain Unpublished while research
begins. Only Published Projects appear in public catalogs and must provide all
three report forms. A Proposed Project cannot be Published. Whenever a
state changes, record who changed it, when, and why in the current immutable
iteration record and summarize the operative decision in `STATE.md`.

`updated` means the end time of the newest substantive Scholar iteration or PI
intervention. Use an ISO 8601 UTC timestamp when a time is recorded, or the ISO
date when the historical record gives only a date. Do not advance it for CSS
edits, deployment, or unrelated commits. The public Projects directory is
ordered by this field.

## Create a Project

From the repository root, run:

```bash
python3 python/create_project.py <project-slug> "Project title"
```

The slug is a permanent lowercase, hyphen-separated identifier such as
`collective-memory-online`. The command validates it, refuses to overwrite an
existing path, stages the copy before renaming it into place, and personalizes
the title and initial metadata. It never modifies the public website.

Then:

1. Dr. Jones completes `projects/<project-slug>/PROJECT.md`. Only the PI edits
   the charter.
2. Change the state from Proposed to Active only when work is authorized. Record
   the change and its reason in the next immutable iteration record and set
   `updated` to that intervention time.
3. Invoke any rostered Scholar for one iteration using permanent slugs:
   `./run-scholar.sh <scholar-slug> <project-slug>`. The runner validates the
   identity and requires the Project to be Active. The invocation is the
   assignment; it does not create a durable Scholar–Project relationship.
4. Conduct research in `projects/<project-slug>/`. Keep sources, code, data
   provenance, results, and Quarto source there.
5. Publish only after substantive content exists. Create the Quarto Full Report,
   two-column short PDF, and five-minute Executive Summary under
   `website/projects/<project-slug>/`, link the three forms to one another, and
   add the Project to both public indexes. Change `publication` to `Published`
   only in the same validated change.
6. Set the Projects-directory `data-project` and `data-updated` attributes from
   `STATE.md`; run the Version 1 verifier and project-specific checks. Inspect
   the rendered outputs before marking publication ready or the Project
   Completed.

When a later iteration materially changes a published claim, method, result,
interpretation, limitation, or report structure, archive the outgoing report
set before replacement. Record the clean pre-iteration commit and reason in
`projects/<project-slug>/REPORT-VERSIONS.md` following
`projects/vcsserg-repo-v1/REPORT-ARCHIVING.md`. Canonical URLs continue to show
the current release; the full commit key preserves the superseded Executive
Summary, Full Report, short PDF, dependencies, sources, and Project record.
Cosmetic maintenance remains available through ordinary Git history and does
not require a ledger entry.

Manual copying of `_template` remains a recovery option, but the command is the
default because it makes validation and no-overwrite behavior consistent.

## Pause or resume a Project

Pausing changes priority, not evidence. Use this sequence:

1. Dr. Jones appends an explicit pause instruction as a dated blockquote to the
   newest relevant iteration record. Include a reason when useful; a pause does
   not require a technical blocker. Keep that record linked under active PI
   guidance until a Scholar incorporates the instruction.
2. A Scholar sets the `STATE.md` lifecycle value to `Paused`, sets `updated` to
   the PI intervention time, and summarizes what remains valid and what work is
   deferred. Record the state change in the current immutable iteration file.
3. Preserve published reports, data, and code unless the PI separately asks to
   retract or archive them. Public status labels should say Paused so readers do
   not mistake publication for current activity.
4. Dr. Jones disables future host-scheduler invocations for the Project. Host
   scheduler details remain outside the public repository, so a Scholar can
   record this required action but cannot verify it from repository files.

To resume, Dr. Jones appends an explicit resume instruction to the newest
relevant iteration record and later invokes any Scholar after the Project state
returns to Active. The next Scholar updates public labels and `updated`, reads
the preserved state and relevant dialog records, and continues the highest-value
work.

## Create a Scholar

Scholar identity remains PI-authored, while the mechanical creation work is
automated. First write the complete biography in a plain UTF-8 Markdown file.
Then run:

```bash
python3 python/create_scholar.py \
  <scholar-slug> \
  "Scholar display name" \
  <MONOGRAM> \
  --bio-file <biography-file>
```

The permanent slug uses lowercase letters, digits, and single hyphens. The
unique monogram uses one to eight uppercase letters or digits. The command
validates identity data, refuses overwrite, copies the complete biography to
`scholars/<scholar-slug>/BIOGRAPHY.md`, adds the schema-versioned roster record,
creates the public profile, and regenerates the homepage and Scholar directory
entries. It rolls back affected files if installation fails. It does not assign,
schedule, or invoke the Scholar.

Review the generated profile and run:

```bash
python3 python/scholar_roster.py
python3 projects/vcsserg-repo-v1/verify_v1.py
```

To authorize work, invoke the Scholar on any Active Project for one iteration:

```bash
./run-scholar.sh <scholar-slug> <project-slug>
```

The runner rejects unknown identities, non-Active Projects, and dirty working
trees. It independently validates successful Scholar work before commit, push,
and deployment, and rejects an iteration that changes the PI-owned runner. Do
not invent history, demographics, credentials,
relationships, preferences, or accomplishments beyond the PI-authored
biography and work actually recorded by that Scholar.

## Scholar-generated images

Monograms remain the default. A generated representation may become canonical
only after PI selection and must be clearly illustrative rather than
photorealistic biography. Commit the image beside a metadata file recording the
Scholar, date, tool and method, complete prompt or design brief, and any source
image provenance. Provide useful alt text, check small-screen crops, and do not
imply an unsupported age, race, gender, body, location, credential, or lived
history.

## Dialog records

The immutable-dialog protocol is now operative. Each iteration creates exactly
one `dialog/iterations/YYYY-MM-DDTHHMMSSZ-scholar-slug.md` file, updates its
complete yearly index, and adds the record newest-first to the bounded
`DIALOG.md` landing page. The landing page retains no more than 20 recent
iteration links. Scholars never alter an earlier record or write PI
blockquotes; Dr. Jones appends feedback to the record he is answering.

The creation command removes `_template`'s migration archive from each new
scaffold and initializes a fresh dialog tree. `DIALOG-MIGRATION.md` records the
completed coordination and the exact reading and feedback conventions.
The one-time conversion was dry-run and then applied from the repository root:

```bash
python3 python/migrate_dialogs.py --through-date 2026-09-16
python3 python/migrate_dialogs.py --through-date 2026-09-16 --apply
```

The command now refuses to overwrite the migrated layout; it remains versioned
as executable evidence of the dry-run, no-overwrite, and all-Project procedure.

Footer links are now grouped on every public page as **About** (Dr. Jones and
CSSERG) and **Open work** (GitHub and CC BY 4.0). The verifier checks both the
presence and placement of those links.
