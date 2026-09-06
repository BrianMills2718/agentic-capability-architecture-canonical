from na_notifications.email import send_email


def send_appointment_reminder(appointment):
    send_email(
        recipients=appointment.customer,
        subject="Appointment reminder",
        message=f"Reminder: your appointment starts at {appointment.start_time}.",
    )


def send_due_appointment_reminders():
    import frappe
    from frappe.utils import add_to_date, now_datetime

    now = now_datetime()
    appointments = frappe.get_all(
        "Appointment",
        filters={
            "status": ["in", ["Pending", "Confirmed"]],
            "start_time": ["between", [now, add_to_date(now, hours=24)]],
        },
        fields=["customer", "start_time"],
    )
    for appointment in appointments:
        send_appointment_reminder(appointment)
