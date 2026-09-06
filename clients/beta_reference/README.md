# Beta Reference Project

This project composes `core`, `scheduling`, `approvals`, and `notifications`.
The `beta_rules` extension keeps the project-specific approval threshold and
reminder policy outside the shared capabilities.

## Project behavior

- Appointments longer than 90 minutes require approval.
- Due reminders are checked hourly and sent through `na_notifications`.
- Reminder delivery is recorded with a durable idempotency key so scheduler
  retries do not send the same reminder twice.
