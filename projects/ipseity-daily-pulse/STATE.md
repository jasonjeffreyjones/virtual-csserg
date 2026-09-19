---
title: "Ipseity Daily Pulse"
status: Active
publication: Unpublished
updated: 2026-09-19T10:12:45Z
---

# Ipseity Daily Pulse — Current state

## Status

Active and Unpublished. Research artifacts remain under `projects/`; no empty
public report has been created.

## Current findings and completed work

- Four daily outside-in checks are recorded. At `2026-09-19T10:07:11Z`, the
  homepage and canonical microdata returned HTTP 200. The 4,996,170-byte gzip
  parsed with the documented schema: 704,797 response observations from
  2025-07-08 through 2026-09-18, 5,005 hashed respondents, 707 signifiers, no
  malformed rows or duplicate canonical keys, and a one-day data lag. No
  anomaly was detected. Since the prior check, the file gained 1,657
  observations and eight respondents, and its latest observation date advanced
  one day. Its SHA-256 is
  `445ea5b5dee32d387c7b403766328528fc10c9491e8cd200ad2cca2b68c3d767`.
- The current growth table and accessible SVG rise to 704,797 observations
  across 428 observation dates. Four history rows remain too few to
  characterize service reliability or merit a separate check-history figure.
- Unweighted linear probability trends remain estimable for 704 signifiers
  meeting the prespecified 300-response, 30-date, and 180-day thresholds. The
  median annualized estimate is +0.5 percentage points; the middle half ranges
  from -1.7 to +3.2 points. `beautiful` is the most positive pooled leader
  (+23.6 points/year), and `social conservative` is the most negative (-14.9).
- Respondent-clustered inference and both multiplicity screens still yield no
  discovery among 704 tests: zero Benjamini–Hochberg q-values and zero
  Bonferroni-adjusted p-values are at or below .05.
- The refreshed composition-and-calendar sensitivity retains the direction of
  19 of 20 pooled leaders; `single` reverses. The median absolute slope shift is
  6.1 points/year. This remains a selected-leader diagnostic rather than a
  discovery test.
- A new respondent-fixed-effect sensitivity estimates temporal change using
  only people who answered the same signifier on multiple dates. Only 13 of 20
  pooled leaders retain their direction, the median absolute pooled-to-within
  shift is 13.9 points/year, and the median signifier has only 26 repeat
  respondents. `beautiful` shifts from +23.6 pooled to -0.7 within person
  (clustered 95% interval -2.6 to +1.2; 30 repeat respondents). `overthinker`
  shifts the most, from +14.3 to -20.5. `she/her` and `social conservative`
  have no endorsement switches among their repeat respondents, so their zero
  within slopes and zero sandwich intervals are mechanical, not precise
  population evidence.
- The internal outreach draft now explains why a pooled sample trend and
  within-person change answer different questions. It remains unpublished
  pending PI guidance.

## Decisions and constraints

- Follow `PROJECT.md` and observe Ipseity Daily only from outside. Only the PI
  edits the charter or the production Ipseity Daily system.
- A live monitor run appends history. Routine validation must use unit tests or
  a saved file with `--no-history`; do not repeat a network check on the same
  UTC day absent a suspected failure.
- Keep the unweighted pooled daily slope as the charter-requested descriptive
  point estimate. Use respondent-clustered intervals and both BH and Bonferroni
  adjustments for the primary screen.
- Treat the composition-and-calendar and respondent-fixed-effect models as
  selected-leader sensitivities, not replacement estimands or multiplicity
  corrections. The fixed-effect model removes stable respondent differences
  but also restricts analysis to a small, selected repeat-respondent subset, so
  the pooled-to-within gap is not a literal turnover decomposition.
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

- Four history rows establish three healthy daily intervals, not enough
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
2. For the selected leaders, compare three estimates—pooled among everyone,
   pooled among repeat respondents, and respondent fixed effects—to separate
   repeat-sample selection from the within-person contrast without calling the
   result a causal decomposition.
3. Add a check-history visualization after several more daily observations
   make it interpretable.
4. Incorporate PI outreach guidance and keep public trend claims deferred until
   robustness evidence is stronger.
