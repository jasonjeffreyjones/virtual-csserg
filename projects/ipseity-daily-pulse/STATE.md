---
title: "Ipseity Daily Pulse"
status: Active
publication: Unpublished
updated: 2026-09-25T10:11:43Z
---

# Ipseity Daily Pulse — Current state

## Status

Active and Unpublished. Research artifacts remain under `projects/`; no empty
public report has been created.

## Current findings and completed work

- Ten daily outside-in checks are recorded. At `2026-09-25T10:07:47Z`, the
  homepage and canonical microdata returned HTTP 200. The 5,067,464-byte gzip
  parsed with the documented schema: 714,574 response observations from
  2025-07-08 through 2026-09-24, 5,053 hashed respondents, 707 signifiers, no
  malformed rows or duplicate canonical keys, and a one-day data lag. No
  anomaly was detected. Since the prior check, the file gained 1,621
  observations and eight respondents, and its latest observation date advanced
  one day. Its SHA-256 is
  `f914207cd3626c6bd8197cb90509b95d6bdd05eca17c21cbe017908de19ffdb8`.
- The current growth table and accessible SVG rise to 714,574 observations
  across 444 observation dates. The accessible monitoring-history SVG aligns
  endpoint and parse status, data lag, and observation count across checks.
  All ten checks were healthy, lag was one day each time, and the canonical
  file gained 14,739 observations from the first check to the latest. This is
  a short operational view, not an uptime or long-run reliability estimate.
- Unweighted linear probability trends remain estimable for 704 signifiers
  meeting the prespecified 300-response, 30-date, and 180-day thresholds. The
  median annualized estimate is +0.5 percentage points; the middle half ranges
  from -1.9 to +3.0 points. `beautiful` is the most positive pooled leader
  (+24.6 points/year), and `star wars fan` is the most negative (-14.2).
- Respondent-clustered inference and both multiplicity screens still yield no
  discovery among 704 tests: zero Benjamini–Hochberg q-values and zero
  Bonferroni-adjusted p-values are at or below .05.
- The two-period sensitivity compares prevalence through 2026-02-14 with
  prevalence from 2026-02-15 onward for the 20 selected linear-trend leaders.
  All 20 raw and all 20 adjusted contrasts retain the linear slope's direction.
  The median absolute raw difference is 10.2 percentage points, and observed
  composition and calendar adjustment moves a contrast by a median absolute
  4.8 points. This is a selected diagnostic, not a discovery test, and its
  point difference is not directly comparable with an annualized slope.
- The four-period shape diagnostic shows that all 20 selected leaders have
  first-to-last raw changes matching their linear slope, but only six move in
  that direction across all three adjacent transitions; 17 align in at least
  two transitions. The largest adjacent move accounts for a median 58% of each
  raw absolute path. `star wars fan` is most concentrated at 96%.
- A new composition-and-calendar-adjusted four-period path standardizes each
  period to the same full-sample observed covariate distribution. All 20
  adjusted endpoints retain the selected slope direction, none aligns in all
  three transitions, and 13 align in at least two. The median largest-move
  share remains 54%, but only eight leaders retain the same largest transition;
  `singer` is most concentrated after adjustment at 80%. Concentration persists
  in aggregate while its apparent timing is composition-sensitive.
- The refreshed composition-and-calendar sensitivity retains the direction of
  all 20 pooled leaders; the median absolute slope shift is 5.3 points/year.
- The three-way leader panel now has 16 of 20 repeat-sample slopes retaining
  the all-response direction, 14 of 20 within-person slopes retaining the
  repeat-sample direction, and 12 of 20 retaining the original direction. The
  median absolute shifts are 12.4 points/year for sample restriction, 15.0 for
  absorbing respondent effects, and 13.3 end to end; the median signifier has
  26 repeat respondents. Three signifiers have no endorsement switchers, so
  their zero within slopes and intervals are mechanical rather than precise
  population evidence.
- A new internal outreach draft explains that adjustment preserves average
  path concentration but often changes which transition appears largest. It
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
- Treat the composition-and-calendar, raw and adjusted early-versus-late, raw
  and standardized adjusted four-period trajectory, repeat-sample pooled, and
  respondent-fixed-effect models as selected-leader sensitivities, not
  replacement estimands or multiplicity corrections. The early/late contrast relaxes straight-line form
  but can hide shorter reversals; its adjusted version addresses recorded
  composition and calendar terms only. The raw four-period path is unweighted;
  its adjusted counterpart standardizes non-period model columns to full-sample
  means. Both are noninferential, and their concentration share describes the
  largest adjacent move relative to total absolute movement. Unbounded adjusted
  linear-probability levels are model diagnostics rather than literal
  prevalences when outside 0%–100%. The repeat-sample and fixed-effect shifts
  are not a causal turnover decomposition.
- Do not interpret nominal intervals excluding zero as discoveries when none
  of the 704 primary tests passes either multiplicity screen. Do not interpret
  a zero sandwich interval as precision when repeat respondents never change
  their outcome.
- Treat the ten-check history view as evidence about the sampled moments,
  not continuous availability or a service-level estimate.
- Keep outreach material internal until the PI establishes a publication
  surface and approval/posting workflow.

## Important files

- `PROJECT.md`: PI-owned charter.
- `CURRENT-FINDINGS.md`: replaceable reader-facing current results and sources.
- `ANALYSIS.md` and `analysis/monitor.py`: method, reproduction, live monitor,
  clustered inference, multiplicity adjustment, leader sensitivities, and
  artifact generation.
- `data/monitoring-history.csv`: append-only outside-in check history.
- `outputs/`: current summary, growth tables, full trend estimates, four
  leader sensitivity tables, and eight accessible SVGs.
- `tests/test_monitor.py`: synthetic validation, inference, sensitivity, and
  artifact consistency tests.
- `outreach/`: workflow recommendation and internal content drafts.
- `DIALOG.md`, `dialog/iterations/`, and `dialog/indexes/`: bounded handoff and
  immutable iteration history.

## Problems and unresolved PI questions

- Ten history rows establish nine healthy daily intervals and a useful first
  operational view, but not enough evidence to characterize service
  reliability or interruptions between checks.
- No signifier slope survives either multiplicity adjustment. Leader
  sensitivities use small, selected subsets and do not address population
  weighting, time-varying confounding, selective retention, or changing
  unobserved composition. The raw and adjusted four-period patterns also depend
  on the chosen calendar partition; the adjusted timing result is
  model-sensitive and supplies no new inferential test.
- Should Virtual CSSERG adopt the proposed shared, Project-organized outreach
  feed in which Scholars leave evidence-linked drafts and Dr. Jones approves or
  posts them? Until guidance arrives, drafts remain internal and unpublished.

## Likely next steps

1. On the next UTC day, run the live monitor once; investigate only if its
   anomaly field is not `none`.
2. Continue the check history so the operational view can eventually
   distinguish isolated from continuing failures and summarize longer-run lag.
3. Assess whether the dominant-transition and concentration conclusions are
   robust to reasonable alternative period boundaries or segment counts,
   while retaining the linear primary estimand and all selection and
   multiplicity cautions.
4. Incorporate PI outreach guidance and keep public trend claims deferred until
   robustness evidence is stronger.
