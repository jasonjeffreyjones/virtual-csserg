#!/usr/bin/env bash
set -euo pipefail

# Locate Virtual CSSERG from this script rather than assuming a username,
# home directory, or installation path.
REPO="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
LOG_DIR="$REPO/logs"

# Host-specific resource configuration lives outside the repository.
HOST_CONFIG="${VCSSERG_HOST_CONFIG:-$HOME/.config/virtual-csserg/host.env}"

# Give scheduled/non-interactive runs a useful, portable baseline PATH.
export PATH="$HOME/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:${PATH:-}"

if [[ $# -ne 2 ]]; then
    echo "Usage: $0 SCHOLAR_NAME PROJECT_NAME" >&2
    exit 2
fi

SCHOLAR_NAME="$1"
PROJECT_NAME="$2"
LOG_FILE="$LOG_DIR/${SCHOLAR_NAME}_${PROJECT_NAME}.log"

# Fail closed if this host has not been given explicit Scholar limits.
if [[ ! -r "$HOST_CONFIG" ]]; then
    echo "Host configuration not found: $HOST_CONFIG" >&2
    echo "Refusing to run a Scholar without explicit resource limits." >&2
    exit 2
fi

# shellcheck disable=SC1090
source "$HOST_CONFIG"

MAX_CPUS="${VCSSERG_MAX_CPUS:-}"
WALL_TIME="${VCSSERG_WALL_TIME:-}"
MEMORY_MAX="${VCSSERG_MEMORY_MAX:-}"

if [[ -z "$MAX_CPUS" || -z "$WALL_TIME" || -z "$MEMORY_MAX" ]]; then
    echo "Host configuration must define VCSSERG_MAX_CPUS, VCSSERG_WALL_TIME, and VCSSERG_MEMORY_MAX." >&2
    exit 2
fi

if ! [[ "$MAX_CPUS" =~ ^[1-9][0-9]*$ ]]; then
    echo "VCSSERG_MAX_CPUS must be a positive integer." >&2
    exit 2
fi

HOST_CPUS="$(nproc)"
if (( MAX_CPUS > HOST_CPUS )); then
    echo "VCSSERG_MAX_CPUS=$MAX_CPUS exceeds host CPU count $HOST_CPUS." >&2
    exit 2
fi

if ! [[ "$WALL_TIME" =~ ^[1-9][0-9]*[smhd]$ ]]; then
    echo "VCSSERG_WALL_TIME must look like 30m, 1h, or 2h." >&2
    exit 2
fi

if ! [[ "$MEMORY_MAX" =~ ^[1-9][0-9]*(K|M|G|T)$ ]]; then
    echo "VCSSERG_MEMORY_MAX must look like 2500M or 4G." >&2
    exit 2
fi

CPU_QUOTA="$((MAX_CPUS * 100))%"

for cmd in git flock systemd-run systemctl codex python3; do
    if ! command -v "$cmd" >/dev/null 2>&1; then
        echo "Required command is not installed: $cmd" >&2
        exit 127
    fi
done

# Resource enforcement depends on the per-user systemd manager.
if ! systemctl --user show-environment >/dev/null 2>&1; then
    echo "The user systemd manager is unavailable." >&2
    echo "Refusing to run a Scholar without resource enforcement." >&2
    exit 1
fi

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

This iteration also has hard resource limits enforced by the host:

Maximum CPU capacity: $MAX_CPUS logical CPU(s)
Maximum memory: $MEMORY_MAX
Maximum wall time: $WALL_TIME
Scholar swap usage: disabled

Plan and scope your work accordingly. Do not attempt to circumvent or change
these resource limits.

Follow these steps:
1. Read AGENTS.md.
2. Read README.md.
3. Read RESEARCHER-ORIENTATION.md.
4. Find your own subdirectory within website/scholars/, and read all files within that subdirectory.
5. Read the Project files for $PROJECT_NAME, including PROJECT.md, STATE.md, and DIALOG.md.
6. Complete one iteration of work on $PROJECT_NAME.
7. Update the Project as required by RESEARCHER-ORIENTATION.md.
8. End the iteration.
PROMPT_EOF
)

echo "$(date -u '+%Y-%m-%d %H:%M:%S UTC') ITERATION START: $SCHOLAR_NAME / $PROJECT_NAME" \
    >> "$LOG_FILE"

echo "Resource limits: CPUs=$MAX_CPUS Memory=$MEMORY_MAX WallTime=$WALL_TIME Swap=0" \
    >> "$LOG_FILE"

# Run the entire Scholar process tree inside one cgroup-enforced systemd scope.
#
# CPUQuota: MAX_CPUS=1 -> 100%, MAX_CPUS=4 -> 400%, etc.
# MemoryMax: hard memory ceiling for the complete Scholar process tree.
# MemorySwapMax=0: Scholar work cannot consume host swap.
# RuntimeMaxSec: hard wall-time ceiling for the complete scope.
# OOMPolicy=kill: memory exhaustion terminates the scope rather than leaving
#                 a partially surviving process tree.
set +e

systemd-run --user --scope --quiet \
    -p "CPUQuota=$CPU_QUOTA" \
    -p "MemoryMax=$MEMORY_MAX" \
    -p "MemorySwapMax=0" \
    -p "RuntimeMaxSec=$WALL_TIME" \
    -p "KillMode=control-group" \
    -p "OOMPolicy=kill" \
    codex exec \
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
