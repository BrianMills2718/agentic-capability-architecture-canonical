#!/usr/bin/env python3
"""Manifest-derived capability catalog.

Capability manifests are the source of truth. This CLI provides a stable machine
surface that can later be wrapped by MCP without duplicating capability metadata.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "capability_registry.yml"


class CatalogError(ValueError):
    pass


def _load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text())
    if not isinstance(data, dict):
        raise CatalogError(f"expected mapping in {path}")
    return data


def build_catalog(root: Path = ROOT) -> dict[str, Any]:
    registry = _load_yaml(root / "capability_registry.yml")
    capabilities: list[dict[str, Any]] = []
    for name, entry in (registry.get("capabilities") or {}).items():
        capability_path = root / str(entry["path"]) / "capability.yml"
        manifest = _load_yaml(capability_path)
        public = set(str(v) for v in manifest.get("public_interfaces") or ())
        exports: list[dict[str, Any]] = []
        for export in manifest.get("semantic_exports") or ():
            implementation = str(export.get("implementation") or "")
            if not implementation or implementation not in public:
                raise CatalogError(
                    f"{name}: semantic export implementation {implementation!r} is not public"
                )
            version = int(export.get("implementation_version") or 0)
            if version < 1:
                raise CatalogError(f"{name}: implementation_version must be >= 1")
            exports.append(
                {
                    "semantic_action": str(export["semantic_action"]),
                    "implementation": implementation,
                    "implementation_ref": f"{implementation}/{version}",
                    "inputs": [str(v) for v in export.get("inputs") or ()],
                    "outputs": [str(v) for v in export.get("outputs") or ()],
                }
            )
        capabilities.append(
            {
                "name": str(manifest.get("name") or name),
                "status": manifest.get("status"),
                "version": str(manifest.get("version") or entry.get("version") or ""),
                "runtime": manifest.get("runtime"),
                "requires": list(manifest.get("requires") or ()),
                "public_interfaces": sorted(public),
                "semantic_exports": exports,
                "evidence": manifest.get("evidence") or {},
                "manifest": str(capability_path.relative_to(root)),
            }
        )
    return {"schema_version": "1.0", "capabilities": capabilities}


def build_publication(root: Path = ROOT) -> dict[str, Any]:
    """Compatibility view for the current resolver; derived, never hand-maintained."""
    catalog = build_catalog(root)
    actions: list[dict[str, Any]] = []
    for capability in catalog["capabilities"]:
        for export in capability["semantic_exports"]:
            actions.append(
                {
                    "semantic_action": export["semantic_action"],
                    "capability_owner": capability["name"],
                    "selected_implementation": export["implementation"],
                    "composition_implementation_ref": export["implementation_ref"],
                    "owner_manifest": capability["manifest"],
                    "semantic_contract": {
                        "inputs": export["inputs"],
                        "outputs": export["outputs"],
                    },
                }
            )
    return {
        "schema_version": "1.0",
        "source_registry": "manifest-derived",
        "published_actions": actions,
    }


def _dump(value: Any, as_json: bool) -> None:
    if as_json:
        print(json.dumps(value, indent=2, sort_keys=True))
    else:
        print(yaml.safe_dump(value, sort_keys=False), end="")


def main() -> int:
    parser = argparse.ArgumentParser(description="Inspect manifest-derived reusable capabilities")
    sub = parser.add_subparsers(dest="command", required=True)

    list_parser = sub.add_parser("list", help="List capabilities")
    list_parser.add_argument("--json", action="store_true", dest="as_json")

    describe_parser = sub.add_parser("describe", help="Describe one capability or semantic action")
    describe_parser.add_argument("name")
    describe_parser.add_argument("--json", action="store_true", dest="as_json")

    publication_parser = sub.add_parser("publication", help="Emit resolver compatibility view")
    publication_parser.add_argument("--json", action="store_true", dest="as_json")

    args = parser.parse_args()
    try:
        catalog = build_catalog()
        if args.command == "list":
            _dump(catalog, args.as_json)
            return 0
        if args.command == "publication":
            _dump(build_publication(), args.as_json)
            return 0
        matches = [c for c in catalog["capabilities"] if c["name"] == args.name]
        if not matches:
            matches = [
                {"capability": c["name"], **e}
                for c in catalog["capabilities"]
                for e in c["semantic_exports"]
                if e["semantic_action"] == args.name
            ]
        if not matches:
            print(json.dumps({"ok": False, "error": {"code": "NOT_FOUND", "name": args.name}}), file=sys.stderr)
            return 2
        _dump(matches[0] if len(matches) == 1 else matches, args.as_json)
        return 0
    except CatalogError as exc:
        print(json.dumps({"ok": False, "error": {"code": "INVALID_CATALOG", "message": str(exc)}}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
