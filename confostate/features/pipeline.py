"""Feature extraction pipeline — orchestrates per-module extractors."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Optional

import pandas as pd

from confostate.features._structure import load_structure
from confostate.features.cavity import extract_cavity_features
from confostate.features.domains import extract_domain_features
from confostate.features.orientation import (
    extract_orientation_features,
    get_membrane_normal,
)
from confostate.features.rmsd import extract_rmsd_features

FEATURE_GROUPS = ("cavity", "domains", "rmsd", "orientation")


def extract_features(
    pdb_path: str,
    pdb_id: Optional[str] = None,
    family: str = "LeuT",  # reserved for multi-family support (LeuT only for now)
    annotations_row: Optional[dict[str, Any]] = None,
    reference_dir: Optional[str] = None,
    include_rmsd: bool = True,
) -> dict[str, float]:
    """
    Extract all structural features from a PDB file.

    Loads the structure once via MDAnalysis, then runs each feature module.
    """
    structure = load_structure(pdb_path, pdb_id=pdb_id)
    membrane_normal = get_membrane_normal(annotations_row)

    features: dict[str, float] = {}

    features.update(extract_cavity_features(structure, membrane_normal=membrane_normal))
    features.update(extract_domain_features(structure))
    features.update(extract_orientation_features(structure, annotations_row=annotations_row))

    if include_rmsd:
        try:
            features.update(
                extract_rmsd_features(
                    structure,
                    reference_dir=reference_dir or str(Path(pdb_path).parent),
                )
            )
        except FileNotFoundError:
            pass

    return features


def extract_features_batch(
    pdb_paths: list[str],
    annotations_df: Optional[pd.DataFrame] = None,
    reference_dir: Optional[str] = None,
) -> pd.DataFrame:
    """Extract features for multiple PDB files (one row per structure)."""
    rows = []
    for pdb_path in pdb_paths:
        pdb_id = Path(pdb_path).stem.upper()
        row_data: Optional[dict[str, Any]] = None
        if annotations_df is not None and "pdb_id" in annotations_df.columns:
            matches = annotations_df[
                annotations_df["pdb_id"].str.upper() == pdb_id
            ]
            if len(matches) > 0:
                row_data = matches.iloc[0].to_dict()

        features = extract_features(
            pdb_path,
            pdb_id=pdb_id,
            annotations_row=row_data,
            reference_dir=reference_dir,
        )
        features["pdb_id"] = pdb_id
        features["file_path"] = pdb_path
        if row_data and "conformation" in row_data:
            features["conformation"] = row_data["conformation"]
        rows.append(features)

    return pd.DataFrame(rows)
