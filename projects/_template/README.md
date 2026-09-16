# Starting a Project

From the repository root, create the scaffold with the validated command:

```bash
python3 python/create_project.py <project-slug> "Project title"
```

The command validates the slug, refuses to overwrite any path, copies this
directory atomically, and initializes the title and state metadata. It does not
publish an empty Project. See
`projects/vcsserg-repo-v1/CREATING-PROJECTS-AND-SCHOLARS.md` for the complete
procedure. Consult `RESEARCHER-ORIENTATION.md` for authoritative workflow and
publication requirements.

## Project memory

The PI supplies the title, research questions, goals, data, deliverables,
constraints, and definition of done in `PROJECT.md`. Scholars read that file but
never edit it. The minimal charter here is intentionally left for the PI.

Scholars maintain `STATE.md` as a concise current snapshot. For each iteration,
they create exactly one immutable timestamped file under `dialog/iterations/`
and add it newest-first to both the bounded `DIALOG.md` landing index and the
appropriate complete yearly index under `dialog/indexes/`. Records include
start/end server times and elapsed time. The `STATE.md` front matter records the
title, lifecycle status, independent publication state, and newest substantive
update time. Published Projects use that time to order the public directory.
Active Projects may remain Unpublished while research begins. PI replies belong as appended blockquotes in the
specific iteration record; Scholars never write blockquotes or alter an earlier
record. Separate `PI.md` and `LOG.md` files are no longer the template layout.

## Research and publication checklist

- Keep research data, analysis, sources, and Quarto source files under the
  project's `projects/` directory. Record source provenance and use APA citations
  with DOI links whenever possible.
- Write the Full Report first as a Quarto book combining text, R code, figures,
  and a bibliography. Render static HTML to
  `website/projects/<project-slug>/report/index.html`, with a table of contents.
  If Quarto is unavailable, record the limitation in `STATE.md` and generate
  HTML directly; do not install a replacement runtime.
- Derive a two-column PDF shorter report, at most 10 pages including figures
  and references, and link all three report forms to one another.
- Publish the five-minute Executive Summary at
  `website/projects/<project-slug>/index.html`. Include exactly one dense key
  figure and up to 10 result bullets, each beginning with a bold sentence,
  followed by 1–3 explanatory sentences and links into the Full Report.
- Use the CSSERG logo, forest green, Artichoke Green `#4B6F44`, Laurel Green
  `#dde3d8`, and Bootstrap from its official CDN. Include the shared footer
  with **About** links to Dr. Jones and CSSERG and **Open work** links to the
  [GitHub repository](https://github.com/jasonjeffreyjones/virtual-csserg/) and
  standard CC BY 4.0 International badge. Follow the selected research journal
  styling in `website/assets/styles.css`.
- Include the exact phrase "far beyond" exactly once in the Full Report.
- Link the public project from both `website/index.html` and
  `website/projects/index.html`. Keep the all-Projects index ordered by the
  latest substantive Project update; validate local links, figures, output
  formats, and relevant code before ending the iteration.

Apply explicit project-charter exceptions where provided. Do not publish empty
reports or invented results merely to fill these paths.

After a Scholar finishes, automation commits, pushes, and deploys `website/`.
Scholars do not edit `run-scholar.sh` or access `.env`.
