#!/usr/bin/env python3
"""Resolve and structurally validate the appointment federation canary.

The compiler owns requirement meaning. This command consumes one exact
compiler artifact, resolves its semantic action IDs against this repository's
manifest-derived catalog, and delegates only graph/type invariants to
``data-contracts``. It performs no provider invocation or external effect.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from typing import Any

try:
    from tools.capability_catalog import CatalogError, resolve_action
except ModuleNotFoundError:  # direct execution from tools/
    from capability_catalog import CatalogError, resolve_action


ROOT = Path(__file__).resolve().parents[1]
DATA_CONTRACTS_REVISION = "22b0c3078e5c1ff68a536529d56a3346efc105f3"
REQUIRED_ACTIONS = (
    "approval.resolve",
    "state.transition.plan",
    "notification.email.send",
)
REQUIRED_BRANCHES = {
    "allow": "transition:appointment_allow",
    "pending_approval": "transition:appointment_requires_approval",
    "approve": "transition:appointment_approval_granted",
    "reject": "transition:appointment_approval_rejected",
    "notification": "transition:schedule_appointment_reminder",
}
CANARY_PARAMETERS = {
    "approval_threshold_minutes": 90,
    "reminder_offset_minutes": -1440,
    "delivery_channel": "email",
    "approver_type": "biz:Manager",
}


class CanaryError(ValueError):
    """Stable, visible canary failure."""

    def __init__(self, code: str, detail: str):
        super().__init__(f"{code}: {detail}")
        self.code = code
        self.detail = detail


def _git(repo: Path, *args: str) -> str:
    try:
        return subprocess.run(
            ["git", "-C", str(repo), *args],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
    except subprocess.CalledProcessError as exc:
        detail = exc.stderr.strip() or exc.stdout.strip() or "git command failed"
        raise CanaryError("SOURCE_REVISION_UNAVAILABLE", detail) from exc


def load_git_json(repo: Path, revision: str, relative_path: str) -> tuple[dict[str, Any], str]:
    """Load JSON from an exact Git object, never from mutable working-tree bytes."""

    resolved = _git(repo, "rev-parse", "--verify", f"{revision}^{{commit}}")
    raw = _git(repo, "show", f"{resolved}:{relative_path}")
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise CanaryError("INVALID_REQUIREMENTS_JSON", str(exc)) from exc
    if not isinstance(payload, dict):
        raise CanaryError("INVALID_REQUIREMENTS", "root must be an object")
    return payload, resolved


def _named_contracts(items: object) -> dict[str, str]:
    if not isinstance(items, list):
        raise CanaryError("INVALID_REQUIREMENTS", "inputs and outputs must be arrays")
    contracts: dict[str, str] = {}
    for item in items:
        if not isinstance(item, dict) or not item.get("name") or not item.get("contract_id"):
            raise CanaryError("INVALID_REQUIREMENTS", "every input/output needs name and contract_id")
        name = str(item["name"])
        if name in contracts:
            raise CanaryError("INVALID_REQUIREMENTS", f"duplicate contract name {name!r}")
        contracts[name] = str(item["contract_id"])
    return contracts


def _provider_graph(requirements: list[dict[str, Any]]) -> dict[str, Any]:
    nodes: list[dict[str, Any]] = []
    for requirement in requirements:
        requirement_id = str(requirement.get("id") or "")
        if not requirement_id:
            raise CanaryError("INVALID_REQUIREMENTS", "requirement id is missing")
        inputs = requirement.get("inputs")
        input_contracts = _named_contracts(inputs)
        input_sources: dict[str, dict[str, Any]] = {}
        for item in inputs:
            source = item.get("source")
            if not isinstance(source, dict):
                raise CanaryError("INPUT_SOURCE_MISSING", f"{requirement_id}.{item.get('name')}")
            input_sources[str(item["name"])] = source
        nodes.append(
            {
                "requirement_id": requirement_id,
                "input_contracts": input_contracts,
                "input_sources": input_sources,
                "output_contracts": _named_contracts(requirement.get("required_outputs")),
            }
        )
    return {"schema_version": "1.0", "requirements": nodes}


def _source_clauses(requirements: list[dict[str, Any]]) -> list[dict[str, str]]:
    clauses: dict[str, str] = {}
    referenced: set[str] = set()
    for requirement in requirements:
        provenance = requirement.get("provenance")
        rows = provenance.get("source_clauses") if isinstance(provenance, dict) else None
        if not isinstance(rows, list) or not rows:
            raise CanaryError("PROVENANCE_MISSING", str(requirement.get("id") or "<missing-id>"))
        for row in rows:
            if not isinstance(row, dict) or not row.get("id") or not row.get("text"):
                raise CanaryError("PROVENANCE_MISSING", "source clause requires id and text")
            clause_id, text = str(row["id"]), str(row["text"])
            if clause_id in clauses and clauses[clause_id] != text:
                raise CanaryError("PROVENANCE_CONFLICT", clause_id)
            clauses[clause_id] = text

        context = requirement.get("semantic_context")
        if not isinstance(context, dict):
            raise CanaryError("INVALID_REQUIREMENTS", "semantic_context is missing")
        for rule in context.get("business_rules") or ():
            prov = rule.get("provenance") if isinstance(rule, dict) else None
            if not isinstance(prov, dict) or not prov.get("source_clause"):
                raise CanaryError("PROVENANCE_MISSING", f"business rule in {requirement.get('id')}")
            referenced.add(str(prov["source_clause"]))
        for binding in context.get("role_bindings") or ():
            if not isinstance(binding, dict) or not binding.get("source_clause"):
                raise CanaryError("PROVENANCE_MISSING", f"role binding in {requirement.get('id')}")
            referenced.add(str(binding["source_clause"]))

    missing = sorted(referenced - set(clauses))
    if missing:
        raise CanaryError("PROVENANCE_MISSING", f"unknown source clause references: {missing}")
    return [{"id": clause_id, "text": clauses[clause_id]} for clause_id in sorted(clauses)]


def _branches(requirements: list[dict[str, Any]]) -> dict[str, str]:
    transitions: dict[str, dict[str, Any]] = {}
    for requirement in requirements:
        context = requirement.get("semantic_context") or {}
        for transition in context.get("lifecycle_transitions") or ():
            if isinstance(transition, dict) and transition.get("id"):
                transitions[str(transition["id"])] = transition
    missing = [name for name, transition_id in REQUIRED_BRANCHES.items() if transition_id not in transitions]
    if missing:
        raise CanaryError("APPROVAL_BRANCH_MISSING", ", ".join(missing))

    confirming = False
    for transition_id in (
        REQUIRED_BRANCHES["allow"],
        REQUIRED_BRANCHES["approve"],
    ):
        for effect in transitions[transition_id].get("effects") or ():
            setter = effect.get("set") if isinstance(effect, dict) else None
            if isinstance(setter, dict) and setter.get("value") == "confirmed":
                confirming = True
    if not confirming:
        raise CanaryError("CONFIRM_BRANCH_MISSING", "allow/approve paths never set confirmed state")
    return {name: REQUIRED_BRANCHES[name] for name in sorted(REQUIRED_BRANCHES)}


def _semantic_parameters(requirements: list[dict[str, Any]]) -> dict[str, Any]:
    """Verify the fixed canary through structured semantics, never prose matching."""

    thresholds: set[object] = set()
    offsets: set[object] = set()
    channels: set[object] = set()
    approver_types: set[object] = set()
    for requirement in requirements:
        context = requirement.get("semantic_context") or {}
        for rule in context.get("business_rules") or ():
            if not isinstance(rule, dict) or rule.get("id") != "rule:long_appointment_requires_approval":
                continue
            conclusion = rule.get("conclude") or {}
            approval_request = conclusion.get("approval_request") or {}
            approver_types.add(approval_request.get("approver_type"))
            condition = rule.get("when") or {}
            for clause in condition.get("all") or ():
                comparison = clause.get("compare") if isinstance(clause, dict) else None
                if not isinstance(comparison, dict):
                    continue
                left = comparison.get("left") or {}
                right = comparison.get("right") or {}
                if left.get("property") == "rel:durationMinutes" and comparison.get("operator") == ">":
                    thresholds.add(right.get("literal"))
        for config in context.get("configuration_values") or ():
            if not isinstance(config, dict):
                continue
            path = config.get("path")
            if path == ["cap:Notification", "cap:notification.defaultReminderOffsetMinutes"]:
                offsets.add(config.get("value"))
            if path == ["cap:Notification", "delivery_channel"]:
                channels.add(config.get("value"))

    observed = {
        "approval_threshold_minutes": sorted(thresholds, key=repr),
        "reminder_offset_minutes": sorted(offsets, key=repr),
        "delivery_channel": sorted(channels, key=repr),
        "approver_type": sorted(approver_types, key=repr),
    }
    mismatches = {
        name: values
        for name, values in observed.items()
        if values != [CANARY_PARAMETERS[name]]
    }
    if mismatches:
        raise CanaryError(
            "CANARY_PARAMETER_MISMATCH",
            json.dumps({"expected": CANARY_PARAMETERS, "observed": mismatches}, sort_keys=True),
        )
    return dict(CANARY_PARAMETERS)


def run_canary(requirements_payload: dict[str, Any]) -> dict[str, Any]:
    """Return a deterministic, side-effect-free conformance result."""

    if requirements_payload.get("status") != "supported":
        raise CanaryError("REQUIREMENTS_NOT_SUPPORTED", str(requirements_payload.get("status")))
    requirements = requirements_payload.get("requirements")
    if not isinstance(requirements, list) or not requirements:
        raise CanaryError("INVALID_REQUIREMENTS", "requirements must be a non-empty array")

    action_ids = [str(requirement.get("semantic_action") or "") for requirement in requirements]
    resolved_actions: list[dict[str, Any]] = []
    for action_id in action_ids:
        try:
            resolved_actions.append(resolve_action(action_id, ROOT))
        except CatalogError as exc:
            raise CanaryError("UNRESOLVED_ACTION", str(exc)) from exc
    missing_actions = sorted(set(REQUIRED_ACTIONS) - set(action_ids))
    if missing_actions:
        raise CanaryError("REQUIRED_ACTION_MISSING", ", ".join(missing_actions))

    source_clauses = _source_clauses(requirements)
    branches = _branches(requirements)
    semantic_parameters = _semantic_parameters(requirements)
    graph = _provider_graph(requirements)
    try:
        from data_contracts.composition import ProviderGraphError, validate_provider_bound_graph
    except ImportError as exc:
        raise CanaryError(
            "DATA_CONTRACTS_UNAVAILABLE",
            f"install pinned data_contracts revision {DATA_CONTRACTS_REVISION}",
        ) from exc
    try:
        graph_result = validate_provider_bound_graph(graph)
    except ProviderGraphError as exc:
        raise CanaryError("INCOMPATIBLE_GRAPH", str(exc)) from exc

    return {
        "schema_version": "1.0",
        "result": "pass",
        "source_system_spec": requirements_payload.get("source_system_spec"),
        "source_clauses": source_clauses,
        "semantic_parameters": semantic_parameters,
        "derived_branches": branches,
        "resolved_actions": resolved_actions,
        "graph_validation": {
            "validator": "data_contracts.composition.validate_provider_bound_graph",
            "data_contracts_revision": DATA_CONTRACTS_REVISION,
            "order": list(graph_result.order),
            "seed_contracts": list(graph_result.seed_contracts),
        },
        "side_effects_executed": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--compiler-repo", type=Path, required=True)
    parser.add_argument("--compiler-revision", required=True)
    parser.add_argument("--requirements-path", required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        payload, compiler_revision = load_git_json(
            args.compiler_repo, args.compiler_revision, args.requirements_path
        )
        result = run_canary(payload)
        raw_input = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
        result["source_revisions"] = {
            "compiler": compiler_revision,
            "capability_catalog": _git(ROOT, "rev-parse", "HEAD"),
            "data_contracts": DATA_CONTRACTS_REVISION,
        }
        result["requirements_sha256"] = hashlib.sha256(raw_input).hexdigest()
        rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(rendered, encoding="utf-8")
        print(rendered, end="")
        return 0
    except CanaryError as exc:
        print(json.dumps({"result": "fail", "code": exc.code, "detail": exc.detail}, sort_keys=True), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
