# Version 1 design and workflow recommendations

Prepared by Bee Boring Vanilla on September 11, 2026 in response to the latest
PI guidance in `DIALOG.md`.

## Decision and implementation status

Dr. Jones approved every recommendation below and selected both A alternatives.
On September 12, the production Executive Summary adopted the evidence brief,
and the production Scholar directory adopted the portrait roster. All Project
states and `_template` now carry authoritative `title`, `status`, independent
`publication`, and `updated`
metadata; the verifier derives public update order from it. A tested, atomic,
no-overwrite `python/create_project.py` command and a complete Project/Scholar
creation guide implement the first growth workflow. The guide also makes the
approved generated-image safeguards operational.

The VCSSERG v1 Full Report is now a Quarto HTML book, with a linked two-column
short PDF and evidence-brief Executive Summary. Predict the Self now uses the
same three-form system, closing the final automated promise-group gap. The
coordinated immutable-dialog migration was completed across every Project and
the template on September 16. One manual Version 1 gate remains. The conceptual
footer grouping and a single identity/biography source
were implemented and later hardened with command-driven Scholar creation. On September 14, all 109 expected public
files matched the repository byte-for-byte, and deployment gained a required
post-transfer checksum/inventory dry run. The September 15 normal run reached
completion after that inventory phase, and the September 16 public probe found
all 110 expected files byte-identical. The successful workflow and deployment
gate are therefore observed. Isolated runner tests now witness dirty-start and
status-inspection refusal, prohibited runner edits, plus Scholar and validation
failures without commit, push, or deployment. They run as a separate
integration suite rather than recursively inside a live runner. A September 18
claim-to-evidence review closes the substantive report gate and documents its
internal-review boundary; rendered keyboard and assistive-technology usability
remains the sole manual gate. On September 19, the generated-report build made
every bypass link first in static HTML without runtime relocation, and
`ACCESSIBILITY-REVIEW.md` made the remaining 11-page manual gate reproducible.
On September 20, its summary record became a page-by-page worksheet with four
results per page, and the verifier began deriving the required sample from
current Published summaries and Full Reports. Automated checks now prevent an
incomplete **Closed** record without claiming to perform the human review.
On September 22, a deterministic landmark audit found 14 unnamed navigation
regions across the four generated Quarto pages. The shared post-render
normalizer now names those regions, and the whole-site verifier rejects unnamed
repeated navigation landmarks or missing `aria-labelledby` targets. This
reduces a known screen-reader risk but does not replace the open rendered
review.
The superseded-report archive policy is now
specified and exercised by the v1 release ledger, including the clean
September 17 outgoing report preserved before substantive review and the clean
September 18 report preserved before static bypass-link promotion.

## Recommended design choices

### Project Executive Summaries

Three working alternatives are published under
`website/projects/vcsserg-repo-v1/designs/project-summaries/`:

1. **A — Evidence brief:** question and status, one key figure, then findings.
2. **B — Research poster:** a dominant figure beside a compact findings rail.
3. **C — Field notes:** a dated question–evidence–decision narrative.

I recommend **A as the default system**. It maps most directly onto the
orientation's five-minute reading contract, remains legible when a Project's
figure is not visually spectacular, and creates a predictable place for limits
and report links. B is strongest when a genuinely explanatory figure can carry
the page. C is unusually well suited to infrastructure and provisional work,
but is less efficient for comparing several stylized facts.

### Scholar directory

Three working alternatives are published under
`website/projects/vcsserg-repo-v1/designs/scholar-directories/`:

1. **A — Portrait roster:** parallel cards, equal weight, direct profile links.
2. **B — Work map:** roster plus a Scholar-to-current-Project matrix.
3. **C — Field guide:** full charter biographies lead each long entry.

I recommend **A for Version 1**, retaining monograms under the approved image
policy. It scales cleanly beyond three Scholars and keeps authoritative
profiles one click away. B becomes more useful when the lab has enough
simultaneous work that recent contribution histories are otherwise hard to see. C best expresses
personality, but makes the directory slower to scan and duplicates biography
content that belongs authoritatively on profile pages.

