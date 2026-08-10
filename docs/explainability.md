# Explainability

ConfoState generates human-readable explanations for conformational-state
predictions. The explainability layer sits downstream of feature extraction
(Person 2) and model inference (Person 3).

## Package layout

```
confostate/explain/
├── __init__.py       # explain() public API
├── _types.py         # PredictionResult, ExplanationResult, etc.
├── importance.py     # Feature importance extraction
├── render.py         # Template-based text/markdown rendering
└── citations.py      # Literature references (DOI, PubMed)
```

## Quick start

```python
from confostate.explain import explain, PredictionResult

prediction = PredictionResult(
    pdb_id="3F3E",
    predicted_state="OF_open",
    probabilities={"IF_open": 0.05, "OF_open": 0.80, "Occluded": 0.10,
                   "Intermediate": 0.05},
    features={
        "domain_TM1_TM7_distance": 22.5,
        "rmsd_OF_open": 1.2,
        "cavity_accessibility_out": 0.52,
    },
)

result = explain(prediction)
print(result.text)
```

Plain-text output:

```
Structure 3F3E is predicted to be outward-facing open (80% confidence).

Key structural evidence:
- The TM1–TM7 gate distance (22.50) supports an outward-facing open conformation.
- The RMSD to outward-open reference (3F3E) (1.200) supports an outward-facing open conformation.
...

Importance method: heuristic.

References:
- Singh et al., Science 2008 — DOI: 10.1126/science.1159299 — PubMed: 18403708
```

Markdown output is available via `explain(prediction, output_format="markdown")`.

## Importance methods

The `explain()` function picks the best available importance source:

| Priority | Method | When used |
|----------|--------|-----------|
| 1 | `provided` | Caller passes pre-computed importances (Person 3 pipeline) |
| 2 | `coefficient` | Linear-model coefficients are supplied |
| 3 | `permutation` | sklearn-compatible model + feature matrix |
| 4 | `heuristic` | Default stub: compares features to LeuT state profiles |

### Heuristic mode (current default)

While Person 3's models are in development, heuristic importance compares
each feature to literature-informed LeuT state profiles in
`confostate/explain/importance.py`. RMSD features matching the predicted
state receive higher scores; domain and cavity features are scored by
agreement with the profile.

### Permutation importance

When a trained model with `predict_proba` is available:

```python
import numpy as np
from confostate.explain import explain

result = explain(
    prediction,
    model=trained_model,
    feature_matrix=X,          # shape (n_samples, n_features)
    feature_names=feature_cols,
)
```

### Provided importances

Person 3 can pass SHAP or other importances directly:

```python
from confostate.explain import FeatureImportance, explain

importances = [
    FeatureImportance(
        feature_name="domain_TM1_TM7_distance",
        display_name="TM1–TM7 gate distance",
        importance=0.85,
        value=22.5,
        direction="supports",
    ),
]
result = explain(prediction, importances=importances)
```

## Citations

`confostate/explain/citations.py` maps LeuT states and key structural
features to curated DOI and PubMed references. Citations are included
automatically in rendered output.

Supported states: `IF_open`, `OF_open`, `Occluded`, `Intermediate`.

## Integration with Person 5 (CLI)

The planned `Classifier.classify()` API will call `explain()` internally.
Expected flow:

```
PDB → extract_features() → model.predict() → explain() → PredictionResult
```

## Testing

```bash
pip install -e ".[dev]"
pytest tests/test_explain.py -v
```

## Future work

- SHAP values for tree and neural models
- LLM polish pass (local Llama at ASU)
- Multi-family citation and profile tables
- HTML explanation renderer for CLI `--output-format html`
