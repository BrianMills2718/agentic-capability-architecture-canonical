from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WORKFLOW = ROOT / ".github" / "workflows" / "frappe-integration.yml"
RUNNER = ROOT / "tools" / "run_frappe_reference_tests.sh"


def test_frappe_ci_workflow_has_required_runtime_and_isolated_sites():
    text = WORKFLOW.read_text(encoding="utf-8")

    required = [
        "frappe-branch version-15",
        "mariadb:10.6",
        "redis:alpine",
        'python-version: "3.11"',
        'node-version: "20"',
        "SITE_ACME: acme_test",
        "SITE_INTAKE: intake_test",
        "SITE_PROCUREMENT: procurement_test",
        "SITE_ACCESS: access_test",
        "SITE_MAINTENANCE: maintenance_test",
        "SITE_SERVICE_DESK: service_desk_test",
        "SITE_RESOURCE_RESERVATION: resource_reservation_test",
        "Create isolated project test sites",
        "run_frappe_reference_tests.sh",
        'clients/**',
    ]

    for item in required:
        assert item in text, f"Frappe CI contract missing: {item}"

    assert "proof/procurement_payload" not in text
    assert "proof/it_access_delta" not in text


def test_local_frappe_runner_keeps_client_extensions_on_separate_sites():
    text = RUNNER.read_text(encoding="utf-8")

    assert 'run-tests --app acme_rules' in text
    assert 'run-tests --app intake_booking' in text
    assert 'install_if_missing "$SITE_ACME" "$app"' in text
    assert 'install_if_missing "$SITE_INTAKE" "$app"' in text
    assert 'intake_booking must not be installed on the ACME site' in text
    assert 'acme_rules must not be installed on the intake site' in text


def test_bench_apps_registry_handles_missing_trailing_newline(tmp_path):
    import subprocess

    apps_txt = tmp_path / "apps.txt"
    apps_txt.write_bytes(b"frappe")  # deliberately no trailing newline
    helper = ROOT / "tools" / "lib" / "bench_apps_registry.sh"

    subprocess.run(
        [
            "bash",
            "-c",
            'source "$1"; ensure_bench_apps_entry "$2" na_scheduling; ensure_bench_apps_entry "$2" na_scheduling',
            "_",
            str(helper),
            str(apps_txt),
        ],
        check=True,
    )

    assert apps_txt.read_text(encoding="utf-8").splitlines() == [
        "frappe",
        "na_scheduling",
    ]
