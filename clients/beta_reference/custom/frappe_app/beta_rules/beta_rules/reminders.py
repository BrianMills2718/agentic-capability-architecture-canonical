from datetime import datetime

from na_notifications.email import send_email


REMINDER_WINDOW_MINUTES = 15


def reminder_is_due(start_time: datetime, now: datetime, window_minutes: int = REMINDER_WINDOW_MINUTES) -> bool:
    minutes_until_start = (start_time - now).total_seconds() / 60
    return 0 <= minutes_until_start <= window_minutes


def send_appointment_reminders(now=None):
    import frappe
    from frappe.utils import now_datetime

    now = now or now_datetime()
    appointments = frappe.get_all(
        "Appointment",
        filters={"status": ["in", ["Pending", "Confirmed"]]},
        fields=["name", "customer", "start_time"],
    )
    for appointment in appointments:
        if appointment.customer and reminder_is_due(appointment.start_time, now):
            send_email(
                recipients=appointment.customer,
                subject="Appointment reminder",
                message=f"Your appointment starts at {appointment.start_time}.",
            )
