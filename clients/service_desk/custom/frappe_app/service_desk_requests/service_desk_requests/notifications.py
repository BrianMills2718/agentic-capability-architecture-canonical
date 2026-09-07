from na_notifications.email import send_email

def notify_user(user, *, subject, message):
    if user:
        send_email(recipients=[user], subject=subject, message=message)

def notify_role(role, *, subject, message):
    import frappe
    users = frappe.get_all("Has Role", filters={"role": role, "parenttype": "User"}, pluck="parent")
    recipients = sorted({u for u in users if u and u != "Administrator"})
    if recipients:
        send_email(recipients=recipients, subject=subject, message=message)

def notify_overdue(doc):
    if doc.assigned_to:
        notify_user(doc.assigned_to, subject=f"Support request {doc.name} is overdue", message=f"{doc.name}: {doc.subject}")
    notify_role("Support Dispatcher", subject=f"Support request {doc.name} is overdue", message=f"{doc.name} is past its SLA due time.")
