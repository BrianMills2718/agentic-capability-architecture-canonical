from na_core.transitions import InvalidTransition, TransitionSpec, plan_transition
from service_desk_requests.notifications import notify_user
from service_desk_requests.permissions import (
    DISPATCHER_ROLE,
    require_assigned_agent,
    require_requester_agent_or_dispatcher,
    require_requester_or_dispatcher,
    require_role,
)
from service_desk_requests.sla import calculate_due_at

VALID_CATEGORIES = {"Access", "Bug", "How To", "Incident", "Other"}
VALID_PRIORITIES = {"Low", "Normal", "High", "Urgent"}

def _actor(actor=None):
    import frappe
    return actor or frappe.session.user

def _now():
    from frappe.utils import now_datetime
    return now_datetime()

def _settings():
    import frappe
    try:
        return frappe.get_single("Support Settings")
    except Exception:
        return None

def _transition(doc, *, stage, action, allowed_from, to_state, actor, already=False, reason=""):
    import frappe
    try:
        return plan_transition(
            current_state=doc.status,
            spec=TransitionSpec(stage=stage, action=action, allowed_from=frozenset(allowed_from), to_state=to_state),
            actor=actor,
            occurred_at=_now(),
            already_applied=already,
            reason=reason,
        )
    except InvalidTransition as exc:
        frappe.throw(str(exc))

def triage(doc, *, category, priority, actor=None):
    import frappe
    actor = _actor(actor)
    require_role(actor, DISPATCHER_ROLE)
    category = str(category or "").strip()
    priority = str(priority or "").strip()
    if category not in VALID_CATEGORIES:
        frappe.throw("Invalid support category")
    if priority not in VALID_PRIORITIES:
        frappe.throw("Invalid support priority")
    if doc.status == "Triaged" and doc.category == category and doc.priority == priority:
        return doc.status
    result = _transition(doc, stage="Triage", action="Triage", allowed_from={"New"}, to_state="Triaged", actor=actor)
    doc.category = category
    doc.priority = priority
    doc.status = result.next_state
    doc.save(ignore_permissions=True)
    return doc.status

def assign(doc, *, agent, actor=None):
    import frappe
    actor = _actor(actor)
    require_role(actor, DISPATCHER_ROLE)
    if doc.status == "Assigned" and doc.assigned_to == agent:
        return doc.status
    if doc.status not in {"Triaged", "Assigned"}:
        frappe.throw("Only a Triaged or already Assigned request can be assigned")
    now = _now()
    doc.assigned_to = agent
    doc.assigned_by = actor
    doc.assigned_at = now
    doc.due_at = calculate_due_at(now, doc.priority, _settings())
    doc.overdue_notified_at = None
    doc.status = "Assigned"
    doc.save(ignore_permissions=True)
    notify_user(agent, subject=f"Support request {doc.name} assigned", message=f"{doc.subject}. SLA due: {doc.due_at}")
    return doc.status

def start(doc, *, actor=None):
    actor = _actor(actor)
    require_assigned_agent(doc, actor)
    if doc.status == "In Progress":
        return doc.status
    result = _transition(doc, stage="Work", action="Start", allowed_from={"Assigned"}, to_state="In Progress", actor=actor)
    doc.status = result.next_state
    doc.started_at = result.occurred_at
    doc.save(ignore_permissions=True)
    return doc.status

def wait_for_requester(doc, *, actor=None):
    actor = _actor(actor)
    require_assigned_agent(doc, actor)
    if doc.status == "Waiting on Requester":
        return doc.status
    result = _transition(doc, stage="Work", action="Wait for Requester", allowed_from={"In Progress"}, to_state="Waiting on Requester", actor=actor)
    doc.status = result.next_state
    doc.waiting_since = result.occurred_at
    doc.save(ignore_permissions=True)
    notify_user(doc.requester, subject=f"Support request {doc.name} needs your input", message="The assigned support agent is waiting for more information.")
    return doc.status

def resume(doc, *, actor=None):
    actor = _actor(actor)
    require_requester_agent_or_dispatcher(doc, actor)
    if doc.status == "In Progress" and doc.resumed_at:
        return doc.status
    result = _transition(doc, stage="Work", action="Resume", allowed_from={"Waiting on Requester"}, to_state="In Progress", actor=actor)
    doc.status = result.next_state
    doc.resumed_at = result.occurred_at
    doc.save(ignore_permissions=True)
    return doc.status

def resolve(doc, *, resolution, actor=None):
    import frappe
    actor = _actor(actor)
    require_assigned_agent(doc, actor)
    resolution = str(resolution or "").strip()
    if doc.status == "Resolved":
        return doc.status
    if not resolution:
        frappe.throw("Resolution is required")
    result = _transition(doc, stage="Work", action="Resolve", allowed_from={"In Progress", "Waiting on Requester"}, to_state="Resolved", actor=actor, reason=resolution)
    doc.status = result.next_state
    doc.resolution = resolution
    doc.resolved_at = result.occurred_at
    doc.save(ignore_permissions=True)
    notify_user(doc.requester, subject=f"Support request {doc.name} resolved", message=f"Resolution: {resolution}")
    return doc.status

def close(doc, *, actor=None):
    actor = _actor(actor)
    require_requester_or_dispatcher(doc, actor)
    if doc.status == "Closed":
        return doc.status
    result = _transition(doc, stage="Closure", action="Close", allowed_from={"Resolved"}, to_state="Closed", actor=actor)
    doc.status = result.next_state
    doc.closed_at = result.occurred_at
    doc.save(ignore_permissions=True)
    return doc.status
