#!/usr/bin/env python3
"""Create, validate, and close isolated paid/client engagement workspaces.

The canonical repository supplies reusable background capability knowledge. Client
work product stays in the engagement workspace. Closeout emits only a sanitized,
human-reviewable evidence proposal; it never promotes capability code automatically.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
from typing import Any

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = ROOT / "schemas"

SOURCE_CLASSES = {
    "platform_native",
    "ecosystem",
    "external_oss",
    "external_saas",
    "standard",
    "internal",
}


def load_yaml(path: Path) -> Any:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def write_yaml(path: Path, data: Any) -> None:
    path.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True), encoding="utf-8")


def load_schema(name: str) -> dict[str, Any]:
    return json.loads((SCHEMAS / name).read_text(encoding="utf-8"))


def schema_errors(path: Path, schema_name: str) -> list[str]:
    try:
        data = load_yaml(path)
    except Exception as exc:  # pragma: no cover - surfaced as validation output
        return [f"{path.name}: unable to parse YAML: {exc}"]
    validator = Draft202012Validator(load_schema(schema_name))
    errors = []
    for error in sorted(validator.iter_errors(data), key=lambda item: list(item.path)):
        where = ".".join(str(piece) for piece in error.path) or "<root>"
        errors.append(f"{path.name}:{where}: {error.message}")
    return errors


def git_head() -> str:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, check=True, capture_output=True, text=True
    )
    return result.stdout.strip()


def task_title(task_text: str, engagement_id: str) -> str:
    for line in task_text.splitlines():
        if line.startswith("# ") and line[2:].strip():
            return line[2:].strip()
    return engagement_id.replace("_", " ").replace("-", " ").title()


def dependency_closed(names: list[str], registry: dict[str, Any]) -> list[str]:
    known = registry["capabilities"]
    if names == ["all"]:
        return sorted(known)
    unknown = sorted(set(names) - set(known))
    if unknown:
        raise SystemExit("unknown capabilities: " + ", ".join(unknown))
    selected = set(names)
    changed = True
    while changed:
        changed = False
        for name in list(selected):
            for dependency in known[name].get("requires", []):
                if dependency not in selected:
                    selected.add(dependency)
                    changed = True
    return sorted(selected)


def runtime_source(name: str, registry_entry: dict[str, Any], metadata: dict[str, Any]) -> Path | None:
    runtime_path = metadata.get("runtime_path") or registry_entry.get("runtime_path")
    if runtime_path:
        path = ROOT / runtime_path
        if path.exists():
            return path
    frappe_root = ROOT / "capabilities" / name / "frappe_app"
    candidates = [path for path in frappe_root.iterdir()] if frappe_root.exists() else []
    candidates = [path for path in candidates if path.is_dir()]
    return candidates[0] if len(candidates) == 1 else None


def hash_snapshot(snapshot: Path) -> None:
    rows = []
    for path in sorted(snapshot.rglob("*")):
        if not path.is_file() or path.name == "SHA256SUMS":
            continue
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        rows.append(f"{digest}  {path.relative_to(snapshot).as_posix()}")
    (snapshot / "SHA256SUMS").write_text("\n".join(rows) + "\n", encoding="utf-8")


def verify_snapshot(snapshot: Path) -> list[str]:
    sums = snapshot / "SHA256SUMS"
    if not sums.exists():
        return ["snapshot/SHA256SUMS is missing"]
    errors = []
    expected_files: set[str] = set()
    for row in sums.read_text(encoding="utf-8").splitlines():
        if not row.strip():
            continue
        expected, relative = row.split("  ", 1)
        expected_files.add(relative)
        path = snapshot / relative
        if not path.exists():
            errors.append(f"snapshot file missing: {relative}")
            continue
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != expected:
            errors.append(f"snapshot file changed: {relative}")
    actual_files = {
        path.relative_to(snapshot).as_posix()
        for path in snapshot.rglob("*")
        if path.is_file() and path.name != "SHA256SUMS"
    }
    for relative in sorted(actual_files - expected_files):
        errors.append(f"unexpected file added to read-only snapshot: {relative}")
    return errors


def create_snapshot(workspace: Path, capability_names: list[str], baseline: str) -> None:
    source_registry = load_yaml(ROOT / "capability_registry.yml")
    names = dependency_closed(capability_names, source_registry)
    snapshot = workspace / "snapshot"
    metadata_root = snapshot / "metadata"
    vendor_root = snapshot / "vendor"
    metadata_root.mkdir(parents=True)
    vendor_root.mkdir()

    portable_registry = {"schema_version": 1, "source_commit": baseline, "capabilities": {}}
    for name in names:
        source_entry = copy.deepcopy(source_registry["capabilities"][name])
        source_dir = ROOT / source_entry["path"]
        metadata = load_yaml(source_dir / "capability.yml")
        destination = metadata_root / name
        destination.mkdir()
        shutil.copy2(source_dir / "capability.yml", destination / "capability.yml")
        if (source_dir / "README.md").exists():
            shutil.copy2(source_dir / "README.md", destination / "README.md")

        source_entry["path"] = f"metadata/{name}"
        source_entry["metadata_path"] = f"metadata/{name}"
        runtime = runtime_source(name, source_entry, metadata)
        if runtime:
            vendor_name = runtime.name
            shutil.copytree(
                runtime,
                vendor_root / vendor_name,
                ignore=shutil.ignore_patterns(
                    "__pycache__", ".pytest_cache", "build", "dist", "*.egg-info", "*.pyc"
                ),
            )
            source_entry["runtime_path"] = f"vendor/{vendor_name}"
        else:
            source_entry.pop("runtime_path", None)
        portable_registry["capabilities"][name] = source_entry

    write_yaml(snapshot / "capability_registry.yml", portable_registry)
    (snapshot / "README.md").write_text(
        "# Read-only capability snapshot\n\n"
        f"Generated from canonical commit `{baseline}`. Treat `metadata/`, `vendor/`, and "
        "`capability_registry.yml` as read-only background capability material. Client work "
        "belongs outside this directory. `SHA256SUMS` is checked during engagement validation.\n",
        encoding="utf-8",
    )
    hash_snapshot(snapshot)


def agent_rules() -> str:
    return """# Engagement Agent Rules

