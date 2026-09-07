from intake_booking.intake import confirmation_copy
from na_approvals.transitions import InvalidApprovalTransition, TransitionSpec, plan_transition
from na_notifications.email import send_email


def process_new_intake(intake):
    """Compose a local Service Intake with shared scheduling/approval/notification capabilities."""
    import frappe

    if getattr(intake, "appointment", None):
        return intake.appointment

    appointment = frappe.get_doc(
        {
            "doctype": "Appointment",
            "customer": intake.email,
            "start_time": intake.requested_start_time,
            "duration_minutes": int(intake.requested_duration_minutes),
            "status": "Pending",
        }
    )
    appointment.insert()

    if appointment.approval_required:
        intake_status = "Pending Approval"
    else:
        appointment.status = "Confirmed"
        appointment.save()
        intake_status = "Booked"

    # db_set keeps the current document object and the stored row in sync
    # without recursively invoking after_insert.
    intake.db_set("appointment", appointment.name, update_modified=False)
    intake.db_set("status", intake_status, update_modified=False)

    subject, message = confirmation_copy(
        client_name=intake.client_name,
        pending_approval=bool(appointment.approval_required),
    )
    send_email(recipients=intake.email, subject=subject, message=message)

    return appointment.name


def approve_pending_intake(intake, *, approved_by=None):
    """Approve a project-local pending intake and confirm its shared Appointment."""
    import frappe
    from frappe.utils import now_datetime

    if intake.status == "Booked" and not intake.appointment:
        frappe.throw("Booked intake has no linked appointment")

    actor = approved_by or frappe.session.user
    try:
        transition = plan_transition(
            current_state=intake.status,
            spec=TransitionSpec(
                stage="Staff",
                action="Approve",
                allowed_from=frozenset({"Pending Approval"}),
                to_state="Booked",
            ),
            actor=actor,
            occurred_at=now_datetime(),
            already_applied=intake.status == "Booked",
        )
    except InvalidApprovalTransition:
        frappe.throw("Only a pending intake can be approved")

    if not transition.changed:
        return intake.appointment

    if not intake.appointment:
        frappe.throw("Pending intake has no linked appointment")

    appointment = frappe.get_doc("Appointment", intake.appointment)
    if not bool(appointment.approval_required):
        frappe.throw("Linked appointment does not require approval")

    # The project-local approval action satisfies the requirement. The shared
    # Appointment still records that approval was required.
    appointment.db_set("status", "Confirmed")

    intake.db_set("status", transition.next_state, update_modified=False)
    intake.db_set("approved_by", transition.actor, update_modified=False)
    intake.db_set("approved_at", transition.occurred_at, update_modified=False)

    send_email(
        recipients=intake.email,
        subject="Consultation approved",
        message=f"Hi {intake.client_name}, your consultation has been approved and booked.",
    )

    return appointment.name
