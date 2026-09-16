#!/usr/bin/env python3
"""Inspect verified semantic actions and explicit provider-owned actions.

Local ``semantic_exports`` remain the strongest callable claim: an export enters
that catalog only when its public target resolves to a real top-level callable
in the capability's pinned runtime source.

External provider actions are intentionally different. They contain no local
callable and do not make ACA the runtime owner. A ``provider_operability`` block
only tells an agent which exact provider/interface/version to bind, where to
observe health/traces/failures, and where provider-owned reliability/recovery
semantics live. Structural validation keeps those references complete and
prevents ACA metadata from silently claiming execution or recovery ownership.
"""
from __future__ import annotations

import argparse
import ast
import json
from pathlib import Path
import re
import sys
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
_SHA40 = re.compile(r"^[a-f0-9]{40}$")
_REPOSITORY = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")


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


def _nonempty_string(value: object, *, field: str, capability: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise CatalogError(f"{capability}: provider_operability {field} must be a nonempty string")
    return value


def _string_list(value: object, *, field: str, capability: str) -> list[str]:
    if not isinstance(value, list) or not value or not all(
        isinstance(item, str) and item.strip() for item in value
    ):
        raise CatalogError(
            f"{capability}: provider_operability {field} must be a nonempty list of strings"
        )
    if len(value) != len(set(value)):
        raise CatalogError(f"{capability}: provider_operability {field} contains duplicates")
    return list(value)


def _exact_keys(
    value: object,
    *,
    keys: set[str],
    field: str,
    capability: str,
) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise CatalogError(f"{capability}: provider_operability {field} must be a mapping")
    actual = set(value)
    if actual != keys:
        missing = sorted(keys - actual)
        extra = sorted(actual - keys)
        detail = []
        if missing:
            detail.append("missing=" + ",".join(missing))
        if extra:
            detail.append("unexpected=" + ",".join(extra))
        raise CatalogError(
            f"{capability}: provider_operability {field} has invalid fields ({'; '.join(detail)})"
        )
    return value


def _verify_provider_operability(
    capability: str,
    manifest: dict[str, Any],
    raw: object,
) -> dict[str, Any]:
    """Validate one external provider action without claiming local execution."""

    data = _exact_keys(
        raw,
        keys={
            "action_id",
            "provider_id",
            "provider_repository",
            "provider_revision",
            "interface",
            "observability",
            "reliability",
            "recovery",
            "evidence_refs",
        },
        field="root",
        capability=capability,
    )
    action_id = _nonempty_string(data["action_id"], field="action_id", capability=capability)
    provides = {str(value) for value in manifest.get("provides") or ()}
    if action_id not in provides:
        raise CatalogError(
            f"{capability}: provider action {action_id!r} is not declared in provides"
        )

    provider_id = _nonempty_string(data["provider_id"], field="provider_id", capability=capability)
    repository = _nonempty_string(
        data["provider_repository"], field="provider_repository", capability=capability
    )
    if not _REPOSITORY.fullmatch(repository):
        raise CatalogError(f"{capability}: provider_repository must be owner/name")
    revision = _nonempty_string(
        data["provider_revision"], field="provider_revision", capability=capability
    )
    if not _SHA40.fullmatch(revision):
        raise CatalogError(f"{capability}: provider_revision must be an exact lowercase 40-char SHA")

    interface = _exact_keys(
        data["interface"],
        keys={
            "transport",
            "endpoint",
            "selector",
            "request_contract",
            "result_contract",
            "auth",
        },
        field="interface",
        capability=capability,
    )
    if interface["transport"] != "http":
        raise CatalogError(f"{capability}: only explicit http provider transport is currently supported")
    endpoint = _nonempty_string(interface["endpoint"], field="interface.endpoint", capability=capability)
    if not endpoint.startswith(("GET ", "POST ")):
        raise CatalogError(f"{capability}: interface.endpoint must include HTTP method and path")
    _nonempty_string(interface["selector"], field="interface.selector", capability=capability)
    _nonempty_string(interface["request_contract"], field="interface.request_contract", capability=capability)
    _nonempty_string(interface["result_contract"], field="interface.result_contract", capability=capability)
    if interface["auth"] not in {"bearer", "none"}:
        raise CatalogError(f"{capability}: interface.auth must be bearer or none")

    observability = _exact_keys(
        data["observability"],
        keys={"health_ref", "trace_ref", "failure_ref"},
        field="observability",
        capability=capability,
    )
    for key in ("health_ref", "trace_ref", "failure_ref"):
        _nonempty_string(observability[key], field=f"observability.{key}", capability=capability)

    reliability = _exact_keys(
        data["reliability"],
        keys={"retry_owner", "idempotency_ref"},
        field="reliability",
        capability=capability,
    )
    if reliability["retry_owner"] != "provider":
        raise CatalogError(f"{capability}: retry ownership must remain provider-owned")
    _nonempty_string(reliability["idempotency_ref"], field="reliability.idempotency_ref", capability=capability)

    recovery = _exact_keys(
        data["recovery"],
        keys={"owner", "references"},
        field="recovery",
        capability=capability,
    )
    if recovery["owner"] != "provider":
        raise CatalogError(f"{capability}: recovery ownership must remain provider-owned")
    recovery_refs = _string_list(
        recovery["references"], field="recovery.references", capability=capability
    )
    evidence_refs = _string_list(
        data["evidence_refs"], field="evidence_refs", capability=capability
    )

    expected_prefix = f"{repository}@{revision}:"
    all_refs = [
        str(observability["health_ref"]),
        str(observability["trace_ref"]),
        str(observability["failure_ref"]),
        str(reliability["idempotency_ref"]),
        *recovery_refs,
        *evidence_refs,
    ]
    if any(not ref.startswith(expected_prefix) for ref in all_refs):
        raise CatalogError(
            f"{capability}: provider-owned references must bind exact {repository}@{revision}"
        )

    return {
        "action_id": action_id,
        "capability": capability,
        "capability_version": str(manifest.get("version") or ""),
        "status": str(manifest.get("status") or ""),
        "execution_owner": "provider",
        "provider_id": provider_id,
        "provider_repository": repository,
        "provider_revision": revision,
        "interface": interface,
        "observability": observability,
        "reliability": reliability,
        "recovery": recovery,
        "evidence_refs": evidence_refs,
    }


def build_catalog(root: Path = ROOT) -> dict[str, Any]:
    """Build verified local actions plus validated external provider actions."""

    registry = _load_yaml(root / "capability_registry.yml")
    actions: list[dict[str, Any]] = []
    provider_actions: list[dict[str, Any]] = []
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

        provider = manifest.get("provider_operability")
        if provider is not None:
            item = _verify_provider_operability(str(name), manifest, provider)
            action_id = item["action_id"]
            prior = seen.get(action_id)
            if prior is not None:
                raise CatalogError(
                    f"action {action_id!r} is declared by both {prior!r} and {name!r}"
                )
            seen[action_id] = str(name)
            item["manifest"] = str(manifest_path.relative_to(root))
            provider_actions.append(item)

    actions.sort(key=lambda item: item["action_id"])
    provider_actions.sort(key=lambda item: item["action_id"])
    return {
        "schema_version": 2,
        "semantic_actions": actions,
        "provider_actions": provider_actions,
    }


def resolve_action(action_id: str, root: Path = ROOT) -> dict[str, Any]:
    """Resolve one exact local semantic action to its verified public callable."""

    for action in build_catalog(root)["semantic_actions"]:
        if action["action_id"] == action_id:
            return action
    raise CatalogError(f"unknown semantic action: {action_id}")


def resolve_provider_action(action_id: str, root: Path = ROOT) -> dict[str, Any]:
    """Resolve one exact external provider action without claiming local execution."""

    for action in build_catalog(root)["provider_actions"]:
        if action["action_id"] == action_id:
            return action
    raise CatalogError(f"unknown provider action: {action_id}")


def _emit(value: Any, as_json: bool) -> None:
    if as_json:
        print(json.dumps(value, indent=2, sort_keys=True))
    else:
        print(yaml.safe_dump(value, sort_keys=False), end="")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Inspect verified local actions and explicit provider-owned actions"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    list_parser = sub.add_parser("list", help="List local semantic and provider actions")
    list_parser.add_argument("--json", action="store_true", dest="as_json")

    describe_parser = sub.add_parser("describe", help="Describe one exact verified local semantic action")
    describe_parser.add_argument("action_id")
    describe_parser.add_argument("--json", action="store_true", dest="as_json")

    provider_parser = sub.add_parser(
        "describe-provider", help="Describe one exact provider-owned action"
    )
    provider_parser.add_argument("action_id")
    provider_parser.add_argument("--json", action="store_true", dest="as_json")

    sub.add_parser("check", help="Validate semantic exports and provider-operability metadata")

    args = parser.parse_args()
    try:
        if args.command == "list":
            _emit(build_catalog(), args.as_json)
        elif args.command == "describe":
            _emit(resolve_action(args.action_id), args.as_json)
        elif args.command == "describe-provider":
            _emit(resolve_provider_action(args.action_id), args.as_json)
        else:
            catalog = build_catalog()
            print(
                "OK: "
                f"{len(catalog['semantic_actions'])} verified local semantic actions; "
                f"{len(catalog['provider_actions'])} provider-owned actions"
            )
        return 0
    except CatalogError as exc:
        print(json.dumps({"ok": False, "error": str(exc)}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
