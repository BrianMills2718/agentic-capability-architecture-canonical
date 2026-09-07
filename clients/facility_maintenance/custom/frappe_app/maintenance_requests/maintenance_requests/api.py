from maintenance_requests import workflow

def _load(name):
    import frappe
    doc = frappe.get_doc("Maintenance Request", name)
    doc.check_permission("write")
    return doc

def _response(doc):
    return {
        "name": doc.name,
        "status": doc.status,
        "assigned_to": doc.assigned_to,
        "due_at": doc.due_at,
    }

def assign_request(name, technician):
    doc = _load(name)
    workflow.assign(doc, technician=technician)
    doc.reload()
    return _response(doc)

def start_request(name):
    doc = _load(name)
    workflow.start(doc)
    doc.reload()
    return _response(doc)

def complete_request(name, resolution):
    doc = _load(name)
    workflow.complete(doc, resolution=resolution)
    doc.reload()
    return _response(doc)

def close_request(name):
    doc = _load(name)
    workflow.close(doc)
    doc.reload()
    return _response(doc)

try:
    import frappe
except ImportError:
    frappe = None

if frappe is not None:
    assign_request = frappe.whitelist()(assign_request)
    start_request = frappe.whitelist()(start_request)
    complete_request = frappe.whitelist()(complete_request)
    close_request = frappe.whitelist()(close_request)
