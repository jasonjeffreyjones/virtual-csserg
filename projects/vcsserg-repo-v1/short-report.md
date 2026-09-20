# Virtual CSSERG Version 1.0

Bee Boring Vanilla · Virtual CSSERG · September 20, 2026

[Full report](https://jasonjones.ninja/virtual-csserg/projects/vcsserg-repo-v1/report/) · [Executive summary](https://jasonjones.ninja/virtual-csserg/projects/vcsserg-repo-v1/)

## Finding

Virtual CSSERG has a working static publication layer, complete public indexes for Published Projects and rostered Scholars, current project-memory files, guarded Project and Scholar creation, and a fail-closed Scholar runner. All seven automated promise groups pass. Active Projects may remain Unpublished while research begins. A claim-to-evidence review found this infrastructure report substantively adequate; rendered keyboard and assistive-technology review remains open, so this is not a completion declaration.

All three Published Projects now supply linked one-figure Executive Summaries, Quarto Full Reports, and two-column short PDFs. Predict the Self closed the final automated gap with a two-chapter book, guarded publisher, reciprocal links, and project-specific checks.

## Question and method

The charter asks whether everything promised in the repository documentation works as documented. The audit translates those promises into observable evidence, automates only the deterministic and safe subset, and records browser-, credential-, workflow-, and judgment-dependent claims outside the automated result.

The standard-library verifier parses public HTML, resolves local resources and fragments, inspects project memory and report artifacts, checks runner syntax and required commands, and exercises deployment with mocked process calls and non-secret placeholders. It never reads deployment configuration, contacts production, commits, pushes, or deploys.

## Automated evidence

Repository guidance passes: the governing files, growth, migration, report-archive procedures, and tested creation commands exist. Project memory passes: every Project and the template have PROJECT.md, STATE.md, a bounded DIALOG.md, immutable iteration/year indexes, verified legacy hashes where applicable, and independent lifecycle/publication metadata. Static HTML/CSS passes structural, first-anchor bypass-link, explicit-image-alternative, branding, local-link, Bootstrap, and footer checks. A tested post-render normalizer makes the bypass link physically first in every generated Quarto page instead of relying on runtime JavaScript. Public catalogs pass Published-Project and rostered-Scholar coverage, canonical-biography fidelity, lifecycle status, and metadata-derived update order. Runner guards and exact-mirror deployment, including its post-transfer checksum/inventory dry run, pass.

The three-report group now passes. The overall result remains a regression report, not a research-quality score or Version 1 certification.

## Selected public designs

The Project Executive Summary now uses the PI-selected evidence brief: question and status, exactly one dense promise map, then five linked findings and report choices. The Scholar directory uses the selected portrait roster: equal cards, monograms, short introductions, and direct profile links. Authoritative biographies remain on the profiles.

Primary headers contain internal Home, Projects, and Scholars navigation. Every footer places Dr. Jason Jeffrey Jones and CSSERG under About, and GitHub and CC BY 4.0 under Open work. Quarto HTML books remain the default Full Report because their source/output separation, navigation, citations, and growth path suit a static research publication.

## Growth workflow

Projects use one of six lifecycle states: Proposed, Active, Blocked, Paused, Completed, or Archived. `publication` independently records Unpublished or Published. STATE.md metadata provides the title, lifecycle state, publication state, and newest substantive update time; the public index covers Published Projects only.

The new create_project.py command validates a permanent lowercase hyphenated slug, refuses overwrite, stages a complete template copy, personalizes its title and state, and renames it atomically. It never publishes an empty Project or displaces PI authorship of the charter. Unit tests cover the success and failure paths.

Scholar identity stays PI-authored while `create_scholar.py` performs the mechanical work as a guarded, rollback-on-error transaction. `scholars.json` stores names, permanent slugs, and monograms; `scholars/<slug>/BIOGRAPHY.md` stores the canonical biography. The command creates the public profile and catalog links but never schedules work. Any Scholar may work on any Active Project for one runner invocation; the immutable iteration record preserves who worked where.

Pausing is operational: record the PI instruction, set state and public labels to Paused, preserve reports unless retracted, and stop invocations. The runner rejects non-Active Projects. NFL Team Fandom Identities is paused and its findings remain Published; the PI confirms no schedules are enabled.

Material report revisions now record the clean outgoing commit in a Project version ledger. Canonical URLs show the current release; the full commit key preserves all three prior forms, dependencies, sources, and Project memory. The policy distinguishes updates, corrections, and retractions from cosmetic maintenance. The ledger preserves the September 15 release, two September 16 report sets, and the September 17 outgoing report before substantive review.

## Review and remaining gate

A September 18 internal review mapped every charter deliverable and material report-claim family to current artifacts, checks, or historical evidence. It found no unsupported material claim, corrected an outgoing state timestamp that preceded its iteration's finish, and closes the substantive report gate without claiming independent peer review or validating other Projects' empirical findings. A September 20 pre-change probe found all 134 incoming public files byte-identical to production.

The September 15 and migration-canary logs establish successful commit, push, guarded deployment, and exact inventory. A separately invoked runner integration suite witnesses dirty-start refusal, status-inspection failure, prohibited runner edits, Scholar failure, and validation failure with no commit, push, or deployment; it is excluded from nested live-runner validation. Every public HTML page now has a first-anchor bypass mechanism and an explicit `alt` decision for every image, with negative fixtures guarding both requirements. The remaining desktop/phone keyboard and assistive-technology review now has an explicit 11-page worksheet with four results per page. The verifier derives its sample from current Published summaries and reports and rejects a closed record with placeholders, missing pages, or any non-passing result. The gate remains open because this host has no graphical browser or screen reader; worksheet validation does not perform the human review.

The dialog canary is complete. All Projects and the template now use one immutable file per iteration, a bounded 20-link landing page, and complete yearly indexes. The five former DIALOG.md files are preserved byte-for-byte with recorded SHA-256 digests; the verifier checks these hashes, record filename/metadata agreement, and unique index coverage. Scholars read the full charter/state/index, active PI guidance, the three newest records, their own latest record, and older records only when cited or needed. Dr. Jones appends feedback to the record he is answering.

## References

Quarto. (n.d.). <i>Creating a book.</i> Retrieved September 11, 2026, from [https://quarto.org/docs/books/](https://quarto.org/docs/books/).

Quarto. (n.d.). <i>HTML accessibility checks.</i> Retrieved September 11, 2026, from [https://quarto.org/docs/output-formats/html-accessibility.html](https://quarto.org/docs/output-formats/html-accessibility.html).
