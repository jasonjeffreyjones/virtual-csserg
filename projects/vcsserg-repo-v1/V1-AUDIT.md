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

| Documented promise | Evidence or test | Status on 2026-09-11 |
|---|---|---|
| Scholars receive repository, orientation, identity, and assigned-project context for an iteration. | `run-scholar.sh` constructs the documented prompt; manual inspection. | Verified statically |
| Scholar automation prevents concurrent runs, updates from GitHub, commits iteration changes, rebases, pushes, deploys, and records completion. | `bash -n run-scholar.sh` plus verifier checks for lock/pull/commit/push/deploy wiring and the completion-log variable. | Verified statically; Dr. Jones replaced the undefined `LOG_FILE` reference with the existing per-iteration log path |
| The automated workflow deploys the pushed `website/` tree. | The runner invokes the existing `python/vcsserg_deploy.py` after a successful push. | Verified statically; not executed end to end |
| A deployment error stops the automation instead of being reported as success. | The deployment-component check mocks a failed `rsync` and requires a nonzero exit. | Verified |
| Deployment avoids shell interpolation of configuration values. | The deployment-component check inspects the mocked `rsync` call and requires an argument list with no shell. | Verified |
| The public site is built from static HTML and CSS, local navigation works, and CSSERG branding is consistent. | Verifier parses every HTML page, validates landmarks, unique titles and IDs, descriptions, local files and fragments, CSSERG logo use, the shared required footer including the PI-requested GitHub repository link, brand colors, CSS structure, and responsive/reduced-motion rules. | Verified for repository files |
| The front door catalogs the active projects and initial Scholars documented by the charter. | Verifier compares `website/index.html` and `website/scholars/index.html` with the active project directory and the three initial Scholars in `PROJECT.md`. | Failing: NFL project has no public index |
| Production exactly matches `website/`. | The deployer uses guarded `rsync --delete-delay` mirroring; establishing parity still requires comparing production file inventory and bytes with the local tree after deployment. | Implementation verified; live parity unverified |
| Pages work visually at desktop and mobile sizes. | Requires rendered browser inspection in addition to structural checks. No Chromium, Chrome, or Firefox executable or browser tool was available during this iteration. | Unverified |
| Project pages communicate results through a five-minute Executive Summary and, where appropriate, a Quarto Full Report. | The project has an Executive Summary at `website/projects/vcsserg-repo-v1/index.html`; its charter explicitly says this bootstrap project does not require a Full Report. | Partial: summary exists; required key figure remains missing |

## Current automated result

On September 11, 2026, **four of six groups pass**. Project memory fails because
`nfl-team-fandom-identities` and `predict-the-self` lack `DIALOG.md`. Public
catalogs fail because the NFL project has no public index. These are current
repository gaps, not failures introduced by the template update. The verifier
now includes `_template` in its memory check and accurately describes the three
required files rather than claiming four.

The template contains `PROJECT.md`, `STATE.md`, and `DIALOG.md`, plus setup and
reporting guidance in `README.md`. Empty legacy `PI.md`/`LOG.md` placeholders
were removed. The PI-owned template charter remains unchanged.

## Additional charter and orientation requirements

| Requirement | Current evidence | Status |
|---|---|---|
| Template follows current documentation | Three memory files; README covers ownership, iteration records, report formats, branding, and automated publication | Scaffold updated; no sample reports rendered |
| Three substantially different visual, information-architecture, and layout alternatives | Three isolated homepage previews and comparison page in `website/projects/vcsserg-repo-v1/designs/`; see `DESIGN-REVIEW.md` | Concept C selected by PI and implemented in homepage/shared styles; rendered QA pending |
| Include each initial Scholar's full charter biography | Profile existence is checked, but biography text is not; Bee's supplied two-sentence bio is restored; Aleph/Ceetown still have abbreviated or altered biographies | Partial; remaining biography fidelity review |
| Executive Summary includes exactly one dense key figure | Current v1 summary has no key figure | Outstanding |
| Use Bootstrap from the official CDN | All 12 pages use Bootstrap 5.3.8 CSS from the previously documented CDN; eight current pages share journal styling | Implemented in website tree; automated deployment pending |

Passing the automated verifier alone does not establish Version 1.0. Its checks
are structural and limited; they do not establish full content or report-format
compliance. Live deployment parity, an observed complete Scholar workflow, and
rendered browser QA remain manual gates. Browser availability was rechecked: no Chromium, Chrome, or Firefox executable
or browser tool was available. No infrastructure was installed.
