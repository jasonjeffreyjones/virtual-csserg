# RQ1 Methods and Data Notes

## Sources consulted

- [Ipseity Daily](https://jasonjones.ninja/social-science-dashboard-inator/ipseity-daily/) describes the recurring survey and the identity-signifier measurement.
- [Expert Mode download instructions](https://jasonjones.ninja/social-science-dashboard-inator/ipseity-daily/download.html) identify the responses and demographics microdata and require an inner join on `hashed_respondent_id` and `obs_date`.
- [Building the Ipseome: Large, Free, Open, Human Identity Data](https://arxiv.org/abs/2607.02488) describes Ipseity Daily as a repeated cross-sectional survey of American adults. At the paper's snapshot, each daily respondent saw 80 signifiers selected from 707 eligible signifiers; the exact numbers may change.
- [Zenodo record 22139541](https://zenodo.org/records/22139541) is the archival mirror named in the project charter.
- The [JJJ Pro Dawg Tracker](https://jasonjones.ninja/social-science-dashboard-inator/ipseity-daily/rqs/rq-jjj-pro-dawg-tracker.html) is an independent, first-party benchmark for the planned analysis.

Sources and microdata were accessed on 2026-08-29. The official download page reported 677,121 cumulative observations through 2026-08-28, exactly matching the response file's row count excluding its header. Ipseity Daily is cumulative and updates frequently, so every result records its input-file hashes and observation-date range.

## Independent benchmark

The JJJ Pro Dawg Tracker reports that 83% of Cleveland Browns fans and 77% of non-fans have said they were `happy`. From these rounded percentages, the implied ratio is `0.83 / 0.77 = 1.078`, or about **1.08**, and the difference is **+6 percentage points**. The exact analysis below closely reproduces this first-party benchmark.

## Estimand

The primary estimand is

\[
\frac{P(\texttt{happy}=\mathrm{Yes}\mid\texttt{Cleveland Browns fan}=\mathrm{Yes})}
{P(\texttt{happy}=\mathrm{Yes}\mid\texttt{Cleveland Browns fan}=\mathrm{No})}.
\]

The **prevalence ratio** is the prevalence of `happy` among Cleveland Browns fans divided by its prevalence among explicit non-fans. A risk ratio has the same probability-ratio form, but “prevalence ratio” is the design-specific label because fandom and happiness are measured contemporaneously rather than as exposure and subsequent incidence. The prevalence difference in percentage points is a complementary effect-size measure. An odds ratio is not preferred because `happy` is common and an odds ratio would be less directly interpretable and farther from the relative-prevalence question.

The result is associational and descriptive. Fandom is not randomly assigned, temporal order is absent, and the analysis cannot identify a causal effect of fandom on happiness.

## Risk set and data structure

The unit is a `(hashed_respondent_id, obs_date)` respondent-day. A respondent-day is eligible only if all of the following hold:

1. it has a matching row in the demographics file on both key columns;
2. `Cleveland Browns fan` was presented and answered either Yes or No;
3. `happy` was presented and answered either Yes or No.

The response file uses columns `hashed_respondent_id`, `obs_date`, `signifier`, and `endorsed`; `endorsed` is binary `1`/`0`. The demographics file has one row per join key. Absence of an item is never coded as No. This restriction is essential because most signifiers are presented probabilistically and their presentation tiers can change over time.

Demographics rows containing the explicit `CONSENT_REVOKED` sentinel are excluded before the join. Identical duplicate target answers are collapsed and audited. A respondent-day with conflicting target answers is excluded rather than resolved arbitrarily; one such case occurred. Duplicate demographics join keys still stop the analysis because they would create a many-to-many join.

The 2 × 2 table is:

| | `happy` Yes | `happy` No |
|---|---:|---:|
| `Cleveland Browns fan` Yes | a | b |
| `Cleveland Browns fan` No | c | d |

The prevalence ratio is `[a / (a + b)] / [c / (c + d)]`. The analysis also reports the prevalence difference, a Katz log confidence interval for the ratio, and an unpooled Wald interval for the difference. Because 1,395 eligible respondents occur on more than one eligible date, the primary uncertainty interval is a deterministic percentile bootstrap clustered on `hashed_respondent_id`.

## RQ1 result

The primary unweighted analysis contains 8,253 eligible respondent-days from 4,695 unique respondents spanning 2025-07-08 through 2026-08-28. The exact 2 × 2 cell counts are:

| | `happy` Yes | `happy` No | Total |
|---|---:|---:|---:|
| `Cleveland Browns fan` Yes | 264 | 53 | 317 |
| `Cleveland Browns fan` No | 6,074 | 1,862 | 7,936 |

`happy` prevalence is **83.28%** among Browns fans and **76.54%** among explicit non-fans. The prevalence ratio is **1.088** (respondent-cluster bootstrap 95% CI **1.010 to 1.161**) and the prevalence difference is **+6.74 percentage points** (cluster-bootstrap 95% CI **+0.75 to +12.20 points**). In descriptive terms, observed happiness prevalence is about 8.8% higher among Browns fans. This is not a causal effect.

The analytic respondent-day interval is narrower (prevalence-ratio 95% CI 1.034 to 1.145) because it treats repeated observations as independent; the clustered interval leads in reporting.

## Reproducible implementation

The standard-library-only script is [`analysis/rq1_risk_ratio.py`](analysis/rq1_risk_ratio.py). Run it from the repository root after downloading both Expert Mode files:

```bash
python3 projects/nfl-team-fandom-identities/analysis/rq1_risk_ratio.py \
  projects/nfl-team-fandom-identities/data/ipseity-daily-responses.csv \
  projects/nfl-team-fandom-identities/data/ipseity-daily-demographics.csv \
  --output projects/nfl-team-fandom-identities/results/rq1.json
```

The JSON result includes input SHA-256 hashes, join diagnostics, the eligible date range, repeated-respondent diagnostics, exact cell counts, estimates, analytic intervals, and clustered-bootstrap intervals. The script expects the documented key names and defaults to `signifier` and `endorsed`; column-name overrides are available through command-line options.

The actual response column is now the script default, `endorsed`; it also accepts Yes/No coding for validation fixtures. Run the appendix sensitivity and render publication figures with:

```bash
python3 projects/nfl-team-fandom-identities/analysis/rq1_weighted_sensitivity.py \
  projects/nfl-team-fandom-identities/data/ipseity-daily-responses.csv \
  projects/nfl-team-fandom-identities/data/ipseity-daily-demographics.csv \
  --output projects/nfl-team-fandom-identities/results/rq1_weighted_sensitivity.json

Rscript projects/nfl-team-fandom-identities/analysis/render_figures.R \
  projects/nfl-team-fandom-identities/results/rq1.json \
  website/projects/nfl-team-fandom-identities/images
```

## Sensitivity checks

- The exact result reproduces the tracker after rounding: 83% versus 77% and a ratio near 1.08.
- Fourteen monthly ratios range from 0.963 to 1.209; 12 are above 1. Each month contains only 15 to 29 Browns-fan respondent-days, so this variation is descriptive and imprecise rather than evidence of month-specific effects.
- An appendix age-by-sex post-stratification uses the U.S. Census Bureau's 2024 ACS 1-year table B01001. It retains 8,213 complete respondent-days. Pooled-sample calibration produces a prevalence ratio of 1.082 and a +6.44-point difference. Direct standardization of both fandom groups to the same hypothetical U.S. adult age-sex distribution produces 1.079 and +6.14 points. Both are close to the primary result.
- The weighted results are sensitivity checks, not better population estimates. Age and sex may not capture selection, true fandom-specific demographics are unknown, and direct standardization intentionally replaces observed group composition with a hypothetical common distribution.
