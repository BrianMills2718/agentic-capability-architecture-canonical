from datetime import datetime

from na_notifications.email import send_email


REMINDER_LEAD_TIME_MINUTES = 60


def send_due_appointment_reminders(now: datetime | None = None):
    import frappe
    from frappe.utils import add_to_date, now_datetime

    now = now or now_datetime()
    due_before = add_to_date(now, minutes=REMINDER_LEAD_TIME_MINUTES)
    appointments = frappe.get_all(
        "Appointment",
        filters={
            "start_time": ["between", [now, due_before]],
            "status": ["!=", "Cancelled"],
        },
        fields=["name", "customer", "start_time"],
    )

    sent = 0
    for appointment in appointments:
        if not appointment.customer:
            continue
        if frappe.db.exists(
            "Beta Reminder Delivery", {"appointment": appointment.name}
        ):
            continue

        delivery = frappe.get_doc(
            {
                "doctype": "Beta Reminder Delivery",
                "appointment": appointment.name,
            }
        )
        try:
            delivery.insert(ignore_permissions=True)
        except frappe.DuplicateEntryError:
            continue

        try:
            send_email(
                recipients=appointment.customer,
                subject="Appointment reminder",
                message=(
                    f"Reminder: your appointment starts at "
                    f"{appointment.start_time}."
                ),
            )
        except Exception:
            frappe.delete_doc(
                "Beta Reminder Delivery", delivery.name, ignore_permissions=True
            )
            raise
        sent += 1

    return sent
