#!/usr/bin/env python3
"""Inspect semantic actions derived directly from capability manifests.

Capability manifests and their real public interfaces are the source of truth.
This module deliberately performs exact lookup only; it is not a planner and it
does not maintain a second publication registry.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]


class CatalogError(ValueError):
    """Raised when manifest-derived catalog metadata is inconsistent."""


def _load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise CatalogError(f"expected mapping in {path}")
    return data


def build_catalog(root: Path = ROOT) -> dict[str, Any]:
    """Build the semantic-action catalog from capability manifests."""
    registry = _load_yaml(root / "capability_registry.yml")
    actions: list[dict[str, Any]] = []
    seen: dict[str, str] = {}

    for name, registry_entry in (registry.get("capabilities") or {}).items():
        manifest_path = root / str(registry_entry["path"]) / "capability.yml"
        manifest = _load_yaml(manifest_path)
        provides = {str(v) for v in manifest.get("provides") or ()}
        public_interfaces = {str(v) for v in manifest.get("public_interfaces") or ()}

        for export in manifest.get("semantic_exports") or ():
            if not isinstance(export, dict):
                raise CatalogError(f"{name}: semantic_exports entries must be mappings")
            action_id = str(export.get("action_id") or "")
            public_interface = str(export.get("public_interface") or "")
            if action_id not in provides:
                raise CatalogError(
                    f"{name}: semantic action {action_id!r} is not declared in provides"
                )
            if public_interface not in public_interfaces:
                raise CatalogError(
                    f"{name}: semantic action {action_id!r} points to non-public "
                    f"interface {public_interface!r}"
                )
            prior = seen.get(action_id)
            if prior is not None:
                raise CatalogError(
                    f"semantic action {action_id!r} is exported by both {prior!r} and {name!r}"
                )
            seen[action_id] = str(name)
            actions.append(
                {
                    "action_id": action_id,
                    "capability": str(name),
                    "capability_version": str(manifest.get("version") or ""),
                    "status": str(manifest.get("status") or ""),
                    "runtime": manifest.get("runtime"),
                    "public_interface": public_interface,
                    "manifest": str(manifest_path.relative_to(root)),
                }
            )

    actions.sort(key=lambda item: item["action_id"])
    return {"schema_version": 1, "semantic_actions": actions}


def resolve_action(action_id: str, root: Path = ROOT) -> dict[str, Any]:
    """Resolve one exact semantic action ID to its declared public boundary."""
    for action in build_catalog(root)["semantic_actions"]:
        if action["action_id"] == action_id:
            return action
    raise CatalogError(f"unknown semantic action: {action_id}")


def _emit(value: Any, as_json: bool) -> None:
    if as_json:
        print(json.dumps(value, indent=2, sort_keys=True))
    else:
        print(yaml.safe_dump(value, sort_keys=False), end="")


def main() -> int:
    parser = argparse.ArgumentParser(description="Inspect manifest-derived semantic actions")
    sub = parser.add_subparsers(dest="command", required=True)

    list_parser = sub.add_parser("list", help="List exported semantic actions")
    list_parser.add_argument("--json", action="store_true", dest="as_json")

    describe_parser = sub.add_parser("describe", help="Describe one exact semantic action")
    describe_parser.add_argument("action_id")
    describe_parser.add_argument("--json", action="store_true", dest="as_json")

    sub.add_parser("check", help="Validate semantic-export referential integrity")

    args = parser.parse_args()
    try:
        if args.command == "list":
            _emit(build_catalog(), args.as_json)
        elif args.command == "describe":
            _emit(resolve_action(args.action_id), args.as_json)
        else:
            catalog = build_catalog()
            print(f"OK: {len(catalog['semantic_actions'])} manifest-derived semantic actions")
        return 0
    except CatalogError as exc:
        print(json.dumps({"ok": False, "error": str(exc)}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
