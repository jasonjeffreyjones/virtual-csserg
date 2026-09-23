# Current monitoring and prevalence findings

Current through the monitoring check at **2026-09-23T10:09:23Z**. This file is
replaced when the analysis is refreshed; it is not an archive.

## Monitor

The Ipseity Daily homepage and canonical microdata both returned HTTP 200. The
gzip parsed as UTF-8 CSV with the documented schema and contained
**711,318 observations** from **2025-07-08** through
**2026-09-22**, spanning **5,037 hashed respondents**
and **707 signifiers**. No malformed rows or duplicate
respondent/date/signifier keys were detected. The newest observation was
1 day behind the check date, and this
check records no anomaly.

![Cumulative observations over time](outputs/observation-growth.svg)

The cumulative series is derived from observation dates inside the current
microdata, while `data/monitoring-history.csv` preserves the separate sequence
of outside-in checks for longitudinal monitoring. Across
**8 checks**, **8**
had a reachable homepage, a retrieved and parseable canonical file, and no
anomaly. The file gained
**11,483 observations** from
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
estimates. The median estimate is **+0.6
percentage points per year**; the middle half runs from -1.7 to
+3.1 points.

![Histogram of estimated annual prevalence growth](outputs/annual-prevalence-growth-histogram.svg)

Uncertainty now uses a respondent-clustered sandwich estimator, so repeat
answers by the same hashed respondent are not treated as independent. The file
contains **535,136 respondent–signifier clusters**;
the largest has 50 responses. Across 704 eligible
trend tests, **0** have Benjamini–Hochberg q-values at or below
0.05, and **0** meet the more conservative Bonferroni
0.05 threshold.

### Fastest estimated growth

| Signifier | Annual change (pp) | Clustered 95% CI | BH q | Bonferroni p | Responses |
|---|---:|---:|---:|---:|---:|
| beautiful | +24.3 | [+11.0, +37.6] | 0.111 | 0.246 | 454 |
| COVID survivor | +17.9 | [+3.3, +32.6] | 0.399 | 1.000 | 393 |
| romance fan | +17.5 | [+4.8, +30.1] | 0.334 | 1.000 | 463 |
| amateur artist | +17.3 | [+5.0, +29.7] | 0.321 | 1.000 | 421 |
| pretty | +16.8 | [+2.7, +31.0] | 0.429 | 1.000 | 419 |

### Fastest estimated shrinkage

| Signifier | Annual change (pp) | Clustered 95% CI | BH q | Bonferroni p | Responses |
|---|---:|---:|---:|---:|---:|
| star wars fan | -13.9 | [-27.1, -0.8] | 0.521 | 1.000 | 426 |
| nba fan | -13.6 | [-27.0, -0.2] | 0.563 | 1.000 | 407 |
| social conservative | -13.1 | [-25.1, -1.2] | 0.515 | 1.000 | 429 |
| 2a supporter | -12.7 | [-26.0, +0.5] | 0.599 | 1.000 | 379 |
| Reddit user | -12.6 | [-25.5, +0.3] | 0.599 | 1.000 | 400 |

The largest point estimate is **beautiful** at
24.3 percentage points
per year; the most negative is **star wars fan** at
-13.9 points per year.
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
absolute slope shift was **5.5 percentage points per
year**. The largest shift was for **pretty**, from
+16.8 to
+5.0 points.

![Unadjusted and adjusted leader slopes](outputs/leader-adjustment-sensitivity.svg)

| Signifier | Unadjusted (pp/year) | Adjusted (pp/year) | Adjusted clustered 95% CI |
|---|---:|---:|---:|
| beautiful | +24.3 | +12.5 | [-2.7, +27.7] |
| COVID survivor | +17.9 | +14.1 | [-3.9, +32.1] |
| romance fan | +17.5 | +7.3 | [-6.9, +21.5] |
| amateur artist | +17.3 | +11.7 | [-3.9, +27.4] |
| pretty | +16.8 | +5.0 | [-11.1, +21.2] |
| star wars fan | -13.9 | -10.1 | [-26.2, +5.9] |
| nba fan | -13.6 | -4.8 | [-20.9, +11.3] |
| social conservative | -13.1 | -10.4 | [-25.6, +4.8] |
| 2a supporter | -12.7 | -16.3 | [-31.9, -0.7] |
| Reddit user | -12.6 | -19.8 | [-35.4, -4.2] |

This selected-leader sensitivity is diagnostic, not a new discovery screen.
It cannot correct unobserved composition, nonrepresentative recruitment,
functional-form error, or selection of extremes from the full set of tests.

## Early-versus-late period sensitivity

To relax the assumption that prevalence follows one straight line, a
prespecified two-period check divides the full observation window at its
calendar midpoint, **2026-02-13**. For the
same selected leaders, it compares unweighted prevalence after that date with
prevalence on or before it. **20 of
20** contrasts have the same direction as the
selected linear slope. The median absolute late-minus-early difference is
**10.2 percentage points**. The largest contrast is
for **beautiful**:
33.2% early
versus 51.4%
late, a +18.2-point
difference.

The two-period contrast was then adjusted for the same age, observed sample
composition, weekday, and month terms as the linear sensitivity. **19
of 20** adjusted contrasts retain the selected
linear slope's direction, and **19 of
20** retain the raw contrast's direction. Adjustment
moves a contrast by a median absolute **4.2
percentage points**. The largest shift is for
**Reddit user**, from
-6.0
to
-18.2
points.

![Raw and adjusted late-half versus early-half contrasts](outputs/leader-early-late-sensitivity.svg)

