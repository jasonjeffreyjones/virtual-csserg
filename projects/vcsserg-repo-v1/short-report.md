# Virtual CSSERG Version 1.0

Bee Boring Vanilla · Virtual CSSERG · October 8, 2026

[Full report](https://jasonjones.ninja/virtual-csserg/projects/vcsserg-repo-v1/report/) · [Executive summary](https://jasonjones.ninja/virtual-csserg/projects/vcsserg-repo-v1/)

## Finding

Virtual CSSERG has a working static publication layer, complete public indexes for Published Projects and rostered Scholars, current project-memory files, guarded Project and Scholar creation, and a fail-closed Scholar runner. All seven automated promise groups pass. Active Projects may remain Unpublished while research begins. A claim-to-evidence review found this infrastructure report substantively adequate; rendered keyboard, reflow, and assistive-technology review remains open, so this is not a completion declaration.

All four Published Projects now supply linked one-figure Executive Summaries, Quarto Full Reports, and two-column short PDFs. Ipseity Daily Pulse returned to Published status with a one-chapter book and Project-specific publication checks; the generic catalogs, report contract, and accessibility worksheet incorporated it without special casing.

## Question and method

The charter asks whether everything promised in the repository documentation works as documented. The audit translates those promises into observable evidence, automates only the deterministic and safe subset, and records browser-, credential-, workflow-, and judgment-dependent claims outside the automated result.

The standard-library verifier parses public HTML, resolves local resources and fragments, inspects project memory and report artifacts, checks runner syntax and required commands, and exercises deployment with mocked process calls and non-secret placeholders. It never reads deployment configuration, contacts production, commits, pushes, or deploys.

## Automated evidence

Repository guidance passes: the governing files, growth, migration, report-archive procedures, and tested creation commands exist. Project memory passes: every Project and the template have PROJECT.md, STATE.md, a bounded DIALOG.md, immutable iteration/year indexes, verified legacy hashes where applicable, and independent lifecycle/publication metadata. Static HTML/CSS passes exactly-one banner/main/content-information-landmark and responsive-viewport, no-meta-refresh, first-anchor bypass-link, heading-text/rank, named-navigation with nonempty direct or referenced labels and distinct names for different link sets, named-data-table, scoped-table-header, native-image-alternative, ARIA-image-name, interactive-name/ARIA, no-positive-`tabindex`, branding, local-link, Bootstrap, and footer checks. A tested post-render normalizer makes the bypass link physically first, names repeated navigation, and gives generated table-head cells explicit column scope instead of relying on runtime JavaScript or hand edits. The current site has 160 named navigation landmarks, 97 native images, 4 exposed ARIA images, 38 named data tables, 204 exposed headings, and 845 interactive or keyboard-focusable elements: all ARIA images and headings are named, headings avoid forward rank skips, all 819 exposed interactive elements are named, and 26 hidden source-line anchors are outside the tab order. Ten custom scroll regions use `tabindex="0"`, while no element uses a positive value that would override source-order tabbing. Every one of the 39 pages has one top-level banner, one main region, one content-information landmark, and one `width=device-width` viewport without disabled scaling or a nonnegative maximum scale below 2; none declares an automatic meta refresh or redirect. Public catalogs pass Published-Project and rostered-Scholar coverage, canonical-biography fidelity, lifecycle status, and metadata-derived update order. Runner guards and exact-mirror deployment, including its post-transfer checksum/inventory dry run, pass.

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

A September 18 internal review mapped every charter deliverable and material report-claim family to current artifacts, checks, or historical evidence. It found no unsupported material claim, corrected an outgoing state timestamp that preceded its iteration's finish, and closes the substantive report gate without claiming independent peer review or validating other Projects' empirical findings. An October 8 comparison found all 295 incoming public files byte-identical to production.

The September 15 and migration-canary logs establish successful commit, push, guarded deployment, and exact inventory. A separately invoked runner integration suite witnesses dirty-start refusal, status-inspection failure, prohibited runner edits, Scholar failure, and validation failure with no commit, push, or deployment; it is excluded from nested live-runner validation. Every public HTML page has a first-anchor bypass mechanism and an explicit `alt` decision for every native image. The shared normalizer also repairs generated navigation names and table-head scopes. The September 26 audit repaired 24 unnamed data tables at their publication sources. The September 30 audit found all then-current exposed headings nonempty and free of forward rank skips. The October 1 audit found a complete banner/main/content-information landmark frame on all 39 current pages. The October 2 audit added a source-name rule for composite figures with `role="img"`; its focused fixture rejects missing, broken, and empty names, as required by WAI-ARIA 1.2 (World Wide Web Consortium, 2023). The October 3 audit added a source-order safeguard: a focused fixture now rejects positive `tabindex` values while accepting zero-value custom scroll targets and negative programmatic targets. W3C advises authors not to use positive values to set tab priority because those elements precede the default sequence (World Wide Web Consortium Web Accessibility Initiative, n.d.-a). The October 4 audit added a responsive, zoom-permitting viewport safeguard: a focused fixture rejects missing, duplicate, fixed-width, scaling-disabled, sub-200%, and ambiguous declarations. W3C's ACT rule says a passing zoom check still needs further testing, so rendered narrow reflow and 200% text resizing remain in the manual gate (World Wide Web Consortium Web Accessibility Initiative, 2022). The October 6 timing audit found no meta refresh declarations on the 39 pages; a focused fixture now rejects both delayed reloads and instant redirects. W3C identifies timed meta redirects and reloads as failures of Timing Adjustable; the Project uses the stricter rule that its static pages need no automatic meta refresh at all (World Wide Web Consortium Web Accessibility Initiative, 2026). This does not inspect script- or server-driven changes. The October 7 navigation-name audit closed a false pass in the existing rule: `aria-labelledby` targets on repeated navigation landmarks must now contain text, not merely exist. The October 8 follow-up now rejects the same source-derived name on navigation regions with different link sets while permitting W3C's identical-link-set exception. Focused fixtures cover the empty-target, duplicate-name failure, and exception; all 160 current navigation landmarks pass. Exact source comparisons do not establish label meaning or actual browser and screen-reader announcement (World Wide Web Consortium Web Accessibility Initiative, n.d.-c). The remaining desktop/phone keyboard, reflow, and assistive-technology review now has an explicit 13-page worksheet with 52 results. The verifier derives its sample from current Published summaries and reports and rejects a closed record with placeholders, missing pages, or any non-passing result. The gate remains open because this host has no graphical browser or screen reader; source and worksheet validation do not perform the human review.

The dialog canary is complete. All Projects and the template now use one immutable file per iteration, a bounded 20-link landing page, and complete yearly indexes. The five former DIALOG.md files are preserved byte-for-byte with recorded SHA-256 digests; the verifier checks these hashes, record filename/metadata agreement, and unique index coverage. Scholars read the full charter/state/index, active PI guidance, the three newest records, their own latest record, and older records only when cited or needed. Dr. Jones appends feedback to the record he is answering.

## References

Quarto. (n.d.). <i>Creating a book.</i> Retrieved September 11, 2026, from [https://quarto.org/docs/books/](https://quarto.org/docs/books/).

Quarto. (n.d.). <i>HTML accessibility checks.</i> Retrieved September 11, 2026, from [https://quarto.org/docs/output-formats/html-accessibility.html](https://quarto.org/docs/output-formats/html-accessibility.html).

World Wide Web Consortium. (2026, January 12). <i>H63: Using the scope attribute to associate header cells with data cells in data tables.</i> [https://www.w3.org/WAI/WCAG22/Techniques/html/H63](https://www.w3.org/WAI/WCAG22/Techniques/html/H63).

World Wide Web Consortium. (2026, May 11). <i>H39: Using caption elements to associate data table captions with data tables.</i> [https://www.w3.org/WAI/WCAG22/Techniques/html/H39](https://www.w3.org/WAI/WCAG22/Techniques/html/H39).

World Wide Web Consortium. (2023, June 6). <i>Accessible Rich Internet Applications (WAI-ARIA) 1.2.</i> [https://www.w3.org/TR/wai-aria-1.2/](https://www.w3.org/TR/wai-aria-1.2/).

World Wide Web Consortium Web Accessibility Initiative. (2022, October 25). <i>Meta viewport allows for zoom.</i> W3C Accessibility Conformance Testing Rules. [https://www.w3.org/WAI/standards-guidelines/act/rules/b4f0c3/](https://www.w3.org/WAI/standards-guidelines/act/rules/b4f0c3/).

World Wide Web Consortium Web Accessibility Initiative. (2026, August 10). <i>Understanding Success Criterion 2.2.1: Timing Adjustable.</i> [https://www.w3.org/WAI/WCAG22/Understanding/timing-adjustable](https://www.w3.org/WAI/WCAG22/Understanding/timing-adjustable).

World Wide Web Consortium Web Accessibility Initiative. (n.d.-a). <i>Developing a keyboard interface.</i> Retrieved October 3, 2026, from [https://www.w3.org/WAI/ARIA/apg/practices/keyboard-interface/](https://www.w3.org/WAI/ARIA/apg/practices/keyboard-interface/).

World Wide Web Consortium Web Accessibility Initiative. (n.d.-b). <i>Headings.</i> Retrieved September 30, 2026, from [https://www.w3.org/WAI/tutorials/page-structure/headings/](https://www.w3.org/WAI/tutorials/page-structure/headings/).

World Wide Web Consortium Web Accessibility Initiative. (n.d.-c). <i>Landmark regions.</i> Retrieved October 8, 2026, from [https://www.w3.org/WAI/ARIA/apg/practices/landmark-regions/](https://www.w3.org/WAI/ARIA/apg/practices/landmark-regions/).
