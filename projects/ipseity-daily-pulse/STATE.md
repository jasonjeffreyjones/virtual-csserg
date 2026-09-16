---
title: "Ipseity Daily Pulse"
status: Active
publication: Unpublished
updated: 2026-09-16T20:58:13Z
---

# Ipseity Daily Pulse — Current state

## Status

Active and Unpublished. The activation requested in the preserved PI guidance
has been incorporated. Research artifacts live under `projects/`; no empty
public report has been created.

## Current findings and completed work

- The first outside-in check ran at `2026-09-16T20:47:07Z`. The homepage and
  canonical microdata returned HTTP 200. The 4,960,643-byte gzip parsed with the
  documented UTF-8 CSV schema: 699,835 response observations from 2025-07-08
  through 2026-09-15, 4,979 hashed respondents, and 707 signifiers. There were
  no malformed rows or duplicate respondent/date/signifier keys, the newest
  data lag was one day, and no anomaly was detected. The exact file SHA-256 is
  `b0b5cae9027284acaa28905c22a0ed8fb1357a434c931d31e747687d7fd1fa27`.
- A standard-library monitor now validates downloads, refuses duplicate check
  timestamps, distinguishes retrieval/parsing failures, compares later checks
  with the previous history row, and replaces current derived outputs only
  after successful validation. The initial machine-readable history row is in
  `data/monitoring-history.csv`.
- The cumulative observation series rises to 699,835 across 425 observation
  dates. Its CSV and accessible SVG are current.
- Unweighted linear probability trends are estimable for 704 signifiers meeting
  the prespecified minimum of 300 responses, 30 dates, and a 180-day span. The
  median annualized estimate is +0.5 percentage points; the middle half ranges
  from -1.7 to +3.2 points. The largest point estimate is `beautiful` (+24.4
  points/year, ordinary 95% interval +11.1 to +37.7), and the smallest is
  `star wars fan` (-15.5, interval -28.8 to -2.1). These are descriptive,
  unweighted rankings selected from 704 estimates—not population change claims.
- Correction to the immutable 2026-09-16 Ceetown record: its narrative reports
  the median as +0.2 and the middle-half lower bound as -2.4. The reproducible
  `outputs/signifier-growth.csv` values are +0.5 and -1.7, respectively, as
  reported here and in `CURRENT-FINDINGS.md`; the extreme rankings are
  unaffected. The record itself remains unaltered under the dialog protocol.
- One internal outreach draft communicates observation growth without
  conflating responses with people. A shared Project-organized Virtual CSSERG
  feed with PI approval is recommended over separate Scholar blogs.

## Decisions and constraints

- Follow `PROJECT.md` and observe Ipseity Daily only from outside. Only the PI
  edits the charter or the production Ipseity Daily system.
- A live monitor run appends history, so routine validation must use unit tests
  or `--no-history`; do not repeat the network check on the same UTC day absent
  a suspected failure.
- Current signifier slopes regress each binary response on observation date and
  annualize the slope using 365.2425 days. Retain eligibility flags and ordinary
  intervals, and describe extremes as monitoring leads. Before public claims,
  assess sample-composition, repeated-respondent, seasonality, and
  multiple-comparison sensitivity.
- Keep outreach material internal until the PI establishes a publication
  surface and approval/posting workflow.

## Important files

- `PROJECT.md`: PI-owned charter.
- `CURRENT-FINDINGS.md`: replaceable reader-facing current results and source.
- `ANALYSIS.md` and `analysis/monitor.py`: method, reproduction, and live monitor.
- `data/monitoring-history.csv`: append-only outside-in check history.
- `outputs/`: current summary, complete trend and growth tables, and two SVGs.
- `tests/test_monitor.py`: synthetic failure/estimation tests and artifact
  consistency checks.
- `outreach/`: workflow recommendation and current internal content draft.
- `DIALOG.md`, `dialog/iterations/`, and `dialog/indexes/`: bounded handoff and
  immutable iteration history.

## Problems and unresolved PI questions

- One history row establishes a baseline but cannot yet distinguish recurring
  outages or display across-check growth. Future daily checks will make those
  longitudinal comparisons meaningful.
- Should Virtual CSSERG adopt the proposed shared, Project-organized outreach
  feed in which Scholars leave evidence-linked drafts and Dr. Jones approves or
  posts them? Until guidance arrives, drafts remain internal and unpublished.

## Likely next steps

1. On the next UTC day, run the live monitor once; investigate only if its
   anomaly field is not `none`.
2. Add a history-based check-to-check figure after enough monitoring rows exist.
3. Test whether leading signifier slopes persist after adjustment for observed
   sample composition, repeated respondents, calendar effects, and multiplicity.
4. Incorporate PI outreach guidance and, only when evidence and report scope are
   mature, build the three required publication forms.
