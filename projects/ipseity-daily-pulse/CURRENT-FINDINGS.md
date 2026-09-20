# Current monitoring and prevalence findings

Current through the monitoring check at **2026-09-20T10:06:08Z**. This file is
replaced when the analysis is refreshed; it is not an archive.

## Monitor

The Ipseity Daily homepage and canonical microdata both returned HTTP 200. The
gzip parsed as UTF-8 CSV with the documented schema and contained
**706,425 observations** from **2025-07-08** through
**2026-09-19**, spanning **5,010 hashed respondents**
and **707 signifiers**. No malformed rows or duplicate
respondent/date/signifier keys were detected. The newest observation was
1 day behind the check date, and this
check records no anomaly.

![Cumulative observations over time](outputs/observation-growth.svg)

The cumulative series is derived from observation dates inside the current
microdata, while `data/monitoring-history.csv` preserves the separate sequence
of outside-in checks for longitudinal monitoring.

## Estimated signifier prevalence change

For each signifier, an unweighted linear probability model regresses its binary
endorsement response on observation date. The slope is annualized to percentage
points per year. The histogram includes **704 of
707 signifiers** with at least 300 responses,
30 distinct observation dates, and a 180-day
span. These are descriptive sample trends, not population-weighted or causal
estimates. The median estimate is **+0.6
percentage points per year**; the middle half runs from -1.6 to
+3.2 points.

![Histogram of estimated annual prevalence growth](outputs/annual-prevalence-growth-histogram.svg)

Uncertainty now uses a respondent-clustered sandwich estimator, so repeat
answers by the same hashed respondent are not treated as independent. The file
contains **531,875 respondent–signifier clusters**;
the largest has 50 responses. Across 704 eligible
trend tests, **0** have Benjamini–Hochberg q-values at or below
0.05, and **0** meet the more conservative Bonferroni
0.05 threshold.

### Fastest estimated growth

| Signifier | Annual change (pp) | Clustered 95% CI | BH q | Bonferroni p | Responses |
|---|---:|---:|---:|---:|---:|
| beautiful | +22.9 | [+9.3, +36.5] | 0.109 | 0.669 | 449 |
| romance fan | +18.0 | [+5.2, +30.8] | 0.308 | 1.000 | 460 |
| pretty | +17.5 | [+3.3, +31.8] | 0.402 | 1.000 | 418 |
| amateur artist | +17.5 | [+5.0, +29.9] | 0.308 | 1.000 | 418 |
| COVID survivor | +17.4 | [+2.7, +32.1] | 0.415 | 1.000 | 392 |

### Fastest estimated shrinkage

| Signifier | Annual change (pp) | Clustered 95% CI | BH q | Bonferroni p | Responses |
|---|---:|---:|---:|---:|---:|
| nba fan | -14.6 | [-27.9, -1.2] | 0.492 | 1.000 | 406 |
| star wars fan | -14.4 | [-27.6, -1.2] | 0.492 | 1.000 | 424 |
| social conservative | -13.9 | [-25.8, -2.0] | 0.423 | 1.000 | 427 |
| 2a supporter | -12.5 | [-25.8, +0.9] | 0.626 | 1.000 | 378 |
| planner | -12.1 | [-24.2, -0.1] | 0.585 | 1.000 | 410 |

The largest point estimate is **beautiful** at
22.9 percentage points
per year; the most negative is **nba fan** at
-14.6 points per year.
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
absolute slope shift was **5.4 percentage points per
year**. The largest shift was for **pretty**, from
+17.5 to
+5.3 points.

![Unadjusted and adjusted leader slopes](outputs/leader-adjustment-sensitivity.svg)

| Signifier | Unadjusted (pp/year) | Adjusted (pp/year) | Adjusted clustered 95% CI |
|---|---:|---:|---:|
| beautiful | +22.9 | +11.5 | [-4.0, +27.0] |
| romance fan | +18.0 | +7.6 | [-7.0, +22.2] |
| pretty | +17.5 | +5.3 | [-11.3, +22.0] |
| amateur artist | +17.5 | +9.2 | [-5.9, +24.3] |
| COVID survivor | +17.4 | +13.2 | [-5.1, +31.5] |
| nba fan | -14.6 | -6.1 | [-22.2, +10.1] |
| star wars fan | -14.4 | -11.5 | [-27.4, +4.4] |
| social conservative | -13.9 | -11.5 | [-26.7, +3.7] |
| 2a supporter | -12.5 | -15.8 | [-31.6, -0.1] |
| planner | -12.1 | -15.6 | [-31.2, +0.0] |

