# 6-Person Team Workplan for ConfoState

**Date:** 2026-06-15  
**Status:** Planning Phase  
**Team Size:** 6 people

---

## Overview

ConfoState development split into 6 parallel work streams, each led by one team member. Dependencies are kept minimal to enable parallel progress.

---

## Person 1: Data Curation & Annotation

**Role:** Data lead  
**Duration:** 3–4 weeks  
**Milestone:** Phase 1 completion

### Tasks

1. **Verify and curate LeuT annotations**
   - Cross-check each of the 25 PDB entries in `data/annotations/leu_t_transporters.csv`
   - Fetch authoritative metadata from RCSB API (resolution, experimental method, release date, DOI)
   - Verify conformational state labels against primary literature
   - Add DOI and PubMed IDs to the reference column

2. **Fetch membrane orientations from OPM**
   - For each structure, retrieve orientation from OPM database or submit calculation job
   - Add columns to CSV: `opm_tm_count`, `opm_tilt_angle`, `opm_rotation_angle`

3. **Build data validation pipeline**
   - Create `confostate/data/validators.py` with schema checks for annotations CSV
   - Document data quality requirements in `docs/data-curation.md`

4. **Expand to additional protein families** (if time permits)
   - Curate annotations for 1–2 additional families (e.g., ABC transporters, GPCRs)

### Deliverables

- ✓ Verified `data/annotations/leu_t_transporters.csv` with authoritative metadata
- ✓ OPM orientation data added to annotations
- ✓ `confostate/data/validators.py`
- ✓ Data curation guide in `docs/`

### Blockers / Dependencies

- Requires access to RCSB API and OPM database (no code dependencies on others)

---

## Person 2: Feature Engineering

**Role:** Structural biology & feature engineering lead  
**Duration:** 3–4 weeks  
**Milestone:** Phase 2 completion

### Tasks

1. **Implement cavity/solvent accessibility features**
   - Create `confostate/features/cavity.py`
   - Use MSMS or PyMOL to compute binding site volume and solvent-accessible surface area
   - Features: `cavity_volume`, `cavity_accessibility_in`, `cavity_accessibility_out`

2. **Implement domain distance features**
   - Create `confostate/features/domains.py`
   - Define key helices/domains for LeuT (e.g., TM1–TM7, substrate-binding residues)
   - Compute pairwise distances and angles; track changes relative to reference structures

3. **Implement RMSD-to-reference features**
   - Create `confostate/features/rmsd.py`
   - Select 2–3 reference structures per state from curated dataset
   - Compute RMSD and alignment scores

4. **Implement OPM orientation features**
   - Create `confostate/features/orientation.py`
   - Use OPM tilt, rotation, and depth data as features

5. **Add symmetry features** (optional)
   - Create `confostate/features/symmetry.py`
   - Compute repeat-unit symmetry score

6. **Implement feature vector exporter**
   - Create `confostate/features/__init__.py` with `extract_features(pdb_path)` → feature dict
   - Unit tests for each module

### Deliverables

- ✓ `confostate/features/` with 5–6 feature modules
- ✓ Tested `extract_features()` function
- ✓ Feature documentation in `docs/features.md`
- ✓ Example feature vectors for all 25 LeuT structures

### Blockers / Dependencies

- Depends on: Data person (for reference structures and OPM data)
- Blocks: ML person (feature vectors needed for training)

---

## Person 3: ML Training & Evaluation

**Role:** Machine learning engineer  
**Duration:** 3–4 weeks  
**Milestone:** Phase 3 completion

### Tasks

1. **Build dataset loader**
   - Create `confostate/data/datasets.py`
   - Combine annotations CSV, PDB structures, and feature vectors
   - Implement train/test splits

2. **Implement baseline models**
   - Create `confostate/models/baseline.py`
   - Logistic regression, Random Forest, SVM
   - Hyperparameter tuning

3. **Build training pipeline**
   - Create `confostate/models/train.py`
   - Cross-validation, early stopping, metric logging
   - Save trained models to disk

4. **Implement evaluation & reporting**
   - Create `confostate/models/evaluate.py`
   - Confusion matrix, precision/recall, per-state metrics
   - Generate evaluation report (HTML/Markdown)

5. **Build model registry**
   - Create `confostate/models/registry.py`
   - Map family → trained model artifact
   - Version tracking

6. **Optional: advanced models**
   - XGBoost, neural networks if time permits

### Deliverables

- ✓ `confostate/models/` with training pipeline
- ✓ Trained baseline models saved to `data/models/`
- ✓ Evaluation report with per-family metrics
- ✓ Model registry and versioning scheme

### Blockers / Dependencies

- Depends on: Feature person (feature extraction), Data person (labels)
- Blocks: Explain person (feature importance for explanations)

---

## Person 4: Explainability & Interpretation

**Role:** Interpretability lead  
**Duration:** 2–3 weeks  
**Milestone:** Phase 4 completion

### Tasks

1. **Implement feature importance extraction**
   - Create `confostate/explain/importance.py`
   - SHAP values, permutation importance, or model-specific methods
   - Map features to human-readable names

2. **Build explanation renderer**
   - Create `confostate/explain/render.py`
   - Convert feature importance → natural language
   - Template-based explanations (e.g., "TM1–TM7 distance of X Å is consistent with {state}")

3. **Add literature linking**
   - Create `confostate/explain/citations.py`
   - Map features/states to curated references (DOI, PubMed ID)
   - Include in explanation text

4. **Implement explanation exporter**
   - Create `confostate/explain/__init__.py` with `explain(prediction)` → explanation text
   - Generate example explanations for all test set structures

5. **Documentation and examples**
   - Write `docs/explainability.md`
   - Example explanation outputs