### Header and footer

I agree that the primary header should contain only internal navigation. This
iteration implements **Projects** and **Scholars** as stable directory links and
keeps the wordmark as **Home**; the external CSSERG link remains in every
footer. This is clearer than fragment links whose destination changes with the
homepage editorial layout.

All four external footer destinations remain necessary. Every current static,
generated, and archived-design page now presents them in two conceptual groups:
**About** (Dr. Jason Jeffrey Jones, CSSERG) and **Open work** (GitHub, CC BY
4.0). The verifier rejects missing groups and misplaced links.

The homepage now uses **“Research Updates from Virtual CSSERG”** as its main
heading. It replaces both the rejected journal label and the oversized
“Inquiry, in public.” slogan with a literal description of what follows.

## Full Reports as Quarto HTML books

I recommend keeping Quarto HTML books as the **default required Full Report**.
Their source/output separation supports executable analysis, citations, a table
of contents, stable section links, and multi-chapter growth. Quarto describes an
HTML book as a specialized website and supports book-level navigation and
cross-references; this matches the lab's static publishing model. A one-chapter
book has some interface overhead, but consistency and an obvious growth path
are worth it here. This is not a recommendation for an exact chapter count:
Predict the Self now uses two chapters, while VCSSERG v1 currently needs one.

Direct-authored HTML should be a documented contingency when the host's Quarto
runtime is genuinely unavailable, not an equivalent long-term format. The
current host provides Quarto 1.10.18. VCSSERG v1 and Predict the Self now both
use the book workflow.
Rendered output still needs local-link, visual, and
accessibility checks; Quarto can assist with accessibility testing, but tool
output does not replace manual review.

## Scholar self-representation images

This is feasible and potentially a good idea **as illustration, not
biography**. Generated self-representations could make the Scholars memorable
and give them legitimate creative latitude. The main risk is that a
photorealistic portrait implies a body, history, or demographic identity that
the records do not establish.

I recommend a first-version policy with these constraints:

- use clearly non-photographic avatars or symbolic illustrations;
- preserve the image file in the repository and label it as Scholar-generated;
- record Scholar, date, generation/editing method, prompt or design brief, and
  source-image provenance in a neighboring metadata file;
- provide useful alt text and verify small-screen crops;
- do not infer age, race, gender, credentials, location, or lived history;
- require PI selection before a generated image becomes the canonical profile
  representation.

This policy makes provenance public and keeps claims on the profile grounded in
Virtual CSSERG records. Monograms remain an honest default. The approved policy
is now part of `CREATING-PROJECTS-AND-SCHOLARS.md`; no generated portrait has
been adopted.

## Dialog storage

I do **not** recommend changing the shared file from append-only to prepend-only.
Prepending makes every iteration edit the same first lines, increasing rebase
conflicts and making the chronological record harder to audit in ordinary diffs.
The scrolling problem is real, but reversal is the wrong fix.

I recommend **one immutable file per iteration**, not one per day:

```text
projects/<slug>/dialog/iterations/2026-09-11T185940Z-bee-boring-vanilla.md
```

Daily files can still collide when several Scholars work on the same Project.
Timestamped iteration files provide stable ordering and natural authorship.
`DIALOG.md` is now a short, newest-first index, while each complete legacy log
is retained byte-for-byte under `dialog/legacy/` with a recorded SHA-256 digest.
PI replies are appended as blockquotes to the specific iteration file. The
coordinated migration updated the orientation, template, PI-triggered runner,
every existing Project, creation workflow, states, and verifier together.
`DIALOG-MIGRATION.md` records the trigger, migration sequence, reply protocol,
20-entry current index, yearly indexes, bounded reading rule, and completion
evidence.

## Project states and metadata

Use one lifecycle state, with publication/readiness tracked separately:

| State | Meaning |
|---|---|
| **Proposed** | A charter is being prepared; research iteration has not begun. |
| **Active** | Work is authorized and useful next work exists. |
| **Blocked** | Progress genuinely depends on unavailable input or infrastructure. |
| **Paused** | The PI has intentionally deprioritized otherwise feasible work. |
| **Completed** | The charter's definition of done and required publication are met. |
| **Archived** | A closed Project is retained but superseded, retired, or no longer maintained. |

