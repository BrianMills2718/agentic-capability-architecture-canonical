# Beta Reference Project

Beta composes the shared `core`, `scheduling`, `approvals`, and `notifications`
capabilities. Its `beta_rules` extension adds the project-specific approval
threshold and scheduled reminder policy without changing shared applications.

Appointments longer than 90 minutes require approval. Confirmed appointments
within the reminder window receive an email through `na_notifications`; a
durable reminder record makes repeated scheduler runs idempotent.
