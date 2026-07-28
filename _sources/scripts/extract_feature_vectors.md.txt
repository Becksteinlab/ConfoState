# extract_feature_vectors

Batch-extract structural feature vectors for annotated LeuT transporter PDB files.

## Synopsis

```bash
python scripts/extract_feature_vectors.py [OPTIONS]
```

## Description

Reads the LeuT annotations CSV and PDB files from an input directory, runs
`confostate.features.extract_features_batch()`, and writes a CSV of feature
vectors suitable for ML training (Person 3).

Structures must be downloaded first with `scripts/download_structures.py`.

## Options

| Flag | Default | Description |
|---|---|---|
| `--annotations` | `data/annotations/leu_t_transporters.csv` | Annotations CSV path |
| `--input-dir` | `input` | Directory containing `.pdb` files |
| `--output` | `data/features/leu_t_feature_vectors.csv` | Output feature CSV path |

## Examples

```bash
cp data/annotations/leu_t_transporters.csv.example \
   data/annotations/leu_t_transporters.csv

python scripts/download_structures.py \
    --codes-file data/protein_families/LeuT_transporters.txt \
    --output-dir input

python scripts/extract_feature_vectors.py
```

## Output

Writes a CSV to `data/features/leu_t_feature_vectors.csv` with one row per
structure. Columns include `pdb_id`, `conformation`, cavity/domain/RMSD/orientation
features, and `file_path`.
