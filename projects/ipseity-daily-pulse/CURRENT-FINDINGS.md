# Current monitoring and prevalence findings

Current through the monitoring check at **2026-09-24T10:06:35Z**. This file is
replaced when the analysis is refreshed; it is not an archive.

## Monitor

The Ipseity Daily homepage and canonical microdata both returned HTTP 200. The
gzip parsed as UTF-8 CSV with the documented schema and contained
**712,953 observations** from **2025-07-08** through
**2026-09-23**, spanning **5,045 hashed respondents**
and **707 signifiers**. No malformed rows or duplicate
respondent/date/signifier keys were detected. The newest observation was
1 day behind the check date, and this
check records no anomaly.

![Cumulative observations over time](outputs/observation-growth.svg)

The cumulative series is derived from observation dates inside the current
microdata, while `data/monitoring-history.csv` preserves the separate sequence
of outside-in checks for longitudinal monitoring. Across
**9 checks**, **9**
had a reachable homepage, a retrieved and parseable canonical file, and no
anomaly. The file gained
**13,118 observations** from
the first recorded check to the latest. This short run is an operational view,
not an estimate of long-run service reliability.

![Endpoint status, data lag, and observation growth across checks](outputs/monitoring-history.svg)

## Estimated signifier prevalence change

For each signifier, an unweighted linear probability model regresses its binary
endorsement response on observation date. The slope is annualized to percentage
points per year. The histogram includes **704 of
707 signifiers** with at least 300 responses,
30 distinct observation dates, and a 180-day
span. These are descriptive sample trends, not population-weighted or causal
estimates. The median estimate is **+0.5
percentage points per year**; the middle half runs from -1.8 to
+3.1 points.

![Histogram of estimated annual prevalence growth](outputs/annual-prevalence-growth-histogram.svg)

Uncertainty now uses a respondent-clustered sandwich estimator, so repeat
answers by the same hashed respondent are not treated as independent. The file
contains **536,238 respondent–signifier clusters**;
the largest has 50 responses. Across 704 eligible
trend tests, **0** have Benjamini–Hochberg q-values at or below
0.05, and **0** meet the more conservative Bonferroni
0.05 threshold.

### Fastest estimated growth

| Signifier | Annual change (pp) | Clustered 95% CI | BH q | Bonferroni p | Responses |
|---|---:|---:|---:|---:|---:|
| beautiful | +24.6 | [+11.4, +37.8] | 0.097 | 0.175 | 457 |
| pretty | +17.5 | [+3.3, +31.6] | 0.400 | 1.000 | 420 |
| amateur artist | +17.3 | [+5.0, +29.7] | 0.321 | 1.000 | 421 |
| COVID survivor | +17.1 | [+2.5, +31.7] | 0.424 | 1.000 | 394 |
| romance fan | +15.9 | [+3.4, +28.4] | 0.400 | 1.000 | 466 |

### Fastest estimated shrinkage

| Signifier | Annual change (pp) | Clustered 95% CI | BH q | Bonferroni p | Responses |
|---|---:|---:|---:|---:|---:|
| nba fan | -14.2 | [-27.4, -1.0] | 0.480 | 1.000 | 409 |
| star wars fan | -13.9 | [-27.1, -0.8] | 0.484 | 1.000 | 426 |
| social conservative | -13.4 | [-25.2, -1.5] | 0.468 | 1.000 | 430 |
| 2a supporter | -13.0 | [-26.1, +0.2] | 0.567 | 1.000 | 380 |
| Reddit user | -12.6 | [-25.5, +0.3] | 0.571 | 1.000 | 400 |

The largest point estimate is **beautiful** at
24.6 percentage points
per year; the most negative is **nba fan** at
-14.2 points per year.
The intervals account for dependence within hashed respondents but not changing
sample composition, calendar structure, or model misspecification. The
Benjamini–Hochberg screen follows the original independent-test procedure;
correlation among signifier tests makes the Bonferroni column an important
conservative sensitivity check. Point-estimate rankings selected from
704 tests remain monitoring leads, not evidence that the underlying
US adult population changed at those rates.

