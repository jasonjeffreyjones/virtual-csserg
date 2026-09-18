# Current monitoring and prevalence findings

Current through the monitoring check at **2026-09-18T10:02:22Z**. This file is
replaced when the analysis is refreshed; it is not an archive.

## Monitor

The Ipseity Daily homepage and canonical microdata both returned HTTP 200. The
gzip parsed as UTF-8 CSV with the documented schema and contained
**703,140 observations** from **2025-07-08** through
**2026-09-17**, spanning **4,997 hashed respondents**
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
contains **529,833 respondent–signifier clusters**;
the largest has 49 responses. Across 704 eligible
trend tests, **0** have Benjamini–Hochberg q-values at or below
0.05, and **0** meet the more conservative Bonferroni
0.05 threshold.

### Fastest estimated growth

| Signifier | Annual change (pp) | Clustered 95% CI | BH q | Bonferroni p | Responses |
|---|---:|---:|---:|---:|---:|
| beautiful | +23.6 | [+9.9, +37.2] | 0.124 | 0.492 | 448 |
| romance fan | +18.0 | [+5.1, +30.8] | 0.316 | 1.000 | 458 |
| amateur artist | +17.5 | [+5.0, +29.9] | 0.316 | 1.000 | 418 |
| COVID survivor | +17.1 | [+2.2, +32.1] | 0.495 | 1.000 | 389 |
| pretty | +16.9 | [+2.6, +31.2] | 0.451 | 1.000 | 417 |

### Fastest estimated shrinkage

| Signifier | Annual change (pp) | Clustered 95% CI | BH q | Bonferroni p | Responses |
|---|---:|---:|---:|---:|---:|
| social conservative | -15.9 | [-27.7, -4.0] | 0.329 | 1.000 | 425 |
| nba fan | -14.3 | [-27.7, -0.8] | 0.538 | 1.000 | 405 |
| star wars fan | -13.7 | [-27.0, -0.4] | 0.560 | 1.000 | 422 |
| planner | -13.0 | [-25.1, -0.9] | 0.538 | 1.000 | 408 |
| 2a supporter | -12.2 | [-25.7, +1.2] | 0.639 | 1.000 | 377 |

The largest point estimate is **beautiful** at
23.6 percentage points
per year; the most negative is **social conservative** at
-15.9 points per year.
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
+16.9 to
+4.8 points.

![Unadjusted and adjusted leader slopes](outputs/leader-adjustment-sensitivity.svg)

| Signifier | Unadjusted (pp/year) | Adjusted (pp/year) | Adjusted clustered 95% CI |
|---|---:|---:|---:|
| beautiful | +23.6 | +12.3 | [-3.4, +28.0] |
| romance fan | +18.0 | +8.1 | [-6.7, +22.8] |
| amateur artist | +17.5 | +9.2 | [-5.9, +24.3] |
| COVID survivor | +17.1 | +11.5 | [-7.4, +30.4] |
| pretty | +16.9 | +4.8 | [-12.1, +21.8] |
| social conservative | -15.9 | -14.8 | [-29.5, -0.0] |
| nba fan | -14.3 | -5.3 | [-21.5, +11.0] |
| star wars fan | -13.7 | -11.3 | [-27.3, +4.7] |
| planner | -13.0 | -17.2 | [-32.9, -1.5] |
| 2a supporter | -12.2 | -14.8 | [-30.7, +1.1] |

This selected-leader sensitivity is diagnostic, not a new discovery screen.
It cannot correct unobserved composition, nonrepresentative recruitment,
functional-form error, or selection of extremes from the full set of tests.

Full machine-readable estimates, eligibility flags, and interval bounds are in
`outputs/signifier-growth.csv`; adjusted leader checks are in
`outputs/leader-adjusted-sensitivity.csv`; the daily and cumulative counts are
in `outputs/daily-observation-growth.csv`.

## Source

Jones, J. (2026). *Ipseity Daily Data* [Data set]. Zenodo.
[https://doi.org/10.5281/zenodo.22636514](https://doi.org/10.5281/zenodo.22636514).
The analysis used the newer canonical file served directly by the
[Ipseity Daily download page](https://jasonjones.ninja/social-science-dashboard-inator/ipseity-daily/download.html) at the check time;
SHA-256 `b6a6d70f42daa116df249450c816e5ab2ad815332dad50199d60eb31135fbe0d`.

Liang, K.-Y., & Zeger, S. L. (1986). Longitudinal data analysis using
generalized linear models. *Biometrika, 73*(1), 13–22.
[https://doi.org/10.1093/biomet/73.1.13](https://doi.org/10.1093/biomet/73.1.13).

Benjamini, Y., & Hochberg, Y. (1995). Controlling the false discovery rate: A
practical and powerful approach to multiple testing. *Journal of the Royal
Statistical Society: Series B (Methodological), 57*(1), 289–300.
[https://doi.org/10.1111/j.2517-6161.1995.tb02031.x](https://doi.org/10.1111/j.2517-6161.1995.tb02031.x).
