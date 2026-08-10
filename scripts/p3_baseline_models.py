"""Outline script for Person 3 Task 2: baseline model training."""

from __future__ import annotations

import argparse

from confostate.models.baseline import get_baseline_models
from confostate.models.train import run_training


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Train one baseline model from merged inputs."
    )
    parser.add_argument(
        "--annotations-csv", default="data/annotations/leu_t_transporters.csv"
    )
    parser.add_argument("--features-csv", required=True)
    parser.add_argument("--family", default=None)
    parser.add_argument(
        "--model",
        choices=["logreg", "random_forest", "svm_rbf"],
        default="logreg",
    )
    parser.add_argument("--out-dir", default="data/models")
    parser.add_argument("--test-size", type=float, default=0.2)
    parser.add_argument("--random-state", type=int, default=42)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    available = sorted(
        get_baseline_models(random_state=args.random_state).keys()
    )
    print(f"Available baseline models: {', '.join(available)}")

    result = run_training(
        annotations_csv=args.annotations_csv,
        features_csv=args.features_csv,
        model_name=args.model,
        out_dir=args.out_dir,
        family=args.family,
        test_size=args.test_size,
        random_state=args.random_state,
    )

    print(f"Model artifact: {result['model_path']}")
    print(f"Metadata: {result['metadata_path']}")
    print(f"Accuracy: {result['metrics'].get('accuracy', 0.0):.4f}")


if __name__ == "__main__":
    main()
