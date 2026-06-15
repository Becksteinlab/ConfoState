"""CSV data loader for conformational state annotations."""

import os
from pathlib import Path
from typing import Optional
import pandas as pd


def load_annotations(csv_path: str, family: Optional[str] = None) -> pd.DataFrame:
    """
    Load structure annotations from a CSV file.
    
    Parameters
    ----------
    csv_path : str
        Path to the CSV file containing annotations
    family : str, optional
        Filter by protein family if provided
    
    Returns
    -------
    pd.DataFrame
        DataFrame with columns: pdb_id, conformation, reference, experimental_method
        
    Raises
    ------
    FileNotFoundError
        If the CSV file does not exist
    
    Examples
    --------
    >>> df = load_annotations("data/annotations/leu_t_transporters.csv")
    >>> print(df.head())
    >>> 
    >>> # Filter by family
    >>> df = load_annotations("data/annotations/leu_t_transporters.csv", family="LeuT")
    """
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Annotations file not found: {csv_path}")
    
    df = pd.read_csv(csv_path)
    
    # Validate required columns
    required_cols = {"pdb_id", "conformation"}
    if not required_cols.issubset(df.columns):
        raise ValueError(f"CSV must contain columns: {required_cols}")
    
    # Filter by family if requested
    if family and "family" in df.columns:
        df = df[df["family"] == family]
    
    return df


def load_from_input_dir(input_dir: str = "./input") -> pd.DataFrame:
    """
    Scan input directory for PDB files and return metadata.
    
    Parameters
    ----------
    input_dir : str
        Path to directory containing .pdb files
    
    Returns
    -------
    pd.DataFrame
        DataFrame with pdb_id and file_path for each .pdb file found
    
    Examples
    --------
    >>> df = load_from_input_dir("./input")
    >>> print(df)
    """
    pdb_files = list(Path(input_dir).glob("*.pdb"))
    
    data = []
    for pdb_file in sorted(pdb_files):
        pdb_id = pdb_file.stem.upper()
        data.append({
            "pdb_id": pdb_id,
            "file_path": str(pdb_file),
            "file_exists": True
        })
    
    return pd.DataFrame(data)
