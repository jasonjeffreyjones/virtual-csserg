#!/usr/bin/env bash

# Virtual CSSERG host preflight
# Read-only inventory of hardware, resources, and useful software.
# This script should never modify the host.

set -u

section() {
    printf '\n=== %s ===\n' "$1"
}

show_command() {
    local label="$1"
    local command_name="$2"
    shift 2

    if command -v "$command_name" >/dev/null 2>&1; then
        printf '%-12s %s\n' "$label" "$("$@" 2>/dev/null | head -n 1)"
    else
        printf '%-12s %s\n' "$label" "NOT INSTALLED"
    fi
}

section "HOST"
printf 'Hostname:     %s\n' "$(hostname)"
printf 'OS:           %s\n' "$(
    . /etc/os-release 2>/dev/null
    printf '%s' "${PRETTY_NAME:-unknown}"
)"
printf 'Kernel:       %s\n' "$(uname -r)"
printf 'Architecture: %s\n' "$(uname -m)"

section "CPU"
printf 'Logical CPUs: %s\n' "$(nproc 2>/dev/null || echo unknown)"
if command -v lscpu >/dev/null 2>&1; then
    printf 'Model:        %s\n' "$(lscpu | sed -n 's/^Model name:[[:space:]]*//p' | head -n 1)"
fi

section "MEMORY"
free -h

section "DISK"
df -h /

section "SOFTWARE"
show_command "Codex:"    codex    codex --version
show_command "Quarto:"   quarto   quarto --version
show_command "Python:"   python   python --version
show_command "Python3:"  python3  python3 --version
show_command "R:"        R        R --version
show_command "Git:"      git      git --version
show_command "rsync:"    rsync    rsync --version
show_command "Pandoc:"   pandoc   pandoc --version
show_command "Node:"     node     node --version
show_command "npm:"      npm      npm --version
show_command "curl:"     curl     curl --version
show_command "wget:"     wget     wget --version

section "UTILITIES"
for cmd in flock systemd-run systemctl make gcc unzip zip tar; do
    if command -v "$cmd" >/dev/null 2>&1; then
        printf '%-12s %s\n' "$cmd:" "$(command -v "$cmd")"
    else
        printf '%-12s %s\n' "$cmd:" "NOT INSTALLED"
    fi
done

section "REPOSITORY"
REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || true)"
if [[ -n "$REPO_ROOT" ]]; then
    printf 'Root:         %s\n' "$REPO_ROOT"
    printf 'Branch:       %s\n' "$(git -C "$REPO_ROOT" branch --show-current)"
else
    printf 'Git repo:     not detected\n'
fi

section "PREFLIGHT COMPLETE"
printf 'UTC time:     %s\n' "$(date -u '+%Y-%m-%d %H:%M:%S UTC')"
