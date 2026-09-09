# VCSSERG v1 — Current State

## Status

Active. On September 9, 2026, four of six automated verification groups pass.
Three substantially different homepage design previews and a comparison page
are ready for PI review. The current production design remains in place.

## Completed work and current evidence

- The static site has shared branding, linked Scholar profiles, and the v1
  Executive Summary. All 12 HTML pages and 3 stylesheets pass the verifier's
  structural and local-link checks; this is not full publication compliance.
- `_template` now has the three required memory files and a README covering
  charter ownership, iteration timing, report formats, branding, and publication.
  Empty legacy PI/LOG placeholders were removed; `PROJECT.md` was not edited.
- `verify_v1.py` includes `_template` in memory checks and correctly reports
  three required files. Temporary-fixture checks confirm that a complete template
  passes and removal of its DIALOG file fails.
- Repository guidance, static HTML/CSS, runner wiring, and mocked deployment
  behavior pass. Deployment uses guarded, shell-free rsync mirroring and
  propagates failures. No live deployment was performed by this Scholar.
- `V1-AUDIT.md` and the public summary now disclose current failures and the
  new charter's outstanding design work.

## Current problems and decisions

- `nfl-team-fandom-identities` and `predict-the-self` lack `DIALOG.md`; existing
  legacy research records need careful migration without changing PI text.
- The NFL project lacks `website/projects/nfl-team-fandom-identities/index.html`.
- Three alternatives are implemented: research directory, evidence observatory,
  and research journal. Each differs in visual design, information architecture,
  and layout. They are isolated homepage prototypes; links open existing project
  and Scholar pages. PI selection is pending before a site-wide replacement.
- Initial Scholar biographies need comparison with the charter: Bee's profile
  omits the supplied biography. The verifier checks profile existence, not text.
- The v1 Executive Summary lacks its required dense key figure. Existing v1 pages
  retain custom CSS; the four preview/comparison pages use the official
  documentation's Bootstrap CDN with an integrity hash.
- Live production parity, an observed complete Scholar workflow, and rendered
  desktop/mobile QA remain unverified. This iteration found no Chromium,
  Chrome, or Firefox executable and no browser tool; rendered QA is outstanding.
- The v1 charter exempts this project from a Quarto Full Report.

## Resources

This iteration's preflight reports Python 3.12.3, R 4.3.3, Quarto 1.10.18,
and a hard ceiling of 1 CPU, 3000M memory, 55 minutes, with no Scholar swap.
The work used lightweight local file processing and installed no software.

## Important files

- `projects/_template/`: project scaffold and reporting checklist.
- `projects/vcsserg-repo-v1/verify_v1.py`: non-destructive automated checks.
- `projects/vcsserg-repo-v1/V1-AUDIT.md`: promise-to-evidence matrix and open gates.
- `projects/vcsserg-repo-v1/DESIGN-REVIEW.md`: design rationale, provenance, and review route.
- `website/projects/vcsserg-repo-v1/designs/`: comparison page, three previews, scoped CSS.
- `projects/vcsserg-repo-v1/DIALOG.md`: append-only iteration record.
- `website/projects/vcsserg-repo-v1/index.html`: public Executive Summary.
- `website/assets/styles.css`: current production visual system.
- `python/vcsserg_deploy.py`: deployment component.
- `run-scholar.sh`: PI-owned automation; Scholars must not edit it.

## Unresolved PI questions and next steps

PI review question: select the directory, observatory, journal, a combination,
or another direction; concrete previews are now linked from the v1 summary.
While selection is pending, address memory migration, missing public project
output, biography fidelity, and summary requirements. Rerun verification and arrange browser/production
checks before claiming Version 1.0 is complete. Automation handles commit, push,
and deployment after this iteration.
