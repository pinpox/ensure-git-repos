# ensure-git-repos

This is a simple Python script to automate the initialization and remote
configuration of multiple Git repositories based on a YAML configuration file.
It was created to set up developer workstations quickly with the projects you
want on them to start working.

## 🧩 Features

- Creates local directories if they don't exist
- Initializes Git repositories (if not already present)
- Adds or updates Git remotes
- YAML-based configuration

---

## 📦 Requirements

If you're not using Nix, you'll need:
- Python 3.7+
- [`GitPython`](https://pypi.org/project/GitPython/)
- [`PyYAML`](https://pypi.org/project/PyYAML/)

Or just use the built-in Nix development environment.

---

## 🛠 Usage

### 1. Create your config YAML

```yaml
# repos.yaml
repositories:
  - local_path: ~/projects/my-repo
    remotes:
      origin: git@github.com:username/my-repo.git

  - local_path: ~/projects/another-repo
    remotes:
      origin: git@github.com:username/another-repo.git
      upstream: git@github.com:someone-else/another-repo.git
```

### 2. Run the script

```bash
./script.py repos.yaml
```

---

## 🧪 Usage with Nix

You can use the built-in Nix flake to get an isolated Python dev shell with all
dependencies. It also includes a package for easy installation.

```bash
nix develop
```

