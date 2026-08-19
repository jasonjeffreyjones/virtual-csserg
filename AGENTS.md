# AGENTS.md

## Project purpose

Virtual CSSERG is a group of AI agent scholars committed to the efficient search for truth united by common computational social science methodologies. VSSERG is led by the human
[Dr. Jason Jeffrey Jones](https://jasonjones.ninja/virtual-csserg/)

Virtual CSSERG frequently publishes results as updates to the static website in `website/`. A Python deployment script in `python/` deploys to https://jasonjones.ninja/virtual-csserg/.

  ## Important files

  - `website/index.html`: Website entry point.
  - `python/vcsserg_deploy.py`: Deploys `website/` using rsync over SSH.
  - `.env`: Contains private deployment configuration.

  ## Safety

  - Never read, print, modify, commit, or expose `.env`.
  - Do not put credentials, hostnames, private paths, or SSH keys in committed files.
  - Treat this repository as public.

  ## Development

  - Keep the website deployable as static files.
  - Run relevant checks after making code changes.
  - Do not add production dependencies without explaining why.
