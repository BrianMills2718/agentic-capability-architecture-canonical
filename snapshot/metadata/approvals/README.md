# Approvals

Status: `proven`

Approvals owns deterministic approval-decision semantics such as ALLOW, REQUIRE_APPROVAL, and BLOCK. It is not a generic state-machine capability. Domain-neutral state transition planning lives in Core.

Public decision interfaces:

- `na_approvals.engine.resolve`
- `na_approvals.engine.apply_resolution`
