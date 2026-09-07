# Session Context — 6 September 2026

## North star

Build an agent-native composable software architecture in which every real project makes future projects easier by contributing reusable capabilities, semantic primitives, tests, contracts, compatibility evidence, and agent instructions.

The business model is optional. The larger architectural question is whether many software systems can be assembled from a relatively small set of configurable semantic primitives plus higher-order capabilities while domain-specific semantics remain local.

## Reuse lifecycle

```text
local / observed
→ candidate
→ proven
→ core
```

Promotion is evidence-driven. Raw project count is insufficient; uses should be materially different and compatibility should survive later consumers.

## Current capabilities

- **Core** — foundational conventions and neutral state-transition planning.
- **Approvals** — deterministic approval-decision semantics, proven across distinct domains.
- **Notifications** — small shared transport boundary; domain code owns timing, recipients, and copy.
- **Scheduling** — appointment behavior plus newer neutral time-window availability semantics; still candidate pending stronger cross-domain evidence.
## Real project pressure

The architecture has been exercised through six production-shaped projects:

1. Client Intake + Booking
2. Internal Procurement
3. IT Access Control
4. Facility Maintenance
5. Service Desk
6. Shared Resource Reservation

They were deliberately chosen to create different pressure: booking, monetary workflow, security entitlement, SLA/assignment, support intake, and non-appointment resource scheduling.

The implementation strategy keeps client/project extensions on separate Frappe sites/databases while shared capability source can be reused across sites.

## Primitive hypothesis

A later research layer asks whether apparently different applications share a small coordination vocabulary such as:

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
The current preferred interpretation is a hybrid:

```text
typed node/port graph        = composition topology
state/action/transition      = lifecycle/execution semantics
capability registry          = reusable higher-order interfaces + evidence
project-local actions        = irreducible domain semantics
architecture viewpoints      = projections over one underlying model
backend adapters             = runtime implementation
```

The graph/editor is not the architecture. The machine-readable semantic model is the source of truth.

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

The next network-level test is stronger: a fresh agent should receive only a portable registry snapshot plus a new requirement and independently choose relevant capabilities while rejecting irrelevant ones.

The isolated challenge is stored under:

`proof/fresh_agent_registry_discovery/challenge/`

## Strategic phase

The architecture itself has substantial technical evidence. The most valuable next evidence comes from:

1. independent agents using the registry without conversational coaching;
2. truly operational deployments producing upgrade, incident, backup, migration, observability, and user-change pressure;
3. independent architectural criticism of the primitive hypothesis;
4. only then, experiments in wider federation and multi-contributor capability sharing.

Prefer another genuine use over building more platform machinery unless a concrete failure requires new infrastructure.
