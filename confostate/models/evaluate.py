"""Evaluation and reporting helpers for ConfoState models."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np


def evaluate_model(
    model, X_test, y_test, labels: list[str] | None = None
) -> dict:
    """Compute standard classification metrics.

    Returns a serializable dictionary.
    """
    try:
        from sklearn.metrics import (
            accuracy_score,
            classification_report,
            confusion_matrix,
            precision_recall_fscore_support,
        )
    except ImportError as exc:
        raise ImportError(
            "scikit-learn is required for evaluation. "
            "Install with: pip install scikit-learn"
        ) from exc

    y_pred = model.predict(X_test)
    used_labels = labels or sorted({str(v) for v in y_test})

    accuracy = float(accuracy_score(y_test, y_pred))
    precision, recall, f1, support = precision_recall_fscore_support(
        y_test,
        y_pred,
        labels=used_labels,
        zero_division=0,
    )

    cm = confusion_matrix(y_test, y_pred, labels=used_labels)
    cls_report = classification_report(
        y_test, y_pred, labels=used_labels, output_dict=True, zero_division=0
    )

    metrics = {
        "accuracy": accuracy,
        "labels": used_labels,
        "confusion_matrix": cm.tolist(),
        "per_label": {
            label: {
                "precision": float(precision[i]),
                "recall": float(recall[i]),
                "f1": float(f1[i]),
                "support": int(support[i]),
            }
            for i, label in enumerate(used_labels)
        },
        "report": cls_report,
        "n_test": int(len(y_test)),
    }

    if hasattr(model, "predict_proba"):
        proba = model.predict_proba(X_test)
        metrics["mean_confidence"] = float(np.max(proba, axis=1).mean())

    return metrics


def write_evaluation_report(
    metrics: dict,
    output_path: str,
    title: str = "ConfoState Evaluation Report",
) -> None:
    """Write a compact markdown report from metrics."""
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        f"# {title}",
        "",
        f"- Test samples: {metrics.get('n_test', 'n/a')}",
        f"- Accuracy: {metrics.get('accuracy', 0.0):.4f}",
    ]

    if "mean_confidence" in metrics:
        lines.append(f"- Mean confidence: {metrics['mean_confidence']:.4f}")

    lines.extend(
        [
            "",
            "## Per-label Metrics",
            "",
            "| Label | Precision | Recall | F1 | Support |",
            "|---|---:|---:|---:|---:|",
        ]
    )

    for label, m in metrics.get("per_label", {}).items():
        lines.append(
            f"| {label} | {m['precision']:.3f} | {m['recall']:.3f} | "
            f"{m['f1']:.3f} | {m['support']} |"
        )

    lines.extend(
        [
            "",
            "## Confusion Matrix",
            "",
            "```json",
            json.dumps(metrics.get("confusion_matrix", []), indent=2),
            "```",
        ]
    )

    out.write_text("\n".join(lines), encoding="utf-8")
