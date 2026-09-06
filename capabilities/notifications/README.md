# Notifications

Status: `candidate`

A small reusable transport capability. The first concrete interface is email delivery through Frappe.

The capability intentionally does **not** decide when scheduling reminders should be sent. Scheduling/client code owns reminder policy and calls the notification interface when needed.

Public interface:

```python
from na_notifications.email import send_email

send_email(
    recipients=["person@example.com"],
    subject="Appointment reminder",
    message="Your appointment starts soon.",
)
```
