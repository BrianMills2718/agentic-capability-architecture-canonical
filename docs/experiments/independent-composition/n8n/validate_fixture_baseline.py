#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
cases = json.loads((ROOT / "fixtures" / "CASES.json").read_text())
workflow = json.loads((Path(__file__).resolve().parent / "twitter-prospector-fixture-baseline.json").read_text())

required_top = {"name", "nodes", "connections", "settings"}
missing = required_top - set(workflow)
assert not missing, f"workflow missing top-level fields: {sorted(missing)}"

names = [n["name"] for n in workflow["nodes"]]
assert len(names) == len(set(names)), "node names must be unique"
assert names == [
    "Manual Trigger",
    "Load Frozen Candidates",
    "Score Fixture Candidates",
    "Simulate Human Review Fixture",
    "Build Handoff and Assurance Receipt",
]

normal = next(c for c in cases["cases"] if c["id"] == "normal-composition")
assert normal["expected"]["review_ids"] == ["cand-001", "cand-002"]
assert normal["expected"]["allowed_handoff_ids"] == ["cand-001"]

approval = next(c for c in cases["cases"] if c["id"] == "approval-binding")
assert approval["review"]["decision"] == "reject"
assert approval["expected"]["handoff_created"] is False

retry = next(c for c in cases["cases"] if c["id"] == "retry-duplicate")
assert retry["expected"]["external_effect_count_max"] == 1

print("fixture workflow structure and frozen evaluator invariants: PASS")
