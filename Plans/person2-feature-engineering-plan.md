# Person 2 Feature Engineering Plan

**Date:** 2026-07-13  
**Status:** Completed  
**Assignee:** Amru (Person 2A)

## Goal

Implement Phase 2 feature extraction for ConfoState: structural descriptors from PDB
files, unified `extract_features()` API, tests, and example feature vectors for 25
LeuT transporters.

## Approach

### Modules implemented

| Module | File | Features |
|--------|------|----------|
| Cavity | `confostate/features/cavity.py` | `cavity_volume`, `cavity_accessibility_in/out` |
| Domains | `confostate/features/domains.py` | TM helix pairwise distances and angles |
| RMSD | `confostate/features/rmsd.py` | RMSD to 4 reference structures per state |
| Orientation | `confostate/features/orientation.py` | OPM tilt/rotation/depth (+ computed fallback) |
| Shared | `confostate/features/_structure.py` | PDB parsing, Kabsch RMSD, geometry helpers |

### API

- `extract_features(pdb_path)` — single structure
- `extract_features_batch(pdb_paths, annotations_df)` — batch → DataFrame
- `scripts/extract_feature_vectors.py` — CLI for all 25 LeuT structures

### Data dependencies (Person 1)

Created `data/annotations/leu_t_transporters.csv` with literature-based state labels
and placeholder OPM columns. Person 1 can replace OPM values with authoritative
OPM API data without changing feature code.

## Key decisions

| Decision | Rationale |
|----------|-----------|
| Convex hull for cavity volume | Practical without Hollow (Python 2.7); documented as future upgrade |
| LeuT-specific residue/helix defs | Matches workplan scope; parameterized for future families |
| OPM from CSV with geometric fallback | Unblocks work when Person 1 OPM pipeline not merged |
| BioPython + SciPy | Standard structural biology stack |
| Reference RMSD on shared scaffold residues | Robust to missing loops/ligands |

## Deliverables

- `confostate/features/` (4 feature modules + `extract_features`)
- `tests/test_features.py` (6 tests, all passing)
- `docs/features.md`
- `data/features/leu_t_feature_vectors.csv` (25 structures)
- `scripts/extract_feature_vectors.py` + doc

## Not implemented (optional / future)

- `symmetry.py` — internal repeat symmetry (marked optional in workplan)
- Hollow-based pore detection — requires Python 3 rewrite of Hollow

## Coordination notes for team

- **Person 1:** Confirm binding-site residue list and OPM column names match curated CSV.
- **Person 3:** Use `data/features/leu_t_feature_vectors.csv` or call `extract_features()` directly.
- **Person 2B (Marshal):** API agreed: flat `dict[str, float]` from `extract_features()`.
