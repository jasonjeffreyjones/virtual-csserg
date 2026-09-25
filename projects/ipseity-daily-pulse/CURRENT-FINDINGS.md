# Current monitoring and prevalence findings

Current through the monitoring check at **2026-09-25T10:07:47Z**. This file is
replaced when the analysis is refreshed; it is not an archive.

## Monitor

The Ipseity Daily homepage and canonical microdata both returned HTTP 200. The
gzip parsed as UTF-8 CSV with the documented schema and contained
**714,574 observations** from **2025-07-08** through
**2026-09-24**, spanning **5,053 hashed respondents**
and **707 signifiers**. No malformed rows or duplicate
respondent/date/signifier keys were detected. The newest observation was
1 day behind the check date, and this
check records no anomaly.

![Cumulative observations over time](outputs/observation-growth.svg)

The cumulative series is derived from observation dates inside the current
microdata, while `data/monitoring-history.csv` preserves the separate sequence
of outside-in checks for longitudinal monitoring. Across
**10 checks**, **10**
had a reachable homepage, a retrieved and parseable canonical file, and no
anomaly. The file gained
**14,739 observations** from
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
percentage points per year**; the middle half runs from -1.9 to
+3.0 points.

![Histogram of estimated annual prevalence growth](outputs/annual-prevalence-growth-histogram.svg)

Uncertainty now uses a respondent-clustered sandwich estimator, so repeat
answers by the same hashed respondent are not treated as independent. The file
contains **537,279 respondent–signifier clusters**;
the largest has 50 responses. Across 704 eligible
trend tests, **0** have Benjamini–Hochberg q-values at or below
0.05, and **0** meet the more conservative Bonferroni
0.05 threshold.

### Fastest estimated growth

| Signifier | Annual change (pp) | Clustered 95% CI | BH q | Bonferroni p | Responses |
|---|---:|---:|---:|---:|---:|
| beautiful | +24.6 | [+11.4, +37.8] | 0.087 | 0.175 | 457 |
| COVID survivor | +17.7 | [+3.1, +32.2] | 0.401 | 1.000 | 395 |
| pretty | +17.4 | [+3.4, +31.4] | 0.401 | 1.000 | 422 |
| amateur artist | +17.2 | [+5.0, +29.4] | 0.311 | 1.000 | 424 |
| romance fan | +16.4 | [+4.0, +28.9] | 0.393 | 1.000 | 467 |

### Fastest estimated shrinkage

| Signifier | Annual change (pp) | Clustered 95% CI | BH q | Bonferroni p | Responses |
|---|---:|---:|---:|---:|---:|
| star wars fan | -14.2 | [-27.3, -1.2] | 0.448 | 1.000 | 427 |
| nba fan | -14.2 | [-27.4, -1.0] | 0.448 | 1.000 | 409 |
| social conservative | -13.6 | [-25.4, -1.8] | 0.445 | 1.000 | 431 |
| 2a supporter | -13.0 | [-26.1, +0.2] | 0.590 | 1.000 | 380 |
| planner | -12.7 | [-24.2, -1.1] | 0.448 | 1.000 | 417 |

The largest point estimate is **beautiful** at
24.6 percentage points
per year; the most negative is **star wars fan** at
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
absolute slope shift was **5.3 percentage points per
year**. The largest shift was for **beautiful**, from
+24.6 to
+11.6 points.

![Unadjusted and adjusted leader slopes](outputs/leader-adjustment-sensitivity.svg)

