# Session Context — 6 September 2026

> **Status: historical checkpoint.** This preserves the architecture as understood on 6 September 2026. It is useful provenance, not a current navigation or status authority. Current architecture is in [`ARCHITECTURE_CHARTER.md`](ARCHITECTURE_CHARTER.md), current sourcing/project workflow is in `../AGENTS.md` and [`PROJECT_WORKFLOW.md`](PROJECT_WORKFLOW.md), and current proof status is in [`PROOF_LEDGER_EXTENDED.md`](PROOF_LEDGER_EXTENDED.md). In particular, the current strategic trunk emphasizes capability intelligence/evidence and off-the-shelf-first sourcing; primitive composition remains experimental.

## North star at the checkpoint

Build an agent-native composable software architecture in which every real project makes future projects easier by contributing reusable capabilities, semantic primitives, tests, contracts, compatibility evidence, and agent instructions.

The business model is optional. The larger architectural question was whether many software systems can be assembled from a relatively small set of configurable semantic primitives plus higher-order capabilities while domain-specific semantics remain local.

## Reuse lifecycle

```text
local / observed
→ candidate
→ proven
→ core
```

Promotion is evidence-driven. Raw project count is insufficient; uses should be materially different and compatibility should survive later consumers.

## Capability interpretation at the checkpoint

- **Core** — foundational conventions and neutral state-transition planning.
- **Approvals** — deterministic approval-decision semantics, with evidence across distinct domains.
- **Notifications** — small shared transport boundary; domain code owns timing, recipients, and copy.
- **Scheduling** — appointment behavior plus newer neutral time-window availability semantics; still candidate pending stronger cross-domain evidence.

Do not use this dated prose as a replacement for current machine-readable capability manifests/registry state.

## Real project pressure

The architecture had been exercised through six production-shaped projects:

1. Client Intake + Booking
2. Internal Procurement
3. IT Access Control
4. Facility Maintenance
5. Service Desk
6. Shared Resource Reservation

They were deliberately chosen to create different pressure: booking, monetary workflow, security entitlement, SLA/assignment, support intake, and non-appointment resource scheduling.

The implementation strategy kept client/project extensions on separate Frappe sites/databases while shared capability source could be reused across sites.

## Primitive hypothesis

A later research layer asked whether apparently different applications share a small coordination vocabulary such as:

```text
request.capture
policy.resolve
actor.authorize
state.transition
actor.assign
time.deadline
event.scan
notification.send
artifact.attach
value.aggregate
```

The checkpoint's preferred interpretation was a hybrid:

```text
typed node/port graph        = composition topology
state/action/transition      = lifecycle/execution semantics
capability registry          = reusable higher-order interfaces + evidence
project-local actions        = irreducible domain semantics
architecture viewpoints      = projections over one underlying model
backend adapters             = runtime implementation
```

The graph/editor was not intended to be the architecture. Subsequent decisions further narrowed this: the primitive/composition model is probationary research rather than the default application/runtime path.

## Important negative conclusions

Do not infer from the experiments that:

- every domain action should become a primitive;
- one generic workflow engine is required;
- Frappe defines the abstract architecture;
- retrospective primitive coverage proves prospective usefulness;
- similar labels imply equivalent semantics;
- a capability interface is necessarily a primitive.

Procurement fulfillment and IT access provisioning/revocation were intentionally retained as domain-native actions rather than forced into a generic `execute` primitive.

## Portable capability network

A later experiment exported capability metadata and package source outside the monorepo so an independent consumer could verify hashes, resolve dependencies, install capability packages, and compose them without source-repository context.

The next network-level test identified at this checkpoint was stronger: a fresh agent should receive only a portable registry snapshot plus a new requirement and independently choose relevant capabilities while rejecting irrelevant ones.

The isolated challenge remains stored under:

`proof/fresh_agent_registry_discovery/challenge/`

See `NEXT_PROOF.md` for its current formulation.

## Strategic phase at the checkpoint

The architecture had substantial technical evidence. The most valuable next evidence was expected from:

1. independent agents using the registry without conversational coaching;
2. truly operational deployments producing upgrade, incident, backup, migration, observability, and user-change pressure;
3. independent architectural criticism of the primitive hypothesis;
4. only then, experiments in wider federation and multi-contributor capability sharing.

The durable conclusion still holds: prefer another genuine use or an adequate existing system over building more platform machinery unless a concrete failure requires new infrastructure.
