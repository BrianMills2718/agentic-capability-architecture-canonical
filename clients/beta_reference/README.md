# Beta Reference Project

This project composes the shared `core`, `scheduling`, `approvals`, and
`notifications` capabilities. Its `beta_rules` extension keeps the project-only
approval threshold and reminder policy outside the shared capabilities.

Appointments longer than 90 minutes require approval. An hourly scheduler job
sends reminders for appointments starting within the configured 60-minute
lead time, using a durable delivery record so retries are idempotent.
