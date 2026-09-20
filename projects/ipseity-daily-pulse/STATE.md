---
title: "Ipseity Daily Pulse"
status: Active
publication: Unpublished
updated: 2026-09-20T10:08:59Z
---

# Ipseity Daily Pulse — Current state

## Status

Active and Unpublished. Research artifacts remain under `projects/`; no empty
public report has been created.

## Current findings and completed work

- Five daily outside-in checks are recorded. At `2026-09-20T10:06:08Z`, the
  homepage and canonical microdata returned HTTP 200. The 5,007,868-byte gzip
  parsed with the documented schema: 706,425 response observations from
  2025-07-08 through 2026-09-19, 5,010 hashed respondents, 707 signifiers, no
  malformed rows or duplicate canonical keys, and a one-day data lag. No
  anomaly was detected. Since the prior check, the file gained 1,628
  observations and five respondents, and its latest observation date advanced
  one day. Its SHA-256 is
  `820d311436a00c2333d3b6d342da4ec45c138daa926d60baf00a5636b4b366c8`.
- The current growth table and accessible SVG rise to 706,425 observations
  across 429 observation dates. Five history rows remain too few to
  characterize service reliability or merit a separate check-history figure.
- Unweighted linear probability trends remain estimable for 704 signifiers
  meeting the prespecified 300-response, 30-date, and 180-day thresholds. The
  median annualized estimate is +0.6 percentage points; the middle half ranges
  from -1.6 to +3.2 points. `beautiful` is the most positive pooled leader
  (+22.9 points/year), and `nba fan` is the most negative (-14.6).
- Respondent-clustered inference and both multiplicity screens still yield no
  discovery among 704 tests: zero Benjamini–Hochberg q-values and zero
  Bonferroni-adjusted p-values are at or below .05.
- The refreshed composition-and-calendar sensitivity retains the direction of
  all 20 pooled leaders. The median absolute slope shift is 5.4 points/year.
  This remains a selected-leader diagnostic rather than a
  discovery test.
- The leader panel now compares all-response pooled trends, pooled trends on
  the repeat-respondent subset, and respondent fixed effects on those same
  repeat observations. Sixteen of 20 repeat-sample slopes retain the
  all-response direction; 15 of 20 within-person slopes retain the repeat-sample
  direction; 13 of 20 retain the original direction. The median absolute
  changes are 12.5 points/year for sample restriction, 11.6 for absorbing
  respondent effects, and 14.0 end to end; the median signifier has only 25
  repeat respondents. `beautiful` moves from +22.9 among all responses to +4.0
  pooled among repeat respondents and -0.7 within person (30 repeat respondents,
  one switcher). `singer`, `she/her`, and `social conservative` have no
  endorsement switchers, so their zero within slopes and intervals are
  mechanical rather than precise population evidence.
- A new internal outreach draft uses the `beautiful` three-way comparison to
  explain why sample restriction and within-person change answer distinct
  questions. It remains unpublished pending PI guidance.

## Decisions and constraints

- Follow `PROJECT.md` and observe Ipseity Daily only from outside. Only the PI
  edits the charter or the production Ipseity Daily system.
- A live monitor run appends history. Routine validation must use unit tests or
  a saved file with `--no-history`; do not repeat a network check on the same
  UTC day absent a suspected failure.
- Keep the unweighted pooled daily slope as the charter-requested descriptive
  point estimate. Use respondent-clustered intervals and both BH and Bonferroni
  adjustments for the primary screen.
- Treat the composition-and-calendar, repeat-sample pooled, and
  respondent-fixed-effect models as selected-leader sensitivities, not
  replacement estimands or multiplicity corrections. The repeat-sample model
  isolates the change from restricting the analytic sample; the fixed-effect
  model then removes stable respondent differences on the same observations.
  Their arithmetic shifts are not a causal turnover decomposition.
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
  clustered inference, multiplicity adjustment, leader adjustment, and
  within-respondent sensitivity.
- `data/monitoring-history.csv`: append-only outside-in check history.
- `outputs/`: current summary, growth tables, full trend estimates, two leader
  sensitivity tables, and four accessible SVGs.
- `tests/test_monitor.py`: synthetic validation, inference, adjustment,
  fixed-effect, and artifact consistency tests.
- `outreach/`: workflow recommendation and internal content drafts.
- `DIALOG.md`, `dialog/iterations/`, and `dialog/indexes/`: bounded handoff and
  immutable iteration history.

## Problems and unresolved PI questions

- Five history rows establish four healthy daily intervals, not enough
  evidence to characterize service reliability or create a useful
  check-history figure.
- No signifier slope survives either multiplicity adjustment. Leader
  sensitivities use small, selected subsets and do not address population
  weighting, time-varying confounding, selective retention, or nonlinear trend
  form.
- Should Virtual CSSERG adopt the proposed shared, Project-organized outreach
  feed in which Scholars leave evidence-linked drafts and Dr. Jones approves or
  posts them? Until guidance arrives, drafts remain internal and unpublished.

## Likely next steps

1. On the next UTC day, run the live monitor once; investigate only if its
   anomaly field is not `none`.
2. Test whether selected pooled leaders are stable to nonlinear time form or a
   prespecified early/late-period comparison; retain the primary linear slopes
   and the multiple-testing cautions.
3. Add a check-history visualization after at least seven daily observations
   make a one-week operational view interpretable.
4. Incorporate PI outreach guidance and keep public trend claims deferred until
   robustness evidence is stronger.
