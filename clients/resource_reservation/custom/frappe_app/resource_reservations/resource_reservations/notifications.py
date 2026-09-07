from na_notifications.email import send_email


def notify_requester(doc, *, subject, message):
    if doc.requester:
        send_email(recipients=[doc.requester], subject=subject, message=message)
