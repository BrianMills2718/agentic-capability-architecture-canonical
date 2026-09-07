from pathlib import Path


APP_ROOT = Path(__file__).resolve().parents[2]
JS = (
    APP_ROOT
    / "access_requests"
    / "access_requests"
    / "doctype"
    / "access_request"
    / "access_request.js"
)
PYPROJECT = APP_ROOT / "pyproject.toml"


def test_desk_actions_cover_workflow():
    text = JS.read_text(encoding="utf-8")
    for label in (
        "Submit Request",
        "Approve",
        "Reject",
        "Mark Provisioned",
        "Revoke Access",
    ):
        assert label in text

    for method in (
        "access_requests.api.submit_access_request",
        "access_requests.api.manager_approve",
        "access_requests.api.manager_reject",
        "access_requests.api.security_approve",
        "access_requests.api.security_reject",
        "access_requests.api.mark_provisioned",
        "access_requests.api.revoke_access",
    ):
        assert method in text


def test_javascript_is_packaged():
    assert '"*.js"' in PYPROJECT.read_text(encoding="utf-8")
