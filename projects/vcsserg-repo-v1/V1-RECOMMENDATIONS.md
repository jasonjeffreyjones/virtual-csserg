# Version 1 design and workflow recommendations

Prepared by Bee Boring Vanilla on September 11, 2026 in response to the latest
PI guidance in `DIALOG.md`.

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

I recommend **A for Version 1**, retaining monograms until an image policy is
approved. It scales cleanly beyond three Scholars and keeps authoritative
profiles one click away. B becomes more useful when the lab has enough
simultaneous work that assignments are otherwise hard to see. C best expresses
personality, but makes the directory slower to scan and duplicates biography
content that belongs authoritatively on profile pages.

### Header and footer

I agree that the primary header should contain only internal navigation. This
iteration implements **Projects** and **Scholars** as stable directory links and
keeps the wordmark as **Home**; the external CSSERG link remains in every
footer. This is clearer than fragment links whose destination changes with the
homepage editorial layout.

All four external footer destinations remain necessary. I recommend presenting
them in two conceptual groups when the footer is next redesigned: **About**
(Dr. Jason Jeffrey Jones, CSSERG) and **Open work** (GitHub, CC BY 4.0). This is
an information-architecture recommendation; the current shared footer remains
flat to avoid redesigning production before PI selection.

The homepage now uses **“Research Updates from Virtual CSSERG”** as its main
heading. It replaces both the rejected journal label and the oversized
“Inquiry, in public.” slogan with a literal description of what follows.

## Full Reports as Quarto HTML books

I recommend keeping Quarto HTML books as the **default required Full Report**.
Their source/output separation supports executable analysis, citations, a table
of contents, stable section links, and multi-chapter growth. Quarto describes an
HTML book as a specialized website and supports book-level navigation and
cross-references; this matches the lab's static publishing model. A one-chapter
book has some interface overhead, but consistency and an obvious growth path are
worth it here.

Direct-authored HTML should be a documented contingency when the host's Quarto
runtime is genuinely unavailable, not an equivalent long-term format. The
current host provides Quarto 1.10.18, so the VCSSERG v1 and Predict the Self
reports should be brought into the book workflow rather than retaining a stale
runtime exception. Rendered output still needs local-link, visual, and
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
Virtual CSSERG records. Monograms remain an honest default.

## Dialog storage

I do **not** recommend changing the shared file from append-only to prepend-only.
Prepending makes every iteration edit the same first lines, increasing rebase
conflicts and making the chronological record harder to audit in ordinary diffs.
The scrolling problem is real, but reversal is the wrong fix.

I recommend **one immutable file per iteration**, not one per day:

```text
projects/<slug>/dialog/2026/2026-09-11T185940Z-bee-boring-vanilla.md
```

Daily files can still collide when several Scholars work on the same Project.
Timestamped iteration files provide stable ordering and natural authorship.
`DIALOG.md` should become a short, newest-first index and retain the complete
legacy record unchanged. PI replies can be appended as blockquotes to the
specific iteration file. A migration requires coordinated edits to the
orientation, template, runner prompt, and verifier, so this iteration only
records the recommendation.

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
deployment, or unrelated commit. The new Projects page applies that judgment
manually. For reliable sorting, I recommend small machine-readable front matter
in `STATE.md` with at least `title`, `status`, and `updated`, while keeping the
rest of the file human-readable.

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

Additional details worth specifying centrally are slug immutability, who may
change lifecycle state, the exact completion checklist, whether previews remain
public after selection, how superseded reports are archived, and the source of
truth for Scholar–Project assignments.

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

This iteration adds an explicit three-format report group, biography and
Projects-directory coverage, and report cross-link/phrase/figure checks. It
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
