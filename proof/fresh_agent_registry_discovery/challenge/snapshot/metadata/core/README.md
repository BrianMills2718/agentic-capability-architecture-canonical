# Core

Status: `core`

The foundational capability now has a concrete Frappe runtime package: `na_core`.

Core remains intentionally small. It owns behavior that is genuinely domain-neutral and
foundational across other capabilities/projects.

## Provided behavior

- identity/configuration/shared conventions;
- pure state-transition planning;
- conventional transition audit payload generation.

Public interfaces:

```python
from na_core.transitions import TransitionSpec, TransitionResult, plan_transition, audit_payload
```

The transition primitive:

- validates allowed source state;
- returns explicit previous/next state;
- carries actor/time/reason metadata;
- returns a deterministic changed/no-op result from durable `already_applied` evidence;
- does **not** authorize actors, choose routing, mutate documents, persist audit rows, or send side effects.

## Why transition planning moved here

The first three uses appeared inside approval workflows, so the primitive initially lived
under `na_approvals.transitions`.

Project 5 was modeled **before implementation**. Service Desk needed lifecycle transitions
for triage, start, wait, resume, resolve, and close, but did not need the Approvals
capability. That exposed an architectural error: state transition planning had been placed
under a domain capability even though its semantics were neutral.

The canonical implementation therefore moved to `na_core.transitions` before Service Desk
code was written. `na_approvals.transitions` is retained as a compatibility re-export.

Real proof: six-site Frappe v15 run `34044617169`. Existing ACME, Intake, Procurement, IT
Access, and Maintenance suites remained green while Service Desk used Core directly without
Approvals or Scheduling.

Core status is foundational and is **not** assigned from a reuse-count promotion rule.


Project 6 regression: seven-site Frappe v15 run `34046554727` kept all Core consumers green, including Resource Reservation.

Independent repository portability: **passed** in `BrianMills2718/cc_testing`, run `34047230770`; exported `na_core` installed independently and powered the consumer transition flow.
