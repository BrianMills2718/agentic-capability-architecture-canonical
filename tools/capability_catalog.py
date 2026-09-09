#!/usr/bin/env python3
"""Inspect verified semantic actions derived directly from capability manifests.

Capability manifests name intended semantic exports, but an export is admitted to
this catalog only when its declared public target can also be resolved to a real
top-level callable in the capability's pinned runtime source. This keeps the
agent-facing executable surface narrower and stronger than broad capability-scope
metadata such as ``provides``.
"""
from __future__ import annotations

import argparse
import ast
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


def _runtime_root(
    capability: str,
    registry_entry: dict[str, Any],
    manifest: dict[str, Any],
    root: Path,
) -> Path:
    runtime_path = manifest.get("runtime_path") or registry_entry.get("runtime_path")
    if not runtime_path:
        raise CatalogError(
            f"{capability}: semantic exports require a runtime_path so their targets can be verified"
        )
    runtime_root = root / str(runtime_path)
    if not runtime_root.exists():
        raise CatalogError(f"{capability}: runtime_path does not exist: {runtime_path}")
    return runtime_root


def _verify_public_target(
    capability: str,
    public_interface: str,
    runtime_root: Path,
    root: Path,
) -> str:
    """Resolve ``package.module.symbol`` to a real top-level callable definition."""

    parts = [part for part in public_interface.split(".") if part]
    if len(parts) < 2:
        raise CatalogError(
            f"{capability}: public interface {public_interface!r} must include module and symbol"
        )

    symbol = parts[-1]
    module_parts = parts[:-1]
    module_file = runtime_root.joinpath(*module_parts).with_suffix(".py")
    if not module_file.exists():
        package_init = runtime_root.joinpath(*module_parts, "__init__.py")
        if package_init.exists():
            module_file = package_init
        else:
            raise CatalogError(
                f"{capability}: semantic export target module for {public_interface!r} does not exist"
            )

    try:
        tree = ast.parse(module_file.read_text(encoding="utf-8"), filename=str(module_file))
    except SyntaxError as exc:  # pragma: no cover - surfaced as catalog failure
        raise CatalogError(f"{capability}: unable to parse export source {module_file}: {exc}") from exc

    callable_names = {
        node.name
        for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
    }
    if symbol not in callable_names:
        raise CatalogError(
            f"{capability}: semantic export {public_interface!r} does not resolve to a "
            f"top-level function/class in {module_file.relative_to(root)}"
        )

    return str(module_file.relative_to(root))


def build_catalog(root: Path = ROOT) -> dict[str, Any]:
    """Build the verified semantic-action catalog from capability manifests."""

    registry = _load_yaml(root / "capability_registry.yml")
    actions: list[dict[str, Any]] = []
    seen: dict[str, str] = {}

    for name, registry_entry in (registry.get("capabilities") or {}).items():
        manifest_path = root / str(registry_entry["path"]) / "capability.yml"
        manifest = _load_yaml(manifest_path)
        provides = {str(v) for v in manifest.get("provides") or ()}
        public_interfaces = {str(v) for v in manifest.get("public_interfaces") or ()}
        exports = manifest.get("semantic_exports") or ()
        runtime_root: Path | None = None

        for export in exports:
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

            if runtime_root is None:
                runtime_root = _runtime_root(str(name), registry_entry, manifest, root)
            source_file = _verify_public_target(
                str(name), public_interface, runtime_root, root
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
                    "source_file": source_file,
                    "manifest": str(manifest_path.relative_to(root)),
                }
            )

    actions.sort(key=lambda item: item["action_id"])
    return {"schema_version": 1, "semantic_actions": actions}


def resolve_action(action_id: str, root: Path = ROOT) -> dict[str, Any]:
    """Resolve one exact semantic action ID to its verified public boundary."""

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
    parser = argparse.ArgumentParser(description="Inspect verified manifest-derived semantic actions")
    sub = parser.add_subparsers(dest="command", required=True)

    list_parser = sub.add_parser("list", help="List verified exported semantic actions")
    list_parser.add_argument("--json", action="store_true", dest="as_json")

    describe_parser = sub.add_parser("describe", help="Describe one exact verified semantic action")
    describe_parser.add_argument("action_id")
    describe_parser.add_argument("--json", action="store_true", dest="as_json")

    sub.add_parser("check", help="Validate semantic exports and their runtime source targets")

    args = parser.parse_args()
    try:
        if args.command == "list":
            _emit(build_catalog(), args.as_json)
        elif args.command == "describe":
            _emit(resolve_action(args.action_id), args.as_json)
        else:
            catalog = build_catalog()
            print(f"OK: {len(catalog['semantic_actions'])} verified manifest-derived semantic actions")
        return 0
    except CatalogError as exc:
        print(json.dumps({"ok": False, "error": str(exc)}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
