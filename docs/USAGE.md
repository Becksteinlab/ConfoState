# ConfoState — Usage Guide

Standard workflows for working with ConfoState.

---

## 1. Set up

Clone the repository and install dependencies:

    git clone <repo-url>
    cd ConfoState
    pip install -e .

---

## 2. Download structures

Structure files (`.pdb`, `.cif`, etc.) are **not checked into the repository**.
Download them locally before running any analysis.

### Download a protein family

Use the codes file for the relevant protein family:

    mkdir -p data/structures/LeuT/
    python scripts/download_structures.py \
        --codes-file data/protein_families/LeuT_transporters.txt \
        --output-dir data/structures/LeuT/

### Download specific structures

    python scripts/download_structures.py \
        --codes 3F3A 3F3C 6XWM \
        --output-dir data/structures/LeuT/

### Re-download / refresh

    python scripts/download_structures.py \
        --codes-file data/protein_families/LeuT_transporters.txt \
        --output-dir data/structures/LeuT/ \
        --overwrite

See `docs/scripts/download_structures.md` for the full option reference.

### Protein family codes files

Pre-curated PDB code lists live in `data/protein_families/`:

| File | Family |
|------|--------|
| `LeuT_transporters.txt` | LeuT-fold secondary active transporters |

---

## 3. Annotate structures

*(To be documented as annotation workflows are developed.)*

---

## 4. Extract features

*(To be documented as feature extraction scripts are added.)*

---

## 5. Train and evaluate a classifier

*(To be documented as model training workflows are developed.)*

---

## Notes

- Structure files are excluded from version control via `.gitignore`.
  Never commit `.pdb`, `.cif`, `.mmcif`, or `.ent` files.
- Downloaded structures are expected at `data/structures/<family>/` by convention.
- PDB codes are four characters, case-insensitive (scripts normalise to uppercase).
