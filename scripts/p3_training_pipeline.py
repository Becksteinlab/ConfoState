"""Outline script for Person 3 Task 3: multi-model training pipeline."""

from __future__ import annotations

import argparse
from pathlib import Path

from confostate.models.train import run_training


DEFAULT_MODELS = ["logreg", "random_forest", "svm_rbf"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run baseline training pipeline across selected models."
    )
    parser.add_argument(
        "--annotations-csv", default="data/annotations/leu_t_transporters.csv"
    )
    parser.add_argument("--features-csv", required=True)
    parser.add_argument("--family", default=None)
    parser.add_argument("--models", nargs="+", default=DEFAULT_MODELS)
    parser.add_argument("--out-dir", default="data/models")
    parser.add_argument("--test-size", type=float, default=0.2)
    parser.add_argument("--random-state", type=int, default=42)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    root = Path(args.out_dir)
    root.mkdir(parents=True, exist_ok=True)

    for model_name in args.models:
        model_dir = root / (args.family or "all") / model_name
        print(f"Training: {model_name}")
        result = run_training(
            annotations_csv=args.annotations_csv,
            features_csv=args.features_csv,
            model_name=model_name,
            out_dir=str(model_dir),
            family=args.family,
            test_size=args.test_size,
            random_state=args.random_state,
        )
        print(f"  model: {result['model_path']}")
        print(f"  accuracy: {result['metrics'].get('accuracy', 0.0):.4f}")


if __name__ == "__main__":
    main()
