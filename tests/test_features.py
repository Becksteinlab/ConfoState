"""Tests for confostate.features package."""

from pathlib import Path

import pytest

from confostate.data.loader import load_annotations
from confostate.features import extract_features, extract_features_batch
from confostate.features._structure import load_structure
from confostate.features.cavity import extract_cavity_features
from confostate.features.domains import extract_domain_features
from confostate.features.orientation import extract_orientation_features
from confostate.features.rmsd import extract_rmsd_features

INPUT_DIR = Path(__file__).resolve().parent.parent / "input"
ANNOTATIONS = Path(__file__).resolve().parent.parent / "data/annotations/leu_t_transporters.csv"


@pytest.fixture(scope="module")
def sample_pdb() -> str:
    path = INPUT_DIR / "3F3E.pdb"
    if not path.exists():
        pytest.skip("Sample PDB not found. Run scripts/download_structures.py first.")
    return str(path)


@pytest.fixture(scope="module")
def structure(sample_pdb):
    return load_structure(sample_pdb, pdb_id="3F3E")


def test_cavity_features(structure):
    features = extract_cavity_features(structure)
    assert "cavity_volume" in features
    assert "cavity_accessibility_in" in features
    assert "cavity_accessibility_out" in features
    assert features["cavity_volume"] > 0


def test_domain_features(structure):
    features = extract_domain_features(structure, reference_dir=str(INPUT_DIR))
    assert "domain_TM1_TM7_distance" in features
    assert features["domain_TM1_TM7_distance"] > 0
    assert 0 <= features["domain_TM1_TM7_angle"] <= 180


def test_domain_delta_features_self(structure):
    """Delta vs same structure (3F3E) should be approximately zero."""
    if not (INPUT_DIR / "3F3E.pdb").exists():
        pytest.skip("Reference PDB 3F3E not downloaded")
    features = extract_domain_features(structure, reference_dir=str(INPUT_DIR))
    key = "domain_TM1_TM7_distance_delta_vs_3F3E"
    assert key in features
    assert features[key] == pytest.approx(0.0, abs=0.01)


def test_domain_delta_features_different_conformation():
    """IF-open 3F3A should have non-zero delta vs OF-open reference 3F3E."""
    path = INPUT_DIR / "3F3A.pdb"
    if not path.exists() or not (INPUT_DIR / "3F3E.pdb").exists():
        pytest.skip("Reference PDBs not downloaded")
    structure = load_structure(str(path), pdb_id="3F3A")
    features = extract_domain_features(structure, reference_dir=str(INPUT_DIR))
    key = "domain_TM1_TM7_distance_delta_vs_3F3E"
    assert key in features
    assert abs(features[key]) > 0.01


def test_orientation_features(structure):
    features = extract_orientation_features(structure)
    assert "opm_tilt_angle" in features
    assert "opm_rotation_angle" in features
    assert "opm_depth" in features


def test_rmsd_features(sample_pdb, structure):
    # Self-RMSD should be near zero when reference is available.
    if not (INPUT_DIR / "3F3A.pdb").exists():
        pytest.skip("Reference PDB 3F3A not downloaded")
    features = extract_rmsd_features(structure, reference_dir=str(INPUT_DIR))
    assert "rmsd_OF_open" in features
    assert features["rmsd_OF_open"] < 1.0  # 3F3E vs itself
    assert features["rmsd_min"] >= 0


def test_extract_features(sample_pdb):
    annotations = load_annotations(str(ANNOTATIONS))
    row = annotations[annotations["pdb_id"] == "3F3E"].iloc[0].to_dict()
    features = extract_features(sample_pdb, annotations_row=row, reference_dir=str(INPUT_DIR))
    assert "cavity_volume" in features
    assert "domain_TM1_TM7_distance" in features
    assert "domain_TM1_TM7_distance_delta_vs_3F3E" in features
    assert "opm_tilt_angle" in features
    # OPM columns are N/A in CSV, so tilt must be computed from coordinates.
    assert features["opm_tilt_angle"] > 0


def test_extract_features_batch(sample_pdb):
    df = extract_features_batch([sample_pdb], reference_dir=str(INPUT_DIR))
    assert len(df) == 1
    assert "cavity_volume" in df.columns
    assert df.iloc[0]["pdb_id"] == "3F3E"
