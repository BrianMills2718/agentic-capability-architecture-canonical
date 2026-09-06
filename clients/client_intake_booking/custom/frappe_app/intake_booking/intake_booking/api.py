from intake_booking.intake import normalize_submission
from intake_booking.workflow import approve_pending_intake


def submit_intake(
    client_name,
    email,
    service_type,
    request_summary,
    requested_start_time,
    requested_duration_minutes=30,
):
    import frappe

    data = normalize_submission(
        client_name=client_name,
        email=email,
        service_type=service_type,
        request_summary=request_summary,
        requested_start_time=requested_start_time,
        requested_duration_minutes=requested_duration_minutes,
    )

    intake = frappe.get_doc(
        {
            "doctype": "Service Intake",
            "client_name": data.client_name,
            "email": data.email,
            "service_type": data.service_type,
            "request_summary": data.request_summary,
            "requested_start_time": data.requested_start_time,
            "requested_duration_minutes": data.requested_duration_minutes,
            "status": "Submitted",
        }
    )
    intake.insert()
    intake.reload()

    appointment = frappe.get_doc("Appointment", intake.appointment)

    return {
        "intake": intake.name,
        "appointment": appointment.name,
        "status": intake.status,
        "approval_required": bool(appointment.approval_required),
    }


def approve_intake(intake_name):
    import frappe

    intake = frappe.get_doc("Service Intake", intake_name)
    intake.check_permission("write")

    appointment_name = approve_pending_intake(intake)
    intake.reload()
    appointment = frappe.get_doc("Appointment", appointment_name)

    return {
        "intake": intake.name,
        "appointment": appointment.name,
        "status": intake.status,
        "appointment_status": appointment.status,
        "approved_by": intake.approved_by,
        "approved_at": intake.approved_at,
    }


try:
    import frappe
except ImportError:
    frappe = None

if frappe is not None:
    submit_intake = frappe.whitelist()(submit_intake)
    approve_intake = frappe.whitelist()(approve_intake)
