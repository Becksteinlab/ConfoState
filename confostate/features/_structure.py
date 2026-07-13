"""MDAnalysis-based structure loading and geometry helpers."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional

import MDAnalysis as mda
import numpy as np
from MDAnalysis.core.groups import AtomGroup


@dataclass(frozen=True)
class StructureData:
    """MDAnalysis universe wrapper for feature extraction."""

    universe: mda.Universe
    pdb_path: str
    pdb_id: str
    chain_id: Optional[str] = None

    @property
    def primary_chain_id(self) -> str:
        """First protein chain ID (handles dimers by picking chain A)."""
        if self.chain_id:
            return self.chain_id
        chains = np.unique(self.universe.select_atoms("protein").chainIDs)
        if len(chains) == 0:
            raise ValueError(f"No protein chains found in {self.pdb_path}")
        return str(chains[0])

    @property
    def ca_atoms(self) -> AtomGroup:
        """Alpha-carbon atoms for the primary chain."""
        chain = self.primary_chain_id
        ag = self.universe.select_atoms(f"protein and chainID {chain} and name CA")
        if len(ag) == 0:
            ag = self.universe.select_atoms(f"segid {chain} and name CA")
        return ag

    def select_ca_range(self, start: int, end: int) -> AtomGroup:
        return self.ca_atoms.select_atoms(f"resid {start}:{end}")

    def select_residues(
        self,
        resids: Iterable[int],
        *,
        name: str = "CA",
        heavy_atoms: bool = False,
    ) -> AtomGroup:
        resid_str = " ".join(str(r) for r in resids)
        chain = self.primary_chain_id
        if heavy_atoms:
            return self.universe.select_atoms(
                f"protein and chainID {chain} and resid {resid_str} and not name H*"
            )
        return self.ca_atoms.select_atoms(f"resid {resid_str}")


def infer_pdb_id(pdb_path: str, pdb_id: Optional[str] = None) -> str:
    if pdb_id:
        return pdb_id.upper()
    return Path(pdb_path).stem.upper()


def load_structure(
    pdb_path: str,
    pdb_id: Optional[str] = None,
    chain_id: Optional[str] = None,
) -> StructureData:
    """Load a PDB file as an MDAnalysis Universe."""
    path = Path(pdb_path)
    if not path.exists():
        raise FileNotFoundError(f"PDB file not found: {pdb_path}")

    universe = mda.Universe(str(path))
    structure = StructureData(
        universe=universe,
        pdb_path=str(path),
        pdb_id=infer_pdb_id(pdb_path, pdb_id),
        chain_id=chain_id,
    )
    if len(structure.ca_atoms) == 0:
        raise ValueError(f"No CA atoms found in {pdb_path}")
    return structure


def sort_by_resid(atomgroup: AtomGroup) -> AtomGroup:
    """Return atom group sorted by residue number."""
    return atomgroup[np.argsort(atomgroup.resids)]


def center_of_mass(atomgroup: AtomGroup) -> np.ndarray:
    if len(atomgroup) == 0:
        raise ValueError("Cannot compute center of mass for empty atom group")
    return atomgroup.center_of_mass()


def pairwise_distance(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.linalg.norm(a - b))


def angle_between_vectors(a: np.ndarray, b: np.ndarray) -> float:
    """Return angle in degrees between two 3D vectors."""
    a_norm = np.linalg.norm(a)
    b_norm = np.linalg.norm(b)
    if a_norm == 0 or b_norm == 0:
        return float("nan")
    cos_angle = np.clip(np.dot(a, b) / (a_norm * b_norm), -1.0, 1.0)
    return float(np.degrees(np.arccos(cos_angle)))


def principal_axis(coords: np.ndarray) -> np.ndarray:
    """First principal component of coordinate cloud (unit vector)."""
    centered = coords - coords.mean(axis=0)
    _, _, vh = np.linalg.svd(centered, full_matrices=False)
    axis = vh[0]
    norm = np.linalg.norm(axis)
    if norm == 0:
        return np.array([0.0, 0.0, 1.0])
    return axis / norm


def helix_axis(atomgroup: AtomGroup) -> np.ndarray:
    """Helix axis from CA positions (first principal component)."""
    if len(atomgroup) < 2:
        return np.array([0.0, 0.0, 1.0])
    return principal_axis(atomgroup.positions)