| Signifier | Unadjusted (pp/year) | Adjusted (pp/year) | Adjusted clustered 95% CI |
|---|---:|---:|---:|
| beautiful | +24.6 | +11.6 | [-3.6, +26.7] |
| COVID survivor | +17.7 | +14.8 | [-2.9, +32.6] |
| pretty | +17.4 | +4.4 | [-11.4, +20.2] |
| amateur artist | +17.2 | +12.1 | [-3.3, +27.4] |
| romance fan | +16.4 | +5.9 | [-8.2, +20.0] |
| star wars fan | -14.2 | -10.8 | [-26.9, +5.2] |
| nba fan | -14.2 | -4.9 | [-20.9, +11.2] |
| social conservative | -13.6 | -10.9 | [-25.9, +4.2] |
| 2a supporter | -13.0 | -16.9 | [-32.5, -1.3] |
| planner | -12.7 | -15.8 | [-30.5, -1.2] |

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
**10.2 percentage points**. The largest contrast is
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
| COVID survivor | +17.7 | 45.0% | 53.9% | +8.8 | +11.2 | [-5.0, +27.4] |
| pretty | +17.4 | 35.0% | 48.6% | +13.5 | +7.1 | [-6.7, +20.9] |
| amateur artist | +17.2 | 20.8% | 32.0% | +11.2 | +11.7 | [-2.1, +25.5] |
| romance fan | +16.4 | 32.3% | 43.7% | +11.4 | +3.5 | [-9.3, +16.3] |
| star wars fan | -14.2 | 43.4% | 32.0% | -11.4 | -10.2 | [-24.4, +4.1] |
| nba fan | -14.2 | 37.4% | 26.9% | -10.4 | -2.1 | [-16.8, +12.5] |
| social conservative | -13.6 | 27.9% | 23.8% | -4.1 | -0.4 | [-14.6, +13.8] |
| 2a supporter | -13.0 | 29.5% | 18.5% | -11.0 | -21.3 | [-35.4, -7.2] |
| planner | -12.7 | 74.5% | 68.3% | -6.2 | -11.0 | [-25.0, +2.9] |

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
calendar periods: **2025-07-08–2025-10-26**,
**2025-10-27–2026-02-14**,
**2026-02-15–2026-06-05**, and
**2026-06-06–2026-09-24**.
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
96%
of its total absolute adjacent movement.

![Adjacent changes across four periods for selected leaders](outputs/leader-period-trajectory.svg)

| Signifier | P1 | P2 | P3 | P4 | Aligned transitions | Largest share of path |
|---|---:|---:|---:|---:|---:|---:|
| beautiful | 36.1% | 30.0% | 47.5% | 57.0% | 2/3 | 53% |
| COVID survivor | 42.7% | 47.5% | 49.5% | 59.1% | 3/3 | 58% |
| pretty | 40.8% | 30.2% | 46.4% | 51.0% | 2/3 | 51% |
| amateur artist | 20.6% | 21.0% | 26.0% | 37.4% | 3/3 | 68% |
| romance fan | 31.5% | 33.3% | 41.7% | 45.5% | 3/3 | 60% |
| star wars fan | 43.2% | 43.6% | 32.0% | 32.1% | 1/3 | 96% |
| nba fan | 38.2% | 36.4% | 26.7% | 27.2% | 2/3 | 81% |
| social conservative | 30.3% | 25.7% | 29.7% | 17.1% | 2/3 | 59% |
| 2a supporter | 32.2% | 27.4% | 15.5% | 21.3% | 2/3 | 52% |
| planner | 76.9% | 71.3% | 70.1% | 66.7% | 3/3 | 55% |

Standardizing each signifier's four periods to the same full-sample age,
observed-composition, weekday, and month distribution leaves
**20 of 20**
first-to-last changes in the selected linear direction. After adjustment,
**0** align in all three transitions
and **13** align in at least two. The
same transition remains the largest absolute move for
**8 of 20**
leaders. The median largest-transition share changes from
**58% raw** to
**54% adjusted**. The most
concentrated adjusted path is
**singer**, whose
period 3 to 4
move accounts for
80%
of its adjusted absolute path.

![Raw and adjusted concentration of four-period change](outputs/leader-period-adjustment-sensitivity.svg)

| Signifier | Adjusted P1 | Adjusted P2 | Adjusted P3 | Adjusted P4 | Aligned transitions | Largest share of path | Largest transition retained? |
|---|---:|---:|---:|---:|---:|---:|---:|
| beautiful | 32.8% | 37.6% | 53.3% | 44.9% | 2/3 | 54% | Yes |
| COVID survivor | 34.2% | 57.4% | 58.0% | 47.7% | 2/3 | 68% | No |
| pretty | 43.0% | 29.3% | 49.9% | 45.9% | 1/3 | 54% | Yes |
| amateur artist | 16.4% | 24.2% | 37.1% | 27.9% | 2/3 | 43% | No |
| romance fan | 27.6% | 51.4% | 40.3% | 33.7% | 1/3 | 57% | No |
| star wars fan | 51.4% | 31.7% | 27.3% | 39.9% | 2/3 | 54% | No |
| nba fan | 53.2% | 6.8% | 17.3% | 48.2% | 1/3 | 53% | No |
| social conservative | 36.4% | 3.9% | 33.6% | 29.5% | 2/3 | 49% | No |
| 2a supporter | 38.4% | 35.1% | -0.7% | 20.1% | 2/3 | 60% | Yes |
| planner | 78.6% | 64.1% | 77.9% | 65.0% | 2/3 | 35% | Yes |

