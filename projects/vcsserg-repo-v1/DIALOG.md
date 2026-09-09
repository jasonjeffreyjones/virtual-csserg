# Project Title

Below are log entries from Scholars. This is an append-only file.

## 2026-08-26 — B. Boring Vanilla

- Starting work time: 2026-08-26 21:31:42 UTC
- Project: VCSSERG v1 (`vcsserg-repo-v1`)
- Planned scope: Audit the current static site and implement one foundational Version 1.0 slice, then validate, document, commit, push, and deploy it.
- Work completed:
  - Replaced the placeholder home page with a semantic public front door describing Virtual CSSERG's purpose and linking its current project and scholar.
  - Replaced B. Boring Vanilla's placeholder with a complete scholar profile and current-project link.
  - Created the public VCSSERG v1 project page.
  - Created one dependency-free responsive stylesheet shared by all pages, including keyboard focus treatment, a skip link, and reduced-motion support.
  - Updated `STATE.md` with the current implementation, limitations, important files, and next steps.
- Validation:
  - A repository-local HTML parser checked all 3 pages for language, title, main landmark, H1, duplicate IDs, local files, and fragments; all checks passed.
  - CSS brace-balance, responsive-breakpoint, and reduced-motion checks passed.
  - `git diff --check` passed.
- Problems encountered: The sandbox prohibits opening a local HTTP socket, and no headless browser package is installed, so browser-rendered visual QA was not possible in this iteration. File-level structural and link checks were used instead.
- Question for Dr. Jones: Beyond the documented scholar workflow and public site, are there specific behaviors you consider mandatory for Version 1.0?
- Proposed next step: Build a documentation-to-implementation checklist, then visually QA this foundation and address the highest-value uncovered workflow gap.
- Ending work time: 2026-08-26 21:38:57 UTC
- Post-iteration operations (2026-08-26 21:40:02 UTC): The required commit could not be created because the environment mounts `.git` read-only (`.git/index.lock`: read-only file system). Push and deployment were therefore not attempted; deploying an uncommitted, unpushed tree would violate the required operation order. All work remains present in the working tree for completion from a Git-writable environment.

## 2026-08-28 — B. Boring Vanilla

- Starting work time: 2026-08-28 15:14:57 UTC
- Project: VCSSERG v1 (`vcsserg-repo-v1`)
- Planned scope: Convert the Version 1.0 charter into a reproducible
  documentation-to-evidence audit, then harden the deployment component exposed
  by that audit without editing the PI-owned Scholar runner.
- Work completed:
  - Added `V1-AUDIT.md`, which maps documented promises to verified, failing,
    partial, or unverified evidence and identifies automated versus manual gates.
  - Added `verify_v1.py`, a non-destructive standard-library verifier covering
    repository guidance, project memory, static HTML/CSS and local navigation,
    public catalog coverage, Scholar-runner wiring, and deployment behavior.
  - Hardened `python/vcsserg_deploy.py`: replaced `shell=True` with an argument
    list, validated the SSH port, stopped printing configured destination values,
    and made missing/failed `rsync` operations exit nonzero.
  - Published the audit result in the project's Executive Summary and replaced
    stale project state with the current evidence, blockers, and next steps.
- Validation:
  - Python compilation and `bash -n run-scholar.sh` passed.
  - Four of six verifier groups pass. The two expected failures precisely report
    missing Aleph/Ceetown profiles and the runner's nonexistent deployment path.
  - Mocked deployment tests confirm shell-free invocation, SSH-port validation,
    and nonzero propagation for both failed and missing `rsync`.
  - Scoped `git diff --check` and new-file trailing-whitespace checks passed.
- Problems encountered:
  - `run-scholar.sh` calls `python3 vcsserg_deploy.py`, but the file is
    `python/vcsserg_deploy.py`. Per the orientation, I did not edit the runner.
    Dr. Jones should change its final command to
    `python3 python/vcsserg_deploy.py`.
  - Production parity could not be tested because the environment could not
    resolve the production host. Browser QA also remains unavailable because no
    browser is installed.
  - A repository-wide `git diff --check` is noisy from trailing whitespace in
    pre-existing PI-owned changes to `RESEARCHER-ORIENTATION.md` and `PROJECT.md`;
    neither file was edited during this iteration.
- Question for Dr. Jones: Should this bootstrap project receive a Quarto Full
  Report, or are the five-minute Executive Summary and repository audit the
  intended reporting level?
- Proposed next step: Correct the runner path, publish and catalog Aleph and
  Ceetown, rerun all six automated groups, then perform production-parity and
  desktop/mobile browser checks.
- Ending work time: 2026-08-28 15:23:02 UTC

## 2026-08-28 — B. Boring Vanilla

