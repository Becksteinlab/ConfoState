"""Model registry helpers for tracking trained artifacts."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any


def _load_registry(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"models": []}
    return json.loads(path.read_text(encoding="utf-8"))


def _save_registry(path: Path, registry: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(registry, indent=2), encoding="utf-8")


def register_model(
    registry_path: str,
    family: str,
    model_name: str,
    artifact_path: str,
    metrics: dict[str, Any] | None = None,
    data_version: str | None = None,
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Append a model record to registry and return created record."""
    path = Path(registry_path)
    registry = _load_registry(path)

    entry: dict[str, Any] = {
        "family": family,
        "model_name": model_name,
        "artifact_path": artifact_path,
        "registered_at": datetime.utcnow().isoformat() + "Z",
    }

    if metrics is not None:
        entry["metrics"] = metrics
    if data_version is not None:
        entry["data_version"] = data_version
    if extra:
        entry.update(extra)

    registry.setdefault("models", []).append(entry)
    _save_registry(path, registry)
    return entry


def get_registered_model(
    registry_path: str, family: str
) -> dict[str, Any] | None:
    """Return latest model entry for a family."""
    path = Path(registry_path)
    registry = _load_registry(path)
    family_entries = [
        m for m in registry.get("models", []) if m.get("family") == family
    ]
    if not family_entries:
        return None
    return family_entries[-1]


def list_registered_models(registry_path: str) -> list[dict[str, Any]]:
    """Return all registry entries."""
    path = Path(registry_path)
    registry = _load_registry(path)
    return registry.get("models", [])
