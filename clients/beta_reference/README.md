# Beta Reference Project

This project composes the shared `scheduling`, `approvals`, and `notifications`
capabilities. Its `beta_rules` extension keeps the project-specific approval
threshold and reminder policy outside the shared apps.

Appointments longer than 90 minutes require approval. An hourly scheduler hook
sends a reminder for eligible appointments within the configured 60-minute
lead time. Reminder deliveries use a durable delivery record so retries do not
send the same logical reminder twice.
