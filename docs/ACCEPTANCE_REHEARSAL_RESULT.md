# Acceptance Rehearsal Result

Date: 2026-09-05

## Purpose

Exercise the packaged fresh-agent sandbox and external evaluator end to end without
claiming the final fresh-agent proof. The rehearsal was performed in a disposable copy
of the exact sandbox. Because the implementing assistant already knew the architecture,
this result validates the harness and repository workflow, not agent-context freshness.

## Rehearsal task

> Add a new project called `beta_reference`. It needs appointment scheduling, approvals
> for appointments over 90 minutes, and email reminders. Reuse what already exists where
> possible. Do not change existing project behavior.

## Result

**Harness rehearsal: PASS**

The disposable implementation:

- composed `core`, `scheduling`, `approvals`, and `notifications`;
- kept the 90-minute approval rule in a `beta_rules` project extension;
- reused `na_approvals.engine.resolve` / `apply_resolution`;
- reused `na_notifications.email.send_email`;
- added hourly reminder orchestration locally;
- left shared runtime byte-for-byte unchanged;
- preserved the ACME reference implementation;
- added Beta-specific tests and reuse notes;
- built all five Frappe-style packages successfully;
- passed project/registry/schema validation;
- passed the external acceptance evaluator.

The evaluator ended with:

```text
ACCEPTANCE PASSED
The fresh-agent result reused unchanged shared runtime, isolated beta-specific behavior,
used shared approvals/notifications, preserved ACME, recorded learning, and passed local tests.
```

## Negative control

The untouched acceptance sandbox was also evaluated before any Beta implementation.
It correctly failed with:

```text
ACCEPTANCE FAILED
- clients/beta_reference/manifest.yml does not exist
```

This proves the evaluator is not a rubber stamp.

## What this does NOT prove

This is not the final fresh-agent acceptance result because the implementing assistant
had already participated in the architecture discussion. The untouched sandbox remains
available for a genuinely fresh coding-agent session.

The other outstanding proof remains execution of the authored Frappe lifecycle tests
inside a real Bench/test site.
