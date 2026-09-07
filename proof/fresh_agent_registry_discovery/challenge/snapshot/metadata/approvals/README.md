# Approvals

Status: `proven`

Approvals owns deterministic approval-rule resolution:

```text
rule evaluations
→ deterministic resolver
→ ALLOW / REQUIRE_APPROVAL / BLOCK
```

Public decision interfaces:

- `na_approvals.engine.resolve`
- `na_approvals.engine.apply_resolution`

The resolver provides deterministic priority/conflict semantics and remains specific to the
approval decision domain.

## Transition compatibility namespace

Approval workflows also use the domain-neutral transition planner. Its canonical ownership
is now **Core**:

```python
from na_core.transitions import TransitionSpec, plan_transition
```

For compatibility, existing code may continue to import the same objects from
`na_approvals.transitions`; that module re-exports Core's implementation.

The planner owns state validation, changed/no-op results, and transition/audit metadata. It
does not authorize actors, choose domain routing, mutate documents, persist audit rows, or
send notifications.

## Reuse evidence

Approval decision resolution is proven across materially different uses including
appointment policy, procurement monetary routing, and IT access/security routing.

The approval-action experiments also led to the narrower reusable transition primitive.
Project 5 then proved that primitive outside Approvals entirely: Service Desk uses
`na_core.transitions` without installing the Approvals capability.

Six-site compatibility proof: GitHub Actions run `34044617169`. All earlier approval consumers
remained green.
