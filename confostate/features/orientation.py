"""Membrane orientation features (OPM-derived or computed)."""

from __future__ import annotations

from typing import Any, Optional

import numpy as np

from confostate.features._structure import (
    StructureData,
    angle_between_vectors,
    principal_axis,
)

DEFAULT_MEMBRANE_NORMAL = np.array([0.0, 0.0, 1.0])

_MISSING_VALUES = frozenset(
    {"", "na", "n/a", "none", "null", "nan", "not_fetched", "pending"}
)


def _is_missing(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, float) and np.isnan(value):
        return True
    return str(value).strip().lower() in _MISSING_VALUES


def _maybe_float(value: Any) -> Optional[float]:
    if _is_missing(value):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _tilt_angle(
    protein_axis: np.ndarray, membrane_normal: np.ndarray
) -> float:
    return angle_between_vectors(protein_axis, membrane_normal)


def _rotation_angle(
    protein_axis: np.ndarray, membrane_normal: np.ndarray
) -> float:
    normal = membrane_normal / np.linalg.norm(membrane_normal)
    projected = protein_axis - np.dot(protein_axis, normal) * normal
    proj_norm = np.linalg.norm(projected)
    if proj_norm < 1e-6:
        return 0.0
    projected /= proj_norm
    ref = np.array([1.0, 0.0, 0.0])
    ref = ref - np.dot(ref, normal) * normal
    ref_norm = np.linalg.norm(ref)
    if ref_norm < 1e-6:
        ref = np.array([0.0, 1.0, 0.0])
        ref = ref - np.dot(ref, normal) * normal
        ref /= np.linalg.norm(ref)
    else:
        ref /= ref_norm
    cos_angle = np.clip(np.dot(projected, ref), -1.0, 1.0)
    angle = float(np.degrees(np.arccos(cos_angle)))
    cross = np.cross(ref, projected)
    if np.dot(cross, normal) < 0:
        angle = 360.0 - angle
    return angle


def _membrane_depth(
    structure: StructureData, membrane_normal: np.ndarray
) -> float:
    normal = membrane_normal / np.linalg.norm(membrane_normal)
    centroid = structure.ca_atoms.center_of_mass()
    return float(abs(np.dot(centroid, normal)))


def extract_orientation_features(
    structure: StructureData,
    annotations_row: Optional[dict[str, Any]] = None,
    membrane_normal: Optional[np.ndarray] = None,
) -> dict[str, float]:
    """
    Extract membrane orientation features.

    OPM columns from annotations are used when present; otherwise values are
    computed from MDAnalysis CA coordinates.
    """
    normal = (
        membrane_normal
        if membrane_normal is not None
        else DEFAULT_MEMBRANE_NORMAL.copy()
    )
    axis = principal_axis(structure.ca_atoms.positions)

    features: dict[str, float] = {}

    if annotations_row:
        for col in (
            "opm_tilt_angle",
            "opm_rotation_angle",
            "opm_depth",
            "opm_tm_count",
        ):
            parsed = _maybe_float(annotations_row.get(col))
            if parsed is not None:
                features[col] = parsed

    if "opm_tilt_angle" not in features:
        features["opm_tilt_angle"] = _tilt_angle(axis, normal)
    if "opm_rotation_angle" not in features:
        features["opm_rotation_angle"] = _rotation_angle(axis, normal)
    if "opm_depth" not in features:
        features["opm_depth"] = _membrane_depth(structure, normal)

    features["orientation_principal_axis_x"] = float(axis[0])
    features["orientation_principal_axis_y"] = float(axis[1])
    features["orientation_principal_axis_z"] = float(axis[2])

    return features


def get_membrane_normal(
    annotations_row: Optional[dict[str, Any]] = None,
) -> np.ndarray:
    """Return membrane normal vector, defaulting to Z-axis."""
    return DEFAULT_MEMBRANE_NORMAL.copy()
