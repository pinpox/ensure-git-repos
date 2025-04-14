#!/usr/bin/env python3
import argparse
import yaml
from pathlib import Path
from git import Repo, InvalidGitRepositoryError

def setup_repo(local_path, remotes):
    local_path = Path(local_path).expanduser().resolve()

    if not local_path.exists():
        print(f"[INFO] Creating directory: {local_path}")
        local_path.mkdir(parents=True)

    repo = None
    if (local_path / ".git").exists():
        try:
            repo = Repo(local_path)
            print(f"[INFO] '{local_path}' is already a Git repository.")
        except InvalidGitRepositoryError:
            raise RuntimeError(f"[ERROR] '{local_path}' contains a .git folder but is not a valid Git repo.")
    else:
        if any(local_path.iterdir()):
            raise RuntimeError(f"[ERROR] Directory '{local_path}' is not empty and not a Git repository.")
        print(f"[INFO] Initializing Git repository in '{local_path}'")
        repo = Repo.init(local_path)

    # Add or update remotes
    existing_remotes = {remote.name: remote for remote in repo.remotes}
    for remote_name, remote_url in remotes.items():
        if remote_name in existing_remotes:
            current_url = next(existing_remotes[remote_name].urls, "")
            if current_url != remote_url:
                print(f"[INFO] Updating remote '{remote_name}' in '{local_path}'")
                repo.delete_remote(existing_remotes[remote_name])
                repo.create_remote(remote_name, remote_url)
            else:
                print(f"[INFO] Remote '{remote_name}' already set correctly in '{local_path}'")
        else:
            print(f"[INFO] Adding remote '{remote_name}' to '{local_path}'")
            repo.create_remote(remote_name, remote_url)

    print(f"[SUCCESS] Repository setup complete for '{local_path}'\n")

def load_config(yaml_path):
    with open(yaml_path, 'r') as f:
        return yaml.safe_load(f)

def main():
    parser = argparse.ArgumentParser(description="Set up multiple Git repositories with remotes from a YAML file.")
    parser.add_argument("config", help="Path to YAML config file")
    args = parser.parse_args()

    config = load_config(args.config)

    for repo_info in config.get("repositories", []):
        try:
            setup_repo(repo_info["local_path"], repo_info["remotes"])
        except Exception as e:
            print(e)

if __name__ == "__main__":
    main()
