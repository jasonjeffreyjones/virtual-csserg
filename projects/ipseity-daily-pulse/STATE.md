---
title: "Ipseity Daily Pulse"
status: Active
publication: Published
updated: 2026-09-26T10:10:52Z
---

# Ipseity Daily Pulse — Current state

## Status

Active and Published. Per PI guidance appended to the September 25 iteration,
the production-ready static publication now includes an Executive Summary,
Quarto Full Report, two-column short PDF, and Project blog under
`website/projects/ipseity-daily-pulse/`. The home page links the newest
individual blog entry.

## Current findings and completed work

- Eleven daily outside-in checks are recorded. At `2026-09-26T10:02:00Z`, the
  homepage and canonical microdata returned HTTP 200. The 5,079,260-byte gzip
  parsed with the documented schema: 716,237 response observations from
  2025-07-08 through 2026-09-25, 5,059 hashed respondents, 707 signifiers, no
  malformed rows or duplicate canonical keys, and a one-day data lag. No
  anomaly was detected. Since the prior check, the file gained 1,663
  observations and six respondents, and its latest observation date advanced
  one day. Its SHA-256 is
  `0e3558ecb76f84cb33ca1fa878f81cb82159457987bd384edad13c34b2cd2354`.
- All eleven sampled checks were healthy, lag was one day at each, and the
  canonical file gained 16,402 observations from the first check to the
  latest. The accessible history figure aligns endpoint and parse status, data
  lag, and observations. This is an operational snapshot sequence, not an
  uptime or long-run reliability estimate.
- Unweighted linear probability trends remain estimable for 704 signifiers
  meeting the prespecified 300-response, 30-date, and 180-day thresholds. The
  median annualized estimate is +0.5 percentage points; the middle half ranges
  from -1.9 to +3.0 points. `beautiful` is the most positive pooled leader
  (+24.0 points/year), and `star wars fan` is the most negative (-14.2).
- Respondent-clustered inference and both multiplicity screens yield no
  discovery among 704 tests: zero Benjamini–Hochberg q-values and zero
  Bonferroni-adjusted p-values are at or below .05.
- The selected two-period diagnostic has all 20 raw contrasts retaining the
  linear slope's direction and 19 of 20 adjusted contrasts doing so. The
  median absolute raw difference is 10.0 percentage points, and recorded
  composition and calendar adjustment moves a contrast by a median absolute
  4.7 points. `single` moves from -7.9 raw to approximately zero (+0.05)
  adjusted. This is not a discovery test.
- All 20 selected four-period raw paths retain the first-to-last linear
  direction, but only seven align across all three adjacent transitions; 17
  align in at least two. The median largest-transition share is 64%, and
  `star wars fan` is most concentrated at 91%.
- All 20 standardized four-period paths retain the selected first-to-last
  direction, none aligns across all three transitions, and 14 align in at
  least two. The median largest-transition share is 52%; 11 of 20 retain the
  same largest transition after adjustment. `2a supporter` has the most
  concentrated adjusted path at 82%.
- Composition-and-calendar adjustment retains the direction of all 20 pooled
  leaders; the median absolute slope shift is 5.3 points/year.
- The three-way leader panel has 17 of 20 repeat-sample slopes retaining the
  all-response direction, 15 of 20 within-person slopes retaining the
  repeat-sample direction, and 12 of 20 retaining the original direction. The
  median absolute shifts are 11.5 points/year for sample restriction, 16.7
  for absorbing respondent effects, and 12.9 end to end; the median selected
  signifier has 26.5 repeat respondents. Two signifiers have no endorsement
  switchers, so their zero within slopes are mechanical rather than evidence
  of population precision.
- The Project blog publishes all ten dated outreach entries as HTML pages. Each
  older entry uses the exact SVG from the commit that created its source and
  carries a snapshot note; the new entry, “A trend leaderboard is not a
  discovery list,” explains why the two 704-test multiplicity screens matter.

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
  and standardized four-period trajectory, repeat-sample pooled, and
  respondent-fixed-effect models as selected-leader sensitivities, not
  replacement estimands or multiplicity corrections. Their shifts are not a
  causal decomposition, and unbounded adjusted linear-probability levels are
  model diagnostics rather than literal prevalences when outside 0%–100%.
- Do not interpret nominal intervals excluding zero as discoveries when none
  of the 704 primary tests passes either multiplicity screen. Do not interpret
  a zero sandwich interval as precision when repeat respondents never change
  their outcome.
- Treat the eleven-check history as evidence about sampled moments, not
  continuous availability or a service-level estimate.
- The PI chose a shared, Project-organized website blog and authorized
  publication. New entries should be accessible HTML pages, appear newest
  first in the blog index, and keep the home-page link pointed to the newest
  individual entry. Publish only claims supported by the current cumulative
  report and preserve dated provenance.

## Important files

- `PROJECT.md`: PI-owned charter.
- `CURRENT-FINDINGS.md`: replaceable reader-facing current results and sources.
- `ANALYSIS.md` and `analysis/monitor.py`: method, reproduction, live monitor,
  clustered inference, multiplicity adjustment, leader sensitivities, and
  artifact generation.
- `index.qmd`, `_quarto.yml`, `short-report.md`, and `BUILD.md`: publication
  sources and reproduction instructions.
- `analysis/render_short_report.py`, `analysis/render_blog.py`, and
  `analysis/verify_publication.py`: derivative renderers and Project-specific
  publication checks. The blog renderer pins older figures to their source
  commits.
- `data/monitoring-history.csv`: append-only outside-in check history.
- `outputs/`: current summary, growth tables, full trend estimates, four
  leader sensitivity tables, and eight accessible SVGs.
- `website/projects/ipseity-daily-pulse/`: the public Executive Summary, Full
  Report, short PDF, blog, aggregate artifacts, and figures.
- `tests/test_monitor.py`: synthetic validation, inference, sensitivity, and
  artifact consistency tests.
- `outreach/`: the ten dated source entries for the public Project blog.
- `DIALOG.md`, `dialog/iterations/`, and `dialog/indexes/`: bounded handoff and
  immutable iteration history.

## Problems and unresolved PI questions

- Eleven daily snapshots establish ten healthy intervals but cannot reveal
  outages between checks or characterize long-run reliability.
- No signifier slope survives either multiplicity adjustment. Leader
  sensitivities use small, selected subsets and do not address population
  weighting, time-varying confounding, selective retention, changing
  unobserved composition, or the dependence of four-period findings on chosen
  boundaries and model form.
- No PI question is currently unresolved. The publication and shared Project
  blog instructions are incorporated.

## Likely next steps

1. On the next UTC day, run the live monitor once; investigate only if its
   anomaly field is not `none`.
2. Refresh all three report forms and public aggregate artifacts after a
   materially changed result, while retaining dated provenance for blog posts.
3. Continue the check history so the operational view can eventually
   distinguish isolated from continuing failures and summarize longer-run lag.
4. Assess whether the dominant-transition and concentration conclusions are
   robust to reasonable alternative period boundaries or segment counts,
   while retaining the linear primary estimand and all selection and
   multiplicity cautions.
