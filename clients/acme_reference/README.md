# ACME Reference Project

This is the first end-to-end example project for the capability-base workflow.

It composes:

- `core`
- `scheduling`
- `approvals`

and adds one project-specific extension:

- `acme_rules`

The extension does **not** modify `na_scheduling`. It hooks `Appointment.validate`
and delegates competing approval decisions to the shared `na_approvals` resolver.

## Project-specific rule

ACME requires appointments longer than 120 minutes to require approval.

This is intentionally local because it has only one demonstrated consumer.
If another materially different project needs the same behavior, it becomes a
candidate for generalization into shared configuration or a reusable rule.
