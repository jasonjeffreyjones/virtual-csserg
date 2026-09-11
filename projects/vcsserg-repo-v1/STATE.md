# VCSSERG v1 — Current State

## Status

Active. On September 11, 2026, six of seven automated promise groups pass.
Version 1.0 is not complete because required report artifacts and manual
publication/workflow evidence remain open. The current charter now requires all
three report forms for this bootstrap Project; the former Full Report exemption
is obsolete.

## Completed work and current evidence

- `website/projects/index.html` now resolves as the public all-Projects index.
  It links all three Projects in descending order of their latest substantive
  project record: VCSSERG v1, NFL Team Fandom Identities, Predict the Self.
- The homepage heading is “Research Updates from Virtual CSSERG.” The rejected
  “Inquiry, in public.” headline is gone. Primary headers use internal Home,
  Projects, and Scholars navigation; external institutional/source/license
  links remain in footers.
- Three isolated Project Executive Summary alternatives compare an evidence
  brief, research poster, and field-notes layout. Three Scholar-directory
  alternatives compare a portrait roster, work map, and field guide. No new
  production design is presumed pending PI review.
- All three initial Scholar profiles contain the complete charter biographies.
  This is enforced with normalized text comparison rather than mere profile
  existence.
- Predict the Self now has the current `DIALOG.md` memory file; legacy `LOG.md`
  and `PI.md` remain unchanged. Every Project and `_template` now has the three
  required memory files.
- The production v1 Executive Summary now includes exactly one dense key figure
  showing the automated promise map and links both new design reviews.
- The NFL Full Report's Quarto footer source and generated HTML retain the
  required GitHub repository link.

## Verifier assessment

`verify_v1.py` is a promise regression suite, not a Version 1 certification.
The earlier version had false positives (omitted report formats, project index,
and biography fidelity) and false negatives (applied first-party design rules to
vendored Quarto CSS and rejected a valid multi-H1 Quarto book hierarchy).

The verifier now has seven groups. It checks automatable parts of the three-form
report contract, including summary figure count, local cross-links, Quarto book
source/configuration, PDF signature, and the exact Full Report phrase. Design
assertions apply to first-party CSS; third-party libraries still participate in
local-reference checking through their HTML consumers. The Projects directory,
declared update order, and full charter biographies are checked.

Six groups pass: repository guidance, project memory, static HTML/CSS, public
catalogs, runner wiring, and guarded deployment behavior. Report formats fail:

- VCSSERG v1 lacks a Quarto Full Report and short PDF.
- Predict the Self lacks a short PDF and summary figure, and its direct-HTML
  report lacks current Quarto book configuration and the required phrase.

The generic check does not validate PDF page count/columns, substantive research
quality, production parity, rendered usability, or observed automation.

## Current design and governance recommendations

`V1-RECOMMENDATIONS.md` records the requested opinions. Current recommendations:

- Select Executive Summary **A (evidence brief)** as the reusable default.
- Select Scholar directory **A (portrait roster)** for Version 1; add a work map
  later when the group is larger.
- Keep Quarto HTML books as the default Full Report, using direct HTML only as a
  documented temporary runtime contingency.
- Permit generated Scholar self-representations only as clearly illustrative,
  provenance-recorded, non-biographical assets; keep monograms as the default.
- Do not prepend to `DIALOG.md`. Migrate, after PI approval and documentation
  changes, toward one uniquely named immutable file per iteration plus a short
  newest-first index.
- Use lifecycle states Proposed, Active, Blocked, Paused, Completed, Archived;
  track review/publication readiness separately.
- Replace manual template copying with a small validated, no-overwrite scaffold
  command while retaining PI authorship of `PROJECT.md` and withholding public
  listing until substantive content exists.

## Current problems and manual gates

- Build and validate outstanding report forms. This is the only failing
  automated group.
- Live production parity, one observed complete Scholar workflow, and rendered
  desktop/mobile/keyboard/assistive-technology QA remain unverified.
- The Project update order is manually encoded. A durable source of truth for
  `title`, `status`, and `updated` is still underspecified.
- New summary and Scholar-directory selections await PI review.
- Archived September 9 homepage prototypes contain dated evidence and are
  explicitly labeled as archived; they should not be read as current reports.

## Resources and limitations

September 11 preflight: 2 logical CPUs and 3.7 GiB host RAM; enforced ceiling of
1 CPU, 3000M memory, 55 minutes, no Scholar swap. Installed tools include Python
3.12.3, R 4.3.3, and Quarto 1.10.18. Work used lightweight file processing and
standard-library validation. No software or agents were installed or used.
No local Chromium, Chrome, or Firefox executable/browser tool is available, so
rendered QA remains open. The NFL publication verifier could not start because
its declared `pypdf` package is absent from this host; no package was installed
for the small footer-only change, which is covered by the v1 structural check.
No credentials were accessed and no deployment run.

## Important files

- `projects/vcsserg-repo-v1/V1-AUDIT.md`: current promise/evidence matrix.
- `projects/vcsserg-repo-v1/V1-RECOMMENDATIONS.md`: requested design and
  governance opinions with rationale.
- `projects/vcsserg-repo-v1/verify_v1.py`: non-destructive automated checks.
- `website/projects/index.html`: public Project directory.
- `website/projects/vcsserg-repo-v1/designs/project-summaries/`: three Project
  Executive Summary alternatives and comparison.
- `website/projects/vcsserg-repo-v1/designs/scholar-directories/`: three Scholar
  directory alternatives and comparison.
- `website/index.html`, `website/assets/styles.css`: selected journal system.
- `website/projects/vcsserg-repo-v1/index.html`: production Executive Summary.
- `python/vcsserg_deploy.py`: guarded deployment component.
- `run-scholar.sh`: PI-owned automation; Scholars must not edit it.

## Unresolved PI questions and likely next steps

No blocking question. PI choices requested: select or combine one Project
Executive Summary alternative and one Scholar-directory alternative; accept,
revise, or reject the proposed image, dialog, state, and project-creation
policies. Independent next work is to produce the VCSSERG v1 Quarto Full Report
first, derive its two-column short PDF, then address Predict the Self publication
gaps and complete the manual gates. Automation handles commit, push, and
deployment after this iteration.
