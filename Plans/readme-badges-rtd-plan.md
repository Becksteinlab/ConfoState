# README badges and Read the Docs config

**Date:** 2026-08-10  
**Status:** Implemented

## Goal

Add status badges to the README and a Read the Docs configuration so docs can build on RTD.

## Approach

- README badges (multibind-style):
  - GitHub Actions: `tests.yml` workflow status
  - Read the Docs: `confostate` project / `latest`
  - Codecov: coverage for `Becksteinlab/ConfoState` on `main`
- `.readthedocs.yaml` (v2): Ubuntu 24.04, Python 3.12, Sphinx via `docs/conf.py`, `pip install .[docs]`

## Trade-offs

| Decision | Rationale |
|----------|-----------|
| Single Tests GHA badge | Primary CI signal; lint/docs workflows stay in Actions UI |
| RTD slug `confostate` | Matches package name; project must still be linked on RTD |
| Install with `docs` extra | Reuses `pyproject.toml` extras; no separate `docs/requirements.txt` |
| Keep existing `docs.yml` → gh-pages | RTD config enables RTD without removing GitHub Pages deploy |

## Follow-ups (manual)

1. Import/link the GitHub repo on [Read the Docs](https://readthedocs.org/) as project `confostate`
2. Confirm Codecov is connected for the org/repo (badge already works once coverage uploads)
