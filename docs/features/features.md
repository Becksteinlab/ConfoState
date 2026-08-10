# Feature Extraction

ConfoState extracts numerical structural descriptors from membrane protein PDB
files using [MDAnalysis](https://www.mdanalysis.org/) for structure loading,
atom selections, center-of-mass, and RMSD superposition.

These features feed the ML classifier (Person 3) and explainability layer
(Person 4).

## Package layout

```
confostate/features/
├── __init__.py       # Public API re-exports only
├── pipeline.py       # extract_features() orchestration
├── _structure.py     # MDAnalysis Universe wrapper
├── cavity.py         # Binding-site volume & accessibility
├── domains.py        # TM helix distances & angles
├── rmsd.py           # RMSD to reference structures
└── orientation.py    # Membrane orientation features
```

`__init__.py` is intentionally thin — it re-exports the public API.
Orchestration lives in `pipeline.py`; each feature type has its own module.

## Quick start

```python
from confostate.features import extract_features

features = extract_features("input/3F3E.pdb", pdb_id="3F3E")
print(features["cavity_volume"])
print(features["rmsd_IF_open"])
```

Batch extraction for all annotated LeuT structures:

```bash
python scripts/download_structures.py \
    --codes-file data/protein_families/LeuT_transporters.txt \
    --output-dir input

python scripts/extract_feature_vectors.py
```

Output: `data/features/leu_t_feature_vectors.csv` (generated locally; gitignored)

(data-provenance)=
## Data provenance & current status (Person 3)

**Read this before training.** Not all columns in the feature table are equally trustworthy.

### What you get in `leu_t_feature_vectors.csv`

Each row = one PDB structure. Columns fall into three categories:

| Category | Columns | Status | Source |
|----------|---------|--------|--------|
| **Computed features (X)** | `cavity_*`, `domain_*`, `rmsd_*`, `opm_*`, `orientation_principal_axis_*` | **Live computation** | MDAnalysis + SciPy on PDB coordinates from RCSB |
| **Label (y)** | `conformation` | **Unverified stub** | Copied from annotations CSV; `conformation_status = literature_estimate` |
| **Metadata** | `pdb_id`, `file_path` | **Real** | PDB ID list + local file path |

### Annotations CSV (`data/annotations/leu_t_transporters.csv`)

This file is a **local working stub** (gitignored) until Person 1 verifies it.
See `data/annotations/README.md` for full column-level provenance.

| Field | Current status |
|-------|----------------|
| `conformation` | Literature estimate — **do not treat as ground truth** for publication |
| `resolution_angstrom`, `year`, `experimental_method` | Approximate — not fetched from RCSB API |
| `opm_*` | `N/A` / `opm_status = not_fetched` — orientation features are **computed from structure** instead |

### Safe to use now for pipeline development

- All numeric feature columns (`cavity_*`, `domain_*`, `rmsd_*`, etc.) — reproducible from PDBs
- `conformation` as a **provisional label** to wire up `datasets.py`, train/test splits, and model code

### Wait for Person 1 before trusting for results

- Conformation labels (your **y** variable)
- RCSB metadata (resolution, method, year)
- Real OPM orientation values (will replace computed `opm_*` when available)

### Regenerating data locally

Stub annotations and feature vectors are **not committed** (see `.gitignore`). To rebuild:

```bash
# 0. Copy annotation template (first time only)
cp data/annotations/leu_t_transporters.csv.example \
   data/annotations/leu_t_transporters.csv

# 1. PDB coordinates (from RCSB)
python scripts/download_structures.py \
    --codes-file data/protein_families/LeuT_transporters.txt \
    --output-dir input

# 2. Feature table (requires local annotations CSV from step 0)
python scripts/extract_feature_vectors.py
```

### Division of labour (reminder)

```
Person 1  →  labels & metadata (y)     annotations CSV
Person 2  →  features (X)              extract_features() / feature vectors CSV
Person 3  →  join X + y, train model   confostate/data/datasets.py, models/
```


### `extract_features(pdb_path, ...)`

Main entry point in `confostate.features`. Returns a flat `dict[str, float]`.

| Parameter | Description |
|---|---|
| `pdb_path` | Path to PDB file |
| `pdb_id` | Optional PDB ID (inferred from filename) |
| `family` | Protein family (`LeuT` supported) |
| `annotations_row` | Optional dict with OPM columns from annotations CSV |
| `reference_dir` | Directory with reference PDBs for RMSD |
| `include_rmsd` | Set `False` to skip RMSD if references unavailable |

### `extract_features_batch(pdb_paths, annotations_df=None)`

Returns a `pandas.DataFrame` with one row per structure.

## Feature modules

### Cavity (`confostate.features.cavity`)

Binding-site volume and solvent-accessibility proxies.

| Feature | Description |
|---|---|
| `cavity_volume` | Convex-hull volume (Å³) of binding-pocket atoms |
| `cavity_accessibility_in` | Fraction of nearby CA atoms on inward membrane side |
| `cavity_accessibility_out` | Fraction of nearby CA atoms on outward membrane side |

Binding-site residues for LeuT are defined in `LEUT_BINDING_SITE_RESIDUES`
(Yamashita et al. 2005; Singh et al. 2008).

### Domains (`confostate.features.domains`)

Inter-helix distances and angles for LeuT TM helices.

| Feature | Description |
|---|---|
| `domain_TM1_TM7_distance` | COM distance between gate helices TM1 and TM7 |
| `domain_TM1_TM7_angle` | Angle between TM1 and TM7 helix axes |
| `domain_TM1_TM6_distance` | COM distance between TM1 and TM6 |
| `domain_TM5_TM7_distance` | COM distance between TM5 and TM7 |
| `domain_TM3_TM10_distance` | COM distance between TM3 and TM10 |
| `domain_gate_TM1_TM6_distance` | Gate-opening distance (TM1–TM6) |

Helix boundaries are in `LEUT_TM_HELICES`.

### RMSD (`confostate.features.rmsd`)

RMSD after MDAnalysis Kabsch superposition (`MDAnalysis.analysis.rms.rmsd`)
to curated reference structures per state.

| Feature | Description |
|---|---|
| `rmsd_OF_open` | RMSD to outward-open reference (3F3E) |
| `rmsd_IF_open` | RMSD to inward-open reference (3F3A) |
| `rmsd_Occluded` | RMSD to occluded reference (3F4J) |
| `rmsd_Intermediate` | RMSD to intermediate reference (3USI) |
| `rmsd_min` | Minimum RMSD across all references |
| `rmsd_best_state_index` | Index of closest reference state |

Reference PDB files must be present in `reference_dir` (default: same directory
as the input structure).

### Orientation (`confostate.features.orientation`)

Membrane orientation features. Uses OPM columns from the annotations CSV when
available; otherwise estimates tilt/rotation from the structure principal axis.

| Feature | Description |
|---|---|
| `opm_tilt_angle` | Tilt of protein axis relative to membrane normal (°) |
| `opm_rotation_angle` | Rotation in membrane plane (°) |
| `opm_depth` | Centroid depth relative to membrane plane (Å) |
| `orientation_principal_axis_x/y/z` | Unit vector of first principal component |

## Dependencies on Person 1 (data)

Person 1 will deliver a verified `data/annotations/leu_t_transporters.csv`.
Until then, use the local stub described in {ref}`Data provenance & current status <data-provenance>`.

- **Labels:** `conformation` (+ `conformation_status` column when verified)
- **Metadata:** resolution, method, year from RCSB API
- **OPM:** `opm_tilt_angle`, `opm_rotation_angle`, `opm_depth` (replaces computed fallbacks)

Coordinate with Person 1 on binding-site residue definitions and OPM column
names as the annotation schema evolves.

## Testing

```bash
pip install -e ".[dev]"
pytest tests/test_features.py -v
```

Tests use `input/3F3E.pdb` (and `3F3A.pdb` for RMSD). Download with:

```bash
python scripts/download_structures.py --codes 3F3E 3F3A 3F4J 3USI --output-dir input
```

## Future work

- **Cavity**: Integrate Hollow-based pore detection (Python 3 rewrite).
- **Symmetry**: Internal repeat symmetry scores (`confostate.features.symmetry`).
- **Multi-family**: Parameterize helix definitions and binding sites per family.
