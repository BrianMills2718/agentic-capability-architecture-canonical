#!/usr/bin/env python3
"""Run semantic behavior resolution plus the smallest sufficient pre-runtime gate.

Default path:
1. derive the capability catalog from capability manifests;
2. resolve BehaviorRequirements against that provider-independent catalog view;
3. validate the already-provider-bound graph with data-contracts' minimal graph/type gate;
4. fail before runtime when provider or graph constraints are unsatisfied.

An explicit legacy publication YAML and the older ActionPack-based validation path remain
compatibility fallbacks during migration. This command does not execute providers.
"""
from __future__ import annotations

from pathlib import Path
import argparse
import sys
import yaml

from tools.capability_catalog import build_publication
from tools.resolve_behavior_requirements import ResolutionError, resolve

ROOT = Path(__file__).resolve().parents[1]


def _validate_resolution(resolution: dict):
    """Prefer the minimal provider-bound graph gate; fall back for older installs."""
    try:
        from data_contracts.composition import validate_simple_resolution
    except ImportError:
        try:
            from data_contracts.composition.provider_resolution import validate_provider_resolution
        except ImportError as exc:
            raise RuntimeError(
                "data-contracts with provider-resolution validation is required"
            ) from exc
        validation = validate_provider_resolution(resolution)
        if not validation.ok:
            raise RuntimeError(f"COMPOSITION_VALIDATION_FAILED: {validation.reason}")
        return validation

    return validate_simple_resolution(resolution)


def run(requirements: dict, publication: dict | None = None) -> tuple[dict, object]:
    catalog_view = publication if publication is not None else build_publication(ROOT)
    resolution = resolve(requirements, catalog_view)
    validation = _validate_resolution(resolution)
    return resolution, validation


def main() -> int:
    parser = argparse.ArgumentParser(description="Resolve and validate semantic behavior requirements")
    parser.add_argument("requirements", help="BehaviorRequirements v1 YAML")
    parser.add_argument(
        "--publication",
        help="legacy explicit publication YAML; default derives from capability manifests",
    )
    parser.add_argument("--resolution-output", help="optional Provider Resolution Result v1 YAML output")
    args = parser.parse_args()

    requirements = yaml.safe_load(Path(args.requirements).read_text())
    publication = None
    if args.publication:
        pub_path = Path(args.publication)
        if not pub_path.is_absolute():
            pub_path = ROOT / pub_path
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
    if hasattr(validation, "order"):
        print(f"PASS data-contracts graph validation: {len(validation.order)} requirements")
    else:
        # Compatibility output for older data-contracts validation results.
        print(f"PASS data-contracts composition: {len(validation.produced_contract_ids)} contracts reachable")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