1. Read `ENGAGEMENT.yml`, `TASK.md`, and `snapshot/capability_registry.yml` before implementation.
2. Treat `snapshot/` as read-only background capability material. Do not modify or copy client-specific behavior into it.
3. Before writing implementation code, complete `CAPABILITY_PLAN.yml` and set `status: ready`.
4. Source before building: platform/native, ecosystem, mature OSS/SaaS, standards, internal capabilities, then residual local gap.
5. Record material rejected candidates. Internal reuse is not automatically preferable to a better existing option.
6. Compose through declared public interfaces when multiple capabilities jointly satisfy a requirement. Do not reimplement shared behavior locally.
7. Keep consequential client/domain semantics in the engagement implementation. Do not invent a generic framework, registry, workflow engine, or universal abstraction for one job.
8. Client work product, client source, secrets, and confidential material must stay in this engagement workspace and must never be proposed for canonical ingestion.
9. Before closeout, complete `EVIDENCE_PROPOSAL.yml` with generalized learnings only. Set both sanitization flags to `false` only after removing client-confidential information and client-owned code.
10. Complete `METRICS.yml` after delivery so reuse/composition economics can be measured. Business metrics remain engagement-local.
11. Obey `ENGAGEMENT.yml` `research.external_allowed`; when it is false, do not use external research beyond the supplied workspace.
12. Run `python control/engagement.py validate . --require-ready` before declaring the capability plan complete.
13. A human reviewer decides whether any generalized evidence or reusable capability is promoted into the canonical ecosystem.
"""


def command_new(args: argparse.Namespace) -> None:
    task_path = Path(args.task).expanduser().resolve()
    if not task_path.is_file():
        raise SystemExit(f"task file not found: {task_path}")
    output = Path(args.output).expanduser().resolve() if args.output else ROOT / "workspaces" / args.engagement_id
    if output.exists():
        raise SystemExit(f"engagement workspace already exists: {output}")
    output.mkdir(parents=True)

    task_text = task_path.read_text(encoding="utf-8")
    (output / "TASK.md").write_text(task_text, encoding="utf-8")
    (output / "AGENT_RULES.md").write_text(agent_rules(), encoding="utf-8")
    control = output / "control"
    control.mkdir()
    shutil.copy2(Path(__file__), control / "engagement.py")
    (output / "schemas").mkdir()
    for schema_name in [
        "engagement.schema.json",
        "capability_plan.schema.json",
        "evidence_proposal.schema.json",
        "engagement_metrics.schema.json",
    ]:
        shutil.copy2(SCHEMAS / schema_name, output / "schemas" / schema_name)
    (control / "requirements.txt").write_text("jsonschema>=4,<5\nPyYAML>=6,<7\n", encoding="utf-8")
    baseline = git_head()
    capabilities = [item.strip() for item in args.capabilities.split(",") if item.strip()]
    create_snapshot(output, capabilities or ["all"], baseline)

    engagement = {
        "schema_version": 1,
        "engagement_id": args.engagement_id,
        "client_reference": args.client_reference or "",
        "task": {"title": task_title(task_text, args.engagement_id), "source": "TASK.md"},
        "requirements": [
            {
                "id": "task_complete",
                "description": "Complete the behavior and deliverables described in TASK.md.",
                "acceptance": ["All explicit acceptance conditions in TASK.md are satisfied."],
            }
        ],
        "deliverables": ["working implementation", "tests or executable validation", "handoff notes"],
        "constraints": ["Do not modify the read-only capability snapshot."],
        "research": {"external_allowed": bool(args.external_research)},
        "capability_snapshot": {
            "baseline_commit": baseline,
            "registry": "snapshot/capability_registry.yml",
            "mode": "read_only",
        },
        "ip_boundary": {
            "client_work_product_stays_local": True,
            "canonical_capabilities_are_background": True,
            "prohibit_client_code_into_canonical": True,
        },
        "completion": {
            "required_files": ["CAPABILITY_PLAN.yml", "EVIDENCE_PROPOSAL.yml", "METRICS.yml"],
            "acceptance_commands": args.acceptance_command or [],
        },
    }
    write_yaml(output / "ENGAGEMENT.yml", engagement)
    write_yaml(
        output / "CAPABILITY_PLAN.yml",
        {
            "schema_version": 1,
            "engagement_id": args.engagement_id,
            "status": "draft",
            "selected": [],
            "rejected": [],
            "composition": [],
            "local_gaps": [],
        },
    )
    write_yaml(
        output / "EVIDENCE_PROPOSAL.yml",
        {
            "schema_version": 1,
            "engagement_id": args.engagement_id,
            "outcome": "pending",
            "reuse_observations": [],
            "rejected_fits": [],
            "compatibility_findings": [],
            "candidate_capabilities": [],
            "keep_local": [],
            "sanitization": {
                "contains_client_confidential": True,
                "contains_client_owned_code": True,
                "reviewer_required": True,
            },
        },
    )
    write_yaml(
        output / "METRICS.yml",
        {
            "schema_version": 1,
            "engagement_id": args.engagement_id,
            "currency": "USD",
            "revenue": None,
            "contractor_cost": None,
            "human_hours": None,
            "agent_hours": None,
            "requirements_total": 1,
            "requirements_reused": 0,
            "requirements_composed": 0,
            "local_lines_changed": None,
            "rework_events": 0,
        },
    )
    print(output)
    print("Edit ENGAGEMENT.yml to make requirement/acceptance items precise before contractor handoff.")
    print(f"Validate intake with: {sys.executable} {Path(__file__)} validate {output}")
    print("Contractor self-check: python control/engagement.py validate . --require-ready")


def validate_workspace(workspace: Path, require_ready: bool = False) -> list[str]:
    errors: list[str] = []
    contracts = {
        "ENGAGEMENT.yml": "engagement.schema.json",
        "CAPABILITY_PLAN.yml": "capability_plan.schema.json",
        "EVIDENCE_PROPOSAL.yml": "evidence_proposal.schema.json",
        "METRICS.yml": "engagement_metrics.schema.json",
    }
    for filename, schema in contracts.items():
        path = workspace / filename
        if not path.exists():
            errors.append(f"missing required contract: {filename}")
            continue
        errors.extend(schema_errors(path, schema))
    if errors:
        return errors

    engagement = load_yaml(workspace / "ENGAGEMENT.yml")
    plan = load_yaml(workspace / "CAPABILITY_PLAN.yml")
    evidence = load_yaml(workspace / "EVIDENCE_PROPOSAL.yml")
    metrics = load_yaml(workspace / "METRICS.yml")
    engagement_id = engagement["engagement_id"]
    for filename, data in [("CAPABILITY_PLAN.yml", plan), ("EVIDENCE_PROPOSAL.yml", evidence), ("METRICS.yml", metrics)]:
        if data["engagement_id"] != engagement_id:
            errors.append(f"{filename}: engagement_id does not match ENGAGEMENT.yml")

    requirement_ids = [item["id"] for item in engagement["requirements"]]
    if len(requirement_ids) != len(set(requirement_ids)):
        errors.append("ENGAGEMENT.yml: requirement ids must be unique")
    known_requirements = set(requirement_ids)
    if metrics["requirements_total"] != len(requirement_ids):
        errors.append("METRICS.yml: requirements_total must match ENGAGEMENT.yml")
    if metrics["requirements_reused"] > metrics["requirements_total"]:
        errors.append("METRICS.yml: requirements_reused cannot exceed requirements_total")
    if metrics["requirements_composed"] > metrics["requirements_total"]:
        errors.append("METRICS.yml: requirements_composed cannot exceed requirements_total")

    for filename in ["TASK.md", "AGENT_RULES.md", *engagement["completion"]["required_files"]]:
        if not (workspace / filename).exists():
            errors.append(f"required engagement file missing: {filename}")
    errors.extend(verify_snapshot(workspace / "snapshot"))

    registry_path = workspace / engagement["capability_snapshot"]["registry"]
    if not registry_path.exists():
        errors.append("capability snapshot registry is missing")
        return errors
    registry = load_yaml(registry_path)
    internal = registry.get("capabilities", {})

    referenced: set[str] = set()
    selected_names = {item["candidate"] for item in plan["selected"]}
    for section in ["selected", "rejected", "composition", "local_gaps"]:
        for item in plan[section]:
            for requirement_id in item["requirement_ids"]:
                referenced.add(requirement_id)
                if requirement_id not in known_requirements:
                    errors.append(f"CAPABILITY_PLAN.yml:{section}: unknown requirement_id {requirement_id!r}")

    for item in plan["selected"]:
        if item["source_class"] not in SOURCE_CLASSES:
            errors.append(f"CAPABILITY_PLAN.yml:selected: invalid source class {item['source_class']!r}")
            continue
        if item["source_class"] != "internal":
            continue
        candidate = item["candidate"]
        if candidate not in internal:
            errors.append(f"CAPABILITY_PLAN.yml:selected: internal capability {candidate!r} is not in the snapshot")
            continue
        entry = internal[candidate]
        provided = set(entry.get("provides", []))
        for action in item.get("semantic_actions", []):
            if action not in provided:
                errors.append(f"CAPABILITY_PLAN.yml:selected: {candidate!r} does not provide {action!r}")
        metadata_path = workspace / "snapshot" / "metadata" / candidate / "capability.yml"
        metadata = load_yaml(metadata_path) if metadata_path.exists() else {}
        declared_interfaces = set(metadata.get("public_interfaces", []))
        if declared_interfaces:
            for interface in item.get("interfaces", []):
                if interface not in declared_interfaces:
                    errors.append(f"CAPABILITY_PLAN.yml:selected: {candidate!r} does not declare interface {interface!r}")

    for item in plan["composition"]:
        missing = set(item["components"]) - selected_names
        if missing:
            errors.append("CAPABILITY_PLAN.yml:composition: components must be selected candidates: " + ", ".join(sorted(missing)))

    if require_ready or plan["status"] == "ready":
        if plan["status"] != "ready":
            errors.append("CAPABILITY_PLAN.yml: status must be ready")
        satisfied: set[str] = set()
        for section in ["selected", "local_gaps"]:
            for item in plan[section]:
                satisfied.update(item["requirement_ids"])
        uncovered = sorted(known_requirements - satisfied)
        if uncovered:
            errors.append("CAPABILITY_PLAN.yml: requirements have no selected provider or local gap: " + ", ".join(uncovered))

    return errors


def command_validate(args: argparse.Namespace) -> None:
    workspace = Path(args.workspace).expanduser().resolve()
    errors = validate_workspace(workspace, require_ready=args.require_ready)
    if errors:
        raise SystemExit("Engagement validation failed:\n- " + "\n- ".join(errors))
    print("OK: engagement contracts, snapshot integrity, and capability plan are valid")


def metric(value: Any) -> str:
    return "not recorded" if value is None else str(value)


def command_close(args: argparse.Namespace) -> None:
    workspace = Path(args.workspace).expanduser().resolve()
    errors = validate_workspace(workspace, require_ready=True)
    if errors:
        raise SystemExit("Engagement closeout blocked:\n- " + "\n- ".join(errors))
    engagement = load_yaml(workspace / "ENGAGEMENT.yml")
    plan = load_yaml(workspace / "CAPABILITY_PLAN.yml")
    evidence = load_yaml(workspace / "EVIDENCE_PROPOSAL.yml")
    metrics = load_yaml(workspace / "METRICS.yml")
    if evidence["outcome"] == "pending":
        raise SystemExit("Engagement closeout blocked: EVIDENCE_PROPOSAL.yml outcome is still pending")
    sanitization = evidence["sanitization"]
    if sanitization["contains_client_confidential"] or sanitization["contains_client_owned_code"]:
        raise SystemExit(
            "Engagement closeout blocked: sanitize EVIDENCE_PROPOSAL.yml and explicitly set both client-content flags to false"
        )

    portable_selected = [
        {
            "source_class": item["source_class"],
            "candidate": item["candidate"],
            "semantic_actions": item.get("semantic_actions", []),
            "interfaces": item.get("interfaces", []),
        }
        for item in plan["selected"]
    ]
    canonical = {
        "schema_version": 1,
        "source_engagement": engagement["engagement_id"],
        "capability_baseline_commit": engagement["capability_snapshot"]["baseline_commit"],
        "outcome": evidence["outcome"],
        "selected_sources": portable_selected,
        "composition_count": len(plan["composition"]),
        "reuse_observations": evidence["reuse_observations"],
        "rejected_fits": evidence["rejected_fits"],
        "compatibility_findings": evidence["compatibility_findings"],
        "candidate_capabilities": evidence["candidate_capabilities"],
        "keep_local": evidence["keep_local"],
        "review": {
            "status": "pending_human_review",
            "rule": "Do not ingest client-owned code or confidential information; promote reusable behavior only after evidence review.",
        },
    }
    write_yaml(workspace / "CANONICAL_EVIDENCE_PROPOSAL.yml", canonical)

    revenue = metrics["revenue"]
    cost = metrics["contractor_cost"]
    margin = None if revenue is None or cost is None else revenue - cost
    total = metrics["requirements_total"]
    reuse_rate = metrics["requirements_reused"] / total if total else 0
    composition_rate = metrics["requirements_composed"] / total if total else 0
    summary = f"""# Engagement Closeout — {engagement['engagement_id']}

