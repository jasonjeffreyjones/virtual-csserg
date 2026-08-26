# VCSSERG v1 — Current State

## Status

Active. The first public-site foundation is implemented: visitors can move among a substantive home page, the VCSSERG v1 project page, and B. Boring Vanilla's scholar page through a shared static HTML/CSS interface.

## What is complete

- `website/index.html` is now a useful front door with the lab purpose, project catalog, and scholar catalog.
- `website/projects/vcsserg-repo-v1/index.html` publicly explains the project's Version 1.0 charter and current foundation.
- `website/scholars/b-boring-vanilla/index.html` is a full scholar profile connected to the active project.
- `website/assets/styles.css` provides the shared responsive visual system, visible focus states, a skip link, semantic content structure, and reduced-motion behavior without production dependencies.
- All three pages have unique titles and descriptions. Automated checks confirm required document landmarks, balanced CSS, and valid local page, fragment, and asset references.

## Current problems and unknowns

- Visual browser QA has not yet been performed. The execution environment has no headless browser installed and prohibits opening a local HTTP socket.
- The broad Version 1.0 requirement (“everything promised in the documentation works as documented”) still needs a traceable documentation-to-implementation audit beyond this website slice.
- `PI.md` contains no further priorities or definition-of-done decisions.
- Commit, push, and deployment remain pending because this execution environment mounts `.git` read-only; Git could not create `.git/index.lock`. Deployment was intentionally not run against an uncommitted, unpushed tree.

## Important files

- `website/index.html` — public front door
- `website/assets/styles.css` — shared visual system
- `website/projects/vcsserg-repo-v1/index.html` — public project page
- `website/scholars/b-boring-vanilla/index.html` — scholar page
- `projects/vcsserg-repo-v1/PROJECT.md` — stable charter
- `projects/vcsserg-repo-v1/PI.md` — PI direction
- `projects/vcsserg-repo-v1/LOG.md` — append-only iteration record

## Likely next steps

1. Perform desktop and mobile visual QA in a real browser and correct any layout or contrast issues.
2. Turn the Version 1.0 charter into a checklist mapping every documented promise to evidence that it works.
3. Audit the scholar-run and deployment workflows against that checklist, then fix the highest-value gap.
4. From a Git-writable environment, commit and push this iteration, then run `python/vcsserg_deploy.py`.
