"""Domain distance and angle features for LeuT transporters."""

from __future__ import annotations

from typing import Optional

import numpy as np

from confostate.features._structure import (
    StructureData,
    angle_between_vectors,
    center_of_mass,
    helix_axis,
    pairwise_distance,
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


def extract_domain_features(
    structure: StructureData,
    tm_helices: Optional[dict[str, tuple[int, int]]] = None,
    domain_pairs: tuple[tuple[str, str], ...] = LEUT_DOMAIN_PAIRS,
) -> dict[str, float]:
    """
    Compute pairwise helix COM distances and inter-helix angles.

    Uses MDAnalysis selections and ``AtomGroup.center_of_mass()``.
    """
    helices = tm_helices or LEUT_TM_HELICES
    features: dict[str, float] = {}

    coms: dict[str, np.ndarray] = {}
    axes: dict[str, np.ndarray] = {}
    for name, (start, end) in helices.items():
        ag = structure.select_ca_range(start, end)
        if len(ag) == 0:
            continue
        coms[name] = center_of_mass(ag)
        axes[name] = helix_axis(ag)

    for helix_a, helix_b in domain_pairs:
        key_base = f"domain_{helix_a}_{helix_b}"
        if helix_a not in coms or helix_b not in coms:
            features[f"{key_base}_distance"] = float("nan")
            features[f"{key_base}_angle"] = float("nan")
            continue
        features[f"{key_base}_distance"] = pairwise_distance(coms[helix_a], coms[helix_b])
        features[f"{key_base}_angle"] = angle_between_vectors(axes[helix_a], axes[helix_b])

    if "TM1" in coms and "TM6" in coms:
        features["domain_gate_TM1_TM6_distance"] = pairwise_distance(coms["TM1"], coms["TM6"])
    else:
        features["domain_gate_TM1_TM6_distance"] = float("nan")

    return features