| Signifier | Linear slope (pp/year) | Early prevalence | Late prevalence | Raw contrast (pp) | Adjusted contrast (pp) | Adjusted clustered 95% CI |
|---|---:|---:|---:|---:|---:|---:|
| beautiful | +24.3 | 33.2% | 51.4% | +18.2 | +13.0 | [-1.3, +27.3] |
| COVID survivor | +17.9 | 45.0% | 53.9% | +8.9 | +10.6 | [-5.8, +27.0] |
| romance fan | +17.5 | 32.4% | 43.8% | +11.4 | +4.7 | [-8.1, +17.4] |
| amateur artist | +17.3 | 20.8% | 32.0% | +11.2 | +11.4 | [-2.6, +25.4] |
| pretty | +16.8 | 35.0% | 48.3% | +13.2 | +7.6 | [-6.4, +21.5] |
| star wars fan | -13.9 | 43.6% | 32.0% | -11.6 | -10.0 | [-24.2, +4.2] |
| nba fan | -13.6 | 37.8% | 26.9% | -10.8 | -4.3 | [-19.0, +10.3] |
| social conservative | -13.1 | 27.9% | 24.0% | -3.9 | -0.0 | [-14.3, +14.3] |
| 2a supporter | -12.7 | 29.8% | 18.4% | -11.4 | -22.7 | [-36.8, -8.6] |
| Reddit user | -12.6 | 72.9% | 66.8% | -6.0 | -18.2 | [-32.8, -3.6] |

This contrast does not impose a trajectory within either half, but it can hide
shorter reversals. The adjusted version addresses only the recorded covariates
and calendar terms; neither version corrects unobserved composition,
nonrepresentative recruitment, or selection of the 20 linear-trend extremes.
Their percentage-point magnitudes are not on the same scale as the annualized
linear slope; only directions are compared. The clustered intervals are
diagnostic, not a discovery screen.

## Within-respondent sensitivity

A second targeted check separates two diagnostic changes. It first refits the
pooled trend using only people who answered the same signifier on multiple
dates, then absorbs a fixed effect for each of those respondents while keeping
the same observations. **16 of 20**
repeat-sample pooled slopes retained the all-response direction; **15
of 20** within-person slopes retained the repeat-sample
direction, and **13 of 20** retained
the original all-response direction. Restricting the sample moved a selected slope by a median absolute
**12.7 percentage points per year**; absorbing
respondent effects then moved it by **13.4
points**. The largest sample-restriction change was for
**star wars fan**, from
-13.9
to -42.4;
the largest repeat-pooled-to-within change was for
**team player**, from
-3.4
to +42.7.
The full all-response-to-within shift had median absolute magnitude
**13.1 points**, and the median selected signifier
had **26 repeat respondents**. For
**3** selected signifiers, no repeat respondent changed
endorsement; their zero within slopes are mechanical descriptions and clustered
intervals are not displayed.

![All-response, repeat-sample pooled, and within-respondent leader slopes](outputs/leader-within-respondent-sensitivity.svg)

| Signifier | All responses (pp/year) | Repeat sample, pooled (pp/year) | Within respondent (pp/year) | Within clustered 95% CI | Repeat respondents |
|---|---:|---:|---:|---:|---:|
| beautiful | +24.3 | +4.0 | -0.7 | [-2.6, +1.2] | 30 |
| COVID survivor | +17.9 | -10.4 | -15.2 | [-56.7, +26.3] | 28 |
| romance fan | +17.5 | +14.9 | +3.6 | [-21.0, +28.2] | 38 |
| amateur artist | +17.3 | +9.6 | +10.8 | [-16.8, +38.4] | 28 |
| pretty | +16.8 | +13.7 | +8.5 | [-14.2, +31.1] | 27 |
| star wars fan | -13.9 | -42.4 | -20.4 | [-60.9, +20.1] | 25 |
| nba fan | -13.6 | -25.9 | -2.7 | [-10.5, +5.2] | 19 |
| social conservative | -13.1 | +2.5 | +0.0 | No endorsement switches | 23 |
| 2a supporter | -12.7 | -31.9 | -13.2 | [-39.7, +13.2] | 27 |
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
`outputs/leader-early-late-sensitivity.csv`; within-respondent checks are in
`outputs/leader-within-respondent-sensitivity.csv`; the daily and cumulative
counts are in `outputs/daily-observation-growth.csv`.

## Source

Jones, J. (2026). *Ipseity Daily Data* [Data set]. Zenodo.
[https://doi.org/10.5281/zenodo.22636514](https://doi.org/10.5281/zenodo.22636514).
The analysis used the newer canonical file served directly by the
[Ipseity Daily download page](https://jasonjones.ninja/social-science-dashboard-inator/ipseity-daily/download.html) at the check time;
SHA-256 `4badcfea9c902355a2de9215fa1af4beda935758eabd57b24994106406253b10`.

Liang, K.-Y., & Zeger, S. L. (1986). Longitudinal data analysis using
generalized linear models. *Biometrika, 73*(1), 13–22.
[https://doi.org/10.1093/biomet/73.1.13](https://doi.org/10.1093/biomet/73.1.13).

Benjamini, Y., & Hochberg, Y. (1995). Controlling the false discovery rate: A
practical and powerful approach to multiple testing. *Journal of the Royal
Statistical Society: Series B (Methodological), 57*(1), 289–300.
[https://doi.org/10.1111/j.2517-6161.1995.tb02031.x](https://doi.org/10.1111/j.2517-6161.1995.tb02031.x).