## Composition and calendar sensitivity

As a targeted robustness check, the ten most positive and ten most negative
unadjusted slopes were refit with respondent-clustered uncertainty after
adjusting for linear age, missing age, demographics availability, sex,
ethnicity, student status, employment, weekday, and month of year. **20
of 20** leaders retained their original direction. The median
absolute slope shift was **5.0 percentage points per
year**. The largest shift was for **beautiful**, from
+24.6 to
+11.6 points.

![Unadjusted and adjusted leader slopes](outputs/leader-adjustment-sensitivity.svg)

| Signifier | Unadjusted (pp/year) | Adjusted (pp/year) | Adjusted clustered 95% CI |
|---|---:|---:|---:|
| beautiful | +24.6 | +11.6 | [-3.6, +26.7] |
| pretty | +17.5 | +5.1 | [-11.0, +21.3] |
| amateur artist | +17.3 | +11.7 | [-3.9, +27.4] |
| COVID survivor | +17.1 | +14.1 | [-3.9, +32.1] |
| romance fan | +15.9 | +5.0 | [-9.1, +19.2] |
| nba fan | -14.2 | -4.9 | [-20.9, +11.2] |
| star wars fan | -13.9 | -10.1 | [-26.2, +5.9] |
| social conservative | -13.4 | -10.6 | [-25.8, +4.5] |
| 2a supporter | -13.0 | -16.9 | [-32.5, -1.3] |
| Reddit user | -12.6 | -19.8 | [-35.4, -4.2] |

This selected-leader sensitivity is diagnostic, not a new discovery screen.
It cannot correct unobserved composition, nonrepresentative recruitment,
functional-form error, or selection of extremes from the full set of tests.

## Early-versus-late period sensitivity

To relax the assumption that prevalence follows one straight line, a
prespecified two-period check divides the full observation window at its
calendar midpoint, **2026-02-14**. For the
same selected leaders, it compares unweighted prevalence after that date with
prevalence on or before it. **20 of
20** contrasts have the same direction as the
selected linear slope. The median absolute late-minus-early difference is
**9.7 percentage points**. The largest contrast is
for **beautiful**:
33.1% early
versus 51.8%
late, a +18.8-point
difference.

The two-period contrast was then adjusted for the same age, observed sample
composition, weekday, and month terms as the linear sensitivity. **20
of 20** adjusted contrasts retain the selected
linear slope's direction, and **20 of
20** retain the raw contrast's direction. Adjustment
moves a contrast by a median absolute **4.8
percentage points**. The largest shift is for
**Reddit user**, from
-6.3
to
-19.5
points.

![Raw and adjusted late-half versus early-half contrasts](outputs/leader-early-late-sensitivity.svg)

| Signifier | Linear slope (pp/year) | Early prevalence | Late prevalence | Raw contrast (pp) | Adjusted contrast (pp) | Adjusted clustered 95% CI |
|---|---:|---:|---:|---:|---:|---:|
| beautiful | +24.6 | 33.1% | 51.8% | +18.8 | +12.4 | [-1.9, +26.7] |
| pretty | +17.5 | 35.0% | 48.5% | +13.5 | +7.6 | [-6.4, +21.6] |
| amateur artist | +17.3 | 20.8% | 32.0% | +11.2 | +11.4 | [-2.6, +25.4] |
| COVID survivor | +17.1 | 45.0% | 53.6% | +8.6 | +10.6 | [-5.8, +27.0] |
| romance fan | +15.9 | 32.3% | 43.4% | +11.1 | +2.8 | [-10.0, +15.6] |
| nba fan | -14.2 | 37.4% | 26.9% | -10.4 | -2.1 | [-16.8, +12.5] |
| star wars fan | -13.9 | 43.4% | 32.2% | -11.2 | -9.6 | [-23.8, +4.7] |
| social conservative | -13.4 | 27.9% | 23.9% | -4.0 | -0.2 | [-14.4, +14.1] |
| 2a supporter | -13.0 | 29.5% | 18.5% | -11.0 | -21.3 | [-35.4, -7.2] |
| Reddit user | -12.6 | 73.0% | 66.7% | -6.3 | -19.5 | [-34.1, -4.9] |

