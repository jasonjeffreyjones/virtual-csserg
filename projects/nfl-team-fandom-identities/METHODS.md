# RQ1 Methods and Data Notes

## Sources consulted

- [Ipseity Daily](https://jasonjones.ninja/social-science-dashboard-inator/ipseity-daily/) describes the recurring survey and the identity-signifier measurement.
- [Expert Mode download instructions](https://jasonjones.ninja/social-science-dashboard-inator/ipseity-daily/download.html) identify the responses and demographics microdata and require an inner join on `hashed_respondent_id` and `obs_date`.
- [Building the Ipseome: Large, Free, Open, Human Identity Data](https://arxiv.org/abs/2607.02488) describes Ipseity Daily as a repeated cross-sectional survey of American adults. At the paper's snapshot, each daily respondent saw 80 signifiers selected from 707 eligible signifiers; the exact numbers may change.
- [Zenodo record 22139541](https://zenodo.org/records/22139541) is the archival mirror named in the project charter.
- The [JJJ Pro Dawg Tracker](https://jasonjones.ninja/social-science-dashboard-inator/ipseity-daily/rqs/rq-jjj-pro-dawg-tracker.html) is an independent, first-party benchmark for the planned analysis.

Sources were accessed on 2026-08-28. The official download page reported 675,480 cumulative observations through 2026-08-27. Ipseity Daily is cumulative and updates frequently, so every result must record its input-file hashes and observation-date range.

## Preliminary benchmark, not the final RQ1 estimate

The JJJ Pro Dawg Tracker currently reports that 83% of Cleveland Browns fans and 77% of non-fans have said they were `happy`. From these rounded percentages, the implied ratio is `0.83 / 0.77 = 1.078`, or about **1.08**, and the difference is **+6 percentage points**. If both percentages were rounded to the nearest whole percentage point, the compatible ratio is approximately 1.06 to 1.09 even before sampling uncertainty. Exact microdata counts are therefore necessary for the final estimate and confidence interval.

## Estimand

The primary estimand is

\[
\frac{P(\texttt{happy}=\mathrm{Yes}\mid\texttt{Cleveland Browns fan}=\mathrm{Yes})}
{P(\texttt{happy}=\mathrm{Yes}\mid\texttt{Cleveland Browns fan}=\mathrm{No})}.
\]

This is correctly calculated as a risk ratio for a binary outcome. Because the data are contemporaneous and cross-sectional rather than a follow-up study of incident outcomes, **prevalence ratio** is the more precise label. Project reporting will call it a **risk (prevalence) ratio** so the PI's requested terminology and the design are both clear. The prevalence difference in percentage points is a secondary effect-size measure. An odds ratio is not preferred because `happy` is common and an odds ratio would be less directly interpretable and farther from the relative-prevalence question.

The result is associational and descriptive. Fandom is not randomly assigned, temporal order is absent, and the analysis cannot identify a causal effect of fandom on happiness.

## Risk set and data structure

The unit is a `(hashed_respondent_id, obs_date)` respondent-day. A respondent-day is eligible only if all of the following hold:

1. it has a matching row in the demographics file on both key columns;
2. `Cleveland Browns fan` was presented and answered either Yes or No;
3. `happy` was presented and answered either Yes or No.

Absence of an item is never coded as No. This restriction is essential because most signifiers are presented probabilistically and their presentation tiers can change over time. Identical duplicate responses are collapsed and reported; conflicting duplicates or duplicate demographics join keys stop the analysis.

The 2 × 2 table is:

| | `happy` Yes | `happy` No |
|---|---:|---:|
| `Cleveland Browns fan` Yes | a | b |
| `Cleveland Browns fan` No | c | d |

The prevalence ratio is `[a / (a + b)] / [c / (c + d)]`. The analysis also reports the prevalence difference, a Katz log confidence interval for the ratio, and an unpooled Wald interval for the difference. Because a hashed respondent could occur on more than one eligible date, the preferred uncertainty check is a deterministic percentile bootstrap clustered on `hashed_respondent_id`.

## Reproducible implementation

The standard-library-only script is [`analysis/rq1_risk_ratio.py`](analysis/rq1_risk_ratio.py). Run it from the repository root after downloading both Expert Mode files:

```bash
python3 projects/nfl-team-fandom-identities/analysis/rq1_risk_ratio.py \
  projects/nfl-team-fandom-identities/data/ipseity-daily-responses.csv \
  projects/nfl-team-fandom-identities/data/ipseity-daily-demographics.csv \
  --output projects/nfl-team-fandom-identities/results/rq1.json
```

The JSON result includes input SHA-256 hashes, join diagnostics, the eligible date range, repeated-respondent diagnostics, exact cell counts, estimates, analytic intervals, and clustered-bootstrap intervals. The script expects the documented key names and defaults to `signifier` and `response`; column-name overrides are available through command-line options.

## Planned sensitivity checks

- Compare the exact result with the JJJ Pro Dawg Tracker benchmark.
- Inspect co-presentation and eligible sample size by date to detect changes associated with sampling tiers.
- Report seasonal or date-stratified estimates if the pooled result hides meaningful time variation.
- Examine whether demographic weighting is available or appropriate before describing the estimate as population-representative.
