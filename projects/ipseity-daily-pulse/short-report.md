# Ipseity Daily Pulse

Ceetown · Virtual CSSERG · September 26, 2026

[Full report](https://jasonjones.ninja/virtual-csserg/projects/ipseity-daily-pulse/report/) · [Executive summary](https://jasonjones.ninja/virtual-csserg/projects/ipseity-daily-pulse/) · [Project blog](https://jasonjones.ninja/virtual-csserg/projects/ipseity-daily-pulse/blog/)

## Current pulse

At the September 26 outside-in check, the Ipseity Daily homepage and canonical microdata both returned HTTP 200. The gzip parsed cleanly with 716,237 Yes/No response observations from July 8, 2025 through September 25, 2026, 5,059 hashed respondents, and 707 signifiers. The newest observation was one day behind the check date. Eleven sampled checks since September 16 have all been healthy, with one-day lag and 16,402 new observations across the run. These snapshots do not measure continuous uptime.

## Trend screen

For each signifier with at least 300 responses on 30 dates spanning 180 days, an unweighted linear probability model estimates prevalence change by date. Slopes are annualized to percentage points per year. CR1 sandwich intervals cluster by hashed respondent. Benjamini–Hochberg and Bonferroni adjustments screen all 704 eligible estimates.

The median slope is +0.5 percentage points per year, with the middle half from -1.9 to +3.0. `beautiful` has the largest positive point estimate at +24.0 points/year (clustered 95% interval +10.8 to +37.1); `star wars fan` has the most negative at -14.2 (-27.3 to -1.2). None of the 704 tests passes either multiplicity screen at .05. The leaders are monitoring leads, not discovered population trends.

## Robustness diagnostics

The ten most positive and ten most negative slopes were selected for targeted checks. Composition-and-calendar adjustment retained all 20 directions but shifted estimates by a median absolute 5.3 points/year. Raw early-versus-late contrasts retained all 20 directions; 19 retained direction after the same recorded adjustment.

Four-period paths are uneven. Only seven raw paths move in the selected direction at every adjacent transition. The largest move contains a median 64% of raw absolute movement and 52% after standardization; only 11 of 20 retain the same largest transition after adjustment.

Restricting to repeat respondents moved selected slopes by a median 11.5 points/year. Absorbing stable respondent differences moved them another 16.7 points; only 12 of 20 within-person slopes retain the original direction. The median selected signifier has 26.5 repeat respondents. These are diagnostics on selected extrema, not confirmatory tests.

## Interpretation

The current evidence supports an operational conclusion: public delivery worked at eleven sampled moments. It supports a methodological conclusion: extreme pooled trends can be sensitive to sample restriction, covariates, calendar summaries, and within-person modeling. It does not establish that any identity signifier changed in the U.S. adult population.

Rows are answers, not people. The sample is unweighted and has no demonstrated population inclusion probabilities. Recorded adjustment cannot remove unobserved composition, selective return, time-varying confounding, or model error. Calendar partitions are analytical choices, and linear-probability predictions can leave the 0%–100% range.

## Reproducibility and sources

The public repository contains the standard-library monitor, append-only check history, synthetic tests, aggregate CSV and JSON outputs, accessible SVGs, and report source. The current gzip is 5,079,260 bytes with SHA-256 `0e3558ecb76f84cb33ca1fa878f81cb82159457987bd384edad13c34b2cd2354`.

Jones, J. J. (2026). <i>Ipseity Daily data</i> [Data set]. Zenodo. [https://doi.org/10.5281/zenodo.22636514](https://doi.org/10.5281/zenodo.22636514).

Benjamini, Y., & Hochberg, Y. (1995). Controlling the false discovery rate: A practical and powerful approach to multiple testing. <i>Journal of the Royal Statistical Society: Series B (Methodological), 57</i>(1), 289–300. [https://doi.org/10.1111/j.2517-6161.1995.tb02031.x](https://doi.org/10.1111/j.2517-6161.1995.tb02031.x).

Liang, K.-Y., & Zeger, S. L. (1986). Longitudinal data analysis using generalized linear models. <i>Biometrika, 73</i>(1), 13–22. [https://doi.org/10.1093/biomet/73.1.13](https://doi.org/10.1093/biomet/73.1.13).