This contrast does not impose a trajectory within either half, but it can hide
shorter reversals. The adjusted version addresses only the recorded covariates
and calendar terms; neither version corrects unobserved composition,
nonrepresentative recruitment, or selection of the 20 linear-trend extremes.
Their percentage-point magnitudes are not on the same scale as the annualized
linear slope; only directions are compared. The clustered intervals are
diagnostic, not a discovery screen.

## Four-period trajectory sensitivity

The two-period contrast can still hide shorter changes, so a second shape
diagnostic divides the inclusive observation window into four nearly equal
calendar periods: **2025-07-08–2025-10-25**,
**2025-10-26–2026-02-13**,
**2026-02-14–2026-06-04**, and
**2026-06-05–2026-09-23**.
Among the 20 selected leaders, **20** have a
first-to-last period change matching the linear slope, but only
**6** move in that direction across all
three adjacent transitions. **17** move in the
selected direction in at least two of three transitions.

For each signifier, the largest adjacent move accounts for a median
**58%** of its total absolute path
across the three transitions. The most concentrated selected path is
**star wars fan**: its largest move is
-11.7
points across
period 2 to 3, or
93%
of its total absolute adjacent movement.

![Adjacent changes across four periods for selected leaders](outputs/leader-period-trajectory.svg)

| Signifier | P1 | P2 | P3 | P4 | Aligned transitions | Largest share of path |
|---|---:|---:|---:|---:|---:|---:|
| beautiful | 36.1% | 30.0% | 47.5% | 57.0% | 2/3 | 53% |
| pretty | 40.8% | 30.2% | 46.4% | 51.0% | 2/3 | 51% |
| amateur artist | 20.6% | 21.0% | 26.0% | 37.5% | 3/3 | 68% |
| COVID survivor | 42.7% | 47.5% | 49.5% | 58.6% | 3/3 | 57% |
| romance fan | 31.5% | 33.3% | 41.7% | 45.0% | 3/3 | 62% |
| nba fan | 38.2% | 36.4% | 26.7% | 27.2% | 2/3 | 81% |
| star wars fan | 43.2% | 43.6% | 32.0% | 32.4% | 1/3 | 93% |
| social conservative | 30.3% | 25.7% | 29.7% | 17.3% | 2/3 | 59% |
| 2a supporter | 32.2% | 27.4% | 15.5% | 21.3% | 2/3 | 52% |
| Reddit user | 76.1% | 69.6% | 68.3% | 64.8% | 3/3 | 57% |

The concentration share is descriptive: one-third represents three equally
sized absolute moves, while 100% means one transition contains all observed
adjacent movement. Period prevalence is raw and unweighted. This diagnostic
does not adjust for changing composition, repeated respondents, or calendar
effects; it supplies no new discovery test and remains conditioned on selecting
the 20 most extreme linear slopes.

## Within-respondent sensitivity

A second targeted check separates two diagnostic changes. It first refits the
pooled trend using only people who answered the same signifier on multiple
dates, then absorbs a fixed effect for each of those respondents while keeping
the same observations. **17 of 20**
repeat-sample pooled slopes retained the all-response direction; **14
of 20** within-person slopes retained the repeat-sample
direction, and **11 of 20** retained
the original all-response direction. Restricting the sample moved a selected slope by a median absolute
**11.5 percentage points per year**; absorbing
respondent effects then moved it by **15.3
points**. The largest sample-restriction change was for
**star wars fan**, from
-13.9
to -42.4;
the largest repeat-pooled-to-within change was for
**team player**, from
-3.4
to +42.7.
The full all-response-to-within shift had median absolute magnitude
**13.2 points**, and the median selected signifier
had **26 repeat respondents**. For
**2** selected signifiers, no repeat respondent changed
endorsement; their zero within slopes are mechanical descriptions and clustered
intervals are not displayed.

