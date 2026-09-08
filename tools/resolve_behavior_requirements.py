#!/usr/bin/env python3
"""Resolve compiler-owned BehaviorRequirements against available capabilities.

The default catalog is derived from capability manifests. The legacy publication YAML
can still be supplied explicitly for compatibility while subtraction equivalence is
being tested.
"""
from __future__ import annotations

from pathlib import Path
import argparse
import sys
import yaml

try:
    from tools.capability_catalog import build_publication
except ModuleNotFoundError:  # direct `python tools/resolve_behavior_requirements.py`
    from capability_catalog import build_publication

ROOT = Path(__file__).resolve().parents[1]


class ResolutionError(ValueError):
    def __init__(self, code: str, requirement_id: str, detail: str):
        super().__init__(f"{code}: {requirement_id}: {detail}")
        self.code = code
        self.requirement_id = requirement_id
        self.detail = detail


def _named_contracts(requirement: dict, field: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for item in requirement.get(field) or ():
        if not isinstance(item, dict):
            continue
        name = item.get("name")
        contract_id = item.get("contract_id")
        if name and contract_id:
            result[str(name)] = str(contract_id)
    return result


def _input_sources(requirement: dict) -> dict[str, dict]:
    result: dict[str, dict] = {}
    for item in requirement.get("inputs") or ():
        if not isinstance(item, dict):
            continue
        name = item.get("name")
        source = item.get("source")
        if name and isinstance(source, dict):
            result[str(name)] = source
    return result


def _publication_index(publication: dict) -> dict[str, list[dict]]:
    index: dict[str, list[dict]] = {}
    for action in publication.get("published_actions") or ():
        key = action.get("semantic_action")
        if key:
            index.setdefault(str(key), []).append(action)
    return index


def resolve(requirements: dict, publication: dict) -> dict:
    index = _publication_index(publication)
    bindings: list[dict] = []
    for requirement in requirements.get("requirements") or ():
        req_id = str(requirement.get("id") or "<missing-id>")
        semantic_action = str(requirement.get("semantic_action") or "")
        candidates = index.get(semantic_action, [])
        if not candidates:
            raise ResolutionError("UNKNOWN_SEMANTIC_ACTION", req_id, f"no publication for {semantic_action!r}")
        if len(candidates) != 1:
            raise ResolutionError("AMBIGUOUS_PUBLICATION", req_id, f"{len(candidates)} publications for {semantic_action!r}")

        action = candidates[0]
        contract = action.get("semantic_contract") or {}
        required_inputs = set(str(v) for v in contract.get("inputs") or ())
        input_contracts = _named_contracts(requirement, "inputs")
        input_sources = _input_sources(requirement)
        missing_inputs = sorted(required_inputs - set(input_contracts))
        if missing_inputs:
            raise ResolutionError("INPUT_CONTRACT_MISMATCH", req_id, f"missing inputs: {', '.join(missing_inputs)}")
        missing_sources = sorted(set(input_contracts) - set(input_sources))
        if missing_sources:
            raise ResolutionError("INPUT_SOURCE_MISSING", req_id, f"inputs without source: {', '.join(missing_sources)}")

        output_contracts = _named_contracts(requirement, "required_outputs")
        missing_outputs = sorted(set(output_contracts) - set(str(v) for v in contract.get("outputs") or ()))
        if missing_outputs:
            raise ResolutionError("OUTPUT_CONTRACT_MISMATCH", req_id, f"missing outputs: {', '.join(missing_outputs)}")

        bindings.append({
            "requirement_id": req_id,
            "semantic_action": semantic_action,
            "capability_owner": action["capability_owner"],
            "selected_implementation": action["selected_implementation"],
            "composition_implementation_ref": action["composition_implementation_ref"],
            "owner_manifest": action["owner_manifest"],
            "input_contracts": input_contracts,
            "input_sources": input_sources,
            "output_contracts": output_contracts,
            "provenance": requirement.get("provenance") or {},
            "requirement_invariants": requirement.get("invariants") or [],
        })

    return {
        "schema_version": "1.0",
        "source_system_spec": requirements.get("source_system_spec"),
        "publication_source": publication.get("source_registry"),
        "bindings": bindings,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Resolve semantic behavior requirements")
    parser.add_argument("requirements")
    parser.add_argument("--publication", help="legacy explicit publication YAML; default derives from capability manifests")
    parser.add_argument("--output")
    parser.add_argument("--json", action="store_true", help="emit JSON instead of YAML")
    args = parser.parse_args()

    requirements = yaml.safe_load(Path(args.requirements).read_text())
    if args.publication:
        pub_path = Path(args.publication)
        if not pub_path.is_absolute():
            pub_path = ROOT / pub_path
        publication = yaml.safe_load(pub_path.read_text())
    else:
        publication = build_publication(ROOT)

    try:
        result = resolve(requirements, publication)
    except ResolutionError as exc:
        print(f"{exc.code}: {exc.requirement_id}: {exc.detail}", file=sys.stderr)
        return 2

    if args.json:
        import json
        rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    else:
        rendered = yaml.safe_dump(result, sort_keys=False)
    if args.output:
        Path(args.output).write_text(rendered)
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
