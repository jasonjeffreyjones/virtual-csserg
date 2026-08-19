#!/usr/bin/python3

import argparse
import datetime
import json
import os
from pathlib import Path
import re
import subprocess

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

	with open(env_path, "r") as file:
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


def deploy():
	rsync_ssh_command = f'ssh -p {get_required_env_var("VCSSERG_DEPLOY_SSH_PORT")}'
	source_path = str(PROJECT_ROOT / "website") + "/"
	destination = (
		f'{get_required_env_var("VCSSERG_DEPLOY_SSH_USER")}@'
		f'{get_required_env_var("VCSSERG_DEPLOY_SSH_HOST")}:'
		f'{get_required_env_var("VCSSERG_DEPLOY_REMOTE_PATH")}'
	)
	command = [f'rsync -avz -e "{rsync_ssh_command}" {source_path} {destination}']
	try:
		result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
		print(f'rsynced to {get_required_env_var("VCSSERG_DEPLOY_SSH_HOST")}')
	except subprocess.CalledProcessError as e:
		print("rsync failed with error:", e.stderr.strip())


def main():
	load_env_file()
	deploy()
	

if __name__ == "__main__":
        main()
