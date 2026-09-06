from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]


def load_yaml(path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def test_reference_project_uses_registered_capabilities():
    registry = load_yaml(ROOT / "capability_registry.yml")
    manifest = load_yaml(ROOT / "clients/acme_reference/manifest.yml")

    registered = set(registry["capabilities"])
    requested = set(manifest["capabilities"])

    assert requested <= registered


def test_reference_project_keeps_custom_logic_outside_shared_capabilities():
    manifest = load_yaml(ROOT / "clients/acme_reference/manifest.yml")
    assert manifest["custom_extensions"] == ["acme_rules"]

    custom = ROOT / "clients/acme_reference/custom/frappe_app/acme_rules"
    assert custom.exists()

    # Shared runtime/source must not contain ACME-specific behavior.
    # Capability metadata may legitimately name ACME as reuse evidence.
    scheduling_runtime = ROOT / "capabilities/scheduling/frappe_app/na_scheduling"
    text_suffixes = {".py", ".json", ".md", ".yml", ".yaml", ".toml", ".txt"}
    for path in scheduling_runtime.rglob("*"):
        if path.is_file() and path.suffix in text_suffixes:
            assert "acme" not in path.read_text(encoding="utf-8").lower()
