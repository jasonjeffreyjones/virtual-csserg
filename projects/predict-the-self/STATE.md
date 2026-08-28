# Predict the Self — Current State

## Status

Active. Participant preparation for the Predict Future Selves challenge is
documented, but no prediction or score is yet valid because the challenge
README and participant files could not be retrieved in this iteration.

## What is complete

- Read the project charter, PI instructions, complete online *Ipseology* book,
  and Dr. Jones' *Predicting the Self with Generative AI* slides.
- Established the required ipseological framing: bios are personally expressed
  identity text; their tokens and ngrams can be identity signifiers; the target
  is later expressed identity, not a latent "true self."
- Recovered the prior OPTS Mark 1 setup from the slides: 112,541 longitudinal
  pairs of 2015 and 2020 US Twitter bios with `Early_Bio` and `Later_Bio`.
- Added `report.qmd`, a Quarto Full Report source that documents sources,
  participant status, a leakage-resistant protocol, limitations, and next work.
- Published a project Executive Summary and added Predict the Self to the home
  page; Aleph Initial Alpha's profile now shows the assigned project.

## Current problems and unknowns

- The public GitHub profile listed `predict-future-selves`, but the environment's
  web cache returned a cache miss for the new repository page, README, and raw
  file. Direct shell access could not resolve GitHub. The precise current
  instructions, supplied cases, allowed resources, and official scoring rule
  remain unread.
- No challenge predictions, metrics, or comparative claims should be reported
  until those primary materials are available.
- Quarto is not installed. `report.qmd` could not be rendered into
  `website/projects/predict-the-self/report/` during this iteration.

## Important files

- `projects/predict-the-self/PROJECT.md` — stable charter (PI-owned)
- `projects/predict-the-self/PI.md` — PI instructions (PI-owned)
- `projects/predict-the-self/report.qmd` — Full Report source and participant protocol
- `projects/predict-the-self/LOG.md` — append-only iteration record
- `website/projects/predict-the-self/index.html` — public Executive Summary

## Likely next steps

1. Retrieve the challenge README and participant files; record the source
   commit and file hashes.
2. Follow the challenge instructions, freeze predictions before accessing any
   answers, and apply the official scoring procedure.
3. Add permitted simple baselines, case-level results, and error analysis.
4. Render `report.qmd` with Quarto and link the Full Report from the Executive
   Summary.
