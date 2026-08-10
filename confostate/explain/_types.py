"""Shared types for the explainability layer."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class PredictionResult:
    """Output of a conformational-state classifier."""

    pdb_id: str
    predicted_state: str
    probabilities: dict[str, float]
    features: dict[str, float]
    family: str = "LeuT"

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> PredictionResult:
        """Build a prediction from a plain dict."""
        return cls(
            pdb_id=str(data["pdb_id"]),
            predicted_state=str(data["predicted_state"]),
            probabilities={
                str(k): float(v) for k, v in data["probabilities"].items()
            },
            features={str(k): float(v) for k, v in data["features"].items()},
            family=str(data.get("family", "LeuT")),
        )


@dataclass
class FeatureImportance:
    """Importance of a single feature for a prediction."""

    feature_name: str
    display_name: str
    importance: float
    value: float
    direction: str  # "supports" or "opposes"


@dataclass
class Citation:
    """Literature reference for a state or feature."""

    key: str
    label: str
    reference: str
    doi: Optional[str] = None
    pubmed_id: Optional[str] = None


@dataclass
class ExplanationResult:
    """Full explanation for a single prediction."""

    pdb_id: str
    predicted_state: str
    confidence: float
    text: str
    markdown: str
    top_features: list[FeatureImportance] = field(default_factory=list)
    citations: list[Citation] = field(default_factory=list)
    method: str = "heuristic"
