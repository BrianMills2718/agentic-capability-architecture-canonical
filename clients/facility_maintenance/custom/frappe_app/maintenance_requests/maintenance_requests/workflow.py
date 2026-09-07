from maintenance_requests.notifications import notify_user
from maintenance_requests.permissions import (
    DISPATCHER_ROLE,
    require_assigned_technician,
    require_requester_or_dispatcher,
    require_role,
)
from maintenance_requests.sla import calculate_due_at

def _actor(actor=None):
    import frappe
    return actor or frappe.session.user

def _now():
    from frappe.utils import now_datetime
    return now_datetime()

def _settings():
    import frappe
    try:
        return frappe.get_single("Maintenance Settings")
    except Exception:
        return None

def assign(doc, *, technician, actor=None):
    import frappe

    actor = _actor(actor)
    require_role(actor, DISPATCHER_ROLE)

    if doc.status == "Assigned" and doc.assigned_to == technician:
        return doc.status
    if doc.status not in {"New", "Assigned"}:
        frappe.throw("Only a New or already Assigned request can be dispatched")

    assigned_at = _now()
    doc.assigned_to = technician
    doc.assigned_by = actor
    doc.assigned_at = assigned_at
    doc.due_at = calculate_due_at(assigned_at, doc.priority, _settings())
    doc.overdue_notified_at = None
    doc.status = "Assigned"
    doc.save(ignore_permissions=True)

    notify_user(
        technician,
        subject=f"Maintenance request {doc.name} assigned",
        message=f"You were assigned {doc.name} at {doc.location}. SLA due: {doc.due_at}.",
    )
    return doc.status

def start(doc, *, actor=None):
    import frappe

    actor = _actor(actor)
    require_assigned_technician(doc, actor)

    if doc.status == "In Progress":
        return doc.status
    if doc.status != "Assigned":
        frappe.throw("Only an Assigned request can be started")

    doc.status = "In Progress"
    doc.started_at = _now()
    doc.save(ignore_permissions=True)
    return doc.status

def complete(doc, *, resolution, actor=None):
    import frappe

    actor = _actor(actor)
    require_assigned_technician(doc, actor)

    if doc.status == "Completed":
        return doc.status
    if doc.status != "In Progress":
        frappe.throw("Only an In Progress request can be completed")
    if not str(resolution or "").strip():
        frappe.throw("Resolution is required")

    doc.status = "Completed"
    doc.resolution = str(resolution).strip()
    doc.completed_at = _now()
    doc.save(ignore_permissions=True)

    notify_user(
        doc.requester,
        subject=f"Maintenance request {doc.name} completed",
        message=f"Work is complete. Resolution: {doc.resolution}",
    )
    return doc.status

def close(doc, *, actor=None):
    import frappe

    actor = _actor(actor)
    require_requester_or_dispatcher(doc, actor)

    if doc.status == "Closed":
        return doc.status
    if doc.status != "Completed":
        frappe.throw("Only a Completed request can be closed")

    doc.status = "Closed"
    doc.closed_at = _now()
    doc.save(ignore_permissions=True)
    return doc.status
