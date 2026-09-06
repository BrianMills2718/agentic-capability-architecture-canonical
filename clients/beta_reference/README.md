# Beta Reference Project

This project composes the shared `core`, `scheduling`, `approvals`, and
`notifications` capabilities. Its `beta_rules` extension:

- requires approval for appointments longer than 90 minutes;
- sends reminders for appointments starting within the next 15 minutes; and
- wires reminder delivery to Frappe's scheduler.

The extension uses the shared approval resolver and `na_notifications.email.send_email`
without changing any shared capability or the existing ACME project.
