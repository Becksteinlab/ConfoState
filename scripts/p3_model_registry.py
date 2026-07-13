"""Outline script for Person 3 Task 5: model registry update."""

from __future__ import annotations

import argparse
import json

from confostate.models.registry import get_registered_model, list_registered_models, register_model


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Register and inspect model artifacts.")
    parser.add_argument("--registry-path", default="data/models/registry.json")
    parser.add_argument("--family", required=True)
    parser.add_argument("--model-name", required=True)
    parser.add_argument("--artifact-path", required=True)
    parser.add_argument("--metrics-json", default=None)
    parser.add_argument("--data-version", default=None)
    parser.add_argument("--show-latest", action="store_true")
    parser.add_argument("--list", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    metrics = None
    if args.metrics_json:
        with open(args.metrics_json, "r", encoding="utf-8") as handle:
            metrics = json.load(handle)

    entry = register_model(
        registry_path=args.registry_path,
        family=args.family,
        model_name=args.model_name,
        artifact_path=args.artifact_path,
        metrics=metrics,
        data_version=args.data_version,
    )
    print("Registered model entry:")
    print(json.dumps(entry, indent=2))

    if args.show_latest:
        latest = get_registered_model(args.registry_path, args.family)
        print("Latest for family:")
        print(json.dumps(latest, indent=2))

    if args.list:
        print("All registry entries:")
        print(json.dumps(list_registered_models(args.registry_path), indent=2))


if __name__ == "__main__":
    main()
