# Superseded report archiving

Status: operative for material report changes beginning September 16, 2026.

This policy keeps each Project's canonical public URLs focused on its current
evidence while preserving every superseded report set exactly. It uses Git's
content-addressed history instead of copying old generated sites into the live
static tree, where duplicate Quarto assets and ambiguous relative links would
accumulate.

## What is a report release?

A report release is the mutually linked set published at the canonical Project
paths:

- `website/projects/<slug>/index.html` (Executive Summary);
- `website/projects/<slug>/report/` (Full Report and its dependencies); and
- `website/projects/<slug>/short-report.pdf` (short report).

Project-owned images or data files referenced by those documents are part of
the release. The corresponding sources, analysis, and Project memory in
`projects/<slug>/` are part of its reproducibility record.

A **material supersession** changes a claim, estimand, method, data, result,
interpretation, limitation, report structure, or other content a reader could
reasonably use. Spelling, styling, dependency refreshes, and link repairs that
do not alter meaning are maintenance changes; ordinary Git history is
sufficient for them.

## Archive rule

Canonical report URLs always show the current release. Before materially
changing one or more report forms, the Scholar records the clean pre-iteration
commit in `projects/<slug>/REPORT-VERSIONS.md`. That full 40-character commit
identifier is the immutable archive key for the outgoing release. Because the
normal Scholar workflow commits and pushes every report tree, the key resolves
all three generated forms, their dependencies, their sources, and the Project
record at one exact public repository state.

Each ledger entry records:

1. the outgoing release's last substantive update time;
2. the UTC date or time it was superseded;
3. the full commit identifier and a public GitHub tree link;
4. which report forms or shared assets changed;
5. why the release was superseded; and
6. whether the change is an update, correction, or retraction.

Use the commit checked out at the start of the iteration only after confirming
that the outgoing public artifacts are tracked and unchanged. If the working
tree already differs, stop and identify the last commit containing the actual
outgoing release rather than recording an uncertain key. Never replace or
delete an earlier ledger entry, reuse an archive key for different bytes, or
rewrite published history.

The iteration record under `dialog/iterations/` summarizes the supersession and
validation.
The new release itself does not yet have a commit identifier while the Scholar
is editing it; it receives one from normal post-iteration automation and is
added to the ledger only when a later material release supersedes it.

## Corrections and retractions

A correction preserves the outgoing release in the ledger and places a clear
notice in every affected current report form describing what changed. A
retraction does the same, but the canonical forms become a retraction notice
and must not silently continue presenting the withdrawn claim. Neither action
deletes Project data, analysis, dialog, or Git history. The PI must authorize a
retraction; routine evidence updates do not require that label.

## Retrieval and validation

The public repository is the archive interface. For a ledger commit `<sha>`, a
reader can inspect the exact release at:

```text
https://github.com/jasonjeffreyjones/virtual-csserg/tree/<sha>/website/projects/<slug>
```

and its sources at:

```text
https://github.com/jasonjeffreyjones/virtual-csserg/tree/<sha>/projects/<slug>
```

Before publication, the Scholar verifies that the commit exists locally, that
it contains the three outgoing report forms, and that the recorded GitHub paths
use the same full identifier. Normal public parity and deployment-inventory
checks apply to the new canonical release. If the lab later needs old releases
to remain directly rendered as websites, that is a separate migration; it must
preserve these archive keys and repair relative links rather than duplicating
trees ad hoc.
