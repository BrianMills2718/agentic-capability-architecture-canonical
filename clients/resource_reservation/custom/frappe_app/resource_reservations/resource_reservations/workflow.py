from na_core.transitions import InvalidTransition, TransitionSpec, plan_transition
from resource_reservations.availability import query_availability
from resource_reservations.notifications import notify_requester
from resource_reservations.permissions import require_requester_or_manager


def _actor(actor=None):
    import frappe
    return actor or frappe.session.user


def _now():
    from frappe.utils import now_datetime
    return now_datetime()


def _transition(doc, *, action, allowed_from, to_state, actor, already=False):
    import frappe
    try:
        return plan_transition(
            current_state=doc.status,
            spec=TransitionSpec(
                stage="Reservation",
                action=action,
                allowed_from=frozenset(allowed_from),
                to_state=to_state,
            ),
            actor=actor,
            occurred_at=_now(),
            already_applied=already,
        )
    except InvalidTransition as exc:
        frappe.throw(str(exc))


def _lock_resource(resource):
    import frappe
    rows = frappe.db.sql(
        "select name from `tabReservable Resource` where name=%s for update",
        (resource,),
    )
    if not rows:
        frappe.throw("Reservable Resource does not exist")


def _ensure_free(doc, *, start_time, duration_minutes, exclude_reservation=None):
    import frappe
    result = query_availability(
        resource=doc.resource,
        start_time=start_time,
        duration_minutes=duration_minutes,
        exclude_reservation=exclude_reservation,
    )
    if not result.free:
        frappe.throw(
            "Requested time overlaps an existing reservation: "
            + ", ".join(result.conflicts)
        )
    return result


def reserve(doc, *, actor=None):
    actor = _actor(actor)
    require_requester_or_manager(doc, actor)

    if doc.status == "Reserved":
        return doc.status

    _lock_resource(doc.resource)
    _ensure_free(
        doc,
        start_time=doc.start_time,
        duration_minutes=doc.duration_minutes,
    )
    result = _transition(
        doc,
        action="Reserve",
        allowed_from={"Draft"},
        to_state="Reserved",
        actor=actor,
    )
    doc.status = result.next_state
    doc.reserved_at = result.occurred_at
    doc.save(ignore_permissions=True)

    notify_requester(
        doc,
        subject=f"Reservation {doc.name} confirmed",
        message=f"{doc.resource} is reserved from {doc.start_time} for {doc.duration_minutes} minutes.",
    )
    return doc.status


def reschedule(doc, *, start_time, duration_minutes, actor=None):
    import frappe
    from frappe.utils import get_datetime

    actor = _actor(actor)
    require_requester_or_manager(doc, actor)
    new_start = get_datetime(start_time)
    new_duration = int(duration_minutes)

    if (
        doc.status == "Reserved"
        and get_datetime(doc.start_time) == new_start
        and int(doc.duration_minutes) == new_duration
    ):
        return doc.status

    _lock_resource(doc.resource)
    _ensure_free(
        doc,
        start_time=new_start,
        duration_minutes=new_duration,
        exclude_reservation=doc.name,
    )
    result = _transition(
        doc,
        action="Reschedule",
        allowed_from={"Reserved"},
        to_state="Reserved",
        actor=actor,
    )
    doc.start_time = new_start
    doc.duration_minutes = new_duration
    doc.rescheduled_at = result.occurred_at
    doc.save(ignore_permissions=True)

    notify_requester(
        doc,
        subject=f"Reservation {doc.name} rescheduled",
        message=f"{doc.resource} is now reserved from {doc.start_time} for {doc.duration_minutes} minutes.",
    )
    return doc.status


def cancel(doc, *, actor=None):
    actor = _actor(actor)
    require_requester_or_manager(doc, actor)

    if doc.status == "Cancelled":
        return doc.status

    result = _transition(
        doc,
        action="Cancel",
        allowed_from={"Reserved"},
        to_state="Cancelled",
        actor=actor,
    )
    doc.status = result.next_state
    doc.cancelled_at = result.occurred_at
    doc.save(ignore_permissions=True)

    notify_requester(
        doc,
        subject=f"Reservation {doc.name} cancelled",
        message=f"Your reservation for {doc.resource} has been cancelled.",
    )
    return doc.status
