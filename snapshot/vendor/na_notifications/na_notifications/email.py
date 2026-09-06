from collections.abc import Iterable


def normalize_recipients(recipients: str | Iterable[str]) -> list[str]:
    if isinstance(recipients, str):
        recipients = [recipients]
    return [str(value).strip() for value in recipients if str(value).strip()]


def send_email(*, recipients: str | Iterable[str], subject: str, message: str, sender: str | None = None):
    """Send an email through Frappe using a deliberately small stable interface."""
    import frappe

    normalized = normalize_recipients(recipients)
    if not normalized:
        raise ValueError("at least one recipient is required")
    if not subject.strip():
        raise ValueError("subject is required")

    return frappe.sendmail(
        recipients=normalized,
        subject=subject,
        message=message,
        sender=sender,
    )
