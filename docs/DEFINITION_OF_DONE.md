# Definition of Done

## Status

The **original bootstrap completion gates are closed**:

- real Frappe lifecycle/persistence proof passed in GitHub Actions run `34001408766`;
- genuinely fresh coding-agent acceptance passed in run `34010580867`.

See [`PROOF_LEDGER_EXTENDED.md`](PROOF_LEDGER_EXTENDED.md) for the current proof index and [`FRAPPE_TEST_STATUS.md`](FRAPPE_TEST_STATUS.md) for the baseline Frappe environment/result.

The earlier unchecked bootstrap checklist is preserved in repository history; it is no longer the current program-status source.

## Definition of done for a new project or material capability change

A change is not complete until it satisfies the applicable items below.

### Sourcing and architecture

- [ ] The exact requirement is stated.
- [ ] Native platform/runtime, installed ecosystem, mature external, standards/protocol, and internal capability options were considered where relevant.
- [ ] Meaningful rejected candidates and reasons are recorded when they would help a future agent.
- [ ] The selected capability/public boundary honestly matches the required semantics.
- [ ] Consequential project-specific behavior remains in the project-local layer.
- [ ] No new generic infrastructure is introduced when an established system already satisfies the required invariant.

### Implementation and reliability

- [ ] Shared capability dependencies and public interfaces remain explicit.
- [ ] Triggered behavior has a real trigger path, not only a callable helper.
- [ ] Retryable/external side effects use durable idempotency/reliability semantics appropriate to the failure mode.
- [ ] Authorization, persistence, scheduling, transactions, messaging, and similar runtime concerns use established platform/runtime facilities unless a documented gap justifies otherwise.

### Evidence

- [ ] Unit/integration/persistence/compatibility tests cover the behavior appropriate to its boundary.
- [ ] New reusable failure modes leave regression tests.
- [ ] `clients/<project>/LEARNINGS.md` records a reuse/sourcing assessment or explicitly explains why nothing should be promoted.
- [ ] Reuse candidates are recorded without premature maturity promotion.
- [ ] Human-readable status does not contradict machine-readable manifests/catalogs.

### Required repository gate

Run the exact repository-wide gate:

```bash
python tools/check_bootstrap.py
```

Targeted checks do not substitute for this command. A change that fails the full gate is not complete.

## Current program-level proof question

The original bootstrap is complete, but one distinct research question remains open in the current proof ledger: the isolated `proof/fresh_agent_registry_discovery/challenge/` should receive a genuinely separate coding-agent run to test whether an agent can discover, select, reject, and compose portable capabilities without the source monorepo or this conversation.

That is an **ongoing architecture research gate**, not evidence that the original Frappe/fresh-agent bootstrap remains unfinished.

## Success after bootstrap

The capability architecture should now improve through real application pressure. Progress is measured by better sourcing decisions, less unnecessary bespoke implementation, preserved local semantics, stronger compatibility/rejection evidence, and lower marginal effort—not by continually adding framework machinery or internal capabilities.
