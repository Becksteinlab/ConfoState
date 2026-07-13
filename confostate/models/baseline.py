"""Baseline model definitions for conformational state classification."""

from __future__ import annotations


def get_baseline_models(random_state: int = 42) -> dict[str, object]:
    """Return baseline estimators keyed by model name."""
    try:
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.linear_model import LogisticRegression
        from sklearn.svm import SVC
    except ImportError as exc:
        raise ImportError(
            "scikit-learn is required for baseline models. Install with: pip install scikit-learn"
        ) from exc

    return {
        "logreg": LogisticRegression(max_iter=2000, random_state=random_state, class_weight="balanced"),
        "random_forest": RandomForestClassifier(
            n_estimators=300,
            random_state=random_state,
            class_weight="balanced_subsample",
        ),
        "svm_rbf": SVC(C=1.0, kernel="rbf", gamma="scale", probability=True, class_weight="balanced"),
    }


def train_model(estimator: object, X_train, y_train) -> object:
    """Fit and return a baseline model."""
    estimator.fit(X_train, y_train)
    return estimator
