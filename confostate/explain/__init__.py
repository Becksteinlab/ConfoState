"""Explainability layer for conformational-state predictions."""

from __future__ import annotations

from typing import Any, Literal, Optional, Sequence, Union, overload

from confostate.explain._types import (
    Citation,
    ExplanationResult,
    FeatureImportance,
    PredictionResult,
)
from confostate.explain.citations import get_citations, state_label
from confostate.explain.importance import (
    FEATURE_DISPLAY_NAMES,
    display_name,
    rank_importances,
    resolve_importances,
)
from confostate.explain.render import render_markdown, render_text

__all__ = [
    "Citation",
    "ExplanationResult",
    "FeatureImportance",
    "PredictionResult",
    "FEATURE_DISPLAY_NAMES",
    "display_name",
    "explain",
    "state_label",
]


@overload
def explain(
    prediction: Union[PredictionResult, dict[str, Any]],
    *,
    top_k: int = 5,
    importances: Optional[Sequence[FeatureImportance]] = None,
    model: Optional[Any] = None,
    feature_matrix: Optional[Any] = None,
    feature_names: Optional[Sequence[str]] = None,
    coefficients: Optional[dict[str, float]] = None,
    output_format: Literal["result"] = "result",
) -> ExplanationResult: ...


@overload
def explain(
    prediction: Union[PredictionResult, dict[str, Any]],
    *,
    top_k: int = 5,
    importances: Optional[Sequence[FeatureImportance]] = None,
    model: Optional[Any] = None,
    feature_matrix: Optional[Any] = None,
    feature_names: Optional[Sequence[str]] = None,
    coefficients: Optional[dict[str, float]] = None,
    output_format: Literal["text", "markdown"],
) -> str: ...


def explain(
    prediction: Union[PredictionResult, dict[str, Any]],
    *,
    top_k: int = 5,
    importances: Optional[Sequence[FeatureImportance]] = None,
    model: Optional[Any] = None,
    feature_matrix: Optional[Any] = None,
    feature_names: Optional[Sequence[str]] = None,
    coefficients: Optional[dict[str, float]] = None,
    output_format: Literal["result", "text", "markdown"] = "result",
) -> Union[ExplanationResult, str]:
    """
    Generate a human-readable explanation for a classifier prediction.

    Parameters
    ----------
    prediction
        PredictionResult or dict with pdb_id, predicted_state,
        probabilities, and features.
    top_k
        Number of top features to include in the explanation.
    importances
        Pre-computed feature importances (from Person 3's pipeline).
    model
        Optional sklearn-compatible model for permutation importance.
    feature_matrix
        Feature matrix for permutation importance (single row or batch).
    feature_names
        Feature names aligned with feature_matrix columns.
    coefficients
        Linear-model coefficients keyed by feature name.
    output_format
        ``"result"`` returns ExplanationResult; ``"text"`` or
        ``"markdown"`` returns rendered strings.

    Returns
    -------
    ExplanationResult or str
        Full explanation object or rendered text.
    """
    if not isinstance(prediction, PredictionResult):
        prediction = PredictionResult.from_dict(prediction)

    resolved, method = resolve_importances(
        features=prediction.features,
        predicted_state=prediction.predicted_state,
        family=prediction.family,
        importances=importances,
        model=model,
        feature_matrix=feature_matrix,
        feature_names=feature_names,
        coefficients=coefficients,
    )
    top_features = rank_importances(resolved, top_k=top_k)
    citations = get_citations(
        predicted_state=prediction.predicted_state,
        feature_names=[item.feature_name for item in top_features],
        family=prediction.family,
    )

    confidence = prediction.probabilities.get(
        prediction.predicted_state, 0.0
    )
    text = render_text(prediction, top_features, citations, method)
    markdown = render_markdown(
        prediction, top_features, citations, method
    )

    result = ExplanationResult(
        pdb_id=prediction.pdb_id,
        predicted_state=prediction.predicted_state,
        confidence=confidence,
        text=text,
        markdown=markdown,
        top_features=top_features,
        citations=citations,
        method=method,
    )

    if output_format == "text":
        return result.text
    if output_format == "markdown":
        return result.markdown
    return result
