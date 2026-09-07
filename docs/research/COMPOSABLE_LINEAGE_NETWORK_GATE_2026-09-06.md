# Preserved research context: composable-lineage network gate

> **Provenance:** copied from `brianmills-spec/composable-capability-architecture`, `docs/SESSION_NETWORK_GATE.md`, HEAD lineage as reviewed 2026-09-07. Preserved here as research/evidence context; it is not a canonical runtime or composition contract.

# Session Network / Fresh-Agent Gate Context

The longer-term architecture is not only a private capability base. A possible larger goal is a federated capability commons where coding agents can discover, select, compose, test, and strengthen machine-readable capabilities contributed by many independent developers.

The important distinction from an ordinary package registry is evidence: capability metadata should eventually support public interfaces, dependencies, configuration, compatibility, real uses, maturity, known conflicts/limits, tests and provenance rather than only version/download counts.

## Existing portability evidence

An independent repository consumer proof was recorded in `BrianMills2718/cc_testing`, GitHub Actions run `34047230770`, with 7/7 tests and a resolved portable dependency set of `core,notifications`.

This established portable registry/package verification and independent consumer composition. It did not by itself prove that a fresh coding agent can semantically discover and choose the right capabilities.

## Next fresh-agent challenge

A Shipment Exception challenge was prepared:

```text
Open -> Acknowledged -> Resolved
```

All four current capabilities are exposed, but the requirement semantically needs only Core + Notifications. The agent is expected to reject Approvals and Scheduling rather than install everything.

Before coding, the agent must produce `CAPABILITY_PLAN.yml` with:

- selected capability IDs;
- rejected capability IDs plus reasons;
- exact public Python interfaces to consume;
- domain behavior that remains local.

The intended public interfaces include:

- `na_core.transitions.TransitionSpec`
- `na_core.transitions.plan_transition`
- `na_notifications.email.send_email`

A hidden evaluator was designed to check capability selection/rejection, absence of monorepo leakage, no local reimplementation of shared interfaces, transition behavior, durable replay idempotency, no duplicate notifications on no-op, and candidate-authored tests.

The evaluator was validated against a private reference solution, but the network gate must remain **pending** until a genuinely separate coding agent receives only the isolated challenge. The same agent that designed the fixture must not be used to claim a pass.
