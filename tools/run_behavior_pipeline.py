#!/usr/bin/env python3
"""Run the maintained behavior-requirement resolution + composition gate.

This command owns orchestration only:
1. resolve BehaviorRequirements against CapabilityPublication;
2. pass the provider-bound Resolution Result to data-contracts;
3. fail before runtime when provider or composition constraints are unsatisfied.

It does not execute runtime implementations.
"""
from __future__ import annotations

from pathlib import Path
import argparse
import sys
import yaml

from tools.resolve_behavior_requirements import ResolutionError, resolve

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PUBLICATION = ROOT / "architecture/publication/capability_publication_v1.yaml"


def run(requirements: dict, publication: dict) -> tuple[dict, object]:
    resolution = resolve(requirements, publication)
    try:
        from data_contracts.composition.provider_resolution import validate_provider_resolution
    except ImportError as exc:
        raise RuntimeError(
            "maintained data-contracts package with provider_resolution adapter is required"
        ) from exc
    validation = validate_provider_resolution(resolution)
    if not validation.ok:
        raise RuntimeError(f"COMPOSITION_VALIDATION_FAILED: {validation.reason}")
    return resolution, validation


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("requirements", help="BehaviorRequirements v1 YAML")
    parser.add_argument("--publication", default=str(DEFAULT_PUBLICATION))
    parser.add_argument("--resolution-output", help="optional Provider Resolution Result v1 YAML output")
    args = parser.parse_args()

    req_path = Path(args.requirements)
    pub_path = Path(args.publication)
    if not pub_path.is_absolute():
        pub_path = ROOT / pub_path

    requirements = yaml.safe_load(req_path.read_text())
    publication = yaml.safe_load(pub_path.read_text())
    try:
        resolution, validation = run(requirements, publication)
    except ResolutionError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    except (RuntimeError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 3

    if args.resolution_output:
        Path(args.resolution_output).write_text(yaml.safe_dump(resolution, sort_keys=False))

    print(f"PASS provider resolution: {len(resolution['bindings'])} bindings")
    print(f"PASS data-contracts composition: {len(validation.produced_contract_ids)} contracts reachable")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
