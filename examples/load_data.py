#!/usr/bin/env python
"""Example script: Load and inspect annotated structures."""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from confostate.data.loader import load_annotations, load_from_input_dir


def main():
    """Load and display annotations and input structures."""

    print("=" * 60)
    print("ConfoState: Data Loading Example")
    print("=" * 60)

    # Load annotations
    annotations_path = "data/annotations/leu_t_transporters.csv"
    print(f"\n1. Loading annotations from: {annotations_path}")

    if os.path.exists(annotations_path):
        df_annot = load_annotations(annotations_path, family="LeuT")
        print(f"   Loaded {len(df_annot)} annotated structures")
        print(f"   Columns: {', '.join(df_annot.columns)}")
        print("\n   Summary by conformation:")
        print(df_annot["conformation"].value_counts())

        print("\n   First 5 entries:")
        print(
            df_annot[
                ["pdb_id", "conformation", "experimental_method", "year"]
            ].head()
        )
    else:
        print(f"   ERROR: File not found: {annotations_path}")

    # Check input directory
    input_dir = "input"
    print(f"\n2. Scanning input directory: {input_dir}")

    if os.path.isdir(input_dir):
        df_input = load_from_input_dir(input_dir)
        if len(df_input) > 0:
            print(f"   Found {len(df_input)} PDB files")
            print(df_input)
        else:
            print(f"   No .pdb files found in {input_dir}")
            print("   Download structures using:")
            codes = "data/protein_families/LeuT_transporters.txt"
            print(
                "      python scripts/download_structures.py "
                f"--codes-file {codes} --output-dir {input_dir}"
            )
    else:
        print(f"   WARNING: Directory does not exist: {input_dir}")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
