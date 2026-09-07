# Structured Intake Reuse Test

## Existing observation

Project 1 introduced `structured_client_intake`:

```text
person
+ contact
+ service request details
+ normalized downstream orchestration
```

It remained `observed` because there was only one use.

## Project 4

Facility Maintenance independently needs:

```text
requester
+ location / asset
+ category
+ description
+ priority
+ optional evidence
+ normalized downstream dispatch
```

This is materially different from customer booking.

## Expected conclusion if the project proves out

Rename the conceptual candidate from:

```text
structured_client_intake
```

toward:

```text
structured_request_intake
```

and move it from `observed` to `candidate`.

Do **not** extract shared runtime yet.

Two uses prove that the idea recurs; they do not yet prove the correct schema/API.

## New observations to record

This project may also reveal:

- `assignment_sla_tracking`
- `attachment_evidence`

Both should remain observations until another real project independently needs them.
