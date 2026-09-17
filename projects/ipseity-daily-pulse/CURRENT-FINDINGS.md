# Current monitoring and prevalence findings

Current through the monitoring check at **2026-09-17T10:02:27Z**. This file is
replaced when the analysis is refreshed; it is not an archive.

## Monitor

The Ipseity Daily homepage and canonical microdata both returned HTTP 200. The
gzip parsed as UTF-8 CSV with the documented schema and contained
**701,503 observations** from **2025-07-08** through
**2026-09-16**, spanning **4,987 hashed respondents**
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
contains **528,734 respondent–signifier clusters**;
the largest has 49 responses. Across 704 eligible
trend tests, **0** have Benjamini–Hochberg q-values at or below
0.05, and **0** meet the more conservative Bonferroni
0.05 threshold.

### Fastest estimated growth

| Signifier | Annual change (pp) | Clustered 95% CI | BH q | Bonferroni p | Responses |
|---|---:|---:|---:|---:|---:|
| beautiful | +24.9 | [+11.2, +38.6] | 0.157 | 0.258 | 446 |
| romance fan | +18.0 | [+5.1, +30.8] | 0.316 | 1.000 | 458 |
| pretty | +17.6 | [+3.2, +31.9] | 0.395 | 1.000 | 416 |
| amateur artist | +17.5 | [+5.0, +29.9] | 0.316 | 1.000 | 418 |
| COVID survivor | +17.1 | [+2.2, +32.1] | 0.484 | 1.000 | 389 |

### Fastest estimated shrinkage

| Signifier | Annual change (pp) | Clustered 95% CI | BH q | Bonferroni p | Responses |
|---|---:|---:|---:|---:|---:|
| social conservative | -15.7 | [-27.6, -3.7] | 0.341 | 1.000 | 424 |
| star wars fan | -14.5 | [-27.8, -1.2] | 0.546 | 1.000 | 421 |
| nba fan | -14.3 | [-27.7, -0.8] | 0.554 | 1.000 | 405 |
| 2a supporter | -12.2 | [-25.7, +1.2] | 0.655 | 1.000 | 377 |
| planner | -12.2 | [-24.4, -0.1] | 0.588 | 1.000 | 407 |

The largest point estimate is **beautiful** at
24.9 percentage points
per year; the most negative is **social conservative** at
-15.7 points per year.
The intervals account for dependence within hashed respondents but not changing
sample composition, calendar structure, or model misspecification. The
Benjamini–Hochberg screen follows the original independent-test procedure;
correlation among signifier tests makes the Bonferroni column an important
conservative sensitivity check. Point-estimate rankings selected from
704 tests remain monitoring leads, not evidence that the underlying
US adult population changed at those rates.

Full machine-readable estimates, eligibility flags, and interval bounds are in
`outputs/signifier-growth.csv`; the daily and cumulative counts are in
`outputs/daily-observation-growth.csv`.

## Source

Jones, J. (2026). *Ipseity Daily Data* [Data set]. Zenodo.
[https://doi.org/10.5281/zenodo.22636514](https://doi.org/10.5281/zenodo.22636514).
The analysis used the newer canonical file served directly by the
[Ipseity Daily download page](https://jasonjones.ninja/social-science-dashboard-inator/ipseity-daily/download.html) at the check time;
SHA-256 `2f683b69af5152bb89223f432a4dbf6fea10f2ac99e19053cf35cbd74c473232`.

Liang, K.-Y., & Zeger, S. L. (1986). Longitudinal data analysis using
generalized linear models. *Biometrika, 73*(1), 13–22.
[https://doi.org/10.1093/biomet/73.1.13](https://doi.org/10.1093/biomet/73.1.13).

Benjamini, Y., & Hochberg, Y. (1995). Controlling the false discovery rate: A
practical and powerful approach to multiple testing. *Journal of the Royal
Statistical Society: Series B (Methodological), 57*(1), 289–300.
[https://doi.org/10.1111/j.2517-6161.1995.tb02031.x](https://doi.org/10.1111/j.2517-6161.1995.tb02031.x).
