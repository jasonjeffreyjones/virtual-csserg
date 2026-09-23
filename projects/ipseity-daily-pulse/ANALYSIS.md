# Monitoring and trend analysis

`analysis/monitor.py` is a standard-library pipeline for the public Ipseity
Daily canonical microdata. Its default live mode checks the homepage, downloads
the canonical gzip to temporary storage, validates the documented schema and
canonical key, appends one outside-in monitoring record, and replaces the
current derived outputs.

From the repository root:

```bash
python3 projects/ipseity-daily-pulse/analysis/monitor.py
python3 -m unittest discover -s projects/ipseity-daily-pulse/tests -v
```

To reproduce a check from an already retrieved file without falsely claiming a
new network observation, supply the statuses actually observed:

```bash
python3 projects/ipseity-daily-pulse/analysis/monitor.py \
  --input /path/to/ipseity.csv.gz \
  --checked-at 2026-09-16T20:47:07Z \
  --main-http-status 200 \
  --dataset-http-status 200
```

Use `--no-history` and a temporary `--output-dir` for a validation/rendering
replay. The script refuses to append a duplicate check timestamp.

## Outputs

- `data/monitoring-history.csv` is the append-only, machine-readable sequence
  of monitoring checks.
- `outputs/monitoring-history.svg` aligns homepage, dataset, and parse status
  with newest-observation lag and canonical-file observation counts across
  outside-in checks.
- `outputs/current-summary.json` records current provenance, validation, and
  trend leaders.
- `outputs/daily-observation-growth.csv` and `outputs/observation-growth.svg`
  show the dataset's cumulative growth by observation date.
- `outputs/signifier-growth.csv` and
  `outputs/annual-prevalence-growth-histogram.svg` contain the current
  signifier-level trend estimates.
- `outputs/leader-adjusted-sensitivity.csv` refits the ten most positive and
  ten most negative unadjusted slopes with observed composition and calendar
  controls; `outputs/leader-adjustment-sensitivity.svg` compares the displayed
  leaders before and after that adjustment.
- `outputs/leader-early-late-sensitivity.csv` compares endorsement prevalence
  after versus on or before the full observation window's calendar midpoint
  for the same leaders, then adjusts that contrast for observed composition
  and calendar terms; `outputs/leader-early-late-sensitivity.svg` compares the
  raw and adjusted contrasts with respondent-clustered intervals.
- `outputs/leader-within-respondent-sensitivity.csv` refits those leader tails
  first as pooled trends on the repeat-respondent subset and then with
  respondent fixed effects;
  `outputs/leader-within-respondent-sensitivity.svg` compares the displayed
  all-response pooled, repeat-sample pooled, and within-respondent slopes.
- `CURRENT-FINDINGS.md` is the reader-facing current summary and is replaced on
  refresh.

The signifier trend is an unweighted linear probability model for each
signifier (`endorsed ~ observation_date`), annualized to percentage points per
year. Eligibility requires at least 300 responses on 30 distinct dates across
180 days. The output retains ordinary model-based intervals for auditability,
but reader-facing inference uses CR1 sandwich standard errors clustered by
hashed respondent. The cluster calculation is based on respondent-level
sufficient statistics, so repeat answers to a signifier contribute one cluster
score rather than being treated as independent.

Two adjusted probabilities expose sensitivity to searching across all eligible
signifiers. Benjamini–Hochberg q-values provide a false-discovery-rate screen;
Bonferroni-adjusted p-values provide a more conservative benchmark that does
not require independent signifier tests. Neither adjustment corrects changing
sample composition, calendar structure, population nonrepresentativeness, or
model misspecification. Point-estimate leaders remain monitoring leads rather
than estimates of change among US adults.

The leader sensitivity uses a second pass over the validated gzip. For the 20
signifiers selected by their unadjusted slopes, it refits the linear
probability model with linear age, an age-missing indicator, demographics
status, sex, ethnicity, student status, employment, weekday, and
month-of-year indicators. Collinear indicators are deterministically omitted,
and uncertainty remains CR1-clustered by hashed respondent. This targeted
diagnostic tests whether the displayed extremes are fragile to observed
composition and seasonality; because the signifiers were selected as extremes,
its intervals are not a new multiple-testing or discovery procedure.

The early-versus-late sensitivity splits the full dataset window at its
calendar midpoint, uses the same cutoff for every selected signifier, and
reports the unweighted late-half prevalence minus the early-half prevalence.
This direct percentage-point contrast does not assume a straight-line path
within either period. Its uncertainty uses the same respondent-clustered CR1
sandwich correction as the primary two-term fit. A second fit replaces the
linear time term in the composition-and-calendar model with the common late-
period indicator; its coefficient estimates the adjusted period contrast.
This diagnostic addresses only the recorded age, composition, weekday, and
month terms. Both contrasts can still hide shorter reversals, remain vulnerable
to unobserved composition and nonrepresentative recruitment, and are selected
using the most extreme linear slopes. Their magnitudes are not directly
comparable with the annualized slope; only direction is compared.

The within-respondent sensitivity uses the respondent–signifier sufficient
statistics retained during validation. It first refits the pooled trend after
restricting the sample to people who answered the same signifier on multiple
dates. It then demeans response and date within each hashed respondent and
estimates a fixed-effect linear probability slope on exactly those repeat
observations. Both fits use CR1 uncertainty clustered by respondent; the
fixed-effect correction also counts the absorbed respondent effects.
Respondents observed only once do not identify the within slope. The
all-response-to-repeat-sample and repeat-pooled-to-within shifts distinguish
where the displayed estimate changes, but they are not a causal decomposition
of turnover and individual change. The targeted estimates remain vulnerable
to selective retention, time-varying confounding, functional-form error,
nonrepresentative recruitment, and selection of the pooled extremes. The
output also counts repeat respondents who changed endorsement. When none did,
the observed within slope is mechanically zero and its degenerate sandwich
interval should not be interpreted as population-level precision.

## Statistical references

Liang, K.-Y., & Zeger, S. L. (1986). Longitudinal data analysis using
generalized linear models. *Biometrika, 73*(1), 13–22.
[https://doi.org/10.1093/biomet/73.1.13](https://doi.org/10.1093/biomet/73.1.13).

Benjamini, Y., & Hochberg, Y. (1995). Controlling the false discovery rate: A
practical and powerful approach to multiple testing. *Journal of the Royal
Statistical Society: Series B (Methodological), 57*(1), 289–300.
[https://doi.org/10.1111/j.2517-6161.1995.tb02031.x](https://doi.org/10.1111/j.2517-6161.1995.tb02031.x).
