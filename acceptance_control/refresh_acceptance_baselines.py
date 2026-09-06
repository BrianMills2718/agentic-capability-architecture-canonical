#!/usr/bin/env python3
from pathlib import Path
import hashlib
import json
import sys
import yaml

repo = Path(sys.argv[1]).resolve()
baseline = Path(sys.argv[2]).resolve()
accept = repo / "tests" / "acceptance"

acme_paths = [
    "clients/acme_reference/custom/frappe_app/acme_rules/acme_rules/appointment_rules.py",
    "clients/acme_reference/custom/frappe_app/acme_rules/acme_rules/hooks.py",
    "clients/acme_reference/manifest.yml",
]

def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

baseline_hashes = {rel: digest(baseline / rel) for rel in acme_paths}

registry = yaml.safe_load((baseline / "capability_registry.yml").read_text(encoding="utf-8"))
shared = {}
ignored = {"__pycache__", "build", "dist", ".pytest_cache"}
for cap in (registry.get("capabilities") or {}).values():
    runtime_path = cap.get("runtime_path")
    if not runtime_path:
        continue
    base = baseline / runtime_path
    for path in sorted(base.rglob("*")):
        if not path.is_file():
            continue
        rel_parts = set(path.relative_to(base).parts)
        if rel_parts & ignored or path.name.endswith(".pyc") or ".egg-info" in str(path):
            continue
        rel = str(path.relative_to(baseline))
        shared[rel] = digest(path)

accept.mkdir(parents=True, exist_ok=True)
(accept / "baseline_hashes.json").write_text(json.dumps(baseline_hashes, indent=2, sort_keys=True) + "\n", encoding="utf-8")
(accept / "shared_runtime_hashes.json").write_text(json.dumps(shared, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(f"refreshed acceptance baselines: {len(baseline_hashes)} protected ACME files, {len(shared)} shared runtime files")