The concentration share is descriptive: one-third represents three equally
sized absolute moves, while 100% means one transition contains all observed
adjacent movement. Raw period prevalence is unweighted. Adjusted prevalences
come from an additive linear-probability model standardized to a common
observed covariate mix; they control only recorded covariates and calendar
terms and supply no new inferential or discovery test. Because that model is
unbounded, standardized levels can fall outside 0%–100% and should be read as
model diagnostics rather than literal population prevalences. Both paths can
remain sensitive to repeated respondents, unobserved composition, period
boundaries, functional form, and selection of the 20 most extreme linear
slopes.

## Within-respondent sensitivity

A second targeted check separates two diagnostic changes. It first refits the
pooled trend using only people who answered the same signifier on multiple
dates, then absorbs a fixed effect for each of those respondents while keeping
the same observations. **16 of 20**
repeat-sample pooled slopes retained the all-response direction; **14
of 20** within-person slopes retained the repeat-sample
direction, and **12 of 20** retained
the original all-response direction. Restricting the sample moved a selected slope by a median absolute
**12.4 percentage points per year**; absorbing
respondent effects then moved it by **15.0
points**. The largest sample-restriction change was for
**star wars fan**, from
-14.2
to -44.8;
the largest repeat-pooled-to-within change was for
**team player**, from
-3.4
to +42.7.
The full all-response-to-within shift had median absolute magnitude
**13.3 points**, and the median selected signifier
had **26 repeat respondents**. For
**3** selected signifiers, no repeat respondent changed
endorsement; their zero within slopes are mechanical descriptions and clustered
intervals are not displayed.

![All-response, repeat-sample pooled, and within-respondent leader slopes](outputs/leader-within-respondent-sensitivity.svg)

| Signifier | All responses (pp/year) | Repeat sample, pooled (pp/year) | Within respondent (pp/year) | Within clustered 95% CI | Repeat respondents |
|---|---:|---:|---:|---:|---:|
| beautiful | +24.6 | +4.0 | -0.7 | [-2.6, +1.2] | 30 |
| COVID survivor | +17.7 | -10.4 | -15.2 | [-56.7, +26.3] | 28 |
| pretty | +17.4 | +13.7 | +8.5 | [-14.2, +31.1] | 27 |
| amateur artist | +17.2 | +9.6 | +10.8 | [-16.8, +38.4] | 28 |
| romance fan | +16.4 | +9.9 | -3.3 | [-33.2, +26.6] | 40 |
| star wars fan | -14.2 | -44.8 | -19.3 | [-57.8, +19.2] | 25 |
| nba fan | -14.2 | -25.9 | -2.7 | [-10.5, +5.2] | 19 |
| social conservative | -13.6 | +2.5 | +0.0 | No endorsement switches | 23 |
| 2a supporter | -13.0 | -31.9 | -13.2 | [-39.7, +13.2] | 27 |
| planner | -12.7 | -19.5 | -11.3 | [-50.0, +27.4] | 25 |

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
SHA-256 `f914207cd3626c6bd8197cb90509b95d6bdd05eca17c21cbe017908de19ffdb8`.

Liang, K.-Y., & Zeger, S. L. (1986). Longitudinal data analysis using
generalized linear models. *Biometrika, 73*(1), 13–22.
[https://doi.org/10.1093/biomet/73.1.13](https://doi.org/10.1093/biomet/73.1.13).

Benjamini, Y., & Hochberg, Y. (1995). Controlling the false discovery rate: A
practical and powerful approach to multiple testing. *Journal of the Royal
Statistical Society: Series B (Methodological), 57*(1), 289–300.
[https://doi.org/10.1111/j.2517-6161.1995.tb02031.x](https://doi.org/10.1111/j.2517-6161.1995.tb02031.x).
