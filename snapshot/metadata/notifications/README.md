# Notifications

Status: `proven`

Notifications owns a deliberately small stable email transport boundary:

```python
from na_notifications.email import send_email
```

Projects/capabilities own when to notify, recipients, copy, durable idempotency evidence, and domain policy. The shared capability owns recipient normalization and delegation to Frappe's email transport.

Real uses include booking, procurement, IT access, facility maintenance, service desk, and resource reservation flows.
