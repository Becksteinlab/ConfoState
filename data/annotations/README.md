# LeuT Annotations — Data Provenance

This file is a **working stub** until Person 1 (Josh) delivers verified curation.

**Fresh clone setup:**

```bash
cp data/annotations/leu_t_transporters.csv.example \
   data/annotations/leu_t_transporters.csv
```

The `.csv` file is gitignored; the `.csv.example` template is committed.

## Column status

| Column | Status | Source |
|--------|--------|--------|
| `pdb_id` | **Real** | `data/protein_families/LeuT_transporters.txt` |
| `family` | **Real** | Project definition (LeuT) |
| `conformation` | **Unverified estimate** | Assigned from known LeuT papers; **not** re-checked against each primary source |
| `conformation_status` | Meta | `literature_estimate` = needs Person 1 verification |
| `reference` | **Approximate** | Paper associated with each structure family; not linked to DOI/PubMed yet |
| `experimental_method`, `resolution_angstrom`, `year` | **Approximate** | Typical values from PDB/literature memory; **not** fetched live from RCSB API |
| `metadata_status` | Meta | `literature_estimate` = needs RCSB API verification (Person 1 task) |
| `opm_*` columns | **Placeholder** | `N/A` — OPM not fetched yet (Person 1 task) |
| `opm_status` | Meta | `not_fetched` |

## What is computed live (not in this CSV)

Feature vectors in `data/features/leu_t_feature_vectors.csv` are **computed at runtime** by:

1. Downloading PDB coordinates from RCSB (`scripts/download_structures.py`)
2. Running `confostate.features.extract_features()` on each file

Computed from PDB coordinates (MDAnalysis + SciPy):

- `cavity_*` — binding-site geometry
- `domain_*` — TM helix distances/angles
- `rmsd_*` — superposed RMSD vs reference structures
- `opm_*` (in feature output) — **computed from structure** when CSV has `N/A`
- `orientation_principal_axis_*` — computed from structure

## Who fixes what

- **Person 1:** Verify conformation labels, fetch RCSB metadata, fetch real OPM values
- **Person 2:** Feature extraction from PDB files (almost done)
- **Person 3:** Uses feature vectors + `conformation` labels for ML training
