from na_notifications.email import send_email
from procurement_requests.permissions import users_with_role


def notify_role(role, *, subject, message):
    recipients = users_with_role(role)
    if not recipients:
        return None
    return send_email(recipients=recipients, subject=subject, message=message)


def notify_requester(request, *, subject, message):
    return send_email(recipients=request.requester, subject=subject, message=message)
