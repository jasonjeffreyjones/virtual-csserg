# VCSSERG v1 — Current State

## Status

Active. The public-site foundation is implemented and Version 1.0 now has a
traceable documentation-to-evidence audit. Four of six automated verification
groups pass; the remaining failures are the runner's deployment-script path and
two unpublished initial Scholar profiles.

## What is complete

- `website/index.html`, the VCSSERG v1 Executive Summary, and B. Boring
  Vanilla's profile form a linked static HTML/CSS site with a shared responsive
  visual system.
- `projects/vcsserg-repo-v1/V1-AUDIT.md` maps documented promises to verified,
  failing, partial, or unverified evidence instead of treating Version 1.0 as a
  subjective milestone.
- `projects/vcsserg-repo-v1/verify_v1.py` non-destructively checks repository
  guidance, project memory, every HTML page and local reference, CSS safeguards,
  project and Scholar catalog coverage, runner wiring, and deployment behavior.
- `python/vcsserg_deploy.py` now invokes `rsync` without `shell=True`, validates
  the SSH port, avoids printing configured host/path values, and returns a
  nonzero status when `rsync` is missing or fails.
- The Executive Summary now reports the audit result and identifies both
  automated failures plus the remaining manual gates.

## Current problems and unknowns

- `run-scholar.sh` ends with `python3 vcsserg_deploy.py`, but the script is at
  `python/vcsserg_deploy.py`. The automated iteration can commit and push, then
  fail before deployment. The orientation says Scholars may not edit the runner,
  so Dr. Jones must correct this path.
- The charter names Aleph Initial Alpha, Bee Boring Vanilla, and Ceetown as the
  initial Scholars. Only Bee currently has a public profile and home-page entry.
- Production parity with `website/` is unverified. The execution environment
  could not resolve the production host, and deployment was not run.
- Visual browser QA is unverified because no browser is installed in this
  environment. File-level accessibility and responsive-structure checks pass.
- `PI.md` contains no additional priorities or Version 1.0 acceptance decisions.

## Important files

- `projects/vcsserg-repo-v1/V1-AUDIT.md` — promise-to-evidence matrix
- `projects/vcsserg-repo-v1/verify_v1.py` — automated Version 1.0 verifier
- `python/vcsserg_deploy.py` — deployment implementation
- `run-scholar.sh` — PI-owned automation runner with an open path defect
- `website/index.html` — public front door
- `website/assets/styles.css` — shared visual system
- `website/projects/vcsserg-repo-v1/index.html` — public Executive Summary
- `website/scholars/b-boring-vanilla/index.html` — Bee's Scholar profile
- `projects/vcsserg-repo-v1/LOG.md` — append-only iteration record

## Likely next steps

1. Dr. Jones changes the runner's final command to
   `python3 python/vcsserg_deploy.py`.
2. Publish and catalog profiles for Aleph Initial Alpha and Ceetown.
3. Run the verifier until all six automated groups pass.
4. After deployment, compare the production and local file inventories and bytes,
   then perform desktop/mobile browser QA.
