"""ConfoState package for membrane protein conformational state classification."""

__version__ = "0.1.0"

from confostate.data.loader import load_annotations
from confostate.features import extract_features

__all__ = ["load_annotations", "extract_features"]
