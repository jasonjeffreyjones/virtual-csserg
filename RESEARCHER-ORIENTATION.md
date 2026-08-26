# CSSERG Researcher Orientation

Hello! Welcome to CSSERG, the lab of Dr. Jason Jeffrey Jones. CSSERG (pronounced sea surge) stands for Computational Social Science of Emerging Realities Group.

CSSERG is a group of scholars (some of whom are AI agents)
- committed to cross-disciplinary collaboration
- united by common computational methods and
- always with our eyes on the near future.

We investigate human behavior at scale.

## Researcher Duties

As a researcher within CSSERG, it is your right and responsibility to perform rigorous computational social science under the direction of Dr. Jason Jeffrey Jones. Specifically, you will work on Projects. You will work on one Project at a time.

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
13. When this iteration's scoped work and log is complete, do everything necessary to commit the updated repo to GitHub.
14. Push the commit to GitHub.
15. Use the deployment script to rsync `website/` to https://jasonjones.ninja/virtual-csserg/

## Project Markdown Files

Each Project uses four Markdown files as its persistent shared memory:

* **`PROJECT.md`** — The stable project charter: research question, goals, data, deliverables, constraints, and definition of done. Only Dr. Jones may edit PROJECT.md.
* **`STATE.md`** — The current state of the project: what is known, what is complete, current problems, important files, and likely next steps. Keep this current; replace outdated information rather than accumulating history.
* **`PI.md`** — Instructions, decisions, priorities, corrections, and questions from the PI. Read this at the start of every iteration. PI instructions override previously proposed next steps. Only Dr. Jones may edit PI.md.
* **`LOG.md`** — The append-only research log. Record what was attempted, what changed, results, problems, and proposed next steps for each iteration.

At the start of each iteration, read `PROJECT.md`, `PI.md`, and `STATE.md` for the Project you have been told to work on. Do the highest-value work consistent with those instructions, then update `STATE.md` and append the iteration log to `LOG.md`.

When instructions conflict, use this priority:

`PI.md` → `PROJECT.md` → `STATE.md` → agent judgment
