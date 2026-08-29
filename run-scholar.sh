#!/usr/bin/env bash
set -euo pipefail

SCHOLAR_NAME="$1"
PROJECT_NAME="$2"

REPO="/home/ec2-user/virtual-csserg"
LOG_DIR="$REPO/logs"

cd "$REPO"

mkdir -p "$LOG_DIR"

PROMPT=$(cat <<EOF
Hello! Your name is $SCHOLAR_NAME. You are a Scholar within Virtual CSSERG.
Your assigned Project for this iteration is $PROJECT_NAME.

Follow these steps:
1. Read AGENTS.md.
2. Read README.md.
3. Read RESEARCHER-ORIENTATION.md.
4. Find your own subdirectory within website/scholars/, and read all files within that subdirectory.
5. Read the Project files for $PROJECT_NAME, including PROJECT.md, PI.md, STATE.md, and LOG.md.
6. Complete one iteration of work on $PROJECT_NAME.
7. Update the Project as required by RESEARCHER-ORIENTATION.md.
8. End the iteration.
EOF
)

exec 9>/tmp/virtual-csserg.lock
flock -n 9 || {
    echo "Another Scholar iteration is already running."
    exit 1
}

git pull --ff-only origin main

codex exec \
    -c 'web_search="live"' \
    -c 'sandbox_workspace_write.network_access=true' \
    "$PROMPT" \
    >> "$LOG_DIR/${SCHOLAR_NAME}_${PROJECT_NAME}.log" 2>&1

git add -A
git commit -m "Scholar $SCHOLAR_NAME: iterate on $PROJECT_NAME"

git pull --rebase origin main
git push origin main

python3 python/vcsserg_deploy.py

echo "$(date -u '+%Y-%m-%d %H:%M:%S UTC') ITERATION COMPLETE: $SCHOLAR_NAME / $PROJECT_NAME" \
    >> "$LOG_DIR/${SCHOLAR_NAME}_${PROJECT_NAME}.log"
