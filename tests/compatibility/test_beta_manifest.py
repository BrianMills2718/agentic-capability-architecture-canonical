from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]


def test_beta_reference_composes_existing_capabilities():
    manifest = yaml.safe_load(
        (ROOT / "clients/beta_reference/manifest.yml").read_text(encoding="utf-8")
    )

    assert set(manifest["capabilities"]) == {
        "core",
        "scheduling",
        "approvals",
        "notifications",
    }
    assert manifest["configuration"]["scheduling"]["approval_threshold_minutes"] == 90
    assert manifest["configuration"]["scheduling"]["reminder"] == {
        "enabled": True,
        "channel": "email",
        "minutes_before": 60,
    }
    assert manifest["custom_extensions"] == ["beta_rules"]
