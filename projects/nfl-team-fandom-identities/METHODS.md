# RQ1 methods and data notes

Updated September 11, 2026. The current report uses the checksum-verified
Zenodo archive through August 27, 2026. See `BUILD.md` for reproduction.

## Measurement and estimand

Following the ipseological approach of Jones (2023), this analysis compares
self-description through identity signifiers. In Ipseity Daily, respondents
endorse supplied signifiers rather than spontaneously writing a biography.
Thus `happy` endorsement is the measured outcome, not a clinical measure or
an independently assessed psychological state.

The primary estimand is the prevalence of `happy` among eligible
respondent-days explicitly endorsing `Cleveland Browns fan`, divided by its
prevalence among eligible respondent-days explicitly rejecting that signifier.
The prevalence difference in percentage points complements the ratio.

Per PI guidance in `PI.md`, use **prevalence ratio** in publication. A risk
ratio has the same mathematical form, but prevalence ratio better describes
contemporaneous states rather than incident outcomes. The primary estimate
is unweighted. The PI also confirmed the tracker uses explicit No with
same-day happy observation, and requested weighting in an appendix.

## Eligibility and handling

The unit is `(hashed_respondent_id, obs_date)`. Response and demographics
files must be inner-joined on both fields. Eligibility requires explicit
binary answers to both target signifiers. An absent item is never No;
probabilistic signifier presentation and its changing tiers matter.

The response schema is `hashed_respondent_id`, `obs_date`, `signifier`,
`endorsed` (1/0). The estimator also accepts Yes/No for fixtures. Demographics
rows with `CONSENT_REVOKED` are excluded before the join. Duplicate demographics
keys stop analysis. Identical target answers are collapsed; conflicting target
respondent-days are excluded. The archive contains 113 consent-revoked
rows, 1,945 unmatched response rows, three identical target duplicates, and
one conflicting target respondent-day.

## Current result

The verified archive contains 675,480 response rows and 8,776 demographics
rows. There are 8,235 eligible days from 4,686 respondents over July 8,
2025–August 27, 2026. Of these respondents, 1,392 recur (maximum 39 days).

| Browns fan | happy Yes | happy No | Total |
|---|---:|---:|---:|
| Yes | 263 | 53 | 316 |
| Explicit No | 6,062 | 1,857 | 7,919 |

Prevalence is 83.23% versus 76.55%; PR = 1.087234 and difference = +6.6778
percentage points. Primary 95% respondent-cluster percentile bootstrap
intervals are 1.007137–1.160385 and +0.5564–+12.1703 points. The bootstrap
resamples whole respondents 2,000 times, retaining their days; seed 20260828.
All replicates were finite. The Katz interval treating days as independent
is 1.033202–1.144092 and remains secondary.

Clustering does not change respondent-day weighting, address date-level
common shocks, account for presentation probabilities, or correct sample
selection. The estimate is descriptive, not causal or necessarily representative.

## Sensitivity analyses

Twelve of fourteen monthly PRs exceed 1 (range 0.963–1.209); each month has
15–29 fan days. These are sparse descriptive checks, not game-effect tests.

The appendix uses eight adult age-by-sex cells from 2024 ACS B01001. All
national target counts were independently verified against the summary-file
source row (`results/acs_target_check_20260911.json`). Forty eligible days
lack usable numeric-adult-age/binary-sex coding. Among 8,195 complete days,
unweighted PR is 1.085463 (+6.5444 points), pooled calibration PR is 1.080135
(+6.2678 points), and direct standardization PR is 1.078307 (+6.1224 points).

Pooled weights equal target cell share divided by observed complete-day cell
share. Direct standardization applies the same target shares to both groups'
cell-specific prevalence. Fan cells have 9–90 days; maximum pooled weight
is 3.304. Weighted intervals remain uncomputed. The true fandom demographic
distribution is unknown; these are sensitivity analyses, not improved population
estimates. Complete-case comparison separates exclusions from reweighting.

## Provenance discrepancy

On September 11, the primary-host URLs returned 10,570 response rows and 151
demographics rows, with eligible dates July 8–14, 2025. The download page
advertised 677,121 cumulative observations through August 28, 2026. The cause
is unknown. The retrieved subset is preserved separately in
`results/rq1_retrieved_20260911.json` (142 eligible days; PR 1.191667;
cluster interval 0.937729–1.413090). It does not estimate the same time window.

Zenodo record 22139541 supplied a much larger archive; both files passed their
published MD5 checksums. SHA-256 values and download URLs are recorded in
`results/acquisition_20260911.json`. Current results use the dated
`rq1_zenodo_20260911.json` and `rq1_weighted_zenodo_20260911.json` files.

Historical `results/rq1.json` and `results/rq1_weighted_sensitivity.json`
contain the interrupted iteration's August 28 estimates: 8,253 days, PR 1.088,
and 83.28% versus 76.54%. Their exact inputs were unavailable this iteration.
They remain unchanged but are not the current report's source. Agreement
with those estimates is not a same-input reproduction.

## Sources

Jones, J. J. (2023). *Ipseology: A new science of the self*. Jason Jeffrey Jones Productions. https://jasonjones.ninja/ipseology-a-new-science-of-the-self-book/

Jones, J. J. (2026a). *Building the ipseome: Large, free, open, human identity data*. arXiv. https://doi.org/10.48550/arXiv.2607.02488

Jones, J. J. (2026b). *Ipseity Daily data* [Data set]. Zenodo. https://doi.org/10.5281/zenodo.22139541

Jones, J. J. (n.d.). *Download human identity survey data*. Retrieved September 11, 2026, from https://jasonjones.ninja/social-science-dashboard-inator/ipseity-daily/download.html

U.S. Census Bureau. (2025). *2024 ACS 1-year estimates: Table B01001, sex by age* [Data set]. https://data.census.gov/table/ACSDT1Y2024.B01001
