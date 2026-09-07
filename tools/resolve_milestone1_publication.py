#!/usr/bin/env python3
"""Validate milestone-1 primitive publication against capability owners."""
from pathlib import Path
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]
MAPPING = ROOT / "architecture/primitive_model/milestone1/actionpack_publication_mapping_v0_1.yaml"


def main() -> int:
    data = yaml.safe_load(MAPPING.read_text())
    errors = []
    for action in data["published_actions"]:
        owner = action["capability_owner"]
        selected = action["selected_implementation"]
        manifest_path = ROOT / action["owner_manifest"]
        manifest = yaml.safe_load(manifest_path.read_text())
        if manifest.get("name") != owner:
            errors.append(f"{action['primitive_id']}: owner mismatch {manifest.get('name')} != {owner}")
        public_interfaces = set(manifest.get("public_interfaces") or ())
        if selected not in public_interfaces:
            errors.append(f"{action['primitive_id']}: unpublished implementation {selected}")
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    for action in data["published_actions"]:
        print(f"{action['primitive_id']} -> {action['selected_implementation']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
