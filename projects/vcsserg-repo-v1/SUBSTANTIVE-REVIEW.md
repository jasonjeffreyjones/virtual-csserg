# VCSSERG Version 1.0 substantive report review

Reviewed by Bee Boring Vanilla on September 18, 2026 against baseline commit
`89300ad85ba12163ac8a7401005fccc48e35102c`.

## Decision

The current VCSSERG v1 report is substantively adequate for its stated purpose:
it accurately describes the repository's infrastructure and governance,
connects its material current-state claims to observable evidence, and keeps
the remaining rendered-accessibility uncertainty explicit. No unsupported
material claim was found.

This closes the Project's **substantive report review** gate. It does not close
the separate desktop/phone keyboard and assistive-technology gate, certify the
empirical findings of other Projects, or substitute for independent external
review. The reviewer is the Scholar who authored the current report, so this is
a documented internal review rather than independent peer review.

## Scope and method

The unit of review was the mutually linked v1 Executive Summary, Full Report,
and short report, together with the source and governance records needed to
evaluate their claims. The review used four tests:

1. Map every explicit charter deliverable to a current artifact and check.
2. Trace each family of material report claims to current code, tests, public
   artifacts, or timestamped historical evidence.
3. Look for overstatement at the evidence boundary: especially confusing
   structural checks with research validity, mocked deployment with observed
   deployment, or static accessibility with rendered usability.
4. Re-run the current deterministic evidence and compare the incoming public
   tree with production before changing it.

The review read the charter, current state, audit and recommendations; all
three report forms; the creation, dialog, and archiving procedures; the runner,
deployment component, roster and registry; the v1 verifier, publication
verifier, and unit/integration test sources; the applicable PI guidance and
iteration records; and the current public catalogs.

## Charter coverage

| Charter requirement | Current evidence | Review result |
|---|---|---|
| Everything promised in repository documentation works as documented | Seven deliberately bounded verifier groups pass; historical records separately establish a successful normal workflow and exact deployment; this report does not call that a completion oracle | Supported, with rendered accessibility still open |
| `_template` follows current documentation | Memory-layout checks cover `_template`; the Project-creation fixture copies the complete template and initializes a fresh immutable-dialog tree | Supported |
| All three report forms exist | The v1 Executive Summary, Quarto Full Report, and two-column short PDF are mutually linked and pass the Project publication verifier | Supported |
| Initial Scholars have pages with the supplied biographies | The roster validator and public-catalog check compare every profile with canonical PI-authored biography text | Supported |
| Explain how to create Projects | The central creation guide and tested no-overwrite `create_project.py` command cover private setup, activation, publication, pause/resume, and archiving | Supported |
| Explain how to create Scholars | The guide and tested rollback-on-error `create_scholar.py` command cover PI-authored identity, profile/catalog creation, validation, and per-invocation Project pairing | Supported |

## Material claim review

| Claim family in the reports | Evidence examined | Assessment and boundary |
|---|---|---|
| Public catalogs, biographies, and metadata-derived Project order | `scholars.json`, canonical biographies, all `STATE.md` front matter, generated profiles/catalogs, roster/registry checks, and verifier catalog checks | Supported. The verifier proves that public values mirror state metadata; it cannot decide whether a human assigned the correct substantive-update time. |
| Seven automated promise groups pass | A fresh `verify_v1.py` run and all 26 routine v1 unit tests | Supported at the baseline commit. The groups are regression categories, not seven independent estimates or a research-quality score. |
| Every Published Project has three linked report forms | Generic three-report checks plus each Project's stronger publication verifier as recorded in the current state and recent iteration evidence | Supported for the three Projects whose state says `publication: Published`. This does not validate their empirical conclusions. |
| Project and Scholar growth is guarded | Creation implementations, fixture tests, roster/registry validators, and the documented authority boundary | Supported for validation, no-overwrite behavior, atomic Project installation, and Scholar rollback. PI judgment remains required for charters, biographies, activation, and publication. |
| Runner failure boundaries and ordering | `run-scholar.sh`, its separately invoked integration suite, the Version 1 runner inspection, and the September 15/16 workflow records | Supported. Controlled failure paths use harmless fakes; successful live runs supply the external counterpart. The integration suite is intentionally not nested inside a lock-holding live run. |
| Deployment is fail-closed and an earlier release exactly matched production | Deployment code and mocked failure tests; September 15 completion evidence; September 16 110-file probe; September 18 pre-change probe | Supported. The September 18 probe found all 114 incoming files byte-identical. Public HTTP still cannot enumerate remote-only files, so authenticated post-deployment inventory remains essential. |
| Immutable dialog and report-history procedures are operative | Current Project/template layouts, legacy hashes, migration tests, yearly indexes, archive ledger, and `git cat-file` validation | Supported. The ledger preserves material outgoing report sets; ordinary Git history covers maintenance-only changes. |
| Static accessibility requirements are enforced | Whole-site structural check and focused negative fixtures for bypass links and missing image alternatives | Supported only at the stated static boundary. Focus order, responsive rendering, and assistive-technology output remain unobserved on this host. |

## Findings and corrections

The review found no unsupported material report claim, but it found one
recordkeeping defect and two places where the evidence boundary needed fresher
documentation:

- The outgoing v1 state used `updated: 2026-09-17T08:11:02Z`, while its newest
  substantive iteration records `finished: 2026-09-17T08:13:48Z`. The public
  Projects catalog correctly mirrored the state, but the state did not satisfy
  the documented end-time definition. This iteration replaces both with its own
  exact finish time. The general verifier can enforce state-to-catalog
  agreement, but it cannot infer whether an iteration is substantive; that
  classification remains a human recordkeeping decision.
- The report's 110-file production result remains valid historical evidence for
  the September 15 release. A new pre-change probe found the current 114-file
  checkout byte-identical to production. The revised report distinguishes this
  incoming-release observation from the deployment that will follow the present
  material update.
- “Substantive review” now means review of this infrastructure report's claims
  and evidence. It does not imply a new review of Predict the Self or NFL Team
  Fandom Identities' empirical methods or findings.

## Reproduction evidence

The baseline review ran:

```bash
python3 projects/vcsserg-repo-v1/verify_v1.py
python3 -m unittest discover -s projects/vcsserg-repo-v1/tests -v
python3 python/scholar_roster.py
python3 python/project_registry.py
python3 projects/vcsserg-repo-v1/analysis/check_production_parity.py
```

Results were 7 of 7 verifier groups, 26 of 26 routine unit tests, a valid roster
of four Scholars, four valid Projects of which three are Published, and 114 of
114 expected public files byte-identical. The network probe is read-only and
credential-free; it cannot detect an extra remote-only file.

The report revision produced from this review must still pass the Full Report
render, Project publication verifier, Version 1 verifier, routine tests, Python
compilation, and repository whitespace checks. The host-managed workflow—not
this review—will commit, push, deploy, and run authenticated inventory for the
new release.
