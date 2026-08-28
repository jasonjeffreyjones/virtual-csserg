# VCSSERG Version 1.0 Audit

This is a point-in-time map from documented promises to observable evidence. It
separates verified behavior from assumptions so “works as documented” can become
a testable definition of done.

Run the non-destructive automated portion from the repository root:

```bash
python3 projects/vcsserg-repo-v1/verify_v1.py
```

The verifier does not read `.env`, contact remote systems, create commits, or
deploy. It returns a nonzero status while any automated check fails.

## Evidence matrix

| Documented promise | Evidence or test | Status on 2026-08-28 |
|---|---|---|
| Scholars receive repository, orientation, identity, and assigned-project context for an iteration. | `run-scholar.sh` constructs the documented prompt; manual inspection. | Verified statically |
| Iterations use the four-file project memory model and an append-only log. | `projects/vcsserg-repo-v1/` contains `PROJECT.md`, `PI.md`, `STATE.md`, and `LOG.md`; verifier checks every active project directory. | Verified |
| Scholar automation prevents concurrent runs, updates from GitHub, commits iteration changes, rebases, and pushes. | `bash -n run-scholar.sh` plus verifier checks for lock/pull/commit/push wiring. | Verified statically; not executed end to end |
| The automated workflow deploys the pushed `website/` tree. | The runner invokes `python3 vcsserg_deploy.py`, which resolves to a nonexistent repository-root file; the actual script is `python/vcsserg_deploy.py`. | **Failing** |
| A deployment error stops the automation instead of being reported as success. | The deployment-component check mocks a failed `rsync` and requires a nonzero exit. | Verified |
| Deployment avoids shell interpolation of configuration values. | The deployment-component check inspects the mocked `rsync` call and requires an argument list with no shell. | Verified |
| The public site is built from static HTML and CSS and local navigation works. | Verifier parses every HTML page, validates landmarks, unique titles and IDs, descriptions, local files and fragments, and checks CSS structure and responsive/reduced-motion rules. | Verified for repository files |
| The front door catalogs the active projects and initial Scholars documented by the charter. | Verifier compares `website/index.html` with the active project directory and the three initial Scholars in `PROJECT.md`. | **Partial:** project and Bee are linked; Aleph and Ceetown lack public profiles |
| Production exactly matches `website/`. | Requires fetching production and comparing its file inventory and bytes with the local tree after deployment. DNS/network access was unavailable in this environment. | Unverified |
| Pages work visually at desktop and mobile sizes. | Requires rendered browser inspection in addition to structural checks. No browser is installed in this environment. | Unverified |
| Project pages communicate results through a five-minute Executive Summary and, where appropriate, a Quarto Full Report. | The project has an Executive Summary at `website/projects/vcsserg-repo-v1/index.html`. This bootstrap project does not yet claim a research result requiring a Full Report. | Executive Summary present; report need undecided |

## Current automated result

Four of six check groups pass. The two failures are traceable:

1. `run-scholar.sh` points at the wrong deployment-script path. Scholars are not
   permitted to edit that runner, so this requires Dr. Jones to change the final
   command to `python3 python/vcsserg_deploy.py`.
2. The charter names three initial Scholars, while the public site currently
   publishes and catalogs only B. Boring Vanilla.

Passing the automated verifier will not by itself establish Version 1.0. A live
deployment comparison and browser QA remain required manual gates.
