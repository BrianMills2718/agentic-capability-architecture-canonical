from pathlib import Path
import subprocess
import sys

import yaml

ROOT = Path(__file__).resolve().parents[2]
TOOL = ROOT / "tools" / "engagement.py"


def run(*args, check=True):
    return subprocess.run(
        [sys.executable, str(TOOL), *map(str, args)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=check,
    )


def read_yaml(path):
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))


def write_yaml(path, data):
    Path(path).write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")


def make_workspace(tmp_path, engagement_id="job_alpha"):
    task = tmp_path / "TASK.md"
    task.write_text(
        "# Small workflow job\n\nImplement an Open -> Done transition and send email after a real change.\n",
        encoding="utf-8",
    )
    workspace = tmp_path / "workspace"
    run(
        "new",
        engagement_id,
        "--task",
        task,
        "--output",
        workspace,
        "--client-reference",
        "client-alias-42",
        "--acceptance-command",
        "python -m pytest",
    )
    return workspace


def ready_plan(workspace):
    plan_path = workspace / "CAPABILITY_PLAN.yml"
    plan = read_yaml(plan_path)
    plan["status"] = "ready"
    plan["selected"] = [
        {
            "source_class": "internal",
            "candidate": "core",
            "requirement_ids": ["task_complete"],
            "semantic_actions": ["state.transition.plan"],
            "interfaces": ["na_core.transitions.plan_transition"],
            "reason": "Reuse the shared transition planner instead of reimplementing state validation.",
        },
        {
            "source_class": "internal",
            "candidate": "notifications",
            "requirement_ids": ["task_complete"],
            "semantic_actions": ["notification.email.send"],
            "interfaces": ["na_notifications.email.send_email"],
            "reason": "Reuse the shared email transport.",
        },
    ]
    plan["rejected"] = [
        {
            "source_class": "internal",
            "candidate": "scheduling",
            "requirement_ids": ["task_complete"],
            "reason": "The task has no appointment or availability behavior.",
        }
    ]
    plan["composition"] = [
        {
            "requirement_ids": ["task_complete"],
            "components": ["core", "notifications"],
            "description": "Compose transition planning with notification transport; timing remains local.",
        }
    ]
    plan["local_gaps"] = [
        {
            "requirement_ids": ["task_complete"],
            "behavior": "Job-specific notification timing and recipient selection.",
            "reason": "These are consequential domain semantics, not generic transport behavior.",
        }
    ]
    write_yaml(plan_path, plan)


def finish_evidence_and_metrics(workspace):
    evidence_path = workspace / "EVIDENCE_PROPOSAL.yml"
    evidence = read_yaml(evidence_path)
    evidence["outcome"] = "success"
    evidence["reuse_observations"] = ["Shared transition planning composed cleanly with notification transport."]
    evidence["rejected_fits"] = ["Scheduling was correctly rejected for a non-scheduling workflow."]
    evidence["compatibility_findings"] = ["Core and Notifications worked together through declared public interfaces."]
    evidence["candidate_capabilities"] = ["workflow.changed_event_notify may merit observation if it recurs across domains."]
    evidence["keep_local"] = ["Recipient and notification timing remain job-local."]
    evidence["sanitization"]["contains_client_confidential"] = False
    evidence["sanitization"]["contains_client_owned_code"] = False
    write_yaml(evidence_path, evidence)

    metrics_path = workspace / "METRICS.yml"
    metrics = read_yaml(metrics_path)
    metrics.update(
        {
            "revenue": 1000,
            "contractor_cost": 350,
            "human_hours": 2.5,
            "agent_hours": 0.5,
            "requirements_reused": 1,
            "requirements_composed": 1,
            "local_lines_changed": 80,
            "rework_events": 0,
        }
    )
    write_yaml(metrics_path, metrics)


