"""Template-based explanation rendering."""

from __future__ import annotations

from typing import Sequence

from confostate.explain._types import (
    Citation,
    FeatureImportance,
    PredictionResult,
)
from confostate.explain.citations import format_citation, state_label


def _format_value(value: float) -> str:
    if abs(value) >= 100:
        return f"{value:.1f}"
    if abs(value) >= 10:
        return f"{value:.2f}"
    return f"{value:.3f}"


def _feature_sentence(item: FeatureImportance, predicted_state: str) -> str:
    value_str = _format_value(item.value)
    state_name = state_label(predicted_state)
    verb = "supports" if item.direction == "supports" else "is atypical for"
    return (
        f"The {item.display_name} ({value_str}) {verb} "
        f"an {state_name} conformation."
    )


def render_text(
    prediction: PredictionResult,
    top_features: Sequence[FeatureImportance],
    citations: Sequence[Citation],
    method: str,
) -> str:
    """Render a plain-text explanation."""
    confidence = prediction.probabilities.get(prediction.predicted_state, 0.0)
    state_name = state_label(prediction.predicted_state)
    lines = [
        (
            f"Structure {prediction.pdb_id} is predicted to be "
            f"{state_name} ({confidence:.0%} confidence)."
        ),
        "",
        "Key structural evidence:",
    ]

    if top_features:
        for item in top_features:
            sentence = _feature_sentence(item, prediction.predicted_state)
            lines.append(f"- {sentence}")
    else:
        lines.append("- No distinguishing features were identified.")

    lines.extend(["", f"Importance method: {method}."])

    if citations:
        lines.extend(["", "References:"])
        for citation in citations:
            lines.append(f"- {format_citation(citation)}")

    return "\n".join(lines)


def render_markdown(
    prediction: PredictionResult,
    top_features: Sequence[FeatureImportance],
    citations: Sequence[Citation],
    method: str,
) -> str:
    """Render a Markdown explanation."""
    confidence = prediction.probabilities.get(prediction.predicted_state, 0.0)
    state_name = state_label(prediction.predicted_state)
    lines = [
        f"## Prediction: {prediction.pdb_id}",
        "",
        (
            f"**State:** {state_name} "
            f"({prediction.predicted_state})  \n"
            f"**Confidence:** {confidence:.0%}  \n"
            f"**Family:** {prediction.family}"
        ),
        "",
        "### Key structural evidence",
        "",
    ]

    if top_features:
        for item in top_features:
            lines.append(
                f"- {_feature_sentence(item, prediction.predicted_state)}"
            )
    else:
        lines.append("- No distinguishing features were identified.")

    lines.extend(["", f"*Importance method: {method}*", ""])

    if citations:
        lines.extend(["### References", ""])
        for citation in citations:
            ref = citation.reference
            links: list[str] = []
            if citation.doi:
                links.append(f"[DOI](https://doi.org/{citation.doi})")
            if citation.pubmed_id:
                links.append(
                    f"[PubMed](https://pubmed.ncbi.nlm.nih.gov/"
                    f"{citation.pubmed_id}/)"
                )
            suffix = f" ({', '.join(links)})" if links else ""
            lines.append(f"- {ref}{suffix}")

    return "\n".join(lines)
