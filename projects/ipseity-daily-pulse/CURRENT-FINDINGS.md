# Current monitoring and prevalence findings

Current through the monitoring check at **2026-09-16T20:47:07Z**. This file is
replaced when the analysis is refreshed; it is not an archive.

## Monitor

The Ipseity Daily homepage and canonical microdata both returned HTTP 200. The
gzip parsed as UTF-8 CSV with the documented schema and contained
**699,835 observations** from **2025-07-08** through
**2026-09-15**, spanning **4,979 hashed respondents**
and **707 signifiers**. No malformed rows or duplicate
respondent/date/signifier keys were detected. The newest observation was
1 day behind the check date, so this
first check records no anomaly.

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

### Fastest estimated growth

| Signifier | Annual change (pp) | Approx. 95% CI | Responses | Overall yes |
|---|---:|---:|---:|---:|
| beautiful | +24.4 | [+11.1, +37.7] | 445 | 41.6% |
| romance fan | +17.9 | [+5.2, +30.6] | 456 | 37.5% |
| exhausted | +17.9 | [+4.8, +31.0] | 420 | 41.2% |
| pretty | +17.6 | [+3.2, +31.9] | 416 | 41.6% |
| COVID survivor | +17.4 | [+2.5, +32.3] | 387 | 49.1% |

### Fastest estimated shrinkage

| Signifier | Annual change (pp) | Approx. 95% CI | Responses | Overall yes |
|---|---:|---:|---:|---:|
| star wars fan | -15.5 | [-28.8, -2.1] | 417 | 37.9% |
| social conservative | -15.3 | [-27.5, -3.0] | 422 | 25.6% |
| nba fan | -14.3 | [-27.6, -0.9] | 405 | 31.9% |
| 2a supporter | -12.2 | [-25.2, +0.8] | 377 | 24.7% |
| planner | -12.2 | [-24.4, -0.0] | 407 | 72.0% |

The largest point estimate is **beautiful** at
24.4 percentage points
per year; the most negative is **star wars fan** at
-15.5 points per year.
The intervals are ordinary model-based intervals. They do not adjust for
repeated respondents, changing sample composition, or selecting extremes from
704 simultaneous estimates. The rankings are therefore leads for
continued monitoring, not evidence that the underlying US adult population
changed at those rates.

Full machine-readable estimates, eligibility flags, and interval bounds are in
`outputs/signifier-growth.csv`; the daily and cumulative counts are in
`outputs/daily-observation-growth.csv`.

## Source

Jones, J. (2026). *Ipseity Daily Data* [Data set]. Zenodo.
[https://doi.org/10.5281/zenodo.22636514](https://doi.org/10.5281/zenodo.22636514).
The analysis used the newer canonical file served directly by the
[Ipseity Daily download page](https://jasonjones.ninja/social-science-dashboard-inator/ipseity-daily/download.html) at the check time;
SHA-256 `b0b5cae9027284acaa28905c22a0ed8fb1357a434c931d31e747687d7fd1fa27`.
