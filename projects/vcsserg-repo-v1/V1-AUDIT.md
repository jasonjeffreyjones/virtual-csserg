# VCSSERG Version 1.0 Audit

This is a point-in-time map from documented promises to observable evidence. It
separates verified behavior from assumptions so “works as documented” remains a
testable goal.

Run the non-destructive automated portion from the repository root:

```bash
python3 projects/vcsserg-repo-v1/verify_v1.py
```

The verifier does not read `.env`, contact remote systems, create commits, or
deploy. It returns nonzero while an automated group fails. A passing run would
still not establish the manual gates below.

## Evidence matrix

| Documented promise | Evidence or test | Status on September 11, 2026 |
|---|---|---|
| Repository guidance exists | Required top-level files | Automated pass |
| Every Project uses current memory layout | `PROJECT.md`, `STATE.md`, `DIALOG.md`, including `_template` | Automated pass; Predict the Self migration preserves legacy records |
| Public static site is branded and locally connected | First-party HTML/CSS semantics, local paths/fragments, Bootstrap CDN, logo, required footer | Automated pass across 23 HTML pages and 5 first-party stylesheets |
| Projects and initial Scholars are findable | Home, Projects index, Scholar index, profiles, charter biographies | Automated pass |
| Every Project has all three linked report formats | Executive Summary with exactly one figure, Quarto source/book, Full Report, short PDF, cross-links and required phrase | Automated fail; details below |
| Scholar runner wires the documented lifecycle | Syntax and static command/path checks | Automated pass; not executed end to end |
| Deployment safely mirrors `website/` | Mocked guarded, shell-free `rsync`, deletion and error propagation | Automated pass; live parity unverified |

## Current automated result

On September 11, 2026, **six of seven groups pass**. The report group correctly
remains open:

- VCSSERG v1 lacks Quarto book source/output and a short PDF. Its production
  Executive Summary now has exactly one dense key figure.
- Predict the Self lacks a short PDF, a summary figure, current Quarto book
  configuration, and the required phrase in its direct-HTML Full Report.
- NFL Team Fandom Identities supplies all three forms. Its Quarto footer source
  and rendered report now retain the PI-requested GitHub link.

This is a count of automated promise groups, not a completion percentage or a
measure of research quality.

## Verifier validity

The earlier six-group script was a useful regression check, but it did not
accurately certify Version 1. It omitted report formats, full biographies, and
the Projects directory. It also produced false failures by applying CSSERG
palette and motion rules to vendored Quarto libraries and by requiring exactly
one H1 on a multi-level Quarto book page.

The current verifier:

- adds a dedicated three-format report group;
- checks the Executive Summary figure count, report cross-links, Quarto source,
  PDF signature, and the required “far beyond” phrase;
- checks the Projects index and exact normalized charter biographies;
- limits style assertions to first-party CSS and accepts one or more H1s;
- continues to verify local resources and required shared footer links on every
  HTML page, including generated reports.

These changes make the automated claims narrower and more valid. The script is
still a **promise regression report**, not a Version 1 completion oracle. See
`V1-RECOMMENDATIONS.md` for the full assessment.

## Manual gates

- Confirm production file inventory and bytes exactly match `website/` after
  the normal commit, push, and deploy sequence.
- Observe one complete successful Scholar workflow, including logging and
  failure behavior.
- Inspect the selected layouts at desktop and phone widths with keyboard and
  assistive-technology checks.
- Review substantive report completeness and research validity. File existence
  and links cannot establish either.
- Confirm short reports use two columns and remain at or under 10 pages. The
  generic v1 verifier checks only the PDF signature; project publication tests
  may enforce stronger PDF properties.

## Other current requirements

- The Project directory exists at `website/projects/index.html` and is manually
  ordered by the latest substantive Project record: VCSSERG v1, NFL Team Fandom
  Identities, then Predict the Self. `V1-RECOMMENDATIONS.md` proposes durable
  update metadata so this ordering becomes reproducible.
- Homepage copy now reads “Research Updates from Virtual CSSERG.” Primary
  headers contain internal Home/Projects/Scholars navigation; external CSSERG,
  PI, GitHub, and license links remain in footers.
- Three Executive Summary and three Scholar-directory alternatives are linked
  from the v1 public page. They are review artifacts, not production choices.
- All three initial Scholar profiles now contain the complete biographies
  supplied in the charter.
- `_template` provides the three required memory files plus setup, reporting,
  branding, and publication guidance.
