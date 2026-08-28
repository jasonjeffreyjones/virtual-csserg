# VCSSERG v1 — Current State

## Status

Active. All six automated verification groups pass. The public site catalogs
all three initial Scholars, carries the required CSSERG branding on every page,
and has a guarded deployment component designed to mirror the local website.
Live production parity, an end-to-end Scholar run, and rendered browser QA are
not yet verified.

## What is complete

- `website/index.html`, the VCSSERG v1 Executive Summary, the Scholar directory,
  and all three initial Scholar profiles form a linked static HTML/CSS site with
  a shared responsive visual system.
- Every public page uses the CSSERG logo, favicon, forest/Artichoke/Laurel green
  palette, and a common footer linking Dr. Jason Jeffrey Jones, CSSERG, and the
  CC BY 4.0 International license badge.
- Aleph Initial Alpha, B. Boring Vanilla, and Ceetown each have a public profile,
  a home-page catalog entry, and a Scholar-directory entry.
- `projects/vcsserg-repo-v1/V1-AUDIT.md` maps documented promises to verified,
  failing, partial, or unverified evidence instead of treating Version 1.0 as a
  subjective milestone.
- `projects/vcsserg-repo-v1/verify_v1.py` non-destructively checks repository
  guidance, project memory, every HTML page and local reference, CSS safeguards,
  CSSERG branding and footer requirements, both public catalogs, runner wiring,
  and deployment behavior.
- `python/vcsserg_deploy.py` invokes `rsync` without `shell=True`, validates the
  SSH port, restricts mirroring to a remote directory named `virtual-csserg`,
  removes stale remote files only after transfer, avoids printing configured
  host/path values, and returns nonzero when `rsync` is missing or fails.
- Dr. Jones' `run-scholar.sh` fix replaces the undefined `LOG_FILE` reference
  with the defined per-iteration path used for Scholar output; shell syntax and
  the verifier's runner-wiring check pass.
- The Executive Summary reports the current six-of-six automated result and
  identifies the remaining manual gates.
- The charter explicitly exempts this bootstrap project from a Quarto Full
  Report; the required Executive Summary is present.

## Current problems and unknowns

- The corrected `run-scholar.sh` completion path is verified statically but the
  full pull/Scholar/commit/rebase/push/deploy/completion sequence has not yet
  been observed end to end.
- Production parity with `website/` remains unverified. Deployment was not run,
  and the protected `.env` was not read. The existing configured remote path
  must end in `virtual-csserg` to satisfy the new deletion safeguard.
- Visual browser QA is unverified because no browser is installed in this
  environment. File-level accessibility and responsive-structure checks pass.

## Important files

- `projects/vcsserg-repo-v1/V1-AUDIT.md` — promise-to-evidence matrix
- `projects/vcsserg-repo-v1/verify_v1.py` — automated Version 1.0 verifier
- `python/vcsserg_deploy.py` — guarded exact-mirror deployment implementation
- `run-scholar.sh` — PI-owned runner with corrected per-iteration completion logging
- `website/index.html` — public front door and complete initial-Scholar catalog
- `website/assets/styles.css` — shared visual system
- `website/images/csserg-transparent-logo.png` — shared header brand mark
- `website/projects/vcsserg-repo-v1/index.html` — public Executive Summary
- `website/scholars/index.html` — public Scholar directory
- `website/scholars/aleph-initial-alpha/index.html` — Aleph's profile
- `website/scholars/b-boring-vanilla/index.html` — Bee's profile
- `website/scholars/ceetown/index.html` — Ceetown's profile
- `projects/vcsserg-repo-v1/LOG.md` — append-only iteration record

## Likely next steps

1. Observe a complete Scholar runner execution and confirm its completion line
   is appended after a successful deploy.
2. After deployment, compare the production and local file inventories and bytes.
3. Perform desktop/mobile browser QA, including the cropped header logo and
   wrapping footer at narrow widths.
