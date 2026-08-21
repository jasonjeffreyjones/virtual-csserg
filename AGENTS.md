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
