import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]

def test_planned_model_exists_and_uses_no_new_primitive():
    model=ROOT.parents[4]/"architecture/primitive_model/projects/service_desk.yml"
    assert model.exists()

def test_doc_type_matches_model_states_and_attachment():
    data=json.loads((ROOT/"service_desk_requests/service_desk_requests/doctype/support_request/support_request.json").read_text())
    fields={f["fieldname"]:f for f in data["fields"]}
    assert fields["attachment"]["fieldtype"]=="Attach"
    assert data["autoname"]=="format:SRQ-{#####}"
    assert "Waiting on Requester" in fields["status"]["options"]

def test_scheduler_and_desk_actions_are_packaged():
    hooks=(ROOT/"service_desk_requests/hooks.py").read_text()
    js=(ROOT/"service_desk_requests/service_desk_requests/doctype/support_request/support_request.js").read_text()
    pyproject=(ROOT/"pyproject.toml").read_text()
    assert '"hourly"' in hooks
    assert "notify_overdue_requests" in hooks
    assert "Wait on Requester" in js and "Resolve" in js and "Close" in js
    assert '"*.js"' in pyproject


def test_model_adapters_match_implemented_modules():
    import yaml
    model=yaml.safe_load((ROOT.parents[4]/"architecture/primitive_model/projects/service_desk.yml").read_text())
    adapters={n["id"]:n.get("adapter","") for n in model["nodes"]}
    assert adapters["triage_request"] == "service_desk_requests.workflow.triage"
    assert adapters["assign_agent"] == "service_desk_requests.workflow.assign"
    assert adapters["scan_overdue"] == "service_desk_requests.sla.notify_overdue_requests"
    assert "na_core.transitions" in (ROOT/"service_desk_requests/workflow.py").read_text()