### Deliverables

- ✓ `confostate/explain/` with full explanation pipeline
- ✓ Human-readable explanations for test structures
- ✓ Explainability documentation with examples

### Blockers / Dependencies

- Depends on: ML person (trained models and feature importance)
- Blocks: CLI person (explanations integrated into output)

---

## Person 5: CLI & Python API

**Role:** Software engineer / DevOps lead  
**Duration:** 2–3 weeks  
**Milestone:** Phase 5 completion

### Tasks

1. **Implement Python API**
   - Create `confostate/classifier.py` with `Classifier` class
   - Methods: `classify(pdb_path, family=None)` → `PredictionResult`
   - `PredictionResult` contains: states dict, probabilities, explanation

2. **Implement CLI**
   - Create `confostate/cli.py` using Click or argparse
   - Command: `confostate classify <pdb_path_or_id> [--family] [--output-format]`
   - Output formats: JSON, plain text, HTML

3. **Add PDB ID lookup**
   - Download structures on the fly from RCSB if given a PDB ID
   - Cache downloaded files

4. **Integration tests**
   - Create `tests/test_api.py` and `tests/test_cli.py`
   - Test end-to-end workflows

5. **Documentation & examples**
   - Update `docs/USAGE.md` with API and CLI examples
   - Create `examples/api_example.py`, `examples/cli_example.sh`

6. **Packaging & distribution**
   - Ensure `pyproject.toml` is complete
   - Test `pip install confostate`

### Deliverables

- ✓ `confostate/classifier.py` with public API
- ✓ `confostate/cli.py` with `confostate classify` command
- ✓ End-to-end integration tests
- ✓ Usage examples and documentation

### Blockers / Dependencies

- Depends on: ML person (models), Explain person (explanations)
- Blocks: None (parallel finalization)

---

## Person 6: Infrastructure, CI, & Testing

**Role:** DevOps / QA engineer  
**Duration:** 2–3 weeks  
**Milestone:** Phase 5+ completion

### Tasks

1. **Set up continuous integration (CI)**
   - Create `.github/workflows/test.yml`
   - Run tests on push to main/dev
   - Test Python 3.9+ versions

2. **Add linting & code quality**
   - Configure Black, Flake8, Pylint in CI
   - Create `.pre-commit` config

3. **Build comprehensive test suite**
   - Create `tests/` directory with unit and integration tests
   - Aim for >80% code coverage
   - Test fixtures for example structures

4. **Add documentation building**
   - Set up Sphinx or similar for auto-generated docs
   - CI builds docs on each commit

5. **Package versioning & release**
   - Set up semantic versioning in `pyproject.toml`
   - Create release checklist and GitHub Actions workflow

6. **Data storage & reproducibility**
   - Document PDB structure download process
   - Create `.gitignore` rules for large files
   - Optional: set up DVC for structure file tracking

7. **Contribution guidelines**
   - Create `CONTRIBUTING.md`
   - Code review template, pull request checklist

### Deliverables

- ✓ `.github/workflows/` with CI/CD pipelines
- ✓ Comprehensive test suite with >80% coverage
- ✓ Linting and code quality checks
- ✓ Documentation build pipeline
- ✓ `CONTRIBUTING.md` and release guidelines

### Blockers / Dependencies

- Depends on: All others (needs all modules to test)
- Blocks: None (runs in parallel, integrates at the end)

---

## Timeline & Milestones

| Phase | Milestone | Target Date | Owner(s) |
|-------|-----------|-------------|----------|
| 1 | Data foundation (curated CSV, OPM) | 2026-06-29 | Person 1 |
| 2 | Feature extraction complete | 2026-07-13 | Person 2 |
| 3 | Baseline models trained & evaluated | 2026-07-27 | Person 3 |
| 4 | Explainability layer complete | 2026-08-03 | Person 4 |
| 5 | CLI & API complete | 2026-08-10 | Person 5 |
| 5+ | CI/CD & testing finalized | 2026-08-17 | Person 6 |

---

## How to Create GitHub Issues

Use one of these methods:

### Option A: GitHub CLI

If you have `gh` installed:

```bash
cd /nfs/homes5/Projects/SLC26/chenou/test/summer-project/ConfoState
gh issue create --title "Person 1: Data Curation & Annotation" --body "..."
```

### Option B: Web Interface

1. Go to https://github.com/your-org/confostate/issues
2. Click "New Issue"
3. Copy title and description from this file

### Option C: Create Issues Programmatically

Script: `scripts/create_github_issues.py` (optional)

```python
import subprocess
import json

issues = [
    {
        "title": "Person 1: Data Curation & Annotation",
        "body": "See Plans/workplan-2026-06-15.md for full details.",
        "assignee": "person1-username",
        "labels": ["phase-1", "data"]
    },
    # ... 5 more issues
]

for issue in issues:
    cmd = ["gh", "issue", "create", "--title", issue["title"], "--body", issue["body"]]
    if "assignee" in issue:
        cmd.extend(["--assignee", issue["assignee"]])
    if "labels" in issue:
        cmd.extend(["--label", ",".join(issue["labels"])])
    subprocess.run(cmd)
```

---

## Team Communication

- **Weekly standup:** Tuesday 10:00 AM
- **Slack channel:** #confostate-dev
- **Issues tracker:** GitHub Issues (assign to self)
- **Blockers:** Report in standup immediately
- **Async updates:** Commit messages and PR descriptions

---

## Notes

- Features are grouped to minimize cross-team dependencies
- Parallel development recommended; code integration happens at phase-end reviews
- Data curation should start immediately; it blocks others
- All deliverables should include unit tests and documentation
