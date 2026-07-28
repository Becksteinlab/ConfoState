"""Cavity and solvent-accessibility features for substrate-binding sites."""

from __future__ import annotations

from typing import Optional

import numpy as np
from scipy.spatial import ConvexHull

from confostate.features._structure import StructureData, center_of_mass

# LeuT substrate / Na1 binding pocket residues
# (Yamashita et al. 2005, Singh et al. 2008).
LEUT_BINDING_SITE_RESIDUES = (
    21,
    22,
    23,
    24,
    55,
    58,
    91,
    93,
    108,
    152,
    156,
    158,
    256,
    259,
    319,
    322,
)

ACCESSIBILITY_RADIUS = 12.0
ACCESSIBILITY_SLAB_HEIGHT = 8.0


def _convex_hull_volume(coords: np.ndarray) -> float:
    if len(coords) < 4:
        return 0.0
    try:
        hull = ConvexHull(coords)
        return float(hull.volume)
    except Exception:
        return 0.0


def _accessibility_along_axis(
    structure: StructureData,
    site_center: np.ndarray,
    membrane_normal: np.ndarray,
    direction: float,
) -> float:
    """Fraction of CA atoms within a slab on one side of the binding site."""
    normal = membrane_normal / np.linalg.norm(membrane_normal)
    ca_coords = structure.ca_atoms.positions
    relative = ca_coords - site_center
    projections = relative @ normal
    slab_mask = (projections * direction > 0) & (
        np.abs(projections) < ACCESSIBILITY_SLAB_HEIGHT
    )
    if not slab_mask.any():
        return 0.0

    slab_coords = ca_coords[slab_mask]
    lateral = slab_coords - site_center
    lateral = lateral - np.outer(lateral @ normal, normal)
    distances = np.linalg.norm(lateral, axis=1)
    exposed = (distances < ACCESSIBILITY_RADIUS).sum()
    return float(exposed / len(slab_coords))


def extract_cavity_features(
    structure: StructureData,
    membrane_normal: Optional[np.ndarray] = None,
    binding_residues: tuple[int, ...] = LEUT_BINDING_SITE_RESIDUES,
) -> dict[str, float]:
    """
    Compute cavity volume and inward/outward accessibility proxies.

    Uses MDAnalysis atom selections for binding-site atoms and CA positions.
    """
    if membrane_normal is None:
        membrane_normal = np.array([0.0, 0.0, 1.0])

    binding_atoms = structure.select_residues(
        binding_residues, heavy_atoms=True
    )
    if len(binding_atoms) == 0:
        binding_atoms = structure.select_residues(binding_residues)

    if len(binding_atoms) > 0:
        site_center = center_of_mass(binding_atoms)
        volume_coords = binding_atoms.positions
    else:
        site_center = center_of_mass(structure.ca_atoms)
        volume_coords = structure.ca_atoms.positions

    return {
        "cavity_volume": _convex_hull_volume(volume_coords),
        "cavity_accessibility_in": _accessibility_along_axis(
            structure, site_center, membrane_normal, direction=-1.0
        ),
        "cavity_accessibility_out": _accessibility_along_axis(
            structure, site_center, membrane_normal, direction=1.0
        ),
    }
