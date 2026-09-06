from datetime import timedelta

from na_notifications.email import send_email


def reminder_key(appointment):
    return f"beta-reference:appointment:{appointment.name}:reminder"


def send_due_reminders():
    import frappe
    from frappe.utils import now_datetime

    now = now_datetime()
    appointments = frappe.get_all(
        "Appointment",
        filters={
            "status": "Pending",
            "start_time": ["between", [now, now + timedelta(hours=1)]],
        },
        fields=["name", "customer", "start_time"],
    )
    for appointment in appointments:
        key = reminder_key(appointment)
        if frappe.db.exists("Beta Reminder Delivery", {"idempotency_key": key}):
            continue
        send_email(
            recipients=appointment.customer,
            subject="Appointment reminder",
            message=f"Reminder: your appointment starts at {appointment.start_time}.",
        )
        frappe.get_doc(
            {
                "doctype": "Beta Reminder Delivery",
                "appointment": appointment.name,
                "idempotency_key": key,
            }
        ).insert(ignore_permissions=True)