def test_new_engagement_builds_portable_snapshot_with_verified_exports(tmp_path):
    workspace = make_workspace(tmp_path)
    assert (workspace / "snapshot/capability_registry.yml").exists()
    assert (workspace / "snapshot/vendor/na_core/na_core/transitions.py").exists()
    assert (workspace / "snapshot/vendor/na_notifications/na_notifications/email.py").exists()
    assert (workspace / "control/engagement.py").exists()
    assert (workspace / "schemas/capability_plan.schema.json").exists()
    registry = read_yaml(workspace / "snapshot/capability_registry.yml")
    assert set(registry["capabilities"]) == {"approvals", "core", "notifications", "scheduling"}
    assert registry["source_commit"]
    core_exports = registry["capabilities"]["core"]["semantic_exports"]
    assert core_exports == [
        {
            "action_id": "state.transition.plan",
            "public_interface": "na_core.transitions.plan_transition",
        }
    ]
    result = run("validate", workspace)
    assert "snapshot checksum consistency" in result.stdout
    portable = subprocess.run(
        [sys.executable, "control/engagement.py", "validate", "."],
        cwd=workspace,
        text=True,
        capture_output=True,
        check=True,
    )
    assert "snapshot checksum consistency" in portable.stdout


def test_ready_plan_requires_real_internal_capabilities_and_interfaces(tmp_path):
    workspace = make_workspace(tmp_path)
    ready_plan(workspace)
    result = run("validate", workspace, "--require-ready")
    assert result.returncode == 0

    plan_path = workspace / "CAPABILITY_PLAN.yml"
    plan = read_yaml(plan_path)
    plan["selected"][0]["candidate"] = "imaginary_shared_framework"
    write_yaml(plan_path, plan)
    result = run("validate", workspace, "--require-ready", check=False)
    assert result.returncode != 0
    assert "is not in the snapshot" in result.stderr


def test_ready_plan_rejects_broad_provides_label_as_semantic_action(tmp_path):
    workspace = make_workspace(tmp_path)
    plan_path = workspace / "CAPABILITY_PLAN.yml"
    plan = read_yaml(plan_path)
    plan["status"] = "ready"
    plan["selected"] = [
        {
            "source_class": "internal",
            "candidate": "scheduling",
            "requirement_ids": ["task_complete"],
            "semantic_actions": ["appointment.reschedule"],
            "interfaces": [],
            "reason": "This broad provides label should not count as an executable export.",
        }
    ]
    plan["local_gaps"] = []
    write_yaml(plan_path, plan)

    result = run("validate", workspace, "--require-ready", check=False)
    assert result.returncode != 0
    assert "is not a verified semantic export" in result.stderr


def test_ready_plan_requires_bound_interface_for_semantic_action(tmp_path):
    workspace = make_workspace(tmp_path)
    ready_plan(workspace)
    plan_path = workspace / "CAPABILITY_PLAN.yml"
    plan = read_yaml(plan_path)
    plan["selected"][0]["interfaces"] = []
    write_yaml(plan_path, plan)

    result = run("validate", workspace, "--require-ready", check=False)
    assert result.returncode != 0
    assert "must include its bound public interface" in result.stderr


def test_snapshot_change_is_detected_against_shipped_checksum(tmp_path):
    workspace = make_workspace(tmp_path)
    target = workspace / "snapshot/metadata/core/capability.yml"
    target.write_text(target.read_text(encoding="utf-8") + "\n# changed\n", encoding="utf-8")
    result = run("validate", workspace, check=False)
    assert result.returncode != 0
    assert "snapshot file changed" in result.stderr


def test_closeout_emits_proposal_without_client_or_financial_fields(tmp_path):
    workspace = make_workspace(tmp_path)
    ready_plan(workspace)
    finish_evidence_and_metrics(workspace)
    run("close", workspace)

    proposal_text = (workspace / "CANONICAL_EVIDENCE_PROPOSAL.yml").read_text(encoding="utf-8")
    summary_text = (workspace / "CLOSEOUT_SUMMARY.md").read_text(encoding="utf-8")
    assert "client-alias-42" not in proposal_text
    assert "revenue" not in proposal_text.lower()
    assert "1000" not in proposal_text
    assert "pending_human_review" in proposal_text
    assert "65%" not in proposal_text
    assert "Gross contribution before overhead: 650" in summary_text
    assert "Satisfied through multi-component composition: 1 (100%)" in summary_text
    assert "requires human sanitization review" in summary_text


def test_closeout_blocks_evidence_until_human_flags_are_cleared(tmp_path):
    workspace = make_workspace(tmp_path)
    ready_plan(workspace)
    evidence_path = workspace / "EVIDENCE_PROPOSAL.yml"
    evidence = read_yaml(evidence_path)
    evidence["outcome"] = "success"
    write_yaml(evidence_path, evidence)
    result = run("close", workspace, check=False)
    assert result.returncode != 0
    assert "review/sanitize EVIDENCE_PROPOSAL.yml" in result.stderr
