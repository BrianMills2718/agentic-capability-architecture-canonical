# Beta Reference Project

This project composes the shared `core`, `scheduling`, `approvals`, and
`notifications` capabilities. Its local `beta_rules` extension requires
approval for appointments longer than 90 minutes without modifying shared
scheduling code.

Appointment reminders are configured for email delivery 60 minutes before the
appointment and use the shared `na_notifications.email.send_email` transport.
