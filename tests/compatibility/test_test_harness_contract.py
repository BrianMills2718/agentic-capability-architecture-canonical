from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def test_pytest_uses_importlib_mode_for_modular_test_names():
    pytest_ini = (ROOT / "pytest.ini").read_text(encoding="utf-8")
    assert "--import-mode=importlib" in pytest_ini


def test_agent_completion_gate_requires_full_bootstrap_check():
    agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    assert "python tools/check_bootstrap.py" in agents
    assert "do **not** substitute" in agents
