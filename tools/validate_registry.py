#!/usr/bin/env python3
"""Validate registry/manifest structural synchronization.

This check does not prove that every broad ``provides`` label is an executable action.
Verified semantic-export targets are checked separately by ``capability_catalog.py check``.
"""
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "capability_registry.yml"


def load_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def main() -> None:
    data = load_yaml(REGISTRY)
    capabilities = data.get("capabilities", {})
    errors = []

    if not capabilities:
        errors.append("registry contains no capabilities")

    names = set(capabilities)
    for name, spec in capabilities.items():
        path = ROOT / spec.get("path", "")
        if not path.exists():
            errors.append(f"{name}: path does not exist: {path.relative_to(ROOT)}")
            continue

        for dep in spec.get("requires", []) or []:
            if dep not in names:
                errors.append(f"{name}: unknown required capability: {dep}")

        for dep in spec.get("optional", []) or []:
            if dep not in names:
                errors.append(f"{name}: unknown optional capability: {dep}")

        runtime_path = spec.get("runtime_path")
        if runtime_path and not (ROOT / runtime_path).exists():
            errors.append(f"{name}: runtime_path does not exist: {runtime_path}")

        manifest_path = path / "capability.yml"
        if manifest_path.exists():
            manifest = load_yaml(manifest_path)
            if manifest.get("name") != name:
                errors.append(f"{name}: capability.yml name is {manifest.get('name')!r}")
            for field in ("status", "version"):
                if manifest.get(field) != spec.get(field):
                    errors.append(
                        f"{name}: registry {field}={spec.get(field)!r} differs from capability.yml {field}={manifest.get(field)!r}"
                    )
            for field in ("provides", "requires", "optional"):
                registry_values = set(spec.get(field, []) or [])
                manifest_values = set(manifest.get(field, []) or [])
                if registry_values != manifest_values:
                    errors.append(
                        f"{name}: registry {field} differs from capability.yml "
                        f"({sorted(registry_values)} != {sorted(manifest_values)})"
                    )
        else:
            errors.append(f"{name}: missing capability.yml")

    if errors:
        raise SystemExit("Registry structural validation failed:\n- " + "\n- ".join(errors))

    print(
        f"OK: registry and manifests are structurally synchronized for {len(capabilities)} capability entries; "
        "run capability_catalog.py check for verified executable semantic exports"
    )


if __name__ == "__main__":
    main()
