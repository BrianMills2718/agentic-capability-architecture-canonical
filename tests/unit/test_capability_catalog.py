import importlib
import json
from pathlib import Path
import subprocess
import sys

import pytest
from tools.capability_catalog import CatalogError, build_catalog, resolve_action

ROOT = Path(__file__).resolve().parents[2]
EXPECTED = {
    "approval.resolve": ("approvals", "na_approvals.engine.resolve"),
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


def test_exact_resolution_returns_declared_public_interface():
    item = resolve_action("state.transition.plan")
    assert item["capability"] == "core"
    assert item["public_interface"] == "na_core.transitions.plan_transition"
    with pytest.raises(CatalogError, match="unknown semantic action"):
        resolve_action("state.transition")


def test_exported_interfaces_are_real_callables():
    for _, public_interface in EXPECTED.values():
        module_name, attr_name = public_interface.rsplit(".", 1)
        module = importlib.import_module(module_name)
        assert callable(getattr(module, attr_name))


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
