from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WORKFLOW = ROOT / ".github" / "workflows" / "frappe-integration.yml"
RUNNER = ROOT / "tools" / "run_frappe_reference_tests.sh"


def test_frappe_ci_workflow_has_required_runtime_and_proof_steps():
    text = WORKFLOW.read_text(encoding="utf-8")

    required = [
        "frappe-branch version-15",
        "mariadb:10.6",
        "redis:alpine",
        'python-version: "3.11"',
        'node-version: "20"',
        "bench new-site",
        "run_frappe_reference_tests.sh",
    ]

    for item in required:
        assert item in text, f"Frappe CI contract missing: {item}"


def test_local_frappe_runner_enables_tests_and_runs_acme_integration_suite():
    text = RUNNER.read_text(encoding="utf-8")

    assert 'set-config allow_tests true' in text
    assert 'run-tests --app acme_rules' in text
    assert 'install-app "$app"' in text
