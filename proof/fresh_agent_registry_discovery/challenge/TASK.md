# Fresh-Agent Registry Discovery Task

You are in an intentionally isolated capability snapshot. You do not have the source monorepo or its architecture documents.

## Goal

Implement a small **Shipment Exception** workflow for an operations team.

Lifecycle:

```text
Open -> Acknowledged -> Resolved
```

Required behavior:

1. `acknowledge` requires a non-empty actor and changes `Open` to `Acknowledged`.
2. If durable consumer evidence says acknowledgement already occurred, replay is an idempotent no-op (`changed=False`) even if the caller supplies a later state.
3. `resolve` requires a non-empty actor and non-empty resolution text and changes `Acknowledged` to `Resolved`.
4. If durable consumer evidence says resolution already occurred, replay is an idempotent no-op.
5. A notification is sent only when acknowledgement or resolution actually changes state. A no-op must not produce a duplicate notification.
6. The shared notification capability must be the default transport. Tests may inject a fake transport so they do not require Frappe/SMTP.
7. Domain code owns persistence, authorization policy, notification timing/recipients, and shipment-specific schema.

Use `ops@example.test` as the notification recipient.

## Mandatory discovery step

**Before writing implementation code:**

1. Read `snapshot/capability_registry.yml` and relevant `snapshot/metadata/*`.
2. Create `CAPABILITY_PLAN.yml` with these top-level keys:
   - `selected`: capability IDs selected for reuse;
   - `rejected`: mapping of considered but unneeded registry capability IDs to concise reasons;
   - `interfaces`: exact public Python interfaces you intend to consume;
   - `local_gaps`: domain behavior that remains local rather than being generalized.
3. Select/reject based on semantics in the registry. Do not select a capability merely because it is available.
4. Reuse exported public interfaces when they already provide the needed behavior. Do not recreate shared transition or notification transport logic locally.
5. Do not create a new framework, workflow engine, registry, or generic capability.

## Implementation contract

Create exactly the ordinary project files needed for this task, including:

- `shipment_exception/__init__.py`
- `shipment_exception/workflow.py`
- `tests/test_shipment_exception.py`

`shipment_exception.workflow` must expose:

```python
ACKNOWLEDGE_SPEC
RESOLVE_SPEC
acknowledge(*, current_state, actor, occurred_at, already_applied, notify=...)
resolve(*, current_state, actor, occurred_at, resolution, already_applied, notify=...)
```

The default `notify` must be the public shared email transport. A test may pass another callable with the same keyword interface:

```python
notify(recipients=..., subject=..., message=...)
```

Each action returns the shared transition result object.

The local workflow decides **when** to notify: only after a changed transition.

## Isolation rules

- Use only this task, `snapshot/capability_registry.yml`, `snapshot/metadata/*`, and the exported package source under `snapshot/vendor/*`.
- Do not refer to `/mnt/data/composable_capability_base`, parent repositories, prior project names, or external codebases.
- Do not use web search for implementation guidance.

## Success criterion

A reviewer should be able to see that you discovered the registry, chose only relevant capabilities, used their public interfaces, and kept Shipment Exception semantics local.
