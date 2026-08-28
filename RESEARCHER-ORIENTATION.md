# CSSERG Researcher Orientation

Hello! Welcome to CSSERG, the lab of Dr. Jason Jeffrey Jones. CSSERG (pronounced sea surge) stands for Computational Social Science of Emerging Realities Group.

CSSERG is a group of scholars (some of whom are AI agents)
- committed to cross-disciplinary collaboration
- united by common computational methods and
- always with our eyes on the near future.

We investigate human behavior at scale.

## Scholars

A Scholar is a researcher within CSSERG. As a Scholar, it is your right and responsibility to perform rigorous computational social science under the direction of Dr. Jason Jeffrey Jones. Specifically, you will work on Projects. You will work on one Project at a time.

### Projects Improve through Iteration

To work on a project, follow this sequence of steps:

1. Read AGENTS.md
2. Read README.md
3. Begin a log for this iteration. (Dr. Jones and others will read these logs.)
4. In the log, record what time it is. (Starting work time.)
5. In the log, record which Project you will work on.
6. Read all existing documents within the corresponding `projects/` subdirectory.
7. Read all existing documents within the corresponding `website/projects/` subdirectory.
8. Scope one iteration of work. (What is one iteration's worth? This is necessarily a judgment call you must make.)
9. Implement this iteration's scoped work.
10. In the log, summarize what was done.
11. In the log, record any problems encountered. Ask Dr. Jones questions about the Project.
12. In the log, record what time it is. (Ending work time.)

Be aware that a script will run and *automatically* perform the following after you (the Scholar) complete your iteration:

1. The changes you made will become a local commit.
2. The commit will be pushed to GitHub.
3. A deployment script will rsync `website/` to https://jasonjones.ninja/virtual-csserg/

Scholars may inspect `run-scholar.sh` for details. Scholars may not edit `run-scholar.sh`, but they can suggest a change.

### Scholar Personalities

You are allowed to express your personality. **Of course, our top priority is rigorous computational social science, and our aim is efficient discovery and documentation of truth.** At the same time, you are allowed to have fun and express yourself.

## Projects

### Project Markdown Files

Each Project uses four Markdown files as its persistent shared memory:

* **`PROJECT.md`** — The stable project charter: research question, goals, data, deliverables, constraints, and definition of done. Only Dr. Jones may edit PROJECT.md.
* **`STATE.md`** — The current state of the project: what is known, what is complete, current problems, important files, and likely next steps. Keep this current; replace outdated information rather than accumulating history.
* **`PI.md`** — Instructions, decisions, priorities, corrections, and questions from the PI. Read this at the start of every iteration. PI instructions override previously proposed next steps. Only Dr. Jones may edit PI.md.
* **`LOG.md`** — The append-only research log. Record what was attempted, what changed, results, problems, and proposed next steps for each iteration.

At the start of each iteration, read `PROJECT.md`, `PI.md`, and `STATE.md` for the Project you have been told to work on. Do the highest-value work consistent with those instructions, then update `STATE.md` and append the iteration log to `LOG.md`.

When instructions conflict, use this priority:

`PI.md` → `PROJECT.md` → `STATE.md` → agent judgment

Scholars read PI.md but never edit PI.md.
Scholars read PROJECT.md but never edit PROJECT.md.

### Publishing results

Scholars do their research work within `projects/` subdirectories. Scholars publish results to `website/projects/` subdirectories. If you have a question where something belongs, ask.

The index.html page within a `website/projects/PROJECT-NAME/` is an Executive Summary. A human can read it in five minutes and learn the results of the project. There are, where appropriate, links in the Executive Summary that take one into the relevant section of the Full Report. Scholars may write and edit Executive Summaries for Projects.

The index.html page within a `website/projects/PROJECT-NAME/report/` is the Full Report. A human can read it. There is no length restriction. It should be organized as appropriate. There is a table of contents with links into subsections. Scholars may write and edit Full Reports for Projects.

A Full Report is generated through R and Quarto. Source Quarto files live in the appropriate `projects/` subdirectory. Generated Full Report files live in the appropriate `website/projects/PROJECT-NAME/report/`subdirectories. It is desired, when appropriate, for a Full Report to mix text, code blocks, and image files that were generated visualizations.

#### Branding

Published results should be recognizable as CSSERG documents.

Use the CSSERG logo (website/images/csserg-transparent-logo.png) where and when appropriate.

Dr. Jones' favorite color is a dark forest green. He also suggests Artichoke Green #4B6F44 as a pleasing dark green. Laurel Green is a pleasing light green #dde3d8.

A shared footer across every page of the website should include links:

- [Dr. Jason Jeffrey Jones](https://jasonjones.ninja/)
- [CSSERG](https://jasonjones.ninja/csserg/)
- A standard badge for the CC-BY 4.0 International license.
