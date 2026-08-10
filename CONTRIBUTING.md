# Contributing to ConfoState

Thanks for contributing. This document covers the coding style we enforce in CI
and how to set up local checks.

## Development setup

```bash
mamba activate confostate
pip install -e ".[dev]"
```

The `dev` extra includes test, docs, and lint tools (Ruff, pre-commit).

## Code style

We follow [PEP 8](https://peps.python.org/pep-0008/) with these project rules:

| Rule | Setting |
|------|---------|
| Linter & formatter | [Ruff](https://docs.astral.sh/ruff/) |
| Line length | **79** characters |

All style configuration lives in **`pyproject.toml`** under `[tool.ruff]`,
`[tool.ruff.lint]`, and `[tool.ruff.format]`. Do not duplicate settings in
other config files.

```bash
# Format the tree
ruff format .

# Lint (auto-fix safe issues)
ruff check --fix .

# Check without writing (same as CI)
ruff check .
ruff format --check --diff .
```

## Pre-commit (recommended)

[pre-commit](https://pre-commit.com/) runs Ruff on staged files before each
commit so style issues never reach CI.

```bash
pip install pre-commit   # or: pip install -e ".[lint]"
pre-commit install
```

After that, `git commit` formats and lints automatically. To run on the whole
repo:

```bash
pre-commit run --all-files
```

Hooks are defined in `.pre-commit-config.yaml` (they read settings from
`pyproject.toml`).

## Tests and docs

```bash
pytest -v
cd docs && make html
```

CI runs tests, lint, docs, and (on tags/releases) packaging. See
`Plans/ci-setup-plan.md` for workflow details.

## Pull requests

1. Open a branch from `main` (or `develop` when that branch is in use).
2. Keep changes focused; match existing naming and module layout.
3. Ensure `ruff check .`, `ruff format --check .`, and `pytest` pass locally
   (or rely on pre-commit + CI).
4. Update docs under `docs/` when behavior or public APIs change.
