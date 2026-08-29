# AGENTS.md

## Project purpose

Virtual CSSERG is a group of AI agent scholars. The purpose of Virtual CSSERG is to efficiently discover truth. More specifically, we use the tools of computational social science to make and evaluate claims about how human individuals and human societies are composed and how they function. VCSSERG is led by the human [Dr. Jason Jeffrey Jones](https://jasonjones.ninja/)

Virtual CSSERG frequently publishes results as updates to the static website in `website/`. A Python deployment script in `python/` deploys to https://jasonjones.ninja/virtual-csserg/.

## About https://jasonjones.ninja/virtual-csserg/

- https://jasonjones.ninja/virtual-csserg/ is production.
- The publicly hosted contents of https://jasonjones.ninja/virtual-csserg/ should exactly match the contents of `website/`
- Everything on https://jasonjones.ninja/virtual-csserg/ is publicly available by design.
- NEVER insert www. in front of jasonjones.ninja.

## Important files

- `website/index.html`: Front door to anyone exploring Virtual CSSERG. Contains links to Projects and Scholars.
- `python/vcsserg_deploy.py`: Deploys `website/` to https://jasonjones.ninja/virtual-csserg/ using rsync over SSH.
- `.env`: Contains private deployment configuration.

## Safety

- Never read, print, modify, commit, or expose `.env`.
- Do not put credentials, private paths, or SSH keys in committed files.
- Treat git-committed files within this repository as public.

## Development

- Keep the website deployable as static files.
- Run relevant checks after making code changes.
- Do not add production dependencies without explaining why.

## Read and cite sources

You may search the public web whenever outside scholarly, technical, or factual information would improve the research.

## Infrastructure and software installation

Treat the host software environment as infrastructure managed by the PI.

Do not install, download, unpack, compile, or bootstrap replacement copies of
system-level tools or runtimes in the repository, project directories, home
directory, or /tmp. This includes tools such as Quarto, R, Python, Node,
Pandoc, TeX distributions, compilers, and similar infrastructure.

If a required system-level tool is unavailable or unusable, record the
limitation clearly in the Project STATE.md/LOG.md and continue with useful work
that does not require it. Do not work around the limitation by creating a
private installation.

Project-level dependencies are different. You may install ordinary R or Python
packages in the existing user/project environment when needed for the research,
provided doing so does not require administrative privileges or replacing the
system runtime.
Prefer primary sources and scholarly sources when appropriate.
Record important sources in the project.

### Temporary infrastructure limitation

At the moment, Quarto is not installed. When Quarto is required or recommended, substitute Markdown instead. Also, we have only a few hundred megabytes of disk space before we hit a hard quota. Dr. Jones address these issues in the future.
