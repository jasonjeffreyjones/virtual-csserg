# VCSSERG v1 — Current State

## Status

Active. On September 11, 2026, four of six automated verification groups pass.
Dr. Jones selected Concept C (research journal) and requested a GitHub repository
footer link. That decision is implemented in `website/`, ready for the normal
post-iteration automated publication. Version 1.0 is not yet complete.

## Completed work and current evidence

- Three distinct design alternatives remain as archived homepage prototypes with
  a comparison page. Selection labels now reflect the PI decision.
- The homepage adopts C's research lead, notebook entries, and contextual sidebar
  with project and Scholar navigation. Content reflects current project records;
  Predict the Self development findings remain provisional, with test scores pending.
- Eight current HTML pages use Bootstrap CDN CSS and shared journal styling:
  warm paper, serif typography, editorial rules, responsive layouts. The existing
  Full Report retains its specialized contents/table styles. Four archived design
  pages retain their scoped styles and Bootstrap.
- All 12 HTML pages include the GitHub repository link in their footer. The
  verifier enforces this; a temporary copied-site fixture passes before removing
  a footer link and fails after removal. All 12 pages and 3 stylesheets pass
  structural/local-link checks. This does not establish visual or full publication compliance.
- Bee's profile now uses the assigned name and exact supplied biography.
- `_template` has the three required memory files and reporting/workflow guidance;
  its README also records journal styling and the GitHub footer requirement.
- Repository guidance, runner wiring, and mocked deployment behavior pass.
  Deployment uses guarded, shell-free rsync mirroring and propagates failures.

## Current problems and decisions

- `nfl-team-fandom-identities` and `predict-the-self` lack `DIALOG.md`; legacy
  research records need careful migration without changing PI text.
- NFL lacks `website/projects/nfl-team-fandom-identities/index.html`.
- Aleph/Ceetown profiles still abbreviate or alter charter biographies; compare
  against the charter before restoring full supplied text. The verifier checks
  existence, not biography fidelity.
- The v1 Executive Summary still lacks its required dense key figure.
- Live production parity, an observed complete Scholar workflow, and rendered
  desktop/mobile QA remain unverified. No Chromium, Chrome, Firefox, or browser
  tool was available this iteration. No replacement infrastructure was installed.
- The v1 charter exempts this project from a Quarto Full Report.
- Bootstrap CDN access is needed for Bootstrap styling; core journal layouts and
  typography are also defined locally. No JavaScript or new build dependency added.

## Resources

September 11 preflight: Python 3.12.3, R 4.3.3, Quarto 1.10.18; hard ceiling of
1 CPU, 3000M memory, 55 minutes, no Scholar swap. Lightweight local file processing
and standard-library validation fit this envelope; no installations or agents used.

## Important files

- `projects/_template/`: project scaffold and reporting checklist.
- `projects/vcsserg-repo-v1/verify_v1.py`: non-destructive automated checks.
- `projects/vcsserg-repo-v1/V1-AUDIT.md`: promise-to-evidence matrix and open gates.
- `projects/vcsserg-repo-v1/DESIGN-REVIEW.md`: selected design, provenance, QA route.
- `website/projects/vcsserg-repo-v1/designs/`: archived alternatives and comparison.
- `website/index.html`, `website/assets/styles.css`: selected journal implementation.
- `website/projects/vcsserg-repo-v1/index.html`: public Executive Summary.
- `python/vcsserg_deploy.py`: deployment component.
- `run-scholar.sh`: PI-owned automation; Scholars must not edit it.

## Unresolved PI questions and next steps

No blocking PI question; design selection is resolved. Perform rendered QA when
a browser is available. Address memory migration, missing NFL public output,
remaining biography fidelity, and the summary figure; rerun verification.
Automation handles commit, push, and deployment after this iteration.
