# Person 4: Explainability & Interpretation Plan

**Date:** 2026-08-10  
**Branch:** `person4-interpretability`  
**Assignees:** Leah, Apollo  
**Status:** In progress

## Goal

Build the explainability layer (`confostate/explain/`) that turns model
predictions and feature vectors into human-readable justifications with
literature citations.

## Approach

1. **Package location:** Move from root `explain/` stub into
   `confostate/explain/` to match the workplan and package layout.
2. **Feature importance:** Support three paths (in order of preference):
   - Explicit importances passed by the caller (from Person 3's pipeline)
   - Permutation importance for sklearn-compatible models with `predict_proba`
   - Heuristic importance from feature values vs. LeuT state profiles (stub
     path while models are unavailable)
3. **Rendering:** Template-based natural language (no LLM dependency for v1).
   Keeps explanations deterministic, testable, and free of GPU/API cost.
4. **Citations:** Curated DOI/PubMed mappings for LeuT states and key
   structural features, pulled from the annotations reference column.
5. **Public API:** `explain(prediction) -> ExplanationResult` with text and
   markdown output formats.

## Key decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| LLM rendering | Deferred | Workplan mentions Llama/ASU tokens; template v1 unblocks Person 5 CLI |
| SHAP | Deferred | Heavy dependency; permutation + heuristics sufficient for v1 |
| sklearn | Optional import | Used when available; heuristic fallback keeps package lightweight |
| Synthetic data | Heuristic profiles | Workplan: "make up sh**t to move forward" until Person 3 delivers models |

## Deliverables

- [x] `confostate/explain/importance.py`
- [x] `confostate/explain/render.py`
- [x] `confostate/explain/citations.py`
- [x] `confostate/explain/__init__.py` with `explain()`
- [x] `tests/test_explain.py`
- [x] `docs/explainability.md`

## Dependencies

- **Person 2:** Feature names and semantics (`docs/features/features.md`)
- **Person 3:** Trained models and real permutation importances (future)
- **Blocks:** Person 5 CLI integration

## Future work

- SHAP values for tree/neural models
- LLM polish pass (local Llama at ASU)
- Multi-family citation and profile tables
