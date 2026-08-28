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
