import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

def test_attach_fields_and_desk_actions_are_packaged():
    doctype = json.loads(
        (ROOT / "maintenance_requests/maintenance_requests/doctype/maintenance_request/maintenance_request.json").read_text()
    )
    fieldtypes = {field["fieldname"]: field["fieldtype"] for field in doctype["fields"]}
    js = (ROOT / "maintenance_requests/maintenance_requests/doctype/maintenance_request/maintenance_request.js").read_text()
    pyproject = (ROOT / "pyproject.toml").read_text()

    assert fieldtypes["photo"] == "Attach"
    assert fieldtypes["completion_photo"] == "Attach"
    assert "Start Work" in js
    assert "Complete Work" in js
    assert "Close Request" in js
    assert '"*.js"' in pyproject

def test_scheduler_hook_is_hourly_and_project_local():
    hooks = (ROOT / "maintenance_requests/hooks.py").read_text()
    assert '"hourly"' in hooks
    assert "maintenance_requests.sla.notify_overdue_requests" in hooks


def test_select_options_use_real_newlines():
    doctype = json.loads(
        (ROOT / "maintenance_requests/maintenance_requests/doctype/maintenance_request/maintenance_request.json").read_text()
    )
    select_fields = [field for field in doctype["fields"] if field.get("fieldtype") == "Select"]
    assert select_fields
    for field in select_fields:
        assert "\\n" not in field.get("options", ""), (
            f"{field['fieldname']} contains literal backslash-n; "
            "Frappe Select options must be actual newline-separated values"
        )


def test_autoname_uses_proven_frappe_format():
    doctype = json.loads(
        (ROOT / "maintenance_requests/maintenance_requests/doctype/maintenance_request/maintenance_request.json").read_text()
    )
    assert doctype["autoname"] == "format:MRQ-{#####}"
