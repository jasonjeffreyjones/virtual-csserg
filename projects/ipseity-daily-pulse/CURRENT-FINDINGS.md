# Current monitoring and prevalence findings

Current through the monitoring check at **2026-09-19T10:07:11Z**. This file is
replaced when the analysis is refreshed; it is not an archive.

## Monitor

The Ipseity Daily homepage and canonical microdata both returned HTTP 200. The
gzip parsed as UTF-8 CSV with the documented schema and contained
**704,797 observations** from **2025-07-08** through
**2026-09-18**, spanning **5,005 hashed respondents**
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
estimates. The median estimate is **+0.5
percentage points per year**; the middle half runs from -1.7 to
+3.2 points.

![Histogram of estimated annual prevalence growth](outputs/annual-prevalence-growth-histogram.svg)

Uncertainty now uses a respondent-clustered sandwich estimator, so repeat
answers by the same hashed respondent are not treated as independent. The file
contains **530,903 respondent–signifier clusters**;
the largest has 49 responses. Across 704 eligible
trend tests, **0** have Benjamini–Hochberg q-values at or below
0.05, and **0** meet the more conservative Bonferroni
0.05 threshold.

### Fastest estimated growth

| Signifier | Annual change (pp) | Clustered 95% CI | BH q | Bonferroni p | Responses |
|---|---:|---:|---:|---:|---:|
| beautiful | +23.6 | [+9.9, +37.2] | 0.104 | 0.492 | 448 |
| pretty | +17.5 | [+3.3, +31.8] | 0.397 | 1.000 | 418 |
| amateur artist | +17.5 | [+5.0, +29.9] | 0.332 | 1.000 | 418 |
| romance fan | +17.4 | [+4.6, +30.2] | 0.363 | 1.000 | 459 |
| exhausted | +17.3 | [+4.4, +30.1] | 0.363 | 1.000 | 423 |

### Fastest estimated shrinkage

| Signifier | Annual change (pp) | Clustered 95% CI | BH q | Bonferroni p | Responses |
|---|---:|---:|---:|---:|---:|
| social conservative | -14.9 | [-26.7, -3.0] | 0.380 | 1.000 | 426 |
| nba fan | -14.3 | [-27.7, -0.8] | 0.546 | 1.000 | 405 |
| star wars fan | -14.0 | [-27.3, -0.8] | 0.546 | 1.000 | 423 |
| 2a supporter | -12.5 | [-25.8, +0.9] | 0.631 | 1.000 | 378 |
| planner | -12.1 | [-24.2, -0.1] | 0.582 | 1.000 | 410 |

The largest point estimate is **beautiful** at
23.6 percentage points
per year; the most negative is **social conservative** at
-14.9 points per year.
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
ethnicity, student status, employment, weekday, and month of year. **19
of 20** leaders retained their original direction. The median
absolute slope shift was **6.1 percentage points per
year**. The largest shift was for **pretty**, from
+17.5 to
+5.3 points.

![Unadjusted and adjusted leader slopes](outputs/leader-adjustment-sensitivity.svg)

| Signifier | Unadjusted (pp/year) | Adjusted (pp/year) | Adjusted clustered 95% CI |
|---|---:|---:|---:|
| beautiful | +23.6 | +12.3 | [-3.4, +28.0] |
| pretty | +17.5 | +5.3 | [-11.3, +22.0] |
| amateur artist | +17.5 | +9.2 | [-5.9, +24.3] |
| romance fan | +17.4 | +7.6 | [-7.0, +22.2] |
| exhausted | +17.3 | +15.2 | [-0.0, +30.3] |
| social conservative | -14.9 | -12.9 | [-27.9, +2.2] |
| nba fan | -14.3 | -5.3 | [-21.5, +11.0] |
| star wars fan | -14.0 | -11.4 | [-27.3, +4.5] |
| 2a supporter | -12.5 | -15.8 | [-31.6, -0.1] |
| planner | -12.1 | -15.6 | [-31.2, +0.0] |

This selected-leader sensitivity is diagnostic, not a new discovery screen.
It cannot correct unobserved composition, nonrepresentative recruitment,
functional-form error, or selection of extremes from the full set of tests.

## Within-respondent sensitivity

A second targeted check absorbs a fixed effect for each hashed respondent and
therefore estimates change only from people who answered the same signifier on
multiple dates. **13 of 20** pooled
leaders retained their direction. The median absolute pooled-to-within shift
was **13.9 percentage points per year**, and the
median selected signifier had **26 repeat
respondents**. The largest shift was for **overthinker**,
from +14.3
to -20.5
points. For **2** selected signifiers, no repeat respondent
changed endorsement; their zero within slopes are mechanical descriptions and
clustered intervals are not displayed.

![Pooled and within-respondent leader slopes](outputs/leader-within-respondent-sensitivity.svg)

| Signifier | Pooled (pp/year) | Within respondent (pp/year) | Within clustered 95% CI | Repeat respondents |
|---|---:|---:|---:|---:|
| beautiful | +23.6 | -0.7 | [-2.6, +1.2] | 30 |
| pretty | +17.5 | +8.5 | [-14.2, +31.1] | 27 |
| amateur artist | +17.5 | +10.8 | [-16.8, +38.4] | 28 |
| romance fan | +17.4 | +3.6 | [-21.0, +28.2] | 38 |
| exhausted | +17.3 | +2.8 | [-54.4, +59.9] | 20 |
| social conservative | -14.9 | +0.0 | No endorsement switches | 23 |
| nba fan | -14.3 | -2.7 | [-10.5, +5.2] | 19 |
| star wars fan | -14.0 | -20.4 | [-60.9, +20.1] | 25 |
| 2a supporter | -12.5 | -13.2 | [-39.7, +13.2] | 27 |
| planner | -12.1 | -11.1 | [-63.7, +41.5] | 25 |

This comparison removes stable differences between respondents, but it is not
a literal decomposition of the pooled trend into turnover and individual
change. The fixed-effect estimate uses only repeat respondents, so it also
changes the analytic sample; it remains vulnerable to selective retention,
time-varying confounding, functional-form error, and selection of the pooled
extremes. Its intervals are diagnostic rather than a discovery test.

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
SHA-256 `445ea5b5dee32d387c7b403766328528fc10c9491e8cd200ad2cca2b68c3d767`.

Liang, K.-Y., & Zeger, S. L. (1986). Longitudinal data analysis using
generalized linear models. *Biometrika, 73*(1), 13–22.
[https://doi.org/10.1093/biomet/73.1.13](https://doi.org/10.1093/biomet/73.1.13).

Benjamini, Y., & Hochberg, Y. (1995). Controlling the false discovery rate: A
practical and powerful approach to multiple testing. *Journal of the Royal
Statistical Society: Series B (Methodological), 57*(1), 289–300.
[https://doi.org/10.1111/j.2517-6161.1995.tb02031.x](https://doi.org/10.1111/j.2517-6161.1995.tb02031.x).
