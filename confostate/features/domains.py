"""Domain distance and angle features for LeuT transporters."""

from __future__ import annotations

from typing import Optional

import numpy as np

from confostate.features._structure import (
    StructureData,
    angle_between_vectors,
    center_of_mass,
    helix_axis,
    load_structure,
    pairwise_distance,
)
from confostate.features.rmsd import (
    LEUT_REFERENCE_STRUCTURES,
    _resolve_reference_path,
)

LEUT_TM_HELICES: dict[str, tuple[int, int]] = {
    "TM1": (22, 52),
    "TM2": (68, 98),
    "TM3": (101, 133),
    "TM4": (144, 174),
    "TM5": (188, 218),
    "TM6": (248, 278),
    "TM7": (287, 317),
    "TM8": (328, 358),
    "TM9": (371, 401),
    "TM10": (412, 442),
    "TM11": (455, 485),
    "TM12": (496, 515),
}

LEUT_DOMAIN_PAIRS = (
    ("TM1", "TM7"),
    ("TM1", "TM6"),
    ("TM5", "TM7"),
    ("TM3", "TM10"),
)

_DOMAIN_METRIC_KEYS = (
    "domain_TM1_TM7_distance",
    "domain_TM1_TM7_angle",
    "domain_TM1_TM6_distance",
    "domain_TM1_TM6_angle",
    "domain_TM5_TM7_distance",
    "domain_TM5_TM7_angle",
    "domain_TM3_TM10_distance",
    "domain_TM3_TM10_angle",
    "domain_gate_TM1_TM6_distance",
)


def _domain_geometry(
    structure: StructureData,
    tm_helices: dict[str, tuple[int, int]],
    domain_pairs: tuple[tuple[str, str], ...],
) -> dict[str, float]:
    """Compute absolute inter-helix distances and angles."""
    coms: dict[str, np.ndarray] = {}
    axes: dict[str, np.ndarray] = {}
    for name, (start, end) in tm_helices.items():
        ag = structure.select_ca_range(start, end)
        if len(ag) == 0:
            continue
        coms[name] = center_of_mass(ag)
        axes[name] = helix_axis(ag)

    features: dict[str, float] = {}
    for helix_a, helix_b in domain_pairs:
        key_base = f"domain_{helix_a}_{helix_b}"
        if helix_a not in coms or helix_b not in coms:
            features[f"{key_base}_distance"] = float("nan")
            features[f"{key_base}_angle"] = float("nan")
            continue
        features[f"{key_base}_distance"] = pairwise_distance(
            coms[helix_a], coms[helix_b]
        )
        features[f"{key_base}_angle"] = angle_between_vectors(
            axes[helix_a], axes[helix_b]
        )

    if "TM1" in coms and "TM6" in coms:
        features["domain_gate_TM1_TM6_distance"] = pairwise_distance(
            coms["TM1"], coms["TM6"]
        )
    else:
        features["domain_gate_TM1_TM6_distance"] = float("nan")

    return features


def _domain_deltas(
    base_features: dict[str, float],
    reference_dir: str,
    reference_structures: dict[str, str],
    tm_helices: dict[str, tuple[int, int]],
    domain_pairs: tuple[tuple[str, str], ...],
) -> dict[str, float]:
    """Compute domain metric deltas vs each unique reference PDB."""
    deltas: dict[str, float] = {}
    unique_refs = sorted(set(reference_structures.values()))

    for ref_pdb_id in unique_refs:
        try:
            ref_path = _resolve_reference_path(ref_pdb_id, reference_dir)
        except FileNotFoundError:
            continue

        ref_structure = load_structure(str(ref_path), pdb_id=ref_pdb_id)
        ref_features = _domain_geometry(
            ref_structure, tm_helices, domain_pairs
        )

        for key in _DOMAIN_METRIC_KEYS:
            if key not in base_features or key not in ref_features:
                continue
            base_val = base_features[key]
            ref_val = ref_features[key]
            if np.isnan(base_val) or np.isnan(ref_val):
                deltas[f"{key}_delta_vs_{ref_pdb_id}"] = float("nan")
            else:
                deltas[f"{key}_delta_vs_{ref_pdb_id}"] = float(
                    base_val - ref_val
                )

    return deltas


def extract_domain_features(
    structure: StructureData,
    tm_helices: Optional[dict[str, tuple[int, int]]] = None,
    domain_pairs: tuple[tuple[str, str], ...] = LEUT_DOMAIN_PAIRS,
    reference_dir: Optional[str] = None,
    reference_structures: Optional[dict[str, str]] = None,
    include_deltas: bool = True,
) -> dict[str, float]:
    """
    Compute pairwise helix COM distances, angles, and optional deltas.

    When ``reference_dir`` is set, also returns deltas vs each curated
    reference PDB (same references as ``rmsd.py``), e.g.
    ``domain_TM1_TM7_distance_delta_vs_3F3E``.
    """
    helices = tm_helices or LEUT_TM_HELICES
    features = _domain_geometry(structure, helices, domain_pairs)

    if include_deltas and reference_dir:
        refs = reference_structures or LEUT_REFERENCE_STRUCTURES
        features.update(
            _domain_deltas(
                features, reference_dir, refs, helices, domain_pairs
            )
        )

    return features
