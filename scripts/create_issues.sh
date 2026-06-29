#!/bin/bash
# Create GitHub Issues for ConfoState 6-Person Team Workplan
# Date: 2026-06-15
# 
# Prerequisites:
#   - GitHub CLI installed: https://cli.github.com/
#   - Authenticated: gh auth login
#   - In the ConfoState repository directory
#
# Usage:
#   bash scripts/create_issues.sh

set -e

echo "Creating GitHub issues for ConfoState 6-person workplan..."
echo ""

# Issue 1: Data Curation & Annotation
echo "[1/6] Creating issue: Data Curation & Annotation"
gh issue create \
  --title "Person 1: Data Curation & Annotation (Phase 1)" \
  --body "## Role
Data lead responsible for curating and verifying LeuT annotations.

## Tasks
- Verify and curate all 25 PDB entries in \`data/annotations/leu_t_transporters.csv\`
- Fetch authoritative metadata from RCSB API (resolution, experimental method, release date, DOI)
- Verify conformational state labels against primary literature
- Fetch membrane orientations from OPM database or submit calculation jobs
- Build data validation pipeline in \`confostate/data/validators.py\`
- Expand to additional protein families if time permits

## Deliverables
- ✓ Verified \`data/annotations/leu_t_transporters.csv\` with authoritative metadata
- ✓ OPM orientation data added to annotations
- ✓ \`confostate/data/validators.py\` with schema checks
- ✓ Data curation guide in \`docs/data-curation.md\`

## Duration
3–4 weeks

## Blockers / Dependencies
- Requires access to RCSB API and OPM database (no code dependencies)

See \`Plans/workplan-6person-2026-06-15.md\` for full details." \
  --label "phase-1,data,milestone-1" \
  --milestone "Phase 1: Data Foundation"

# Issue 2: Feature Engineering
echo "[2/6] Creating issue: Feature Engineering"
gh issue create \
  --title "Person 2: Feature Engineering (Phase 2)" \
  --body "## Role
Structural biology & feature engineering lead responsible for translating 3D structures into numerical descriptors.

## Tasks
- Implement cavity/solvent accessibility features in \`confostate/features/cavity.py\`
- Implement domain distance features in \`confostate/features/domains.py\`
- Implement RMSD-to-reference features in \`confostate/features/rmsd.py\`
- Implement OPM orientation features in \`confostate/features/orientation.py\`
- Implement symmetry features in \`confostate/features/symmetry.py\`
- Implement feature vector exporter with unit tests

## Deliverables
- ✓ \`confostate/features/\` with 5–6 feature modules
- ✓ Tested \`extract_features(pdb_path)\` function
- ✓ Feature documentation in \`docs/features.md\`
- ✓ Example feature vectors for all 25 LeuT structures

## Duration
3–4 weeks

## Blockers / Dependencies
- Depends on: Person 1 (reference structures and OPM data)
- Blocks: Person 3 (feature vectors needed for training)

See \`Plans/workplan-6person-2026-06-15.md\` for full details." \
  --label "phase-2,features,milestone-2" \
  --milestone "Phase 2: Feature Engineering"

# Issue 3: ML Training & Evaluation
echo "[3/6] Creating issue: ML Training & Evaluation"
gh issue create \
  --title "Person 3: ML Training & Evaluation (Phase 3)" \
  --body "## Role
Machine learning engineer responsible for building and training the classifier.

## Tasks
- Build dataset loader in \`confostate/data/datasets.py\`
- Implement baseline models (logistic regression, Random Forest, SVM) in \`confostate/models/baseline.py\`
- Build training pipeline in \`confostate/models/train.py\` with cross-validation
- Implement evaluation & reporting in \`confostate/models/evaluate.py\`
- Build model registry in \`confostate/models/registry.py\`
- Optional: implement advanced models (XGBoost, neural networks)

## Deliverables
- ✓ \`confostate/models/\` with full training pipeline
- ✓ Trained baseline models saved to \`data/models/\`
- ✓ Evaluation report with per-family metrics
- ✓ Model registry and versioning scheme

## Duration
3–4 weeks

## Blockers / Dependencies
- Depends on: Person 1 (labels), Person 2 (feature extraction)
- Blocks: Person 4 (feature importance for explanations)

See \`Plans/workplan-6person-2026-06-15.md\` for full details." \
  --label "phase-3,ml,milestone-3" \
  --milestone "Phase 3: ML Classifier"

# Issue 4: Explainability & Interpretation
echo "[4/6] Creating issue: Explainability & Interpretation"
gh issue create \
  --title "Person 4: Explainability & Interpretation (Phase 4)" \
  --body "## Role
Interpretability lead responsible for generating human-readable justifications.

## Tasks
- Implement feature importance extraction in \`confostate/explain/importance.py\` (SHAP, permutation, etc.)
- Build explanation renderer in \`confostate/explain/render.py\` (feature importance → natural language)
- Add literature linking in \`confostate/explain/citations.py\`
- Implement explanation exporter with \`explain(prediction)\` → explanation text
- Generate example explanations for all test set structures
- Write \`docs/explainability.md\` with examples

## Deliverables
- ✓ \`confostate/explain/\` with full explanation pipeline
- ✓ Human-readable explanations for test structures
- ✓ Explainability documentation with examples

## Duration
2–3 weeks

## Blockers / Dependencies
- Depends on: Person 3 (trained models and feature importance)
- Blocks: Person 5 (explanations integrated into CLI/API output)

See \`Plans/workplan-6person-2026-06-15.md\` for full details." \
  --label "phase-4,explainability,milestone-4" \
  --milestone "Phase 4: Explainability"

# Issue 5: CLI & Python API
echo "[5/6] Creating issue: CLI & Python API"
gh issue create \
  --title "Person 5: CLI & Python API (Phase 5)" \
  --body "## Role
Software engineer / DevOps lead responsible for user interfaces.

## Tasks
- Implement Python API with \`Classifier\` class in \`confostate/classifier.py\`
- Implement CLI using Click/argparse in \`confostate/cli.py\` (\`confostate classify\` command)
- Add PDB ID lookup and on-the-fly downloads from RCSB
- Create integration tests in \`tests/test_api.py\` and \`tests/test_cli.py\`
- Update \`docs/USAGE.md\` with API and CLI examples
- Create \`examples/api_example.py\` and \`examples/cli_example.sh\`
- Ensure \`pyproject.toml\` is complete and test \`pip install confostate\`

## Deliverables
- ✓ \`confostate/classifier.py\` with public API
- ✓ \`confostate/cli.py\` with \`confostate classify\` command
- ✓ End-to-end integration tests
- ✓ Usage examples and documentation

## Duration
2–3 weeks

## Blockers / Dependencies
- Depends on: Person 3 (models), Person 4 (explanations)
- Blocks: None

See \`Plans/workplan-6person-2026-06-15.md\` for full details." \
  --label "phase-5,cli,api,milestone-5" \
  --milestone "Phase 5: Interfaces"

# Issue 6: Infrastructure, CI, & Testing
echo "[6/6] Creating issue: Infrastructure, CI, & Testing"
gh issue create \
  --title "Person 6: Infrastructure, CI, & Testing (Phase 5+)" \
  --body "## Role
DevOps / QA engineer responsible for infrastructure and quality assurance.

## Tasks
- Set up continuous integration in \`.github/workflows/test.yml\`
- Add linting & code quality (Black, Flake8, Pylint)
- Build comprehensive test suite in \`tests/\` with >80% coverage
- Add documentation building (Sphinx or similar)
- Set up semantic versioning and release workflow
- Document PDB structure download process and data reproducibility
- Create \`CONTRIBUTING.md\` with contribution guidelines

## Deliverables
- ✓ \`.github/workflows/\` with CI/CD pipelines
- ✓ Comprehensive test suite with >80% coverage
- ✓ Linting and code quality checks
- ✓ Documentation build pipeline
- ✓ \`CONTRIBUTING.md\` and release guidelines

## Duration
2–3 weeks

## Blockers / Dependencies
- Depends on: All others (needs all modules to test)
- Blocks: None

See \`Plans/workplan-6person-2026-06-15.md\` for full details." \
  --label "phase-5,infra,testing,ci-cd,milestone-5" \
  --milestone "Phase 5: Interfaces"

echo ""
echo "✓ All 6 issues created successfully!"
echo ""
echo "Next steps:"
echo "1. Assign each issue to a team member on GitHub"
echo "2. Review timeline in Plans/workplan-6person-2026-06-15.md"
echo "3. Kickoff meeting to align on milestones and dependencies"
