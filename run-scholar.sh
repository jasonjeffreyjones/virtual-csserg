#!/usr/bin/env bash
set -euo pipefail

# Locate Virtual CSSERG from this script rather than assuming a username,
# home directory, or installation path. Preserve an explicit PATH prefix so the
# runner can be exercised with harmless fake commands in an isolated test.
REPO="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
LOG_DIR="$REPO/logs"
export PATH="${PATH:-}:$HOME/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

if [[ $# -ne 2 ]]; then
    echo "Usage: $0 SCHOLAR_SLUG PROJECT_SLUG" >&2
    exit 2
fi

SCHOLAR_SLUG="$1"
PROJECT_SLUG="$2"
LOG_FILE="$LOG_DIR/${SCHOLAR_SLUG}_${PROJECT_SLUG}.log"

for cmd in git flock codex python3 bash; do
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
    echo "Another Scholar iteration is already running." >&2
    exit 1
}

# Never absorb changes left by a person or an earlier failed iteration. Treat
# inability to inspect the worktree as unsafe rather than as an empty result.
if ! WORKTREE_STATUS="$(git status --porcelain --untracked-files=all)"; then
    echo "Refusing to start: git could not inspect the repository working tree." >&2
    exit 3
fi
if [[ -n "$WORKTREE_STATUS" ]]; then
    echo "Refusing to start: the repository working tree is not clean." >&2
    echo "Review and resolve existing changes before running a Scholar." >&2
    exit 3
fi

# Start from the current shared repository state, then validate this invocation.
git pull --ff-only origin main
SCHOLAR_NAME="$(python3 python/scholar_roster.py --name-for "$SCHOLAR_SLUG")"
PROJECT_TITLE="$(python3 python/project_registry.py --active-title "$PROJECT_SLUG")"

# Describe the actual host environment at the beginning of every iteration.
PREFLIGHT="$("$REPO/scripts/preflight.sh")"

PROMPT=$(cat <<PROMPT_EOF
Hello! Your name is $SCHOLAR_NAME. You are a Scholar within Virtual CSSERG.
Your assigned Project for this iteration is $PROJECT_TITLE, whose permanent
slug is $PROJECT_SLUG. This invocation assigns you to this Project for this
iteration only; Scholars do not have durable Project assignments.

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
5. Read projects/$PROJECT_SLUG/PROJECT.md, STATE.md, and DIALOG.md.
6. Read every dialog record linked under active PI guidance or unresolved questions, the three newest iteration records, your own newest record for this Project if it is not among those three, and any older record cited as necessary context.
7. Complete one useful iteration of work on $PROJECT_TITLE.
8. Update STATE.md, create exactly one timestamped record under dialog/iterations, add it to the top of the bounded DIALOG.md landing index, and update the appropriate yearly index. Use the iteration's UTC start time and your permanent Scholar slug in the filename. Refuse to overwrite an existing iteration file.
9. Never alter Scholar-authored content in an earlier iteration record. Never create, alter, or delete PI-authored Markdown blockquotes.
10. Run the relevant Project checks and the Version 1 verifier. End the iteration with a nonzero status if required validation does not pass.
11. End the iteration.
PROMPT_EOF
)

abort_iteration() {
    local exit_status="$1"
    local reason="$2"
    {
        echo "$(date -u '+%Y-%m-%d %H:%M:%S UTC') ITERATION ABORTED: $SCHOLAR_SLUG / $PROJECT_SLUG"
        echo "$reason"
        echo "Working-tree changes were NOT committed, pushed, or deployed."
    } | tee -a "$LOG_FILE" >&2
    exit "$exit_status"
}

echo "$(date -u '+%Y-%m-%d %H:%M:%S UTC') ITERATION START: $SCHOLAR_SLUG / $PROJECT_SLUG" \
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
    abort_iteration "$CODEX_STATUS" \
        "Scholar exited with status $CODEX_STATUS or hit a resource limit."
fi

# The runner, rather than the Scholar's prose, decides whether publication is safe.
set +e
{
    git diff --quiet HEAD -- run-scholar.sh &&
    python3 python/scholar_roster.py &&
    python3 python/project_registry.py --active-title "$PROJECT_SLUG" &&
    python3 -m unittest discover -s projects/vcsserg-repo-v1/tests -q &&
    python3 projects/vcsserg-repo-v1/verify_v1.py &&
    git diff --check &&
    bash -n run-scholar.sh
} >> "$LOG_FILE" 2>&1
VALIDATION_STATUS=$?
set -e

if [[ $VALIDATION_STATUS -ne 0 ]]; then
    abort_iteration "$VALIDATION_STATUS" \
        "Independent post-iteration validation failed with status $VALIDATION_STATUS."
fi

git add -A

if git diff --cached --quiet; then
    echo "Scholar completed iteration with no repository changes."
else
    git commit -m "Scholar $SCHOLAR_NAME: iterate on $PROJECT_TITLE"
fi

git pull --rebase origin main
git push origin main
python3 python/vcsserg_deploy.py

echo "$(date -u '+%Y-%m-%d %H:%M:%S UTC') ITERATION COMPLETE: $SCHOLAR_SLUG / $PROJECT_SLUG" \
    >> "$LOG_FILE"
