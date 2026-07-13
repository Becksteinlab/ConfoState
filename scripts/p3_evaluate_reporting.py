"""Outline script for Person 3 Task 4: evaluation and report generation."""

from __future__ import annotations

import argparse
import json
import pickle
from pathlib import Path

import pandas as pd

from confostate.models.evaluate import evaluate_model, write_evaluation_report


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Evaluate trained model and write report artifacts.")
    parser.add_argument("--model-path", required=True)
    parser.add_argument("--test-csv", required=True, help="CSV containing label and feature columns")
    parser.add_argument("--label-col", default="conformation")
    parser.add_argument("--drop-cols", nargs="*", default=["pdb_id", "family", "reference", "experimental_method"])
    parser.add_argument("--report-path", default="docs/reports/phase3-eval-report.md")
    parser.add_argument("--metrics-json", default="docs/reports/phase3-eval-metrics.json")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    with open(args.model_path, "rb") as handle:
        model = pickle.load(handle)

    test_df = pd.read_csv(args.test_csv)
    if args.label_col not in test_df.columns:
        raise ValueError(f"Label column not found: {args.label_col}")

    drop_cols = [c for c in args.drop_cols if c in test_df.columns]
    X_test = test_df.drop(columns=drop_cols + [args.label_col])
    y_test = test_df[args.label_col]

    metrics = evaluate_model(model, X_test, y_test)

    write_evaluation_report(metrics, args.report_path)

    metrics_path = Path(args.metrics_json)
    metrics_path.parent.mkdir(parents=True, exist_ok=True)
    metrics_path.write_text(json.dumps(metrics, indent=2), encoding="utf-8")

    print(f"Accuracy: {metrics.get('accuracy', 0.0):.4f}")
    print(f"Report: {args.report_path}")
    print(f"Metrics JSON: {args.metrics_json}")


if __name__ == "__main__":
    main()
