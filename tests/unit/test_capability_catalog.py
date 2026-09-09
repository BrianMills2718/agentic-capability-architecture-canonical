import importlib
import json
from pathlib import Path
import subprocess
import sys

import pytest
import yaml
from tools.capability_catalog import CatalogError, build_catalog, resolve_action

ROOT = Path(__file__).resolve().parents[2]
EXPECTED = {
    "approval.action.bind": ("approvals", "na_approvals.binding.bind_approval"),
    "approval.action.verify": ("approvals", "na_approvals.binding.verify_approval"),
    "approval.resolve": ("approvals", "na_approvals.engine.resolve"),
    "availability.query": ("scheduling", "na_scheduling.availability.is_available"),
    "notification.email.send": ("notifications", "na_notifications.email.send_email"),
    "state.transition.plan": ("core", "na_core.transitions.plan_transition"),
}


def test_catalog_contains_only_audited_semantic_exports():
    actions = build_catalog()["semantic_actions"]
    actual = {
        item["action_id"]: (item["capability"], item["public_interface"])
        for item in actions
    }
    assert actual == EXPECTED
    assert all(item["source_file"].endswith(".py") for item in actions)


def test_exact_resolution_returns_declared_public_interface():
    item = resolve_action("state.transition.plan")
    assert item["capability"] == "core"
    assert item["public_interface"] == "na_core.transitions.plan_transition"
    assert item["source_file"].endswith("na_core/na_core/transitions.py")
    with pytest.raises(CatalogError, match="unknown semantic action"):
        resolve_action("state.transition")


def test_exported_interfaces_are_real_callables():
    registry = yaml.safe_load((ROOT / "capability_registry.yml").read_text(encoding="utf-8"))
    added = []
    try:
        for capability, _ in EXPECTED.values():
            entry = registry["capabilities"][capability]
            manifest = yaml.safe_load((ROOT / entry["path"] / "capability.yml").read_text(encoding="utf-8"))
            runtime_path = manifest.get("runtime_path") or entry.get("runtime_path")
            if runtime_path:
                value = str(ROOT / runtime_path)
                if value not in sys.path:
                    sys.path.insert(0, value)
                    added.append(value)
        for _, public_interface in EXPECTED.values():
            module_name, attr_name = public_interface.rsplit(".", 1)
            module = importlib.import_module(module_name)
            assert callable(getattr(module, attr_name))
    finally:
        for value in added:
            sys.path.remove(value)


def test_catalog_rejects_non_public_export(tmp_path):
    (tmp_path / "capabilities/example").mkdir(parents=True)
    (tmp_path / "capability_registry.yml").write_text(
        "schema_version: 1\ncapabilities:\n  example:\n    path: capabilities/example\n",
        encoding="utf-8",
    )
    (tmp_path / "capabilities/example/capability.yml").write_text(
        "name: example\nversion: 1\nstatus: candidate\n"
        "provides: [example.run]\npublic_interfaces: [example.public]\n"
        "semantic_exports:\n  - action_id: example.run\n    public_interface: example.private\n",
        encoding="utf-8",
    )
    with pytest.raises(CatalogError, match="non-public interface"):
        build_catalog(tmp_path)


def test_catalog_rejects_export_whose_callable_does_not_exist(tmp_path):
    (tmp_path / "capabilities/example").mkdir(parents=True)
    runtime = tmp_path / "runtime"
    (runtime / "example").mkdir(parents=True)
    (runtime / "example/module.py").write_text(
        "def other():\n    return 1\n",
        encoding="utf-8",
    )
    (tmp_path / "capability_registry.yml").write_text(
        "schema_version: 1\ncapabilities:\n  example:\n"
        "    path: capabilities/example\n    runtime_path: runtime\n",
        encoding="utf-8",
    )
    (tmp_path / "capabilities/example/capability.yml").write_text(
        "name: example\nversion: 1\nstatus: candidate\nruntime_path: runtime\n"
        "provides: [example.run]\npublic_interfaces: [example.module.run]\n"
        "semantic_exports:\n  - action_id: example.run\n    public_interface: example.module.run\n",
        encoding="utf-8",
    )
    with pytest.raises(CatalogError, match="does not resolve to a top-level function/class"):
        build_catalog(tmp_path)


def test_list_cli_is_machine_readable_json():
    result = subprocess.run(
        [sys.executable, "tools/capability_catalog.py", "list", "--json"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    payload = json.loads(result.stdout)
    assert {item["action_id"] for item in payload["semantic_actions"]} == set(EXPECTED)
