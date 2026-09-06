from intake_booking.intake import confirmation_copy
from na_notifications.email import send_email


def process_new_intake(intake):
    import frappe
    if getattr(intake, "appointment", None):
        return intake.appointment
    appointment = frappe.get_doc({"doctype":"Appointment","customer":intake.email,"start_time":intake.requested_start_time,"duration_minutes":int(intake.requested_duration_minutes),"status":"Pending"})
    appointment.insert()
    if appointment.approval_required:
        intake_status = "Pending Approval"
    else:
        appointment.status = "Confirmed"
        appointment.save()
        intake_status = "Booked"
    intake.db_set("appointment", appointment.name, update_modified=False)
    intake.db_set("status", intake_status, update_modified=False)
    subject, message = confirmation_copy(client_name=intake.client_name, pending_approval=bool(appointment.approval_required))
    send_email(recipients=intake.email, subject=subject, message=message)
    return appointment.name
