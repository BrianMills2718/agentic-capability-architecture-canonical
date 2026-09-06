from na_notifications.email import send_email


def reminder_message(appointment):
    return (
        f"Reminder: your appointment starts at {appointment.start_time} "
        f"and lasts {appointment.duration_minutes} minutes."
    )


def send_due_reminders():
    import frappe
    from frappe.utils import add_to_date, now_datetime

    now = now_datetime()
    appointments = frappe.get_all(
        "Appointment",
        filters={
            "start_time": ["between", [now, add_to_date(now, minutes=60)]],
            "status": ["!=", "Cancelled"],
        },
        fields=["name", "customer", "start_time", "duration_minutes"],
    )
    for appointment in appointments:
        if appointment.customer:
            send_email(
                recipients=appointment.customer,
                subject="Appointment reminder",
                message=reminder_message(appointment),
            )
