"""Training helpers that use annotation-table columns as model inputs."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

DEFAULT_NUMERIC_INPUTS = [
    "resolution_angstrom",
    "year",
    "opm_tilt_angle",
    "opm_rotation_angle",
    "opm_depth",
    "opm_tm_count",
]

DEFAULT_CATEGORICAL_INPUTS = [
    "family",
    "conformation_status",
    "reference",
    "experimental_method",
    "metadata_status",
    "opm_status",
]


def _prepare_inputs(df: pd.DataFrame, numeric_cols: list[str], categorical_cols: list[str]) -> pd.DataFrame:
    prepared = df.copy()
    for col in numeric_cols:
        prepared[col] = pd.to_numeric(prepared[col], errors="coerce")
    for col in categorical_cols:
        prepared[col] = prepared[col].astype(str)
    return prepared


def train_from_annotations_table(
    annotations_csv: str,
    model_out: str,
    metrics_out: str,
    target_col: str = "conformation",
    numeric_cols: list[str] | None = None,
    categorical_cols: list[str] | None = None,
    test_size: float = 0.2,
    random_state: int = 42,
) -> dict:
    """Train a baseline classifier from annotation table columns."""
    try:
        import joblib
        from sklearn.compose import ColumnTransformer
        from sklearn.impute import SimpleImputer
        from sklearn.linear_model import LogisticRegression
        from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
        from sklearn.model_selection import train_test_split
        from sklearn.pipeline import Pipeline
        from sklearn.preprocessing import OneHotEncoder
    except ImportError as exc:
        raise ImportError(
            "scikit-learn and joblib are required. Install with: pip install scikit-learn joblib"
        ) from exc

    numeric = numeric_cols or DEFAULT_NUMERIC_INPUTS
    categorical = categorical_cols or DEFAULT_CATEGORICAL_INPUTS

    df = pd.read_csv(
        annotations_csv,
        na_values=["N/A", "n/a", "NA", ""],
        keep_default_na=True,
    )

    required = [target_col] + numeric + categorical
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns in annotations file: {missing}")

    working = _prepare_inputs(df[required], numeric, categorical)
    X = working[numeric + categorical]
    y = working[target_col]

    if y.nunique() < 2:
        raise ValueError("Training needs at least two target classes in the input table")

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=test_size,
        random_state=random_state,
        stratify=y,
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", Pipeline([("imputer", SimpleImputer(strategy="median"))]), numeric),
            (
                "cat",
                Pipeline(
                    [
                        ("imputer", SimpleImputer(strategy="most_frequent")),
                        ("onehot", OneHotEncoder(handle_unknown="ignore")),
                    ]
                ),
                categorical,
            ),
        ]
    )

    model = Pipeline(
        [
            ("preprocessor", preprocessor),
            (
                "classifier",
                LogisticRegression(
                    max_iter=2000,
                    class_weight="balanced",
                    random_state=random_state,
                ),
            ),
        ]
    )

    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    labels = sorted(y.unique().tolist())
    metrics = {
        "annotations_csv": annotations_csv,
        "input_columns": numeric + categorical,
        "numeric_columns": numeric,
        "categorical_columns": categorical,
        "target_column": target_col,
        "n_total": int(len(df)),
        "n_train": int(len(X_train)),
        "n_test": int(len(X_test)),
        "labels": labels,
        "accuracy": float(accuracy_score(y_test, y_pred)),
        "classification_report": classification_report(
            y_test, y_pred, output_dict=True, zero_division=0
        ),
        "confusion_matrix": confusion_matrix(y_test, y_pred, labels=labels).tolist(),
    }

    model_path = Path(model_out)
    metrics_path = Path(metrics_out)
    model_path.parent.mkdir(parents=True, exist_ok=True)
    metrics_path.parent.mkdir(parents=True, exist_ok=True)

    joblib.dump(model, model_path)
    metrics_path.write_text(json.dumps(metrics, indent=2), encoding="utf-8")

    return metrics
