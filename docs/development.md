# Development guide

ConfoState uses a fixed Python style so reviews stay focused on science and
design. Full contribution notes (including PRs) are in
[CONTRIBUTING.md](https://github.com/Becksteinlab/ConfoState/blob/main/CONTRIBUTING.md)
at the repository root; this page summarizes style and tooling.

## Style

| Tool | Role | Project setting |
|------|------|-----------------|
| **Ruff** | Linter and formatter | Line length **79** (PEP 8) |

All settings are in `pyproject.toml` (`[tool.ruff*]`).

```bash
mamba activate confostate
pip install -e ".[lint]"

ruff format .
ruff check --fix .
ruff check .
ruff format --check --diff .
```

## Pre-commit

Install hooks once so every commit is formatted and linted:

```bash
pip install -e ".[lint]"
pre-commit install
pre-commit run --all-files   # optional: check the whole tree
```

See `.pre-commit-config.yaml`. CI runs Ruff on every push and pull request to
`main` / `develop`.
