# Publication and reproduction

The current publication source is `index.qmd`, a single-chapter Quarto book
configured by `_quarto.yml`. `report.qmd` and `report.rmarkdown` are historical
August 29 drafts from the interrupted iteration, not current render targets.
Historical `results/rq1.json` and `results/rq1_weighted_sensitivity.json` are
retained unchanged. The current report uses the dated Zenodo results.

## Reproduce the current archive analysis

From the repository root, obtain the two fixed-archive microdata files:

```bash
curl -fL -o projects/nfl-team-fandom-identities/data/zenodo-responses.csv \
  https://zenodo.org/api/records/22139541/files/ipseity-daily-responses.csv/content
curl -fL -o projects/nfl-team-fandom-identities/data/zenodo-demographics.csv \
  https://zenodo.org/api/records/22139541/files/ipseity-daily-demographics.csv/content
python3 projects/nfl-team-fandom-identities/analysis/rq1_risk_ratio.py \
  projects/nfl-team-fandom-identities/data/zenodo-responses.csv \
  projects/nfl-team-fandom-identities/data/zenodo-demographics.csv \
  --output projects/nfl-team-fandom-identities/results/rq1_zenodo_20260911.json
python3 projects/nfl-team-fandom-identities/analysis/rq1_weighted_sensitivity.py \
  projects/nfl-team-fandom-identities/data/zenodo-responses.csv \
  projects/nfl-team-fandom-identities/data/zenodo-demographics.csv \
  --output projects/nfl-team-fandom-identities/results/rq1_weighted_zenodo_20260911.json
```

Confirm input SHA-256 values against `results/acquisition_20260911.json` before
replacing any published outputs. This iteration additionally checked archive
MD5s against Zenodo metadata. Downloads from the primary host are recorded
separately in `results/rq1_retrieved_20260911.json`; they are not interchangeable.

## Render

Use installed Quarto, R, and the R packages jsonlite, knitr, and rmarkdown.
The short PDF uses optional Python packages in `requirements-publication.txt`.
They are build-only packages, not website dependencies. ReportLab was chosen
because this host has no TeX PDF engine; no replacement runtime was installed.
The session installed these packages in `/tmp/nfl-publishing-deps`; an ordinary
existing project environment with these packages also works.

```bash
Rscript projects/nfl-team-fandom-identities/analysis/render_figures.R \
  projects/nfl-team-fandom-identities/results/rq1_zenodo_20260911.json \
  website/projects/nfl-team-fandom-identities/images
XDG_CACHE_HOME=/tmp/nfl-quarto-cache quarto render projects/nfl-team-fandom-identities
PYTHONPATH=/tmp/nfl-publishing-deps python3 \
  projects/nfl-team-fandom-identities/analysis/render_short_report.py
python3 projects/nfl-team-fandom-identities/analysis/copy_public_artifacts.py
```

The cache override only places Quarto's writable cache in a permitted location.
It does not replace or modify Quarto. A standard-library post-render command
places the source-controlled bypass link at the beginning of the generated body
and names Quarto's repeated navigation landmarks without runtime JavaScript or
hand-editing generated files. It also gives generated table-head cells explicit
column scope. The PDF renderer reads `short-report.md`, uses two columns, and
rejects output above ten pages. The executive summary is maintained as static
HTML in `website/projects/nfl-team-fandom-identities/index.html`.
Revise derivatives after revising the full report, then verify numerical agreement.

```bash
python3 -m unittest discover -s projects/nfl-team-fandom-identities/tests -v
PYTHONPATH=/tmp/nfl-publishing-deps python3 \
  projects/nfl-team-fandom-identities/analysis/verify_publication.py
git diff --check
```

APA CSL is vendored from the Citation Style Language styles repository
(`https://github.com/citation-style-language/styles/blob/master/apa.csl`),
retrieved September 11, 2026; its license is declared in the file.
