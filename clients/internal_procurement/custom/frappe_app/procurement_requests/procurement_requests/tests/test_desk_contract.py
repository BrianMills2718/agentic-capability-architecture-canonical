from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def test_purchase_request_desk_exposes_project_actions():
    js = (ROOT / "procurement_requests/procurement_requests/doctype/purchase_request/purchase_request.js").read_text()

    assert "Submit Request" in js
    assert "Procurement Manager" in js
    assert "Procurement Finance" in js
    assert "Procurement Officer" in js
    assert "manager_approve" in js
    assert "finance_approve" in js
    assert "Mark Purchased" in js
    assert "Mark Received" in js
    assert "Close Request" in js


def test_package_data_includes_doctype_json_and_js():
    pyproject = (ROOT / "pyproject.toml").read_text()
    assert '"*.json"' in pyproject
    assert '"*.js"' in pyproject
