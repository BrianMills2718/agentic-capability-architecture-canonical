#!/usr/bin/env python3
"""Validate the maintained capability publication against owner manifests."""
from pathlib import Path
import argparse
import re
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PUBLICATION = ROOT / "architecture/publication/capability_publication_v1.yaml"
VERSIONED_ID = re.compile(r"^[a-z][a-z0-9_.-]*/[1-9][0-9]*$")


def validate(path: Path) -> list[str]:
    data = yaml.safe_load(path.read_text())
    errors: list[str] = []
    seen: set[str] = set()
    for action in data.get("published_actions", []):
        semantic_action = action.get("semantic_action")
        if not semantic_action:
            errors.append("published action missing semantic_action")
            continue
        if semantic_action in seen:
            errors.append(f"duplicate semantic_action {semantic_action}")
        seen.add(semantic_action)

        owner = action.get("capability_owner")
        selected = action.get("selected_implementation")
        composition_ref = action.get("composition_implementation_ref")
        manifest_rel = action.get("owner_manifest")
        if not owner or not selected or not composition_ref or not manifest_rel:
            errors.append(
                f"{semantic_action}: missing owner, selected implementation, composition implementation ref, or owner manifest"
            )
            continue
        if not VERSIONED_ID.fullmatch(str(composition_ref)):
            errors.append(f"{semantic_action}: invalid composition implementation ref {composition_ref!r}")

        manifest_path = ROOT / manifest_rel
        if not manifest_path.exists():
            errors.append(f"{semantic_action}: owner manifest does not exist: {manifest_rel}")
            continue
        manifest = yaml.safe_load(manifest_path.read_text())
        if manifest.get("name") != owner:
            errors.append(f"{semantic_action}: owner mismatch {manifest.get('name')} != {owner}")
        if selected not in set(manifest.get("public_interfaces") or ()):
            errors.append(f"{semantic_action}: unpublished implementation {selected}")
        candidates = set(action.get("implementation_candidates") or ())
        if candidates and selected not in candidates:
            errors.append(f"{semantic_action}: selected implementation is not an implementation candidate")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("publication", nargs="?", default=str(DEFAULT_PUBLICATION))
    args = parser.parse_args()
    path = Path(args.publication)
    if not path.is_absolute():
        path = ROOT / path
    errors = validate(path)
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    data = yaml.safe_load(path.read_text())
    for action in data["published_actions"]:
        print(
            f"{action['semantic_action']} -> {action['selected_implementation']} "
            f"[{action['composition_implementation_ref']}]"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
