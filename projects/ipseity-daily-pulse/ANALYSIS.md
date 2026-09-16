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
- `outputs/current-summary.json` records current provenance, validation, and
  trend leaders.
- `outputs/daily-observation-growth.csv` and `outputs/observation-growth.svg`
  show the dataset's cumulative growth by observation date.
- `outputs/signifier-growth.csv` and
  `outputs/annual-prevalence-growth-histogram.svg` contain the current
  signifier-level trend estimates.
- `CURRENT-FINDINGS.md` is the reader-facing current summary and is replaced on
  refresh.

The signifier trend is an unweighted linear probability model for each
signifier (`endorsed ~ observation_date`), annualized to percentage points per
year. Eligibility requires at least 300 responses on 30 distinct dates across
180 days. Ordinary model-based 95% intervals are included to expose sampling
uncertainty, but they do not address repeated respondents, changing sample
composition, population weights, or multiple-comparison selection.
