---
title: "Ipseity Daily Pulse"
status: Active
publication: Unpublished
updated: 2026-09-23T10:13:36Z
---

# Ipseity Daily Pulse — Current state

## Status

Active and Unpublished. Research artifacts remain under `projects/`; no empty
public report has been created.

## Current findings and completed work

- Eight daily outside-in checks are recorded. At `2026-09-23T10:09:23Z`, the
  homepage and canonical microdata returned HTTP 200. The 5,043,580-byte gzip
  parsed with the documented schema: 711,318 response observations from
  2025-07-08 through 2026-09-22, 5,037 hashed respondents, 707 signifiers, no
  malformed rows or duplicate canonical keys, and a one-day data lag. No
  anomaly was detected. Since the prior check, the file gained 1,659
  observations and nine respondents, and its latest observation date advanced
  one day. Its SHA-256 is
  `4badcfea9c902355a2de9215fa1af4beda935758eabd57b24994106406253b10`.
- The current growth table and accessible SVG rise to 711,318 observations
  across 432 observation dates. The accessible monitoring-history SVG aligns
  endpoint and parse status, data lag, and observation count across checks.
  All eight checks were healthy, lag was one day each time, and the canonical
  file gained 11,483 observations from the first check to the latest. This is
  a short operational view, not an uptime or long-run reliability estimate.
- Unweighted linear probability trends remain estimable for 704 signifiers
  meeting the prespecified 300-response, 30-date, and 180-day thresholds. The
  median annualized estimate is +0.6 percentage points; the middle half ranges
  from -1.7 to +3.1 points. `beautiful` is the most positive pooled leader
  (+24.3 points/year), and `star wars fan` is the most negative (-13.9).
- Respondent-clustered inference and both multiplicity screens still yield no
  discovery among 704 tests: zero Benjamini–Hochberg q-values and zero
  Bonferroni-adjusted p-values are at or below .05.
- The two-period sensitivity compares prevalence through 2026-02-13 with
  prevalence from 2026-02-14 onward for the 20 selected linear-trend leaders.
  All 20 raw contrasts retain the linear slope's direction; their median
  absolute difference is 10.2 percentage points. After adjustment for age,
  observed composition, weekday, and month, 19 of 20 retain that direction and
  the median absolute adjustment shift is 4.2 points. `single` changes from a
  -7.1-point raw contrast to +1.1 adjusted, with a wide clustered 95% interval
  from -13.9 to +16.2. This is a selected diagnostic, not a discovery test,
  and its point difference is not directly comparable with an annualized slope.
- The refreshed composition-and-calendar sensitivity retains the direction of
  all 20 pooled leaders; the median absolute slope shift is 5.5 points/year.
- The three-way leader panel now has 16 of 20 repeat-sample slopes retaining
  the all-response direction, 15 of 20 within-person slopes retaining the
  repeat-sample direction, and 13 of 20 retaining the original direction. The
  median absolute shifts are 12.7 points/year for sample restriction, 13.4 for
  absorbing respondent effects, and 13.1 end to end; the median signifier has
  26 repeat respondents. Three signifiers have no endorsement switchers, so
  their zero within slopes and intervals are mechanical rather than precise
  population evidence.
- A new internal outreach draft explains why the raw and adjusted two-period
  comparisons can differ and uses the `single` reversal to emphasize
  uncertainty rather than a change claim. It remains unpublished pending PI
  guidance.

## Decisions and constraints

- Follow `PROJECT.md` and observe Ipseity Daily only from outside. Only the PI
  edits the charter or the production Ipseity Daily system.
- A live monitor run appends history. Routine validation must use unit tests or
  a saved file with `--no-history`; do not repeat a network check on the same
  UTC day absent a suspected failure.
- Keep the unweighted pooled daily slope as the charter-requested descriptive
  point estimate. Use respondent-clustered intervals and both BH and Bonferroni
  adjustments for the primary screen.
- Treat the composition-and-calendar, raw and adjusted early-versus-late,
  repeat-sample pooled, and respondent-fixed-effect models as selected-leader
  sensitivities, not replacement estimands or multiplicity corrections. The
  early/late contrast relaxes straight-line form but can hide shorter reversals;
  its adjusted version addresses recorded composition and calendar terms only.
  The repeat-sample and fixed-effect shifts are not a causal turnover
  decomposition.
- Do not interpret nominal intervals excluding zero as discoveries when none
  of the 704 primary tests passes either multiplicity screen. Do not interpret
  a zero sandwich interval as precision when repeat respondents never change
  their outcome.
- Treat the eight-check history view as evidence about the sampled moments,
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
- `outputs/`: current summary, growth tables, full trend estimates, three
  leader sensitivity tables, and six accessible SVGs.
- `tests/test_monitor.py`: synthetic validation, inference, sensitivity, and
  artifact consistency tests.
- `outreach/`: workflow recommendation and internal content drafts.
- `DIALOG.md`, `dialog/iterations/`, and `dialog/indexes/`: bounded handoff and
  immutable iteration history.

## Problems and unresolved PI questions

- Eight history rows establish seven healthy daily intervals and a useful first
  operational view, but not enough evidence to characterize service
  reliability or interruptions between checks.
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
2. Continue the check history so the operational view can eventually
   distinguish isolated from continuing failures and summarize longer-run lag.
3. Assess whether selected leader trajectories are smooth or concentrated in
   shorter periods, while retaining the linear primary estimand and all
   selection, composition, and multiplicity cautions.
4. Incorporate PI outreach guidance and keep public trend claims deferred until
   robustness evidence is stronger.