“In progress” should be display text for Active, not another state. “Under
review” and “ready to publish” describe workflow/readiness and should not compete
with lifecycle state. Every state change should record who changed it, when, and
why. Completion should require both automated evidence and named manual gates.

The phrase **most recently updated** should mean the end time of the newest
substantive Scholar iteration or PI intervention in that Project—not a CSS edit,
deployment, or unrelated commit. Version 1 now uses small machine-readable front
matter in `STATE.md` with `title`, `status`, `publication`, and `updated`, while keeping the
rest of the file human-readable. The verifier makes these records authoritative
for public Projects-directory order and timestamps.

## Creating Projects

Copying `_template` is understandable but too easy to perform partially. The
better Version 1 process is a small standard-library command such as:

```text
python3 python/create_project.py <slug> "<title>"
```

It should validate a lowercase hyphenated slug, refuse overwrite, copy the
template, set initial STATE metadata, and print the next steps. It should **not**
publish an empty Project page or modify the PI's charter content. Dr. Jones would
still write and commit `PROJECT.md`; the script would make the mechanical part
atomic and testable. A separate publication step should add the Project to the
public directory only after a substantive Executive Summary exists.

The command and procedure are now implemented and tested. The central guide
also specifies slug immutability, independent lifecycle/publication state, and
publication gating. A second guarded command creates Scholar identity,
canonical biography, profile, and catalog entries without assigning or
scheduling work. The versioned `scholars.json` file is authoritative for names,
slugs, and monograms; `scholars/<slug>/BIOGRAPHY.md` is authoritative for the
PI-authored biography. Scholar–Project pairing lasts for one runner invocation.

## Superseded reports

Version 1 now uses a Git-backed release ledger rather than copying old Quarto
trees into the live website. Canonical Project URLs always present current
evidence. Before a material report change, the Scholar records the clean
outgoing commit, affected forms, reason, and update/correction/retraction class
in the Project's `REPORT-VERSIONS.md`. The full commit identifies all three
generated forms, their dependencies, sources, and contemporaneous Project
record without breaking relative links or multiplying vendored assets.

`REPORT-ARCHIVING.md` defines materiality, dirty-tree handling, immutable
ledger entries, correction and retraction notices, retrieval URLs, and
validation. The v1 Project applies the policy to the September 15 report set as
the first recorded supersession. Styling-only maintenance remains recoverable
through ordinary Git history and does not create a release entry.

## What `verify_v1.py` can and cannot establish

The earlier verifier did **not** accurately answer whether the website was at
Version 1. It was a useful regression suite with two problems:

- **False positives:** passing six structural groups did not test the required
  three report formats, exact Executive Summary figure count, “far beyond”
  phrase, report cross-links, full charter biographies, or the Projects index.
- **False negatives:** it required every vendored Quarto stylesheet to contain
  CSSERG brand colors and motion/responsive rules, required exactly one H1 on a
  generated Quarto book page, and treated optional descriptions as a release
  gate.

The September 11 revision added an explicit three-format report group,
biography and Projects-directory coverage, and report
cross-link/phrase/figure checks. The current revision adds state metadata,
selected-layout, and guarded-scaffold checks. The suite
limits design assertions to first-party CSS and accepts Quarto's multi-H1 book
structure. These changes make the automated evidence more valid, but the script
still cannot establish production byte parity, rendered layout, keyboard or
assistive-technology usability, research validity, substantive completeness, or
an observed end-to-end Scholar run. Its output should therefore remain a
**promise regression report**, never a Version 1 certification by itself.

## References

Quarto. (n.d.). *Creating a book*. Retrieved September 11, 2026, from
https://quarto.org/docs/books/

Quarto. (n.d.). *HTML accessibility checks*. Retrieved September 11, 2026, from
https://quarto.org/docs/output-formats/html-accessibility.html
