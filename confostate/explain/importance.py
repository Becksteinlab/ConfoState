"""Feature importance extraction for conformational-state predictions."""

from __future__ import annotations

from typing import Any, Optional, Sequence

import numpy as np

from confostate.explain._types import FeatureImportance

FEATURE_DISPLAY_NAMES: dict[str, str] = {
    "cavity_volume": "binding-site cavity volume",
    "cavity_accessibility_in": "inward solvent accessibility",
    "cavity_accessibility_out": "outward solvent accessibility",
    "domain_TM1_TM7_distance": "TM1–TM7 gate distance",
    "domain_TM1_TM7_angle": "TM1–TM7 helix angle",
    "domain_TM1_TM6_distance": "TM1–TM6 distance",
    "domain_TM5_TM7_distance": "TM5–TM7 distance",
    "domain_TM3_TM10_distance": "TM3–TM10 distance",
    "domain_gate_TM1_TM6_distance": "TM1–TM6 gate-opening distance",
    "rmsd_OF_open": "RMSD to outward-open reference (3F3E)",
    "rmsd_IF_open": "RMSD to inward-open reference (3F3A)",
    "rmsd_Occluded": "RMSD to occluded reference (3F4J)",
    "rmsd_Intermediate": "RMSD to intermediate reference (3USI)",
    "rmsd_min": "minimum RMSD across references",
    "opm_tilt_angle": "membrane tilt angle",
    "opm_rotation_angle": "membrane rotation angle",
    "opm_depth": "membrane embedding depth",
    "orientation_principal_axis_x": "principal axis (x)",
    "orientation_principal_axis_y": "principal axis (y)",
    "orientation_principal_axis_z": "principal axis (z)",
}

# Typical feature values per LeuT state for heuristic importance (stub data).
# Values are approximate literature-informed placeholders until Person 3
# provides real training statistics.
LEUT_STATE_PROFILES: dict[str, dict[str, float]] = {
    "IF_open": {
        "domain_TM1_TM7_distance": 18.0,
        "domain_gate_TM1_TM6_distance": 22.0,
        "rmsd_IF_open": 1.5,
        "cavity_accessibility_in": 0.55,
        "cavity_accessibility_out": 0.25,
    },
    "OF_open": {
        "domain_TM1_TM7_distance": 22.0,
        "domain_gate_TM1_TM6_distance": 26.0,
        "rmsd_OF_open": 1.5,
        "cavity_accessibility_in": 0.25,
        "cavity_accessibility_out": 0.55,
    },
    "Occluded": {
        "domain_TM1_TM7_distance": 16.0,
        "domain_gate_TM1_TM6_distance": 18.0,
        "rmsd_Occluded": 1.5,
        "cavity_volume": 450.0,
    },
    "Intermediate": {
        "domain_TM1_TM7_distance": 19.0,
        "domain_gate_TM1_TM6_distance": 20.0,
        "rmsd_Intermediate": 1.5,
    },
}

RMSD_STATE_MAP = {
    "IF_open": "rmsd_IF_open",
    "OF_open": "rmsd_OF_open",
    "Occluded": "rmsd_Occluded",
    "Intermediate": "rmsd_Intermediate",
}


def display_name(feature_name: str) -> str:
    """Return a human-readable label for a feature."""
    return FEATURE_DISPLAY_NAMES.get(
        feature_name, feature_name.replace("_", " ")
    )


def rank_importances(
    importances: Sequence[FeatureImportance], top_k: int = 5
) -> list[FeatureImportance]:
    """Return the top-k features by absolute importance."""
    ranked = sorted(
        importances, key=lambda item: abs(item.importance), reverse=True
    )
    return ranked[:top_k]


def extract_coefficient_importance(
    coefficients: dict[str, float],
    feature_values: dict[str, float],
    predicted_state: str,
) -> list[FeatureImportance]:
    """
    Compute importance from linear-model coefficients.

    Importance is |coefficient * value| for the predicted state's class.
    """
    results: list[FeatureImportance] = []
    for name, coef in coefficients.items():
        if name not in feature_values:
            continue
        value = feature_values[name]
        score = coef * value
        results.append(
            FeatureImportance(
                feature_name=name,
                display_name=display_name(name),
                importance=score,
                value=value,
                direction="supports" if score >= 0 else "opposes",
            )
        )
    return results


