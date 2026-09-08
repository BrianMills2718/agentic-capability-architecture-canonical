#!/usr/bin/env python3
"""Validate repository JSON Schemas and checked-in YAML contracts."""
from pathlib import Path
import json
import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]

def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))

def load_yaml(path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))

def validate(path, schema_path, errors):
    data = load_yaml(path)
    schema = load_json(schema_path)
    validator = Draft202012Validator(schema)
    for error in sorted(validator.iter_errors(data), key=lambda e: list(e.path)):
        where = ".".join(str(x) for x in error.path) or "<root>"
        errors.append(f"{path.relative_to(ROOT)}:{where}: {error.message}")

def main():
    errors = []
    for schema_path in sorted((ROOT / "schemas").glob("*.json")):
        try:
            Draft202012Validator.check_schema(load_json(schema_path))
        except Exception as exc:
            errors.append(f"{schema_path.relative_to(ROOT)}: invalid JSON Schema: {exc}")

    validate(ROOT / "capability_registry.yml", ROOT / "schemas/registry.schema.json", errors)
    validate(ROOT / "reuse_candidates.yml", ROOT / "schemas/reuse_candidates.schema.json", errors)

    for path in sorted((ROOT / "capabilities").glob("*/capability.yml")):
        if path.parent.name == "_template":
            continue
        validate(path, ROOT / "schemas/capability.schema.json", errors)

    for path in sorted((ROOT / "clients").glob("*/manifest.yml")):
        if path.parent.name == "_template":
            continue
        validate(path, ROOT / "schemas/project_manifest.schema.json", errors)

    if errors:
        raise SystemExit("Schema validation failed:\n- " + "\n- ".join(errors))
    print("OK: YAML contracts match repository schemas")

if __name__ == "__main__":
    main()
