from datetime import timedelta

from na_notifications.email import send_email


REMINDER_TYPE = "upcoming_appointment"
LEAD_TIME_MINUTES = 60


def reminder_key(appointment):
    return f"{appointment.name}:{REMINDER_TYPE}"


def is_due(appointment, now, lead_time_minutes=LEAD_TIME_MINUTES):
    if appointment.status in {"Cancelled", "Completed"}:
        return False
    start_time = appointment.start_time
    return now <= start_time <= now + timedelta(minutes=lead_time_minutes)


def send_appointment_reminder(appointment, frappe_module, now=None):
    """Send one reminder, recording the delivery key before transport."""
    if now is not None and not is_due(appointment, now):
        return False

    key = reminder_key(appointment)
    if frappe_module.db.exists("Beta Reminder Delivery", {"delivery_key": key}):
        return False

    delivery = frappe_module.get_doc(
        {
            "doctype": "Beta Reminder Delivery",
            "delivery_key": key,
            "appointment": appointment.name,
        }
    )
    delivery.insert(ignore_permissions=True)
    send_email(
        recipients=appointment.customer,
        subject="Appointment reminder",
        message=f"Your appointment starts at {appointment.start_time}.",
    )
    delivery.db_set("sent_at", frappe_module.utils.now_datetime())
    return True


def send_due_reminders():
    import frappe

    now = frappe.utils.now_datetime()
    appointments = frappe.get_all(
        "Appointment",
        filters={
            "start_time": ["between", [now, now + timedelta(minutes=LEAD_TIME_MINUTES)]],
            "status": ["in", ["Pending", "Confirmed"]],
        },
        fields=["name", "customer", "start_time", "status"],
    )
    sent = 0
    for appointment in appointments:
        if send_appointment_reminder(appointment, frappe, now=now):
            sent += 1
    return sent
