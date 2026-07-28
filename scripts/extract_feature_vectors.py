#!/usr/bin/env python
"""Extract feature vectors for LeuT transporter structures.

Downloads PDB files if missing, then writes a CSV of feature vectors.
"""

import argparse
from pathlib import Path

from confostate.data.loader import load_annotations, load_from_input_dir
from confostate.features import extract_features_batch

DEFAULT_ANNOTATIONS = "data/annotations/leu_t_transporters.csv"
DEFAULT_INPUT_DIR = "input"
DEFAULT_OUTPUT = "data/features/leu_t_feature_vectors.csv"


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract feature vectors for LeuT structures.")
    parser.add_argument(
        "--annotations",
        default=DEFAULT_ANNOTATIONS,
        help=f"Annotations CSV (default: {DEFAULT_ANNOTATIONS})",
    )
    parser.add_argument(
        "--input-dir",
        default=DEFAULT_INPUT_DIR,
        help=f"Directory with PDB files (default: {DEFAULT_INPUT_DIR})",
    )
    parser.add_argument(
        "--output",
        default=DEFAULT_OUTPUT,
        help=f"Output CSV path (default: {DEFAULT_OUTPUT})",
    )
    args = parser.parse_args()

    annotations = load_annotations(args.annotations, family="LeuT")
    structures = load_from_input_dir(args.input_dir)

    if len(structures) == 0:
        raise SystemExit(
            f"No PDB files in {args.input_dir}. Download with:\n"
            f"  python scripts/download_structures.py "
            f"--codes-file data/protein_families/LeuT_transporters.txt "
            f"--output-dir {args.input_dir}"
        )

    merged = annotations.merge(structures, on="pdb_id", how="inner")
    if len(merged) == 0:
        raise SystemExit("No overlap between annotations and downloaded PDB files.")

    print(f"Extracting features for {len(merged)} structures...")
    df = extract_features_batch(
        merged["file_path"].tolist(),
        annotations_df=annotations,
        reference_dir=args.input_dir,
    )

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Wrote {len(df)} feature vectors to {output_path}")
    print(f"Feature columns: {len([c for c in df.columns if c not in ('pdb_id', 'file_path', 'conformation')])}")


if __name__ == "__main__":
    main()
