"""Dataset assembly and split helpers for ML workflows."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np
import pandas as pd


REQUIRED_ANNOTATION_COLUMNS = {"pdb_id", "conformation"}


@dataclass
class DatasetBundle:
    """Container for merged dataset and derived feature metadata."""

    dataframe: pd.DataFrame
    feature_columns: list[str]
    label_column: str = "conformation"


def _require_columns(
    df: pd.DataFrame, required: Iterable[str], name: str
) -> None:
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"{name} is missing required columns: {missing}")


def _normalize_pdb_ids(series: pd.Series) -> pd.Series:
    return series.astype(str).str.strip().str.upper()


def load_dataset(
    annotations_csv: str,
    features_csv: str,
    family: str | None = None,
    label_column: str = "conformation",
    key_column: str = "pdb_id",
) -> DatasetBundle:
    """Load and merge annotations with feature vectors by PDB id."""
    annotations = pd.read_csv(annotations_csv)
    features = pd.read_csv(features_csv)

    _require_columns(
        annotations, REQUIRED_ANNOTATION_COLUMNS, "annotations_csv"
    )
    _require_columns(features, {key_column}, "features_csv")
    _require_columns(
        annotations, {key_column, label_column}, "annotations_csv"
    )

    annotations = annotations.copy()
    features = features.copy()

    annotations[key_column] = _normalize_pdb_ids(annotations[key_column])
    features[key_column] = _normalize_pdb_ids(features[key_column])

    if family is not None:
        if "family" not in annotations.columns:
            raise ValueError(
                "family filter requested, but 'family' is not present in "
                "annotations_csv"
            )
        annotations = annotations[
            annotations["family"].astype(str) == str(family)
        ]

    merged = annotations.merge(
        features, on=key_column, how="inner", suffixes=("", "_feature")
    )
    if merged.empty:
        raise ValueError(
            "Merged dataset is empty. Verify overlap between annotations and "
            "features keys."
        )

    key_like = {
        key_column,
        label_column,
        "family",
        "reference",
        "experimental_method",
    }
    feature_columns = [c for c in merged.columns if c not in key_like]
    if not feature_columns:
        raise ValueError("No feature columns found after merge.")

    for col in feature_columns:
        merged[col] = pd.to_numeric(merged[col], errors="raise")

    return DatasetBundle(
        dataframe=merged,
        feature_columns=feature_columns,
        label_column=label_column,
    )


def train_test_split_dataset(
    df: pd.DataFrame,
    label_column: str = "conformation",
    test_size: float = 0.2,
    random_state: int = 42,
    stratify: bool = True,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Split dataset into train/test.

    Uses scikit-learn if available and falls back otherwise.
    """
    if label_column not in df.columns:
        raise ValueError(
            f"Label column '{label_column}' not found in dataframe"
        )

    if not 0.0 < test_size < 1.0:
        raise ValueError("test_size must be between 0 and 1")

    try:
        from sklearn.model_selection import train_test_split

        stratify_values = df[label_column] if stratify else None
        train_df, test_df = train_test_split(
            df,
            test_size=test_size,
            random_state=random_state,
            stratify=stratify_values,
        )
        return train_df.reset_index(drop=True), test_df.reset_index(drop=True)
    except Exception:
        rng = np.random.default_rng(seed=random_state)
        indices = np.arange(len(df))
        rng.shuffle(indices)

        n_test = max(1, int(round(len(df) * test_size)))
        test_idx = set(indices[:n_test].tolist())

        test_df = df.iloc[[i for i in range(len(df)) if i in test_idx]].copy()
        train_df = df.iloc[
            [i for i in range(len(df)) if i not in test_idx]
        ].copy()
        return train_df.reset_index(drop=True), test_df.reset_index(drop=True)


def build_xy(
    df: pd.DataFrame,
    feature_columns: list[str],
    label_column: str = "conformation",
) -> tuple[pd.DataFrame, pd.Series]:
    """Extract model-ready feature matrix and labels."""
    _require_columns(df, feature_columns, "dataset")
    _require_columns(df, {label_column}, "dataset")
    X = df[feature_columns].copy()
    y = df[label_column].copy()
    return X, y
