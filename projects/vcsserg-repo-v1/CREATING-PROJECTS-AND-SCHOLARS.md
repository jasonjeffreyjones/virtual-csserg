# Creating Projects and Scholars

This is the Version 1 procedure for Dr. Jones. It separates private research
setup from public publication, preserves PI authority over charters and
biographies, and makes the mechanical parts reviewable.

## Project lifecycle and update metadata

Every `STATE.md` begins with these machine-readable fields:

```yaml
---
title: "Project title"
status: Proposed
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

Review and publication readiness are separate from lifecycle state. Whenever a
state changes, record who changed it, when, and why in the Project dialog and
summarize the operative decision in `STATE.md`.

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
   the change and its reason in `DIALOG.md` and set `updated` to that
   intervention time.
3. Record the assignment in the Project state and on the Scholar's public
   profile. The PI's host-managed scheduler invokes
   `run-scholar.sh "Scholar name" "Project title"`; keep scheduler details,
   credentials, and host paths outside this public repository.
4. Conduct research in `projects/<project-slug>/`. Keep sources, code, data
   provenance, results, and Quarto source there.
5. Publish only after substantive content exists. Create the Quarto Full Report,
   two-column short PDF, and five-minute Executive Summary under
   `website/projects/<project-slug>/`, link the three forms to one another, and
   add the Project to both public indexes.
6. Set the Projects-directory `data-project` and `data-updated` attributes from
   `STATE.md`; run the Version 1 verifier and project-specific checks. Inspect
   the rendered outputs before marking publication ready or the Project
   Completed.

Manual copying of `_template` remains a recovery option, but the command is the
default because it makes validation and no-overwrite behavior consistent.

## Create a Scholar

Scholar creation is intentionally review-led in Version 1 because the public
biography and representation are PI-authored identity claims, not boilerplate.

1. Dr. Jones chooses a permanent lowercase, hyphen-separated slug and supplies
   the Scholar's display name and full authoritative biography in a Project
   charter or dialog entry.
2. Create `website/scholars/<scholar-slug>/index.html` by adapting a current
   profile. Preserve the standard header, Bootstrap CDN, logo, footer, skip
   link, responsive behavior, and semantic headings.
3. Reproduce the PI-supplied biography faithfully. Do not invent history,
   demographics, credentials, relationships, preferences, or accomplishments.
4. Add a portrait-roster card to `website/scholars/index.html` and a homepage
   link. Record the current Project assignment on the profile, and update it as
   assignments change.
5. Add a host-managed scheduler invocation using the Scholar name and assigned
   Project title as the two `run-scholar.sh` arguments. Run the static-site
   verifier, open the new profile from both indexes, and inspect it at desktop
   and phone widths with keyboard navigation.

There is no automated Scholar scaffolder yet. Add one only after the source of
truth for the roster and current assignments is specified; otherwise a command
could create a plausible-looking but unauthorized public identity.

## Scholar-generated images

Monograms remain the default. A generated representation may become canonical
only after PI selection and must be clearly illustrative rather than
photorealistic biography. Commit the image beside a metadata file recording the
Scholar, date, tool and method, complete prompt or design brief, and any source
image provenance. Provide useful alt text, check small-screen crops, and do not
imply an unsupported age, race, gender, body, location, credential, or lived
history.

## Still to coordinate

The approved dialog migration requires one immutable file per iteration and a
newest-first `DIALOG.md` index. Implement it in one coordinated change to
`RESEARCHER-ORIENTATION.md`, `_template`, the runner prompt, every active
Project, and the verifier; do not partially switch formats. Footer grouping and
the source of truth for Scholar assignments likewise remain follow-up work.
