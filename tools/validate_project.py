#!/usr/bin/env python3
"""Validate that a project manifest refers only to known capabilities.

Usage:
    python tools/validate_project.py clients/acme_reference/manifest.yml
"""
from pathlib import Path
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]


def load(path):
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))


def main():
    if len(sys.argv) != 2:
        raise SystemExit("usage: validate_project.py <manifest.yml>")

    manifest_path = Path(sys.argv[1])
    if not manifest_path.is_absolute():
        manifest_path = ROOT / manifest_path

    registry = load(ROOT / "capability_registry.yml")
    manifest = load(manifest_path)

    known = set(registry.get("capabilities", {}))
    requested = set(manifest.get("capabilities", {}))
    missing = sorted(requested - known)

    if missing:
        raise SystemExit(f"Unknown capabilities: {', '.join(missing)}")

    print(f"OK: {manifest['project']} uses {len(requested)} registered capabilities")
    for name in sorted(requested):
        print(f"  - {name}: {manifest['capabilities'][name]}")


if __name__ == "__main__":
    main()
