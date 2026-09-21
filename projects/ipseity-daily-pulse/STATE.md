---
title: "Ipseity Daily Pulse"
status: Active
publication: Unpublished
updated: 2026-09-21T10:09:51Z
---

# Ipseity Daily Pulse — Current state

## Status

Active and Unpublished. Research artifacts remain under `projects/`; no empty
public report has been created.

## Current findings and completed work

- Six daily outside-in checks are recorded. At `2026-09-21T10:06:18Z`, the
  homepage and canonical microdata returned HTTP 200. The 5,019,234-byte gzip
  parsed with the documented schema: 707,998 response observations from
  2025-07-08 through 2026-09-20, 5,021 hashed respondents, 707 signifiers, no
  malformed rows or duplicate canonical keys, and a one-day data lag. No
  anomaly was detected. Since the prior check, the file gained 1,573
  observations and 11 respondents, and its latest observation date advanced
  one day. Its SHA-256 is
  `83ee777095ffb9b44f26d222177cf387cb1db96e885b369f6570d1ba4509c519`.
- The current growth table and accessible SVG rise to 707,998 observations
  across 430 observation dates. Six history rows remain one short of the
  planned seven-check operational view.
- Unweighted linear probability trends remain estimable for 704 signifiers
  meeting the prespecified 300-response, 30-date, and 180-day thresholds. The
  median annualized estimate is +0.6 percentage points; the middle half ranges
  from -1.7 to +3.2 points. `beautiful` is the most positive pooled leader
  (+22.9 points/year), and `nba fan` is the most negative (-14.6).
- Respondent-clustered inference and both multiplicity screens still yield no
  discovery among 704 tests: zero Benjamini–Hochberg q-values and zero
  Bonferroni-adjusted p-values are at or below .05.
- A new two-period sensitivity splits the full observation window at
  2026-02-12 and compares late-half with early-half prevalence for the 20
  selected linear-trend leaders. All 20 contrasts retain the linear slope's
  direction; their median absolute difference is 9.4 percentage points.
  `beautiful` rises from 33.2% to 50.7%, a +17.5-point contrast with a
  respondent-clustered 95% interval from +8.4 to +26.7. This is a selected
  diagnostic, not a discovery test, and its point difference is not directly
  comparable with an annualized slope.
- The refreshed composition-and-calendar sensitivity retains the direction of
  all 20 pooled leaders; the median absolute slope shift is 5.6 points/year.
- The three-way leader panel now has 17 of 20 repeat-sample slopes retaining
  the all-response direction, 15 of 20 within-person slopes retaining the
  repeat-sample direction, and 12 of 20 retaining the original direction. The
  median absolute shifts are 11.7 points/year for sample restriction, 13.4 for
  absorbing respondent effects, and 13.8 end to end; the median signifier has
  26 repeat respondents. Two signifiers have no endorsement switchers, so
  their zero within slopes and intervals are mechanical rather than precise
  population evidence.
- A new internal outreach draft explains the two-period robustness check. It
  remains unpublished pending PI guidance.

## Decisions and constraints

- Follow `PROJECT.md` and observe Ipseity Daily only from outside. Only the PI
  edits the charter or the production Ipseity Daily system.
- A live monitor run appends history. Routine validation must use unit tests or
  a saved file with `--no-history`; do not repeat a network check on the same
  UTC day absent a suspected failure.
- Keep the unweighted pooled daily slope as the charter-requested descriptive
  point estimate. Use respondent-clustered intervals and both BH and Bonferroni
  adjustments for the primary screen.
- Treat the composition-and-calendar, early-versus-late, repeat-sample pooled,
  and respondent-fixed-effect models as selected-leader sensitivities, not
  replacement estimands or multiplicity corrections. The early/late contrast
  relaxes straight-line form but can hide shorter reversals and changing
  composition. The repeat-sample and fixed-effect shifts are not a causal
  turnover decomposition.
- Do not interpret nominal intervals excluding zero as discoveries when none
  of the 704 primary tests passes either multiplicity screen. Do not interpret
  a zero sandwich interval as precision when repeat respondents never change
  their outcome.
- Keep outreach material internal until the PI establishes a publication
  surface and approval/posting workflow.

## Important files

- `PROJECT.md`: PI-owned charter.
- `CURRENT-FINDINGS.md`: replaceable reader-facing current results and sources.
- `ANALYSIS.md` and `analysis/monitor.py`: method, reproduction, live monitor,
  clustered inference, multiplicity adjustment, leader sensitivities, and
  artifact generation.
- `data/monitoring-history.csv`: append-only outside-in check history.
- `outputs/`: current summary, growth tables, full trend estimates, three
  leader sensitivity tables, and five accessible SVGs.
- `tests/test_monitor.py`: synthetic validation, inference, sensitivity, and
  artifact consistency tests.
- `outreach/`: workflow recommendation and internal content drafts.
- `DIALOG.md`, `dialog/iterations/`, and `dialog/indexes/`: bounded handoff and
  immutable iteration history.

## Problems and unresolved PI questions

- Six history rows establish five healthy daily intervals, not enough evidence
  to characterize service reliability. The planned one-week operational view
  becomes available after the next successful daily check.
- No signifier slope survives either multiplicity adjustment. Leader
  sensitivities use small, selected subsets and do not address population
  weighting, time-varying confounding, selective retention, or changing
  unobserved composition.
- Should Virtual CSSERG adopt the proposed shared, Project-organized outreach
  feed in which Scholars leave evidence-linked drafts and Dr. Jones approves or
  posts them? Until guidance arrives, drafts remain internal and unpublished.

## Likely next steps

1. On the next UTC day, run the live monitor once; investigate only if its
   anomaly field is not `none`.
2. After the seventh history row, add a compact check-history visualization for
   endpoint status, data lag, and observation growth across checks.
3. Test whether the selected early/late contrasts persist after observed
   composition and calendar adjustment, while retaining the linear primary
   estimand and all selection and multiplicity cautions.
4. Incorporate PI outreach guidance and keep public trend claims deferred until
   robustness evidence is stronger.
