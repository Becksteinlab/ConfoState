#!/usr/bin/env python
"""Train a baseline model directly from annotation-table input columns.

By default this script uses the columns defined in
`data/annotations/leu_t_transporters.csv.example`.
"""

from __future__ import annotations

import argparse

from confostate.models.annotation_table_training import train_from_annotations_table

DEFAULT_ANNOTATIONS = "data/annotations/leu_t_transporters.csv.example"
DEFAULT_MODEL_OUT = "data/models/annotations_baseline_logreg.joblib"
DEFAULT_METRICS_OUT = "data/models/annotations_baseline_metrics.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Train baseline model from annotations-table columns."
    )
    parser.add_argument(
        "--annotations",
        default=DEFAULT_ANNOTATIONS,
        help=f"Path to annotations CSV (default: {DEFAULT_ANNOTATIONS})",
    )
    parser.add_argument(
        "--model-out",
        default=DEFAULT_MODEL_OUT,
        help=f"Output model path (default: {DEFAULT_MODEL_OUT})",
    )
    parser.add_argument(
        "--metrics-out",
        default=DEFAULT_METRICS_OUT,
        help=f"Output metrics JSON path (default: {DEFAULT_METRICS_OUT})",
    )
    parser.add_argument(
        "--target-col",
        default="conformation",
        help="Target column for labels (default: conformation)",
    )
    parser.add_argument(
        "--test-size",
        type=float,
        default=0.2,
        help="Test split fraction (default: 0.2)",
    )
    parser.add_argument(
        "--random-state",
        type=int,
        default=42,
        help="Random seed for split/model (default: 42)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    metrics = train_from_annotations_table(
        annotations_csv=args.annotations,
        model_out=args.model_out,
        metrics_out=args.metrics_out,
        target_col=args.target_col,
        test_size=args.test_size,
        random_state=args.random_state,
    )

    print(f"Trained on {metrics['n_train']} rows, tested on {metrics['n_test']} rows")
    print(f"Accuracy: {metrics['accuracy']:.4f}")
    print(f"Model: {args.model_out}")
    print(f"Metrics: {args.metrics_out}")


if __name__ == "__main__":
    main()
