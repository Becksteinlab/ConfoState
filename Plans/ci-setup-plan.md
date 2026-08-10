# CI / CD Setup Plan

**Date:** 2026-07-27  
**Branch:** `ci`  
**Status:** Implemented

## Goal

Adapt the MIT-licensed `.github` workflows copied from [Becksteinlab/multibind](https://github.com/Becksteinlab/multibind) for ConfoState, covering tests, PyPI deployment, and Sphinx docs published to `gh-pages`.

## Approach

### Tests (`.github/workflows/tests.yml`)
- Trigger on push/PR to `main` and `develop`, plus a nightly cron
- Matrix: Python 3.9–3.14 (matches `requires-python` and the workplan)
- Install with `pip install -e ".[test]"` (setuptools project; no Poetry)
- Run `pytest` with coverage for `confostate`; upload to Codecov (fails PRs if upload errors)

### Deployment (`.github/workflows/deploy.yaml`)
- Tag push → build, test the wheel, publish to TestPyPI, then re-test from TestPyPI
- GitHub Release published → same path for PyPI
- Trusted publishing (`id-token: write`); gated on `Becksteinlab/ConfoState`
- Kept composite action `wait-for-pypi-version` unchanged (package-agnostic)
- Build/test Python pinned to 3.12

### Docs (`.github/workflows/docs.yml`) — new
- Build Sphinx HTML on push/PR to `main`
- PRs: upload HTML artifact for review
- Push to `main`: deploy with `peaceiris/actions-gh-pages` to the `gh-pages` branch
- Docs sources: Markdown via MyST (`docs/`), Furo theme, autodoc for the public API

### Lint (`.github/workflows/lint.yml`)
- Ruff check + format `--check` with **line-length 79** (PEP 8)
- All style settings in `pyproject.toml` (`[tool.ruff*]`)
- Local: `.pre-commit-config.yaml` + `CONTRIBUTING.md` / `docs/development.md`

### Supporting package changes
- `pyproject.toml`: `test`, `docs`, `lint`, and `dev` extras; pytest/coverage/ruff config
- Minimal `tests/test_package.py` so CI is green before the full suite lands
- `.gitignore`: coverage artifacts and `docs/_build/`

## Key trade-offs

| Decision | Rationale |
|----------|-----------|
| pip/setuptools instead of Poetry | Matches existing ConfoState packaging |
| Separate `docs.yml` (not in multibind) | Workplan asks for gh-pages; multibind uses Read the Docs |
| Codecov `fail_ci_if_error` on PRs only | Match multibind; catch missing token/upload issues on PRs without flaking nightly runs |
| Ruff instead of Black/Flake8 | One tool; all style settings in `pyproject.toml` |

## Local verification

Use the project mamba env (do not create ad-hoc venvs):

```bash
mamba activate confostate
pip install -e ".[dev]"
pytest -v
ruff check .
ruff format --check .
cd docs && make html
```

**PR CI note:** GitHub Actions on pull requests checks out a *merge* of the PR
branch into the base (`main`). Lint therefore sees files that exist on `main`
even if they are absent from the PR branch tip alone. Keep `ci` up to date with
`main` (or run ruff on the merge tree) before relying on a local green check.

Verified 2026-07-27: 3 tests passed; Sphinx HTML build succeeded.

## Follow-ups (manual / later)

1. Enable GitHub Pages source = **gh-pages** branch (or Actions) in repo settings
2. Configure TestPyPI/PyPI trusted publishing for `confostate`
3. Ensure `CODECOV_TOKEN` secret is set (required for Codecov uploads; PR CI fails without it)
4. Branch protection on `main` (no force-push) once CI is required
5. Expand the test suite as modules land (Person 6 workplan)