![All-response, repeat-sample pooled, and within-respondent leader slopes](outputs/leader-within-respondent-sensitivity.svg)

| Signifier | All responses (pp/year) | Repeat sample, pooled (pp/year) | Within respondent (pp/year) | Within clustered 95% CI | Repeat respondents |
|---|---:|---:|---:|---:|---:|
| beautiful | +24.6 | +4.0 | -0.7 | [-2.6, +1.2] | 30 |
| pretty | +17.5 | +13.7 | +8.5 | [-14.2, +31.1] | 27 |
| amateur artist | +17.3 | +9.6 | +10.8 | [-16.8, +38.4] | 28 |
| COVID survivor | +17.1 | -10.4 | -15.2 | [-56.7, +26.3] | 28 |
| romance fan | +15.9 | +9.9 | -3.3 | [-33.2, +26.6] | 40 |
| nba fan | -14.2 | -25.9 | -2.7 | [-10.5, +5.2] | 19 |
| star wars fan | -13.9 | -42.4 | -20.4 | [-60.9, +20.1] | 25 |
| social conservative | -13.4 | +2.5 | +0.0 | No endorsement switches | 23 |
| 2a supporter | -13.0 | -31.9 | -13.2 | [-39.7, +13.2] | 27 |
| Reddit user | -12.6 | -22.8 | +6.0 | [-12.0, +24.0] | 18 |

The first comparison changes the analytic sample; the second holds those
observations fixed but changes the model from pooled to within respondent.
Their arithmetic shifts clarify where the displayed estimate changes, but they
are not a causal decomposition into turnover and individual change. The models
remain vulnerable to selective retention, time-varying confounding,
functional-form error, nonrepresentative recruitment, and selection of pooled
extremes. Their intervals are diagnostic rather than a discovery test.

Full machine-readable estimates, eligibility flags, and interval bounds are in
`outputs/signifier-growth.csv`; adjusted leader checks are in
`outputs/leader-adjusted-sensitivity.csv`; two-period checks are in
`outputs/leader-early-late-sensitivity.csv`; four-period paths are in
`outputs/leader-period-trajectory.csv`; within-respondent checks are in
`outputs/leader-within-respondent-sensitivity.csv`; the daily and cumulative
counts are in `outputs/daily-observation-growth.csv`.

## Source

Jones, J. (2026). *Ipseity Daily Data* [Data set]. Zenodo.
[https://doi.org/10.5281/zenodo.22636514](https://doi.org/10.5281/zenodo.22636514).
The analysis used the newer canonical file served directly by the
[Ipseity Daily download page](https://jasonjones.ninja/social-science-dashboard-inator/ipseity-daily/download.html) at the check time;
SHA-256 `134d0c0ca8047b8a209c71fcddf37fa8a0628bfd4ca6bf872d9ca2d80b8b9f8f`.

Liang, K.-Y., & Zeger, S. L. (1986). Longitudinal data analysis using
generalized linear models. *Biometrika, 73*(1), 13–22.
[https://doi.org/10.1093/biomet/73.1.13](https://doi.org/10.1093/biomet/73.1.13).

Benjamini, Y., & Hochberg, Y. (1995). Controlling the false discovery rate: A
practical and powerful approach to multiple testing. *Journal of the Royal
Statistical Society: Series B (Methodological), 57*(1), 289–300.
[https://doi.org/10.1111/j.2517-6161.1995.tb02031.x](https://doi.org/10.1111/j.2517-6161.1995.tb02031.x).
