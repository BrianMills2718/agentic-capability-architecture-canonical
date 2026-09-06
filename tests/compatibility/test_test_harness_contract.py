from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def test_pytest_uses_importlib_mode_for_modular_test_names():
    pytest_ini = (ROOT / "pytest.ini").read_text(encoding="utf-8")
    assert "--import-mode=importlib" in pytest_ini


def test_agent_completion_gate_requires_full_bootstrap_check():
    agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    assert "python tools/check_bootstrap.py" in agents
    assert "do **not** substitute" in agents


def test_bootstrap_discovers_nested_frappe_app_tests_and_import_paths():
    checker = (ROOT / "tools/check_bootstrap.py").read_text(encoding="utf-8")
    assert "discover_frappe_apps" in checker
    assert "discover_test_targets" in checker
    assert "PYTHONPATH" in checker


def test_package_check_validates_frappe_module_markers():
    checker = (ROOT / "tools/check_frappe_packages.py").read_text(encoding="utf-8")
    assert "validate_frappe_module_layout" in checker
    assert "modules.txt" in checker
