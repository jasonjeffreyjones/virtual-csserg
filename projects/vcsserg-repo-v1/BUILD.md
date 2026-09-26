# Build and validate the VCSSERG v1 reports

The Full Report source is `index.qmd`, currently configured as a one-chapter
Quarto book by `_quarto.yml`; that chapter count is an editorial choice, not a
requirement. Quarto renders into the ignored project-local `_book/`, then
`analysis/publish_full_report.py` safely replaces the complete generated tree at
`website/projects/vcsserg-repo-v1/report/`. Keeping Quarto's output inside its
project lets it clean stale libraries without warnings. A standard-library
post-render command moves the source-controlled bypass link to the beginning of
each generated body and names Quarto's repeated navigation landmarks before
publication. It also gives every generated table-head cell an explicit column
scope. Table captions are maintained in report sources, while the whole-site
verifier accepts a nonempty caption or a valid explicit ARIA name. Correct
source order, landmark names, table names, and header relationships therefore
do not depend on runtime JavaScript or hand-editing generated files. The
Executive Summary is maintained as static HTML, and `short-report.md` is the
derivative PDF source.

Quarto uses a writable temporary cache. The host has no TeX PDF engine, so the
short-report renderer uses the optional build-only packages in
`requirements-publication.txt`. These packages do not become website or
production dependencies. The current short report occupies two pages; the
requirement is two columns and no more than ten pages, not an exact page count.

```bash
python3 -m pip install --target /tmp/vcsserg-v1-publishing-deps \
  -r projects/vcsserg-repo-v1/requirements-publication.txt
XDG_CACHE_HOME=/tmp/vcsserg-v1-quarto-cache \
  quarto render projects/vcsserg-repo-v1
python3 projects/vcsserg-repo-v1/analysis/publish_full_report.py
PYTHONPATH=/tmp/vcsserg-v1-publishing-deps \
  python3 projects/vcsserg-repo-v1/analysis/render_short_report.py
```

Validate the scaffold workflow, three-form publication, all Version 1 promise
groups, and repository whitespace:

```bash
python3 python/scholar_roster.py
python3 -m unittest discover -s projects/vcsserg-repo-v1/tests -v
python3 projects/vcsserg-repo-v1/tests/runner_integration.py -v
PYTHONPATH=/tmp/vcsserg-v1-publishing-deps \
  python3 projects/vcsserg-repo-v1/analysis/verify_publication.py
python3 projects/vcsserg-repo-v1/verify_v1.py
git diff --check
```

Default discovery covers routine unit tests. Run `runner_integration.py`
explicitly when `run-scholar.sh`, its publication boundary, or the integration
fixtures change. It is intentionally excluded from a live Scholar iteration
because that parent process already holds the repository-wide iteration lock.

The publication verifier checks reciprocal local links and fragments, exactly
one Executive Summary figure, the required Full Report phrase, PDF link
annotations, both PDF body columns, nonempty pages, and the ten-page ceiling.
The Version 1 verifier also validates the open manual-accessibility worksheet:
it derives the required sample from current Published summaries and Full Report
pages and refuses a `Closed` record with missing environment evidence or any
non-passing result. The whole-site check also requires every data table to have
an accessible name, every table header cell to declare a valid row or column
scope, and every exposed interactive or
keyboard-focusable element to have an accessible name. Coverage includes links,
buttons, native form and disclosure controls, interactive ARIA roles, media
controls, and custom nonnegative-`tabindex` targets. Label and control
references must resolve, expanded states must be boolean, and controls hidden
from assistive technology must be removed from the tab order. These source
checks do not perform the rendered review.

After the normal commit, push, and deployment, compare every expected public
file byte with its production URL:

```bash
python3 projects/vcsserg-repo-v1/analysis/check_production_parity.py
```

This network check does not use `.env` and cannot detect extra stale remote
files. The normal deployment therefore follows its deleting transfer with an
authenticated checksum/inventory dry run and exits nonzero on any residual
difference. Do not run the deployment manually during a Scholar iteration;
observe its result in the host-managed post-iteration workflow.