This selected-leader sensitivity is diagnostic, not a new discovery screen.
It cannot correct unobserved composition, nonrepresentative recruitment,
functional-form error, or selection of extremes from the full set of tests.

## Within-respondent sensitivity

A second targeted check separates two diagnostic changes. It first refits the
pooled trend using only people who answered the same signifier on multiple
dates, then absorbs a fixed effect for each of those respondents while keeping
the same observations. **16 of 20**
repeat-sample pooled slopes retained the all-response direction; **15
of 20** within-person slopes retained the repeat-sample
direction, and **13 of 20** retained
the original all-response direction. Restricting the sample moved a selected slope by a median absolute
**12.5 percentage points per year**; absorbing
respondent effects then moved it by **11.6
points**. The largest sample-restriction change was for
**star wars fan**, from
-14.4
to -42.4;
the largest repeat-pooled-to-within change was for
**team player**, from
-6.9
to +51.4.
The full all-response-to-within shift had median absolute magnitude
**14.0 points**, and the median selected signifier
had **25 repeat respondents**. For
**3** selected signifiers, no repeat respondent changed
endorsement; their zero within slopes are mechanical descriptions and clustered
intervals are not displayed.

![All-response, repeat-sample pooled, and within-respondent leader slopes](outputs/leader-within-respondent-sensitivity.svg)

| Signifier | All responses (pp/year) | Repeat sample, pooled (pp/year) | Within respondent (pp/year) | Within clustered 95% CI | Repeat respondents |
|---|---:|---:|---:|---:|---:|
| beautiful | +22.9 | +4.0 | -0.7 | [-2.6, +1.2] | 30 |
| romance fan | +18.0 | +14.9 | +3.6 | [-21.0, +28.2] | 38 |
| pretty | +17.5 | +13.7 | +8.5 | [-14.2, +31.1] | 27 |
| amateur artist | +17.5 | +9.6 | +10.8 | [-16.8, +38.4] | 28 |
| COVID survivor | +17.4 | -10.4 | -15.2 | [-56.7, +26.3] | 28 |
| nba fan | -14.6 | -25.9 | -2.7 | [-10.5, +5.2] | 19 |
| star wars fan | -14.4 | -42.4 | -20.4 | [-60.9, +20.1] | 25 |
| social conservative | -13.9 | +2.5 | +0.0 | No endorsement switches | 23 |
| 2a supporter | -12.5 | -31.9 | -13.2 | [-39.7, +13.2] | 27 |
| planner | -12.1 | -8.2 | -11.1 | [-63.7, +41.5] | 25 |

The first comparison changes the analytic sample; the second holds those
observations fixed but changes the model from pooled to within respondent.
Their arithmetic shifts clarify where the displayed estimate changes, but they
are not a causal decomposition into turnover and individual change. The models
remain vulnerable to selective retention, time-varying confounding,
functional-form error, nonrepresentative recruitment, and selection of pooled
extremes. Their intervals are diagnostic rather than a discovery test.

Full machine-readable estimates, eligibility flags, and interval bounds are in
`outputs/signifier-growth.csv`; adjusted leader checks are in
`outputs/leader-adjusted-sensitivity.csv`; within-respondent checks are in
`outputs/leader-within-respondent-sensitivity.csv`; the daily and cumulative
counts are in `outputs/daily-observation-growth.csv`.

## Source

Jones, J. (2026). *Ipseity Daily Data* [Data set]. Zenodo.
[https://doi.org/10.5281/zenodo.22636514](https://doi.org/10.5281/zenodo.22636514).
The analysis used the newer canonical file served directly by the
[Ipseity Daily download page](https://jasonjones.ninja/social-science-dashboard-inator/ipseity-daily/download.html) at the check time;
SHA-256 `820d311436a00c2333d3b6d342da4ec45c138daa926d60baf00a5636b4b366c8`.

Liang, K.-Y., & Zeger, S. L. (1986). Longitudinal data analysis using
generalized linear models. *Biometrika, 73*(1), 13–22.
[https://doi.org/10.1093/biomet/73.1.13](https://doi.org/10.1093/biomet/73.1.13).

Benjamini, Y., & Hochberg, Y. (1995). Controlling the false discovery rate: A
practical and powerful approach to multiple testing. *Journal of the Royal
Statistical Society: Series B (Methodological), 57*(1), 289–300.
[https://doi.org/10.1111/j.2517-6161.1995.tb02031.x](https://doi.org/10.1111/j.2517-6161.1995.tb02031.x).