Outcome: **{evidence['outcome']}**

## Economics and throughput

- Currency: {metrics['currency']}
- Revenue: {metric(revenue)}
- Contractor cost: {metric(cost)}
- Gross contribution before overhead: {metric(margin)}
- Human hours: {metric(metrics['human_hours'])}
- Agent hours: {metric(metrics['agent_hours'])}
- Rework events: {metrics['rework_events']}

## Capability flywheel

- Requirements: {total}
- Reused from existing capability/provider: {metrics['requirements_reused']} ({reuse_rate:.0%})
- Satisfied through multi-component composition: {metrics['requirements_composed']} ({composition_rate:.0%})
- Local lines changed: {metric(metrics['local_lines_changed'])}
- Candidate capabilities proposed: {len(evidence['candidate_capabilities'])}

`CANONICAL_EVIDENCE_PROPOSAL.yml` is sanitized proposal-only input for a human reviewer. It contains no business metrics or client task text by design.
"""
    (workspace / "CLOSEOUT_SUMMARY.md").write_text(summary, encoding="utf-8")
    print(workspace / "CANONICAL_EVIDENCE_PROPOSAL.yml")
    print(workspace / "CLOSEOUT_SUMMARY.md")


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    sub = result.add_subparsers(dest="command", required=True)

    new = sub.add_parser("new", help="Create an isolated contractor/client engagement workspace")
    new.add_argument("engagement_id")
    new.add_argument("--task", required=True, help="Markdown task file")
    new.add_argument("--output", help="Output directory; defaults to workspaces/<engagement_id>")
    new.add_argument("--client-reference", default="", help="Non-sensitive internal client/job reference")
    new.add_argument("--capabilities", default="all", help="Comma-separated internal capability candidates or 'all'")
    new.add_argument("--external-research", action="store_true", help="Allow external sourcing research for this engagement")
    new.add_argument("--acceptance-command", action="append", default=[], help="Command contractor/reviewer should run; repeatable")
    new.set_defaults(func=command_new)

    validate = sub.add_parser("validate", help="Validate engagement contracts and snapshot integrity")
    validate.add_argument("workspace")
    validate.add_argument("--require-ready", action="store_true")
    validate.set_defaults(func=command_validate)

    close = sub.add_parser("close", help="Create sanitized evidence proposal and local business closeout summary")
    close.add_argument("workspace")
    close.set_defaults(func=command_close)
    return result


def main() -> None:
    args = parser().parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
