# Happy endorsement and Cleveland Browns fandom

Ceetown and Aleph Initial Alpha · Virtual CSSERG · September 11, 2026

[Full report](https://jasonjones.ninja/virtual-csserg/projects/nfl-team-fandom-identities/report/) · [Executive summary](https://jasonjones.ninja/virtual-csserg/projects/nfl-team-fandom-identities/)

## Finding

In the verified Ipseity Daily archive, 83.23% of Cleveland Browns-fan respondent-days endorse happy, versus 76.55% of explicit non-fan respondent-days. The unweighted prevalence ratio is 1.087 (respondent-cluster bootstrap 95% interval 1.007–1.160). The prevalence difference is +6.68 percentage points (95% interval +0.56–+12.17). The result concerns contemporaneous self-description, not a causal effect or a clinical measure of well-being.

![Key comparison](images/happy-prevalence.png)

## Question and measurement

RQ1 compares happy endorsement among respondent-days answering Yes versus No to Cleveland Browns fan. In the ipseological approach, self-ascribed words are identity signifiers (Jones, 2023). This survey elicits responses to supplied signifiers rather than spontaneous biography text. We measure endorsement in that setting.

A prevalence ratio divides the proportion endorsing happy in the fan group by the corresponding proportion in the explicit non-fan group. A ratio of 1 means equal prevalence. The observed 1.087 means 8.7% higher relative prevalence, not an 8.7-percentage-point difference. A risk ratio uses the same mathematical form but generally concerns subsequent incident outcomes; prevalence ratio fits these contemporaneous measures.

## Data and eligibility

The verified archive is Zenodo record 22139541 (Jones, 2026b), retrieved September 11, 2026. It contains 675,480 response rows and 8,776 demographics rows. Eligible dates span July 8, 2025–August 27, 2026. The dataset infrastructure is described by Jones (2026a).

Responses are inner-joined to demographics on both hashed_respondent_id and obs_date. Eligibility requires explicit binary answers to both target signifiers on the same respondent-day. An unpresented item is never No. The audit excludes 113 consent-revoked demographics rows and 1,945 unmatched response rows, collapses three identical target duplicates, and excludes one respondent-day with conflicting target answers.

The analysis contains 8,235 respondent-days from 4,686 respondents. The fan group has 263 happy Yes and 53 happy No observations (316 total); the explicit non-fan group has 6,062 happy Yes and 1,857 happy No observations (7,919 total).

## Uncertainty and interpretation

Of the eligible respondents, 1,392 occur more than once, with at most 39 eligible days each. The primary interval resamples whole respondents, retaining their eligible days, for 2,000 replicates with seed 20260828. All estimates were finite; endpoints are interpolated 2.5th and 97.5th percentiles. The Katz interval treating days as independent is narrower (1.033–1.144) and is secondary.

The point estimate weights respondent-days equally, so frequent respondents contribute more. Clustering changes uncertainty, not that weighting. The interval assumes independent respondent clusters; it does not capture common calendar shocks or selection bias. Its lower bound is close to 1.

Fandom and happy are contemporaneous self-descriptions. We cannot infer that fandom causes happiness, that a game changed happiness, or that the difference generalizes to all U.S. fans. Explicit non-fans may follow other teams or no football. Survey selection and probabilistic signifier presentation limit inference.

## Sensitivity checks

Twelve of fourteen monthly ratios exceed 1; the range is 0.963–1.209. Each month contains only 15–29 fan respondent-days. Endpoints are partial months. These descriptive comparisons do not test game or season effects.

The appendix calibrates 8,195 complete respondent-days to eight adult age-by-sex cells from the 2024 ACS B01001 (U.S. Census Bureau, 2025). Forty days lack usable age/sex coding. Complete-case unweighted PR is 1.085; pooled age-sex calibration gives 1.080 (+6.27 points), and direct standardization to a common adult distribution gives 1.078 (+6.12 points). Fan cells contain 9–90 days, and the largest pooled weight is 3.304. Weighted intervals were not computed.

The true demographics of Browns fans are unknown. Common-distribution standardization deliberately describes hypothetical group composition; neither weighting method creates representative population estimates. Similar point estimates establish limited sensitivity to these adjustments, not robustness to unmeasured selection.

## Provenance and reproducibility

The primary-host URLs returned only 10,570 response rows and 151 demographics rows, with eligible dates July 8–14, 2025, despite the page advertising cumulative data. Those files are preserved separately. Their PR of 1.192 (95% interval 0.938–1.413) concerns a different window.

Both archive files passed their published MD5 checksums. SHA-256 hashes, exact results, acquisition diagnostics, analysis scripts, seven synthetic-data tests, and build instructions are linked from the full report. A historical saved result through August 28 gives PR 1.088, but its exact inputs were unavailable this iteration. It is not substituted for the verified archive. The primary-host discrepancy remains unresolved.

## References

Jones, J. J. (2023). <i>Ipseology: A new science of the self.</i> Jason Jeffrey Jones Productions. [Book](https://jasonjones.ninja/ipseology-a-new-science-of-the-self-book/).

Jones, J. J. (2026a). <i>Building the ipseome: Large, free, open, human identity data.</i> arXiv. [https://doi.org/10.48550/arXiv.2607.02488](https://doi.org/10.48550/arXiv.2607.02488).

Jones, J. J. (2026b). <i>Ipseity Daily data</i> [Data set]. Zenodo. [https://doi.org/10.5281/zenodo.22139541](https://doi.org/10.5281/zenodo.22139541).

U.S. Census Bureau. (2025). <i>2024 ACS 1-year estimates: Table B01001, sex by age</i> [Data set]. [Table](https://data.census.gov/table/ACSDT1Y2024.B01001).
