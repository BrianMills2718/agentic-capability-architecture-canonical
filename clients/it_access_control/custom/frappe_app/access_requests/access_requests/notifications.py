from na_notifications.email import send_email
from access_requests.permissions import roles_for


def users_with_role(role):
    import frappe

    users = frappe.get_all(
        "Has Role",
        filters={"role": role, "parenttype": "User"},
        pluck="parent",
    )
    return sorted(set(users))


def notify_role(role, *, subject, message):
    recipients = users_with_role(role)
    if recipients:
        send_email(recipients=recipients, subject=subject, message=message)


def notify_requester_and_target(request, *, subject, message):
    recipients = sorted({request.requester, request.target_user})
    send_email(recipients=recipients, subject=subject, message=message)
