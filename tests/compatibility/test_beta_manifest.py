from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]


def test_beta_reference_composes_registered_capabilities():
    registry = yaml.safe_load((ROOT / "capability_registry.yml").read_text(encoding="utf-8"))
    manifest = yaml.safe_load(
        (ROOT / "clients/beta_reference/manifest.yml").read_text(encoding="utf-8")
    )
    assert set(manifest["capabilities"]) <= set(registry["capabilities"])
    assert manifest["custom_extensions"] == ["beta_rules"]


def test_beta_reminder_has_an_explicit_hourly_trigger():
    hooks = (
        ROOT
        / "clients/beta_reference/custom/frappe_app/beta_rules/beta_rules/hooks.py"
    ).read_text(encoding="utf-8")
    assert '"hourly"' in hooks
    assert "beta_rules.reminders.send_due_reminders" in hooks
