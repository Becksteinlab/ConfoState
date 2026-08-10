"""RMSD-to-reference features for conformational state comparison."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import numpy as np
from MDAnalysis.analysis import rms

from confostate.features._structure import StructureData, load_structure

LEUT_REFERENCE_STRUCTURES: dict[str, str] = {
    "OF_open": "3F3E",
    "IF_open": "3F3A",
    "Occluded": "3F4J",
    "Intermediate": "3USI",
}

LEUT_ALIGNMENT_RESIDUES = tuple(range(50, 480, 5))


def _aligned_ca_groups(
    mobile: StructureData,
    reference: StructureData,
    alignment_residues: tuple[int, ...],
):
    mobile_ids = set(mobile.ca_atoms.resids)
    ref_ids = set(reference.ca_atoms.resids)
    common = sorted(mobile_ids & ref_ids & set(alignment_residues))
    if len(common) < 3:
        raise ValueError("Insufficient shared residues for RMSD alignment")

    mobile_coords = []
    ref_coords = []
    for resid in common:
        m_ag = mobile.ca_atoms.select_atoms(f"resid {resid}")
        r_ag = reference.ca_atoms.select_atoms(f"resid {resid}")
        if len(m_ag) == 0 or len(r_ag) == 0:
            continue
        mobile_coords.append(m_ag[0].position)
        ref_coords.append(r_ag[0].position)

    if len(mobile_coords) < 3:
        raise ValueError("Insufficient shared residues for RMSD alignment")

    return np.asarray(mobile_coords), np.asarray(ref_coords)


def _resolve_reference_path(pdb_id: str, reference_dir: Optional[str]) -> Path:
    candidates = []
    if reference_dir:
        candidates.append(Path(reference_dir) / f"{pdb_id}.pdb")
    candidates.extend(
        [
            Path("input") / f"{pdb_id}.pdb",
            Path("data/structures") / f"{pdb_id}.pdb",
        ]
    )
    for path in candidates:
        if path.exists():
            return path
    raise FileNotFoundError(
        f"Reference structure {pdb_id}.pdb not found. "
        f"Searched: {', '.join(str(p) for p in candidates)}"
    )


def extract_rmsd_features(
    structure: StructureData,
    reference_structures: Optional[dict[str, str]] = None,
    reference_dir: Optional[str] = None,
    alignment_residues: tuple[int, ...] = LEUT_ALIGNMENT_RESIDUES,
) -> dict[str, float]:
    """
    Compute RMSD to reference structures using MDAnalysis ``rms.rmsd``.

    Superposition is performed automatically (Kabsch algorithm).
    """
    refs = reference_structures or LEUT_REFERENCE_STRUCTURES
    features: dict[str, float] = {}
    rmsd_values: list[float] = []

    for state, ref_pdb_id in refs.items():
        ref_path = _resolve_reference_path(ref_pdb_id, reference_dir)
        reference = load_structure(str(ref_path), pdb_id=ref_pdb_id)
        mobile_coords, ref_coords = _aligned_ca_groups(
            structure, reference, alignment_residues
        )
        rmsd_val = rms.rmsd(mobile_coords, ref_coords, superposition=True)
        features[f"rmsd_{state}"] = float(rmsd_val)
        rmsd_values.append(float(rmsd_val))

    features["rmsd_min"] = float(min(rmsd_values)) if rmsd_values else float("nan")
    if rmsd_values:
        best_state = min(refs.keys(), key=lambda s: features[f"rmsd_{s}"])
        features["rmsd_best_state_index"] = float(list(refs.keys()).index(best_state))
    else:
        features["rmsd_best_state_index"] = float("nan")

    return features
