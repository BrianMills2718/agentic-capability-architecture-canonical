from na_notifications.email import send_email


def send_appointment_reminder(appointment):
    """Send one reminder, recording the delivery before the external side effect."""
    import frappe

    if frappe.db.exists(
        "Appointment Reminder Sent", {"appointment": appointment.name}
    ):
        return False

    marker = frappe.get_doc(
        {
            "doctype": "Appointment Reminder Sent",
            "appointment": appointment.name,
        }
    )
    marker.insert(ignore_permissions=True)
    try:
        send_email(
            recipients=getattr(appointment, "customer_email", None)
            or appointment.customer,
            subject="Appointment reminder",
            message="This is a reminder for your upcoming appointment.",
        )
    except Exception:
        frappe.delete_doc("Appointment Reminder Sent", marker.name, force=True)
        raise
    return True


def schedule_reminders():
    import frappe
    from frappe.utils import add_to_date, now_datetime

    now = now_datetime()
    appointments = frappe.get_all(
        "Appointment",
        filters={
            "status": "Confirmed",
            "start_time": ["between", [now, add_to_date(now, hours=1)]],
        },
        pluck="name",
    )
    for name in appointments:
        send_appointment_reminder(frappe.get_doc("Appointment", name))
