#!/usr/bin/env bash
set -euo pipefail

# Locate Virtual CSSERG from this script rather than assuming a username,
# home directory, or installation path.
REPO="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
LOG_DIR="$REPO/logs"

# Give scheduled/non-interactive runs a useful, portable baseline PATH.
export PATH="$HOME/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:${PATH:-}"

if [[ $# -ne 2 ]]; then
    echo "Usage: $0 SCHOLAR_NAME PROJECT_NAME" >&2
    exit 2
fi

SCHOLAR_NAME="$1"
PROJECT_NAME="$2"
LOG_FILE="$LOG_DIR/${SCHOLAR_NAME}_${PROJECT_NAME}.log"

for cmd in git flock codex python3; do
    if ! command -v "$cmd" >/dev/null 2>&1; then
        echo "Required command is not installed: $cmd" >&2
        exit 127
    fi
done

cd "$REPO"
mkdir -p "$LOG_DIR"

# Only one Scholar may work on this host at a time.
exec 9>/tmp/virtual-csserg.lock
flock -n 9 || {
    echo "Another Scholar iteration is already running."
    exit 1
}

# Start from the current shared repository state.
git pull --ff-only origin main

# Describe the actual host environment at the beginning of every iteration.
PREFLIGHT="$("$REPO/scripts/preflight.sh")"

PROMPT=$(cat <<PROMPT_EOF
Hello! Your name is $SCHOLAR_NAME. You are a Scholar within Virtual CSSERG.
Your assigned Project for this iteration is $PROJECT_NAME.

Here is the Virtual CSSERG preflight report for the host on which you are
working during this iteration:

$PREFLIGHT

This iteration may be subject to CPU, memory, and runtime limits enforced
externally by the host. Plan and scope your work conservatively. Do not attempt
to circumvent or change host resource limits.

Follow these steps:
  1. Read AGENTS.md.
  2. Read README.md.
  3. Read RESEARCHER-ORIENTATION.md.
  4. Find your own subdirectory within website/scholars/, and read all files within that subdirectory.
  5. Read the assigned Project's PROJECT.md, STATE.md, and DIALOG.md.
  6. Determine which dialog protocol applies:
     a. If DIALOG.md is a bounded landing index and dialog/iterations exists, read every record linked under active PI guidance or unresolved questions, the three newest iteration records, your own newest
     record for this Project if it is not among those three, and any older record cited as necessary context.
     b. If the new structure does not exist, read the complete legacy DIALOG.md. If this is the coordinated VCSSERG v1 migration canary, read projects/vcsserg-repo-v1/DIALOG-MIGRATION.md and perform the
     migration across _template and every existing Project as one all-or-nothing change. For any other legacy Project, follow the legacy append-only procedure and do not partially migrate the repository.
  7. Complete one useful iteration of work on the assigned Project.
  8. At the end of an iteration using the migrated protocol, update STATE.md, create exactly one timestamped record under dialog/iterations, add it to the top of the bounded DIALOG.md landing index, and update
  the appropriate yearly index. Use the iteration's UTC start time and the Scholar's permanent slug in the filename. Refuse to overwrite an existing iteration file.
  9. At the end of an iteration still using the legacy protocol, update STATE.md and append the iteration record to DIALOG.md.
  10. Never alter Scholar-authored content in an earlier iteration record. Never create, alter, or delete PI-authored Markdown blockquotes.
  11. Run the relevant Project checks and the Version 1 verifier. If migration or validation fails, leave the legacy protocol operative across the repository and report the failure; do not leave or publish a
  mixed protocol.
  12. End the iteration.
PROMPT_EOF
)

echo "$(date -u '+%Y-%m-%d %H:%M:%S UTC') ITERATION START: $SCHOLAR_NAME / $PROJECT_NAME" \
    >> "$LOG_FILE"
set +e

    codex exec \
        -m gpt-5.6-sol \
        -c 'model_reasoning_effort="xhigh"' \
        --sandbox workspace-write \
        -c 'web_search="live"' \
        -c 'sandbox_workspace_write.network_access=true' \
        "$PROMPT" \
    >> "$LOG_FILE" 2>&1

CODEX_STATUS=$?

set -e

if [[ $CODEX_STATUS -ne 0 ]]; then
    {
        echo "$(date -u '+%Y-%m-%d %H:%M:%S UTC') ITERATION ABORTED: $SCHOLAR_NAME / $PROJECT_NAME"
        echo "Scholar exited with status $CODEX_STATUS or hit a resource limit."
        echo "Partial working-tree changes were NOT committed, pushed, or deployed."
    } | tee -a "$LOG_FILE" >&2

    exit "$CODEX_STATUS"
fi

git add -A

if git diff --cached --quiet; then
    echo "Scholar completed iteration with no repository changes."
else
    git commit -m "Scholar $SCHOLAR_NAME: iterate on $PROJECT_NAME"
fi

git pull --rebase origin main
git push origin main

python3 python/vcsserg_deploy.py

echo "$(date -u '+%Y-%m-%d %H:%M:%S UTC') ITERATION COMPLETE: $SCHOLAR_NAME / $PROJECT_NAME" \
    >> "$LOG_FILE"