- Starting work time: 2026-08-28 15:49:43 UTC
- Project: VCSSERG v1 (`vcsserg-repo-v1`)
- Planned scope: Implement the PI-prioritized public Scholar catalog and the
  missing Aleph Initial Alpha and Ceetown profiles, then re-review the corrected
  deployment path and update the Version 1.0 evidence.
- Work completed:
  - Published profiles for Aleph Initial Alpha and Ceetown, added a Scholar
    directory linking all three initial Scholars, expanded the home-page roster,
    and connected profile and project navigation to the directory.
  - Re-reviewed `python/vcsserg_deploy.py` and corrected an exact-parity gap:
    `rsync` now removes stale remote files after transfer. Added a guard that
    permits this mirroring only when the configured destination directory is
    named `virtual-csserg`.
  - Extended `verify_v1.py` to require the Scholar directory and its roster
    links, verify stale-file deletion and the remote-path guard, and detect an
    undefined completion-log variable in the Scholar runner.
  - Updated the audit, current state, and public Executive Summary from the new
    evidence.
- Validation:
  - Python compilation and `bash -n run-scholar.sh` passed.
  - Five of six verifier groups pass. The public catalogs and guarded deployment
    component pass; the sole expected failure precisely reports the PI-owned
    runner's undefined `LOG_FILE`.
  - All 6 HTML pages and the shared stylesheet passed structural, metadata,
    unique-title/ID, local-link, fragment, responsive, and reduced-motion checks.
  - `git diff --check` passed.
- Problems encountered:
  - The corrected runner invokes deployment successfully, but then redirects its
    completion message to `"$LOG_FILE"` even though `LOG_FILE` is never assigned.
    Under `set -u`, the run ends nonzero after deployment. Per the orientation, I
    did not edit `run-scholar.sh`.
  - Production parity and rendered desktop/mobile QA remain unverified. I did not
    deploy or read the protected `.env`; the configured remote path must end in
    `virtual-csserg` for the new deletion safeguard.
- Question for Dr. Jones: Should the runner's final completion message append to
  the existing per-iteration file at
  `$LOG_DIR/${SCHOLAR_NAME}_${PROJECT_NAME}.log`, or did you intend a separate
  completion log?
- Proposed next step: Correct the runner's completion-log target, rerun all six
  checks and the complete Scholar workflow, then compare deployed bytes and
  perform desktop/mobile browser QA.
- Ending work time: 2026-08-28 15:55:26 UTC

## 2026-08-28 — B. Boring Vanilla

- Starting work time: 2026-08-28 16:53:17 UTC
- Project: VCSSERG v1 (`vcsserg-repo-v1`)
- Planned scope: Complete the PI-prioritized branding revision across every
  public HTML page and the shared stylesheet, validate Dr. Jones' runner-log
  fix, and make the branding requirements reproducibly testable.
- Work completed:
  - Revised all six public HTML pages to use the provided CSSERG logo and
    favicon, plus a shared footer linking Dr. Jason Jeffrey Jones, CSSERG, and
    the official CC BY 4.0 International deed through its standard badge.
  - Reworked the shared palette around forest green, Artichoke Green `#4B6F44`,
    and Laurel Green `#dde3d8`; added responsive footer and cropped-logo styles.
  - Extended `verify_v1.py` so every page must use the CSSERG logo and complete
    branded footer, and every stylesheet must contain the specified Artichoke
    and Laurel colors.
  - Evaluated Dr. Jones' `run-scholar.sh` change. The final completion message
    now uses the same defined per-iteration path as Scholar output, eliminating
    the unbound `LOG_FILE` failure under `set -u`; I did not edit the runner.
  - Re-reviewed `python/vcsserg_deploy.py`. Static inspection and the existing
    mocked success/failure/path-safety checks exposed no new problem.
  - Updated the audit, current state, and public Executive Summary to report the
    six-of-six automated result and the remaining manual gates.
- Validation:
  - All six verifier groups pass, including every local reference across all 6
    HTML pages, the branded footer/logo/palette assertions, runner wiring, and
    guarded deployment behavior.
  - Python compilation, `bash -n run-scholar.sh`, and `git diff --check` pass.
  - The Creative Commons canonical CC BY 4.0 deed and official badge asset were
    reachable when checked.
- Problems encountered:
  - Production parity and the full Scholar workflow remain unverified because I
    did not deploy, run commit/push automation, or read the protected `.env`.
  - No browser is installed, so the new logo crop and footer wrapping could not
    receive rendered desktop/mobile QA; file-level responsive checks pass.
- Question for Dr. Jones: None this iteration.
- Proposed next step: Observe the completed Scholar workflow, compare deployed
  files and bytes with `website/`, and visually inspect desktop/mobile layouts.
- Ending work time: 2026-08-28 17:08:16 UTC
