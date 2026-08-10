"""CSV data loader for conformational state annotations."""

import os
from pathlib import Path
from typing import Optional

import pandas as pd


def load_annotations(
    csv_path: str, family: Optional[str] = None
) -> pd.DataFrame:
    """
    Load structure annotations from a CSV file.

    Parameters
    ----------
    csv_path : str
        Path to the CSV file containing annotations.
    family : str, optional
        Filter by protein family if provided.

    Returns
    -------
    pd.DataFrame
        DataFrame with annotation columns from the CSV file.

    Raises
    ------
    FileNotFoundError
        If the CSV file does not exist.
    ValueError
        If required columns are missing.
    """
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Annotations file not found: {csv_path}")

    df = pd.read_csv(csv_path)

    required_cols = {"pdb_id", "conformation"}
    if not required_cols.issubset(df.columns):
        raise ValueError(f"CSV must contain columns: {required_cols}")

    if family and "family" in df.columns:
        df = df[df["family"] == family]

    return df


def load_from_input_dir(input_dir: str = "./input") -> pd.DataFrame:
    """
    Scan input directory for PDB files and return metadata.

    Parameters
    ----------
    input_dir : str
        Path to directory containing .pdb files.

    Returns
    -------
    pd.DataFrame
        DataFrame with pdb_id and file_path for each .pdb file found.
    """
    pdb_files = list(Path(input_dir).glob("*.pdb"))

    data = []
    for pdb_file in sorted(pdb_files):
        pdb_id = pdb_file.stem.upper()
        data.append(
            {"pdb_id": pdb_id, "file_path": str(pdb_file), "file_exists": True}
        )

    return pd.DataFrame(data)
