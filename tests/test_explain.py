"""Tests for confostate.explain package."""

from __future__ import annotations

import numpy as np
import pytest

from confostate.explain import (
    ExplanationResult,
    FeatureImportance,
    PredictionResult,
    display_name,
    explain,
    state_label,
)
from confostate.explain.citations import format_citation, get_citations
from confostate.explain.importance import (
    extract_coefficient_importance,
    extract_heuristic_importance,
    extract_permutation_importance,
    rank_importances,
)


@pytest.fixture
def sample_prediction() -> PredictionResult:
    return PredictionResult(
        pdb_id="3F3E",
        predicted_state="OF_open",
        probabilities={
            "IF_open": 0.05,
            "OF_open": 0.80,
            "Occluded": 0.10,
            "Intermediate": 0.05,
        },
        features={
            "domain_TM1_TM7_distance": 22.5,
            "domain_gate_TM1_TM6_distance": 26.1,
            "rmsd_OF_open": 1.2,
            "rmsd_IF_open": 3.8,
            "cavity_accessibility_out": 0.52,
            "cavity_volume": 480.0,
        },
        family="LeuT",
    )


def test_display_name():
    assert display_name("domain_TM1_TM7_distance") == "TM1–TM7 gate distance"
    assert display_name("unknown_feature") == "unknown feature"


def test_state_label():
    assert state_label("OF_open") == "outward-facing open"
    assert state_label("Custom_state") == "Custom state"


def test_heuristic_importance(sample_prediction):
    importances = extract_heuristic_importance(
        sample_prediction.features,
        sample_prediction.predicted_state,
        family="LeuT",
    )
    assert len(importances) == len(sample_prediction.features)
    names = {item.feature_name for item in importances}
    assert "rmsd_OF_open" in names
    top = rank_importances(importances, top_k=3)
    assert len(top) == 3
    assert all(item.importance >= 0 for item in top)


def test_coefficient_importance(sample_prediction):
    coefficients = {
        "domain_TM1_TM7_distance": 0.5,
        "rmsd_OF_open": -1.0,
        "rmsd_IF_open": 0.3,
    }
    importances = extract_coefficient_importance(
        coefficients,
        sample_prediction.features,
        sample_prediction.predicted_state,
    )
    rmsd_of = next(i for i in importances if i.feature_name == "rmsd_OF_open")
    assert rmsd_of.direction == "opposes"
    assert rmsd_of.importance < 0


class DummyModel:
    """Minimal sklearn-like model for permutation-importance tests."""

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        # Higher domain_TM1_TM7_distance -> more OF_open probability.
        scores = X[:, 0] if X.shape[1] >= 1 else np.zeros(len(X))
        of_prob = np.clip(scores / 30.0, 0.0, 1.0)
        if_prob = 1.0 - of_prob
        return np.column_stack([if_prob, of_prob])


def test_permutation_importance():
    feature_names = ["domain_TM1_TM7_distance", "rmsd_OF_open"]
    X = np.array(
        [
            [22.0, 1.2],
            [18.0, 2.5],
            [20.0, 1.8],
        ]
    )
    model = DummyModel()
    baseline_proba = model.predict_proba(X)[0]
    importances = extract_permutation_importance(
        model,
        X,
        feature_names,
        baseline_proba,
        random_state=42,
    )
    assert len(importances) == 2
    assert importances[0].feature_name in feature_names


def test_get_citations(sample_prediction):
    citations = get_citations(
        predicted_state="OF_open",
        feature_names=["domain_TM1_TM7_distance", "rmsd_OF_open"],
        family="LeuT",
    )
    # State and features share Singh et al. 2008 — deduplicated.
    assert len(citations) == 1
    assert citations[0].key == "OF_open"
    formatted = format_citation(citations[0])
    assert "DOI" in formatted
    assert "PubMed" in formatted


def test_get_citations_deduplicates_shared_doi():
    citations = get_citations(
        predicted_state="Occluded",
        feature_names=["rmsd_Occluded", "cavity_volume"],
        family="LeuT",
    )
    dois = [c.doi for c in citations if c.doi]
    assert len(dois) == len(set(dois))
    assert len(citations) == 2


def test_explain_returns_result(sample_prediction):
    result = explain(sample_prediction)
    assert isinstance(result, ExplanationResult)
    assert result.pdb_id == "3F3E"
    assert result.predicted_state == "OF_open"
    assert result.confidence == pytest.approx(0.80)
    assert result.method == "heuristic"
    assert len(result.top_features) <= 5
    assert "3F3E" in result.text
    assert "outward-facing open" in result.text
    assert "## Prediction" in result.markdown


def test_explain_text_and_markdown_formats(sample_prediction):
    text = explain(sample_prediction, output_format="text")
    markdown = explain(sample_prediction, output_format="markdown")
    assert isinstance(text, str)
    assert isinstance(markdown, str)
    assert "References:" in text
    assert "### References" in markdown


def test_explain_from_dict(sample_prediction):
    result = explain(sample_prediction.__dict__)
    assert result.pdb_id == "3F3E"


def test_explain_with_provided_importances(sample_prediction):
    provided = [
        FeatureImportance(
            feature_name="domain_TM1_TM7_distance",
            display_name="TM1–TM7 gate distance",
            importance=0.9,
            value=22.5,
            direction="supports",
        )
    ]
    result = explain(sample_prediction, importances=provided, top_k=1)
    assert result.method == "provided"
    assert len(result.top_features) == 1
    assert result.top_features[0].feature_name == "domain_TM1_TM7_distance"
