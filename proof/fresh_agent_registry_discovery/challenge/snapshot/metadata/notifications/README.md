# Notifications

Status: `proven`

A small reusable transport capability. The concrete interface is email delivery through
Frappe.

The capability intentionally does **not** decide when a message should be sent. Domain
workflow code owns triggering, recipients, subject/body policy, and business timing.

Public interface:

```python
from na_notifications.email import send_email

send_email(
    recipients=["person@example.com"],
    subject="Notification",
    message="Business-specific message.",
)
```

## Reuse evidence

Materially different uses:

1. `client_intake_booking` — customer-facing booking and approval messages.
2. `internal_procurement` — requester/manager/finance/procurement workflow messages.
3. `it_access_control` — requester/target/manager/security/provisioner access messages.
4. `facility_maintenance` — technician assignment, completion, and overdue SLA messages.
5. `service_desk` — support assignment, requester follow-up, resolution, and overdue messages.
6. `resource_reservation` — reservation, reschedule, and cancellation notifications in a non-appointment scheduling domain.

Third-use compatibility: **passed**.

Four-site third-use proof: GitHub Actions run `34017058788`.

Fourth-use regression: five-site Facility Maintenance proof run `34020413484`.

The shared capability owns transport; domain code continues to decide when, why, and to
whom a message is sent.

Fifth-use regression: six-site Service Desk/Core proof run `34044617169`.


Independent repository portability: **passed** in `BrianMills2718/cc_testing`, run `34047230770`; the portable registry resolved `notifications -> core` and the consumer suite passed 7/7.
