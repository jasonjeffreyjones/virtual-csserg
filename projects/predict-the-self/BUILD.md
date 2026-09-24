# Build and validate the Predict the Self reports

The Full Report is a two-chapter Quarto HTML book: `index.qmd` introduces the
claim boundary and `report.qmd` contains the evidence, method, complete public
development scorecard, artifacts, and references. Two chapters suit this
report; Virtual CSSERG does not prescribe an exact chapter count.

Quarto renders into ignored project-local `_book/`. A standard-library
post-render command moves the source-controlled bypass link to the beginning of
each generated body, names Quarto's repeated navigation landmarks, and gives
generated table-head cells explicit column scope without runtime JavaScript or
hand-editing generated files. The guarded publisher then replaces the complete
public report tree, including copied reproducibility artifacts, so stale
generated libraries cannot survive. It also preserves the matching
`report/artifacts/` URLs as byte-identical compatibility copies and removes
Quarto-introduced line-end whitespace from generated HTML. The Executive Summary
is maintained as static HTML. `short-report.md` is the derivative PDF source.

The host has no TeX PDF engine, so the short-report renderer uses optional
build-only packages. They do not become website or production dependencies.

Regenerate the post hoc development diagnostics from the pinned benchmark
checkout before building the reports. The script verifies the recorded hashes
of both the development data and authoritative evaluator:

```bash
python3 projects/predict-the-self/analysis/analyze_dev_diagnostics.py \
  --benchmark-dir /path/to/predict-future-selves-at-9b6a766
```

Regenerate the locked matched-trajectory development baseline and its complete
comparison. These commands hash-guard the training data, development data,
evaluator, stable predictions, and pre-prediction analysis plan. They never
generate a private-test artifact:

```bash
python3 projects/predict-the-self/analysis/trajectory_retrieval.py \
  --benchmark-dir /path/to/predict-future-selves-at-9b6a766 \
  --dev-output projects/predict-the-self/results/trajectory_retrieval_dev_predictions.csv \
  --audit-output projects/predict-the-self/results/trajectory_retrieval_dev_audit.csv
python3 projects/predict-the-self/analysis/analyze_trajectory_retrieval.py \
  --benchmark-dir /path/to/predict-future-selves-at-9b6a766
```

Regenerate the post hoc volume-matched marginal-addition diagnostic. It
hash-guards the training and development data, evaluator, and frozen retrieval
predictions. It writes the complete machine-readable result and token audit:

```bash
python3 projects/predict-the-self/analysis/analyze_novelty_prior.py \
  --benchmark-dir /path/to/predict-future-selves-at-9b6a766
```

Regenerate the locked training-only leave-one-out comparison of marginal and
source-conditioned Add rankings. It hash-guards the training data, evaluator,
and pre-analysis plan and writes a machine-readable result plus case audit:

```bash
python3 projects/predict-the-self/analysis/analyze_source_conditioned_additions.py \
  --benchmark-dir /path/to/predict-future-selves-at-9b6a766
```

Regenerate the locked training-only leave-one-out comparison of the
regularized-neighborhood and marginal Add rankings. It hash-guards the training
data, evaluator, and its pre-analysis plan and writes a machine-readable result
plus case audit:

```bash
python3 projects/predict-the-self/analysis/analyze_neighborhood_additions.py \
  --benchmark-dir /path/to/predict-future-selves-at-9b6a766
```

Regenerate the locked leave-one-out cross-validation of the frozen stable-
signifier projection. It hash-guards the training data, evaluator, frozen
generator, and analysis plan; it does not read or alter development or test
artifacts:

```bash
python3 projects/predict-the-self/analysis/analyze_stable_projection_cross_validation.py \
  --benchmark-dir /path/to/predict-future-selves-at-9b6a766
```

Regenerate the locked training-only leave-one-out forecasts of revision volume
and response form. The script hash-guards the training data, evaluator,
pre-analysis plan, and inherited retrieval features; it never reads or writes a
development or test artifact:

```bash
python3 projects/predict-the-self/analysis/analyze_change_volume.py \
  --benchmark-dir /path/to/predict-future-selves-at-9b6a766
```

Regenerate the locked probabilistic extension of those volume forecasts. It
hash-guards the training data, evaluator, analysis plan, fixed change-volume
implementation, and inherited retrieval features. It compares complete
leave-one-out predictive distributions with CRPS and central-interval scores;
it never reads or writes a development or test artifact:

```bash
python3 projects/predict-the-self/analysis/analyze_change_distributions.py \
  --benchmark-dir /path/to/predict-future-selves-at-9b6a766
```

```bash
python3 -m pip install --target /tmp/predict-self-publishing-deps \
  -r projects/predict-the-self/requirements-publication.txt
XDG_CACHE_HOME=/tmp/predict-self-quarto-cache \
  quarto render projects/predict-the-self
python3 projects/predict-the-self/analysis/publish_full_report.py
PYTHONPATH=/tmp/predict-self-publishing-deps \
  python3 projects/predict-the-self/analysis/render_short_report.py
```

Validate the research code, guarded publisher, three-form publication, v1
promise groups, and whitespace:

```bash
python3 -m unittest discover -s projects/predict-the-self/tests -v
PYTHONPATH=/tmp/predict-self-publishing-deps \
  python3 projects/predict-the-self/analysis/verify_publication.py
python3 projects/vcsserg-repo-v1/verify_v1.py
git diff --check
```

The publication verifier accepts any short-report length from one through ten
nonempty pages and checks that body text occupies both columns. No exact page
count is required.
