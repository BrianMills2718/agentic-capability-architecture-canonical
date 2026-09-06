from intake_booking.intake import confirmation_copy
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

    intake.db_set("appointment", appointment.name, update_modified=False)
    intake.db_set("status", intake_status, update_modified=False)

    subject, message = confirmation_copy(
        client_name=intake.client_name,
        pending_approval=bool(appointment.approval_required),
    )
    send_email(recipients=intake.email, subject=subject, message=message)

    return appointment.name


def approve_pending_intake(intake, *, approved_by=None):
    """Approve a project-local pending intake and confirm its shared Appointment.

    The transition is idempotent: approving an already booked intake returns the
    existing appointment without queuing another confirmation email.
    """
    import frappe
    from frappe.utils import now_datetime

    if intake.status == "Booked":
        if not intake.appointment:
            frappe.throw("Booked intake has no linked appointment")
        return intake.appointment

    if intake.status != "Pending Approval":
        frappe.throw("Only a pending intake can be approved")

    if not intake.appointment:
        frappe.throw("Pending intake has no linked appointment")

    appointment = frappe.get_doc("Appointment", intake.appointment)

    if not bool(appointment.approval_required):
        frappe.throw("Linked appointment does not require approval")

    appointment.db_set("status", "Confirmed")

    actor = approved_by or frappe.session.user
    decided_at = now_datetime()
    intake.db_set("status", "Booked", update_modified=False)
    intake.db_set("approved_by", actor, update_modified=False)
    intake.db_set("approved_at", decided_at, update_modified=False)

    send_email(
        recipients=intake.email,
        subject="Consultation approved",
        message=f"Hi {intake.client_name}, your consultation has been approved and booked.",
    )

    return appointment.name
