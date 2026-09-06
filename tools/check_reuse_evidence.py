#!/usr/bin/env python3
"""Enforce evidence thresholds for promoted capabilities."""
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]

def main():
    errors = []
    for path in sorted((ROOT / "capabilities").glob("*/capability.yml")):
        if path.parent.name == "_template":
            continue
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        status = data.get("status")
        if data.get("foundation"):
            continue
        evidence = data.get("evidence") or {}
        uses = evidence.get("materially_different_uses") or []
        third = bool(evidence.get("third_use_checked"))
        if status == "proven" and len(uses) < 2:
            errors.append(f"{data['name']}: proven requires at least two materially different uses")
        if status == "core" and (len(uses) < 3 or not third):
            errors.append(f"{data['name']}: core requires at least three uses and third_use_checked=true")
    if errors:
        raise SystemExit("Reuse evidence check failed:\n- " + "\n- ".join(errors))
    print("OK: promoted capabilities meet reuse-evidence thresholds")

if __name__ == "__main__":
    main()
