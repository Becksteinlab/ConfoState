"""Training pipeline helpers for baseline ConfoState models."""

from __future__ import annotations

import json
import pickle
from pathlib import Path
from typing import Any

from confostate.data.datasets import build_xy, load_dataset, train_test_split_dataset
from confostate.models.baseline import get_baseline_models, train_model
from confostate.models.evaluate import evaluate_model


def save_model_artifact(model: object, out_dir: str, metadata: dict[str, Any]) -> tuple[str, str]:
    """Save model pickle and metadata JSON and return paths."""
    output = Path(out_dir)
    output.mkdir(parents=True, exist_ok=True)

    model_path = output / "model.pkl"
    metadata_path = output / "metadata.json"

    with model_path.open("wb") as f:
        pickle.dump(model, f)

    metadata_path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    return str(model_path), str(metadata_path)


def run_training(
    annotations_csv: str,
    features_csv: str,
    model_name: str,
    out_dir: str,
    family: str | None = None,
    test_size: float = 0.2,
    random_state: int = 42,
) -> dict[str, Any]:
    """Run a train/eval cycle for a selected baseline model."""
    bundle = load_dataset(annotations_csv=annotations_csv, features_csv=features_csv, family=family)
    train_df, test_df = train_test_split_dataset(
        bundle.dataframe,
        label_column=bundle.label_column,
        test_size=test_size,
        random_state=random_state,
        stratify=True,
    )

    X_train, y_train = build_xy(train_df, bundle.feature_columns, label_column=bundle.label_column)
    X_test, y_test = build_xy(test_df, bundle.feature_columns, label_column=bundle.label_column)

    models = get_baseline_models(random_state=random_state)
    if model_name not in models:
        available = ", ".join(sorted(models))
        raise ValueError(f"Unknown model '{model_name}'. Available: {available}")

    model = train_model(models[model_name], X_train, y_train)
    metrics = evaluate_model(model, X_test, y_test)

    metadata: dict[str, Any] = {
        "model_name": model_name,
        "family": family,
        "test_size": test_size,
        "random_state": random_state,
        "feature_columns": bundle.feature_columns,
        "n_train": int(len(train_df)),
        "n_test": int(len(test_df)),
        "metrics": metrics,
    }

    model_path, metadata_path = save_model_artifact(model, out_dir, metadata)

    return {
        "model_path": model_path,
        "metadata_path": metadata_path,
        "metrics": metrics,
        "feature_columns": bundle.feature_columns,
        "test_dataframe": test_df,
    }
