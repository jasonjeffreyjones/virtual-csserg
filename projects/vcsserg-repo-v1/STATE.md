# VCSSERG v1 — Current State

## Status

Active. The public site now catalogs all three initial Scholars, and the
deployment component is guarded to mirror the local website rather than leave
stale remote files. Five of six automated verification groups pass. The
remaining automated failure is a completion-logging defect in the PI-owned
Scholar runner.

## What is complete

- `website/index.html`, the VCSSERG v1 Executive Summary, the Scholar directory,
  and all three initial Scholar profiles form a linked static HTML/CSS site with
  a shared responsive visual system.
- Aleph Initial Alpha, B. Boring Vanilla, and Ceetown each have a public profile,
  a home-page catalog entry, and a Scholar-directory entry.
- `projects/vcsserg-repo-v1/V1-AUDIT.md` maps documented promises to verified,
  failing, partial, or unverified evidence instead of treating Version 1.0 as a
  subjective milestone.
- `projects/vcsserg-repo-v1/verify_v1.py` non-destructively checks repository
  guidance, project memory, every HTML page and local reference, CSS safeguards,
  both public catalogs, runner wiring, and deployment behavior.
- `python/vcsserg_deploy.py` invokes `rsync` without `shell=True`, validates the
  SSH port, restricts mirroring to a remote directory named `virtual-csserg`,
  removes stale remote files only after transfer, avoids printing configured
  host/path values, and returns nonzero when `rsync` is missing or fails.
- The Executive Summary reports the current five-of-six automated result and
  identifies the remaining automated and manual gates.

## Current problems and unknowns

- `run-scholar.sh` now invokes the correct deployment path, but its final command
  redirects to `"$LOG_FILE"` without ever assigning `LOG_FILE`. Under `set -u`,
  a successful iteration will deploy and then terminate nonzero while trying to
  record completion. The orientation says Scholars may not edit the runner, so
  Dr. Jones must define the intended log file or remove that redirect.
- Production parity with `website/` remains unverified. Deployment was not run,
  and the protected `.env` was not read. The existing configured remote path
  must end in `virtual-csserg` to satisfy the new deletion safeguard.
- Visual browser QA is unverified because no browser is installed in this
  environment. File-level accessibility and responsive-structure checks pass.
- Whether this bootstrap project needs a Quarto Full Report remains undecided.

## Important files

- `projects/vcsserg-repo-v1/V1-AUDIT.md` — promise-to-evidence matrix
- `projects/vcsserg-repo-v1/verify_v1.py` — automated Version 1.0 verifier
- `python/vcsserg_deploy.py` — guarded exact-mirror deployment implementation
- `run-scholar.sh` — PI-owned runner with an undefined completion-log variable
- `website/index.html` — public front door and complete initial-Scholar catalog
- `website/assets/styles.css` — shared visual system
- `website/projects/vcsserg-repo-v1/index.html` — public Executive Summary
- `website/scholars/index.html` — public Scholar directory
- `website/scholars/aleph-initial-alpha/index.html` — Aleph's profile
- `website/scholars/b-boring-vanilla/index.html` — Bee's profile
- `website/scholars/ceetown/index.html` — Ceetown's profile
- `projects/vcsserg-repo-v1/LOG.md` — append-only iteration record

## Likely next steps

1. Dr. Jones defines `LOG_FILE` in `run-scholar.sh` or removes the final redirect.
2. Run the verifier until all six automated groups pass, then exercise the
   Scholar runner end to end.
3. After deployment, compare the production and local file inventories and bytes.
4. Perform desktop/mobile browser QA and decide whether a Full Report is needed.
