"""Outline script for Person 3 Task 1: dataset assembly and split."""

from __future__ import annotations

import argparse
from pathlib import Path

from confostate.data.datasets import load_dataset, train_test_split_dataset


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build merged ML dataset and train/test splits."
    )
    parser.add_argument(
        "--annotations-csv", default="data/annotations/leu_t_transporters.csv"
    )
    parser.add_argument("--features-csv", required=True)
    parser.add_argument("--family", default=None)
    parser.add_argument("--out-dir", default="data/processed")
    parser.add_argument("--test-size", type=float, default=0.2)
    parser.add_argument("--random-state", type=int, default=42)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    bundle = load_dataset(
        annotations_csv=args.annotations_csv,
        features_csv=args.features_csv,
        family=args.family,
    )

    train_df, test_df = train_test_split_dataset(
        bundle.dataframe,
        label_column=bundle.label_column,
        test_size=args.test_size,
        random_state=args.random_state,
        stratify=True,
    )

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    merged_path = out_dir / "merged_dataset.csv"
    train_path = out_dir / "train_split.csv"
    test_path = out_dir / "test_split.csv"

    bundle.dataframe.to_csv(merged_path, index=False)
    train_df.to_csv(train_path, index=False)
    test_df.to_csv(test_path, index=False)

    print(f"Merged dataset: {len(bundle.dataframe)} rows")
    print(f"Train split: {len(train_df)} rows")
    print(f"Test split: {len(test_df)} rows")
    print(f"Feature count: {len(bundle.feature_columns)}")
    print(f"Wrote: {merged_path}")
    print(f"Wrote: {train_path}")
    print(f"Wrote: {test_path}")


if __name__ == "__main__":
    main()
