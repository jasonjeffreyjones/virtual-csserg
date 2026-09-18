---
title: "Ipseity Daily Pulse"
status: Active
publication: Unpublished
updated: 2026-09-18T10:11:31Z
---

# Ipseity Daily Pulse — Current state

## Status

Active and Unpublished. Research artifacts remain under `projects/`; no empty
public report has been created.

## Current findings and completed work

- Three daily outside-in checks are recorded. At `2026-09-18T10:02:22Z`, the
  homepage and canonical microdata returned HTTP 200. The 4,984,183-byte gzip
  parsed with the documented schema: 703,140 response observations from
  2025-07-08 through 2026-09-17, 4,997 hashed respondents, 707 signifiers, no
  malformed rows or duplicate canonical keys, and a one-day data lag. No
  anomaly was detected. Since the prior check, the file gained 1,637
  observations and ten respondents, and its latest observation date advanced
  one day. Its SHA-256 is
  `b6a6d70f42daa116df249450c816e5ab2ad815332dad50199d60eb31135fbe0d`.
- The current growth table and accessible SVG rise to 703,140 observations
  across 427 observation dates. Three history rows remain too few to
  characterize service reliability or merit a separate check-history figure.
- Unweighted linear probability trends remain estimable for 704 signifiers
  meeting the prespecified 300-response, 30-date, and 180-day thresholds. The
  median annualized estimate is +0.5 percentage points; the middle half ranges
  from -1.7 to +3.2 points. `beautiful` is the most positive unadjusted leader
  (+23.6 points/year), and `social conservative` is the most negative (-15.9).
- Respondent-clustered inference and both multiplicity screens still yield no
  discovery among 704 tests: zero Benjamini–Hochberg q-values and zero
  Bonferroni-adjusted p-values are at or below .05.
- A new targeted sensitivity refits the ten most positive and ten most
  negative unadjusted leaders with age, demographics availability, sex,
  ethnicity, student status, employment, weekday, and month-of-year controls.
  All 20 retain their direction, but the median absolute slope shift is 5.5
  points/year. `beautiful` falls from +23.6 to +12.3 with an adjusted clustered
  95% interval of -3.4 to +28.0; `pretty` moves the most, from +16.9 to +4.8.
  The selected-leader intervals are diagnostic rather than a discovery test.
- The internal outreach draft now uses the adjustment result and its accessible
  dumbbell SVG to explain why raw rankings are leads rather than findings. It
  remains unpublished pending PI guidance.

## Decisions and constraints

- Follow `PROJECT.md` and observe Ipseity Daily only from outside. Only the PI
  edits the charter or the production Ipseity Daily system.
- A live monitor run appends history. Routine validation must use unit tests or
  a saved file with `--no-history`; do not repeat a network check on the same
  UTC day absent a suspected failure.
- Keep the unweighted daily slope as the charter-requested descriptive point
  estimate. Use respondent-clustered intervals and both BH and Bonferroni
  adjustments for the primary screen.
- Treat the composition-and-calendar model as a selected-leader sensitivity,
  not a replacement estimand or multiplicity correction. It does not repair
  unobserved composition, nonrepresentative recruitment, or model form.
- Do not interpret nominal intervals excluding zero as discoveries when none
  of the 704 primary tests passes either multiplicity screen.
- Keep outreach material internal until the PI establishes a publication
  surface and approval/posting workflow.

## Important files

- `PROJECT.md`: PI-owned charter.
- `CURRENT-FINDINGS.md`: replaceable reader-facing current results and sources.
- `ANALYSIS.md` and `analysis/monitor.py`: method, reproduction, live monitor,
  clustered inference, multiplicity adjustment, and leader sensitivity.
- `data/monitoring-history.csv`: append-only outside-in check history.
- `outputs/`: current summary, growth tables, full trend estimates, adjusted
  leader estimates, and three accessible SVGs.
- `tests/test_monitor.py`: synthetic validation, inference, adjustment, and
  artifact consistency tests.
- `outreach/`: workflow recommendation and internal content drafts.
- `DIALOG.md`, `dialog/iterations/`, and `dialog/indexes/`: bounded handoff and
  immutable iteration history.

## Problems and unresolved PI questions

- Three history rows establish two healthy daily intervals, not enough evidence
  to characterize service reliability or create a useful check-history figure.
- No signifier slope survives either multiplicity adjustment. The targeted
  controls address only observed composition and simple seasonality; turnover,
  unobserved composition, population weighting, and model form remain open.
- Should Virtual CSSERG adopt the proposed shared, Project-organized outreach
  feed in which Scholars leave evidence-linked drafts and Dr. Jones approves or
  posts them? Until guidance arrives, drafts remain internal and unpublished.

## Likely next steps

1. On the next UTC day, run the live monitor once; investigate only if its
   anomaly field is not `none`.
2. Separate respondent turnover from within-respondent change, for example
   with a repeat-respondent or respondent-fixed-effect sensitivity, while
   preserving the primary descriptive estimand and selection caveat.
3. Add a check-history visualization after several more daily observations
   make it interpretable.
4. Incorporate PI outreach guidance and keep public trend claims deferred until
   robustness evidence is stronger.
