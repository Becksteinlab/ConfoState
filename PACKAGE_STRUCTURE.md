# Package Structure

Your ConfoState project now follows a Python package workflow:

## Directory Layout

```
ConfoState/
├── confostate/                 # Main Python package
│   ├── __init__.py            # Package initialization
│   └── data/                  # Data handling subpackage
│       ├── __init__.py
│       └── loader.py          # CSV loading utilities
├── data/
│   └── annotations/           # Annotated datasets
│       └── leu_t_transporters.csv  # 25 LeuT transporters with states
├── input/                      # Input directory for PDB files (empty initially)
├── examples/
│   └── load_data.py           # Example: load and inspect data
├── scripts/
│   └── download_structures.py  # Download PDB files from RCSB
├── pyproject.toml             # Package configuration
└── README.md                  # Main documentation
```

## Quick Start

### 1. Install the package (already done)

```bash
pip install -e .
```

### 2. Download structures to the input directory

```bash
python scripts/download_structures.py \
    --codes-file data/protein_families/LeuT_transporters.txt \
    --output-dir input
```

### 3. Load and inspect the data

```bash
python examples/load_data.py
```

### 4. Use the package in your code

```python
from confostate.data.loader import load_annotations, load_from_input_dir

# Load annotations
df = load_annotations("data/annotations/leu_t_transporters.csv")
print(df.head())

# Load structures from input directory
df_structures = load_from_input_dir("input")
print(f"Found {len(df_structures)} structures")
```

## What's Included

### Annotated Dataset: LeuT Transporters (25 structures)

The CSV file contains:
- **pdb_id**: PDB identifier
- **family**: Protein family
- **conformation**: Conformational state (OF_open, IF_open, Occluded, Intermediate)
- **reference**: Literature reference
- **experimental_method**: X-ray or Cryo-EM
- **resolution_angstrom**: Crystal/EM resolution
- **year**: Publication year

States are based on the alternating access model:
- **OF_open**: Outward-facing, open to substrate
- **IF_open**: Inward-facing, open to substrate
- **Occluded**: Substrate bound, closed on both sides
- **Intermediate**: Transitional conformation

### Data Loader (`confostate.data.loader`)

Functions:
- `load_annotations(csv_path, family=None)` — Load CSV with optional filtering
- `load_from_input_dir(input_dir)` — Scan input directory for PDB files

## Next Steps

1. Download all PDB structures to `input/` directory
2. Add feature extraction modules to `confostate/features/`
3. Build ML classifier in `confostate/models/`
4. Add explainability layer in `confostate/explain/`
5. Create CLI in `confostate/cli.py`