def extract_permutation_importance(
    model: Any,
    feature_matrix: np.ndarray,
    feature_names: Sequence[str],
    baseline_proba: np.ndarray,
    n_repeats: int = 5,
    random_state: int = 0,
) -> list[FeatureImportance]:
    """
    Model-agnostic permutation importance for a single prediction.

    Shuffles each feature column and measures the drop in predicted
    probability for the baseline class.
    """
    rng = np.random.default_rng(random_state)
    baseline_score = float(np.max(baseline_proba))
    predicted_index = int(np.argmax(baseline_proba))
    row_idx = 0
    n_samples = feature_matrix.shape[0]
    importances = np.zeros(len(feature_names))

    for col_idx, name in enumerate(feature_names):
        drops: list[float] = []
        original_value = float(feature_matrix[row_idx, col_idx])
        for _ in range(n_repeats):
            permuted = feature_matrix.copy()
            if n_samples > 1:
                other_values = np.delete(feature_matrix[:, col_idx], row_idx)
                permuted[row_idx, col_idx] = rng.choice(other_values)
            else:
                scale = max(abs(original_value), 1.0)
                permuted[row_idx, col_idx] = original_value + rng.normal(
                    0, 0.2 * scale
                )
            proba = model.predict_proba(permuted)[row_idx]
            drops.append(baseline_score - float(proba[predicted_index]))
        importances[col_idx] = float(np.mean(drops))

    results: list[FeatureImportance] = []
    for name, score in zip(feature_names, importances):
        value = float(feature_matrix[row_idx, list(feature_names).index(name)])
        results.append(
            FeatureImportance(
                feature_name=name,
                display_name=display_name(name),
                importance=score,
                value=value,
                direction="supports" if score >= 0 else "opposes",
            )
        )
    return results


def extract_heuristic_importance(
    features: dict[str, float],
    predicted_state: str,
    family: str = "LeuT",
) -> list[FeatureImportance]:
    """
    Estimate feature importance without a trained model.

    Compares each numeric feature to family-specific state profiles.
    Lower RMSD to the matching reference and closer agreement with the
    predicted-state profile yield higher scores.
    """
    if family != "LeuT":
        return _generic_heuristic_importance(features, predicted_state)

    profile = LEUT_STATE_PROFILES.get(predicted_state, {})
    results: list[FeatureImportance] = []

    for name, value in features.items():
        if not isinstance(value, (int, float)) or np.isnan(value):
            continue

        score = 0.0
        direction = "supports"

        if name in profile:
            expected = profile[name]
            rel_error = abs(value - expected) / max(abs(expected), 1e-6)
            score = max(0.0, 1.0 - rel_error)
            direction = "supports" if score > 0.3 else "opposes"
        elif name.startswith("rmsd_"):
            if name == RMSD_STATE_MAP.get(predicted_state):
                score = max(0.0, 3.0 - value)
                direction = "supports"
            else:
                score = max(0.0, value - 2.0) * 0.3
                direction = "opposes"
        elif name.startswith("domain_") or name.startswith("cavity_"):
            score = abs(value) * 0.01
            direction = "supports"
        else:
            score = abs(value) * 0.001
            direction = "supports"

        results.append(
            FeatureImportance(
                feature_name=name,
                display_name=display_name(name),
                importance=score,
                value=float(value),
                direction=direction,
            )
        )

    return results


def _generic_heuristic_importance(
    features: dict[str, float], predicted_state: str
) -> list[FeatureImportance]:
    """Fallback heuristic when no family profile is available."""
    results: list[FeatureImportance] = []
    for name, value in features.items():
        if not isinstance(value, (int, float)) or np.isnan(value):
            continue
        score = abs(float(value)) * 0.01
        results.append(
            FeatureImportance(
                feature_name=name,
                display_name=display_name(name),
                importance=score,
                value=float(value),
                direction="supports",
            )
        )
    return results


def resolve_importances(
    features: dict[str, float],
    predicted_state: str,
    family: str = "LeuT",
    importances: Optional[Sequence[FeatureImportance]] = None,
    model: Optional[Any] = None,
    feature_matrix: Optional[np.ndarray] = None,
    feature_names: Optional[Sequence[str]] = None,
    coefficients: Optional[dict[str, float]] = None,
) -> tuple[list[FeatureImportance], str]:
    """
    Resolve feature importances using the best available method.

    Returns (importances, method_name).
    """
    if importances is not None:
        return list(importances), "provided"

    if coefficients is not None:
        return (
            extract_coefficient_importance(
                coefficients, features, predicted_state
            ),
            "coefficient",
        )

    if model is not None and feature_matrix is not None and feature_names:
        baseline_proba = model.predict_proba(feature_matrix)[0]
        return (
            extract_permutation_importance(
                model,
                feature_matrix,
                feature_names,
                baseline_proba,
            ),
            "permutation",
        )

    return (
        extract_heuristic_importance(features, predicted_state, family),
        "heuristic",
    )
