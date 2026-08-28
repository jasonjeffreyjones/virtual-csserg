#!/usr/bin/python3

import os
from pathlib import Path
from pathlib import PurePosixPath
import subprocess
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ENV_PATH = PROJECT_ROOT / ".env"


def load_env_file():
    env_path_override = os.environ.get("VCSSERG_ENV_FILE")
    if env_path_override:
        candidate_paths = [Path(env_path_override)]
    else:
        candidate_paths = [DEFAULT_ENV_PATH]

    env_path = next((path for path in candidate_paths if path.is_file()), None)
    if env_path is None:
        raise FileNotFoundError(
            "Environment file not found. Checked: "
            + ", ".join(str(path) for path in candidate_paths)
        )

    with open(env_path, "r", encoding="utf-8") as file:
        for raw_line in file:
            line = raw_line.strip()
            if line == "" or line.startswith("#"):
                continue

            key, separator, value = line.partition("=")
            if separator == "":
                continue

            key = key.strip()
            value = value.strip()
            if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
                value = value[1:-1]
            os.environ[key] = value


def get_required_env_var(name):
    value = os.environ.get(name)
    if value in {None, ""}:
        raise ValueError(f"Missing required environment variable: {name}")
    return value


def get_ssh_port():
    raw_port = get_required_env_var("VCSSERG_DEPLOY_SSH_PORT")
    try:
        port = int(raw_port)
    except ValueError:
        raise ValueError("VCSSERG_DEPLOY_SSH_PORT must be an integer") from None
    if not 1 <= port <= 65535:
        raise ValueError("VCSSERG_DEPLOY_SSH_PORT must be between 1 and 65535")
    return str(port)


def get_remote_path():
    raw_path = get_required_env_var("VCSSERG_DEPLOY_REMOTE_PATH")
    normalized_path = raw_path.rstrip("/")
    if PurePosixPath(normalized_path).name != "virtual-csserg":
        raise ValueError(
            "VCSSERG_DEPLOY_REMOTE_PATH must end with a virtual-csserg directory"
        )
    return normalized_path + "/"


def deploy():
    source_path = str(PROJECT_ROOT / "website") + "/"
    destination = (
        f'{get_required_env_var("VCSSERG_DEPLOY_SSH_USER")}@'
        f'{get_required_env_var("VCSSERG_DEPLOY_SSH_HOST")}:'
        f'{get_remote_path()}'
    )
    command = [
        "rsync",
        "-avz",
        "--delete-delay",
        "-e",
        f"ssh -p {get_ssh_port()}",
        source_path,
        destination,
    ]

    try:
        subprocess.run(command, check=True, capture_output=True, text=True)
    except FileNotFoundError:
        print("Deployment failed: rsync is not installed.", file=sys.stderr)
        raise SystemExit(127) from None
    except subprocess.CalledProcessError as error:
        print("Deployment failed during rsync.", file=sys.stderr)
        raise SystemExit(error.returncode or 1) from None

    print("Deployment completed successfully.")


def main():
    load_env_file()
    deploy()


if __name__ == "__main__":
    main()
