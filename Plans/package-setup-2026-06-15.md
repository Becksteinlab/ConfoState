# Package Setup and Data Foundation Plan

**Date:** 2026-06-15  
**Status:** Completed — Phase 1 (Data Foundation) Infrastructure

## Goal

Establish a Python package-style workflow for ConfoState with CSV-based data loading and an `input/` directory for PDB structures.

## Approach

### 1. Package Structure
- Created `confostate/` as main package with `__init__.py`
- Added `confostate/data/` subpackage for data handling
- Implemented `confostate/data/loader.py` with CSV utilities:
  - `load_annotations(csv_path, family=None)` — Load annotated dataset with optional filtering
  - `load_from_input_dir(input_dir)` — Scan input directory for PDB files

### 2. Annotated Dataset
- Created `data/annotations/leu_t_transporters.csv` with 25 LeuT structures
- Columns: pdb_id, family, conformation, reference, experimental_method, resolution_angstrom, year
- Conformational states based on alternating access model:
  - IF_open (9 structures)
  - OF_open (7 structures)
  - Occluded (6 structures)
  - Intermediate (3 structures)
- Labels derived from literature (Yamashita, Forrest, Coleman, etc.)

### 3. Input Directory
- Created `input/` directory as central location for PDB files
- Instructions in `input/README.md` for downloading structures
- Works seamlessly with existing `scripts/download_structures.py`

### 4. Package Configuration
- Created `pyproject.toml` with:
  - Package metadata (name, version, description)
  - Dependencies: pandas, numpy
  - Dev dependencies: pytest, black, flake8
  - Package data includes annotations

### 5. Example and Documentation
- Created `examples/load_data.py` demonstrating package usage
- Added `PACKAGE_STRUCTURE.md` documenting the layout and quick start

## Key Decisions

| Decision | Rationale |
|----------|-----------|
| CSV format for annotations | Simple, version-controllable, human-readable |
| `input/` vs `data/structures/` | Clearer separation: curated data vs. downloaded structures |
| Pandas for loading | Standard, integrates well with ML workflows |
| Editable install (`pip install -e .`) | Enables rapid development without reinstalling |

## What's Ready

✅ Python package infrastructure  
✅ CSV data loader with validation  
✅ 25 annotated LeuT transporters  
✅ Input directory setup  
✅ Example usage script  

## Next Steps

1. Document `scripts/download_structures.py` at `docs/scripts/download_structures.md`
2. Download structures: `python scripts/download_structures.py --codes-file data/protein_families/LeuT_transporters.txt --output-dir input`
3. Phase 2: Implement feature extraction modules in `confostate/features/`
4. Phase 3: Build ML classifier in `confostate/models/`
