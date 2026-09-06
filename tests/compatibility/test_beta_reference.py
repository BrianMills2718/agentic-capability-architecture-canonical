from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]


def test_beta_composes_registered_capabilities_and_custom_extension():
    manifest = yaml.safe_load(
        (ROOT / "clients/beta_reference/manifest.yml").read_text(encoding="utf-8")
    )

    assert set(manifest["capabilities"]) == {
        "core",
        "scheduling",
        "approvals",
        "notifications",
    }
    assert manifest["custom_extensions"] == ["beta_rules"]


def test_beta_scheduler_wiring_uses_notifications_and_is_hourly():
    hooks = (
        ROOT
        / "clients/beta_reference/custom/frappe_app/beta_rules/beta_rules/hooks.py"
    ).read_text(encoding="utf-8")
    scheduler = (
        ROOT
        / "clients/beta_reference/custom/frappe_app/beta_rules/beta_rules/reminder_scheduler.py"
    ).read_text(encoding="utf-8")

    assert '"hourly"' in hooks
    assert "beta_rules.reminder_scheduler.schedule_reminders" in hooks
    assert "from na_notifications.email import send_email" in scheduler
    assert "Appointment Reminder Sent" in scheduler
