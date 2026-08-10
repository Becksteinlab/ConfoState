"""Literature citations for explainability output."""

from __future__ import annotations

from typing import Sequence

from confostate.explain._types import Citation

# Curated references for LeuT conformational states and structural motifs.
LEUT_STATE_CITATIONS: dict[str, Citation] = {
    "IF_open": Citation(
        key="IF_open",
        label="Inward-facing open",
        reference="Yamashita et al., Nature 2005",
        doi="10.1038/nature03578",
        pubmed_id="15880103",
    ),
    "OF_open": Citation(
        key="OF_open",
        label="Outward-facing open",
        reference="Singh et al., Science 2008",
        doi="10.1126/science.1159299",
        pubmed_id="18403708",
    ),
    "Occluded": Citation(
        key="Occluded",
        label="Occluded",
        reference="Shi et al., Nature 2008",
        doi="10.1038/nature06932",
        pubmed_id="18497808",
    ),
    "Intermediate": Citation(
        key="Intermediate",
        label="Intermediate",
        reference="Claxton et al., J. Mol. Biol. 2010",
        doi="10.1016/j.jmb.2010.09.022",
        pubmed_id="20869387",
    ),
}

LEUT_FEATURE_CITATIONS: dict[str, Citation] = {
    "domain_TM1_TM7_distance": Citation(
        key="domain_TM1_TM7_distance",
        label="TM1–TM7 gate distance",
        reference="Singh et al., Science 2008 (outward-open gate)",
        doi="10.1126/science.1159299",
        pubmed_id="18403708",
    ),
    "domain_gate_TM1_TM6_distance": Citation(
        key="domain_gate_TM1_TM6_distance",
        label="TM1–TM6 gate opening",
        reference="Yamashita et al., Nature 2005 (inward-open gate)",
        doi="10.1038/nature03578",
        pubmed_id="15880103",
    ),
    "cavity_volume": Citation(
        key="cavity_volume",
        label="Binding-site cavity",
        reference="Yamashita et al., Nature 2005",
        doi="10.1038/nature03578",
        pubmed_id="15880103",
    ),
    "rmsd_IF_open": Citation(
        key="rmsd_IF_open",
        label="RMSD to inward-open reference",
        reference="Yamashita et al., Nature 2005 (3F3A)",
        doi="10.1038/nature03578",
        pubmed_id="15880103",
    ),
    "rmsd_OF_open": Citation(
        key="rmsd_OF_open",
        label="RMSD to outward-open reference",
        reference="Singh et al., Science 2008 (3F3E)",
        doi="10.1126/science.1159299",
        pubmed_id="18403708",
    ),
    "rmsd_Occluded": Citation(
        key="rmsd_Occluded",
        label="RMSD to occluded reference",
        reference="Shi et al., Nature 2008 (3F4J)",
        doi="10.1038/nature06932",
        pubmed_id="18497808",
    ),
    "rmsd_Intermediate": Citation(
        key="rmsd_Intermediate",
        label="RMSD to intermediate reference",
        reference="Claxton et al., J. Mol. Biol. 2010 (3USI)",
        doi="10.1016/j.jmb.2010.09.022",
        pubmed_id="20869387",
    ),
}

STATE_LABELS: dict[str, str] = {
    "IF_open": "inward-facing open",
    "OF_open": "outward-facing open",
    "Occluded": "occluded",
    "Intermediate": "intermediate",
}


def state_label(state: str) -> str:
    """Return a human-readable state name."""
    return STATE_LABELS.get(state, state.replace("_", " "))


def get_citations(
    predicted_state: str,
    feature_names: Sequence[str],
    family: str = "LeuT",
) -> list[Citation]:
    """
    Collect literature citations for a predicted state and its top features.

    Deduplicates by DOI when the same reference covers multiple items.
    """
    if family != "LeuT":
        return []

    seen_dois: set[str] = set()
    citations: list[Citation] = []

    state_citation = LEUT_STATE_CITATIONS.get(predicted_state)
    if state_citation is not None:
        citations.append(state_citation)
        if state_citation.doi:
            seen_dois.add(state_citation.doi)

    for name in feature_names:
        feature_citation = LEUT_FEATURE_CITATIONS.get(name)
        if feature_citation is None:
            continue
        if feature_citation.doi and feature_citation.doi in seen_dois:
            continue
        citations.append(feature_citation)
        if feature_citation.doi:
            seen_dois.add(feature_citation.doi)

    return citations


def format_citation(citation: Citation) -> str:
    """Format a single citation for plain-text output."""
    parts = [citation.reference]
    if citation.doi:
        parts.append(f"DOI: {citation.doi}")
    if citation.pubmed_id:
        parts.append(f"PubMed: {citation.pubmed_id}")
    return " — ".join(parts)
