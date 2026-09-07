import json
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[2]
REPO = ROOT.parents[4]


def test_prospective_model_exists_and_uses_scheduling_capability_interface():
    model = yaml.safe_load(
        (REPO / "architecture/primitive_model/projects/resource_reservation.yml").read_text()
    )
    availability = [
        node for node in model["nodes"]
        if node.get("capability_ref") == "scheduling" and node["operation"] == "availability.query"
    ]
    assert len(availability) == 2


def test_resource_reservation_is_project_local_not_appointment_relabeling():
    data = json.loads(
        (ROOT / "resource_reservations/resource_reservations/doctype/resource_reservation/resource_reservation.json").read_text()
    )
    fields = {field["fieldname"]: field for field in data["fields"]}
    assert data["name"] == "Resource Reservation"
    assert fields["resource"]["options"] == "Reservable Resource"
    assert fields["status"]["options"] == "Draft\nReserved\nCancelled"


def test_desk_actions_and_package_data():
    js = (
        ROOT
        / "resource_reservations/resource_reservations/doctype/resource_reservation/resource_reservation.js"
    ).read_text()
    pyproject = (ROOT / "pyproject.toml").read_text()
    assert "Reserve" in js and "Reschedule" in js and "Cancel" in js
    assert '"*.js"' in pyproject


def test_project_uses_core_transition_and_shared_scheduling_availability():
    workflow = (ROOT / "resource_reservations/workflow.py").read_text()
    availability = (ROOT / "resource_reservations/availability.py").read_text()
    assert "from na_core.transitions" in workflow
    assert "from na_scheduling.availability" in availability
    assert "for update" in workflow.lower()


def test_select_options_use_real_newlines():
    for rel in [
        "resource_reservations/resource_reservations/doctype/reservable_resource/reservable_resource.json",
        "resource_reservations/resource_reservations/doctype/resource_reservation/resource_reservation.json",
    ]:
        data = json.loads((ROOT / rel).read_text())
        for field in data.get("fields", []):
            if field.get("fieldtype") == "Select":
                assert "\\n" not in field.get("options", "")
