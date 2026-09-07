from na_notifications.email import send_email

def notify_user(user, *, subject, message):
    if user:
        send_email(recipients=[user], subject=subject, message=message)

def notify_role(role, *, subject, message):
    import frappe

    users = frappe.get_all(
        "Has Role",
        filters={"role": role, "parenttype": "User"},
        pluck="parent",
    )
    recipients = sorted({user for user in users if user and user != "Administrator"})
    if recipients:
        send_email(recipients=recipients, subject=subject, message=message)

def notify_overdue(doc):
    recipients = [doc.assigned_to] if doc.assigned_to else []
    if recipients:
        send_email(
            recipients=recipients,
            subject=f"Maintenance request {doc.name} is overdue",
            message=f"{doc.name} at {doc.location} is past its SLA due time.",
        )
    notify_role(
        "Maintenance Dispatcher",
        subject=f"Maintenance request {doc.name} is overdue",
        message=f"{doc.name} assigned to {doc.assigned_to or 'unassigned'} is overdue.",
    )
