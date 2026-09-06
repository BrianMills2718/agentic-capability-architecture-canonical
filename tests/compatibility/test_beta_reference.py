from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]


def test_beta_manifest_composes_registered_capabilities():
    registry = yaml.safe_load((ROOT / "capability_registry.yml").read_text())
    manifest = yaml.safe_load((ROOT / "clients/beta_reference/manifest.yml").read_text())
    assert set(manifest["capabilities"]) <= set(registry["capabilities"])
    assert manifest["custom_extensions"] == ["beta_rules"]


def test_beta_reminders_are_scheduler_wired():
    hooks = (ROOT / "clients/beta_reference/custom/frappe_app/beta_rules/beta_rules/hooks.py").read_text()
    assert "scheduler_events" in hooks
    assert "send_due_appointment_reminders" in hooks
    assert "na_notifications" in hooks
