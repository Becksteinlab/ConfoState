# Person 3 Work Plan (ML Training & Evaluation)

**Owner:** Chenou  
**Date:** 2026-07-13  
**Branch:** person3-ml-training-eval  
**Target milestone:** Phase 3 complete by 2026-07-27

---

## Scope

Build the end-to-end ML pipeline for ConfoState:

1. Dataset assembly and split logic
2. Baseline model training
3. Evaluation + report generation
4. Model artifact management / registry

Primary deliverables:
- confostate/data/datasets.py
- confostate/models/baseline.py
- confostate/models/train.py
- confostate/models/evaluate.py
- confostate/models/registry.py
- tests for datasets/model training/evaluation
- trained artifacts in data/models/
- evaluation report in docs/reports/

---

## Dependencies and Risk Controls

### Needed from Person 1 and 2
- Stable annotations schema in data/annotations/leu_t_transporters.csv
- Feature vectors for training rows (or at least a subset)

### Risk if features are delayed
- Use a synthetic feature table to unblock model/training/evaluation development.
- Keep synthetic schema aligned with expected real feature names.
- Add a quick integration check that can switch from synthetic to real features by changing only file paths.

### Definition of done for integration
- Train command runs successfully from raw tabular features + labels.
- Evaluation command produces metrics and confusion matrix artifact.
- Registry points to a reproducible model artifact and metadata.

---

## Week-by-Week Plan

## Week 1 (2026-07-13 to 2026-07-19): Pipeline Skeleton + Baselines

### Day 1: Data contract and dataset loader
- Finalize expected columns:
  - keys: pdb_id, family, conformation
  - features: numeric columns only
- Implement confostate/data/datasets.py:
  - load_dataset(annotations_csv, features_csv)
  - validate label and key integrity
  - make_split(strategy="stratified", test_size=0.2, random_state=...)

### Day 2: Baseline model module
- Implement confostate/models/baseline.py:
  - logistic regression baseline
  - random forest baseline
  - SVM baseline
- Add uniform interface:
  - get_model(name, random_state, class_weight)

### Day 3: Training pipeline
- Implement confostate/models/train.py:
  - fit single model
  - cross-validation score summary
  - save artifact + metadata
- Save outputs under data/models/{family}/{model_name}/

### Day 4: Evaluation module
- Implement confostate/models/evaluate.py:
  - confusion matrix
  - per-class precision/recall/F1
  - macro and weighted scores
  - optional ROC-AUC (when applicable)
- Emit markdown report to docs/reports/

### Day 5: Smoke tests + first run
- Add tests for:
  - dataset split stability
  - model train/predict shape and class consistency
  - evaluation output keys and file generation
- Run first end-to-end experiment with available data or synthetic fallback

## Week 2 (2026-07-20 to 2026-07-27): Hardening + Reporting + Handoff

### Day 6-7: Hyperparameter tuning and comparison
- Add small grid/random search for each baseline model
- Compare by macro-F1 and balanced accuracy
- Select default baseline for each family

### Day 8: Registry and reproducibility
- Implement confostate/models/registry.py:
  - register_model(family, model_name, artifact_path, metrics, data_version)
  - load_registered_model(family)
- Include metadata fields:
  - timestamp, git commit hash, feature schema hash, random_state

### Day 9: Final report package
- Produce docs/reports/phase3-baseline-report.md
- Include:
  - train/test split method
  - model comparison table
  - per-state metrics
  - known limitations and next steps

### Day 10: Handoff to Person 4 and Person 5
- Share:
  - top model artifacts
  - feature importance-compatible model outputs
  - stable prediction API contract for explainability and CLI

---

## Suggested File Interfaces

### confostate/data/datasets.py
- load_dataset(annotations_csv: str, features_csv: str, family: str | None = None)
- train_test_split_dataset(df, label_col="conformation", test_size=0.2, random_state=42)

### confostate/models/baseline.py
- get_baseline_models(random_state=42) -> dict[str, estimator]
- train_model(estimator, X_train, y_train)

### confostate/models/train.py
- run_training(config: dict) -> dict
- save_model_artifact(model, out_dir, metadata)

### confostate/models/evaluate.py
- evaluate_model(model, X_test, y_test, labels=None) -> dict
- write_evaluation_report(metrics: dict, output_path: str)

### confostate/models/registry.py
- register_model(...)
- get_registered_model(family: str)

---

## Daily Execution Checklist

- Confirm branch and pull latest main changes (if needed)
- Implement one scoped unit of functionality
- Add or update tests
- Run local test subset
- Commit with concise message
- Post async update in team channel with blockers/dependencies

---

## Communication Cadence

- Tuesday standup: report progress, current blocker, next 48h plan
- Async updates: at least every 2 working days in #confostate-dev
- Dependency syncs:
  - with Person 2 on feature table schema
  - with Person 4 on importance/explanation-ready outputs

---

## Exit Criteria (Phase 3 Complete)

- End-to-end training command works on at least one family
- >=2 baseline models compared and documented
- Evaluation report generated with per-state metrics
- Model registry points to reproducible artifacts
- Person 4 receives model + outputs needed for explainability
