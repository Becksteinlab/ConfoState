"""Model training and evaluation utilities for ConfoState."""

from confostate.models.baseline import get_baseline_models
from confostate.models.evaluate import evaluate_model, write_evaluation_report
from confostate.models.registry import get_registered_model, register_model
from confostate.models.train import run_training

__all__ = [
    "evaluate_model",
    "get_baseline_models",
    "get_registered_model",
    "register_model",
    "run_training",
    "write_evaluation_report",
]
