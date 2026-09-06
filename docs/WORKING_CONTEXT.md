# Working Context

## Objective

Build a development system for projects created with coding agents where each completed project strengthens a larger reusable capability base.

The aim is not to make every piece of code reusable. The aim is to make new work **eligible to become reusable**, while keeping project-specific behavior isolated until reuse is demonstrated.

## Origin of the idea

The working model came from discussing a configurable, composable software business:

- Clients/projects should be assembled from reusable capabilities rather than rebuilt from scratch.
- Capabilities should be configurable.
- Capabilities should compose through explicit interfaces.
- Unique requirements should remain local.
- Repeated requirements can later be generalized and promoted.
- Tests and compatibility checks should protect existing consumers.

## Chosen foundation direction

Frappe is currently the preferred example foundation because it supports:

- installable apps,
- per-site configuration/data,
- hooks and extension points,
- DocTypes,
- APIs,
- background jobs,
- reusable business applications,
- permissive framework licensing.

This repository is not yet tied irreversibly to Frappe. The capability model should remain conceptually useful even if another runtime is used.

## Core architecture

```text
Shared capabilities
        ↓
Project/client configuration
        ↓
Project/client custom extensions
```

Example capability base:

```text
core
scheduling
notifications
approvals
customer_intake
reporting
crm
```

A project should ideally be describable as a composition manifest plus only the genuinely custom code.

## Capability lifecycle

Use four states:

1. `local`
2. `candidate`
3. `proven`
4. `core`

Suggested promotion discipline:

- First use: local.
- Second materially different use: candidate/proven extraction is justified.
- Third use: compatibility/composability test.
- Core: mature and intentionally depended upon.

## Frappe Scheduling example discussed

A reusable Scheduling app could contain DocTypes such as:

- Appointment
- Appointment Type
- Availability
- Scheduling Settings

Multiple client sites can install the same Scheduling app while maintaining separate data and settings.

Client differences such as duration, approval thresholds, reminders, and cancellation policy should usually be configuration rather than copied code.

## Client-specific extensions

A unique client rule should live outside the shared Scheduling app.

Example:

> Appointments longer than two hours require manager approval for one client.

That belongs in a client-specific extension app using Frappe hooks rather than modifying `na_scheduling`.

If similar behavior appears in later projects, generalize it into a configurable shared capability.

## Rule composition model

Independent hooks that directly overwrite the same field are dangerous.

Instead:

1. Use one dispatcher/rule engine.
2. Rules return decision objects.
3. Each result includes a rule name, decision, priority, reason, and optional conflicts.
4. Resolver handles results deterministically.

Current decision vocabulary:

- `ALLOW`
- `REQUIRE_APPROVAL`
- `BLOCK`

Current precedence concept:

1. Explicit conflict → error.
2. BLOCK → strongest outcome.
3. Otherwise highest priority wins.
4. Same-priority disagreement → error.
5. Same-priority agreement → deterministic ordering.

Important safety invariant:

A project-specific `ALLOW` must not silently undo a mandatory approval already imposed by shared Scheduling/core policy.

## Testing model discussed

Three levels:

### Pure rule tests

Test resolution behavior without Frappe documents.

Cases:

- ALLOW beats lower-priority REQUIRE_APPROVAL.
- REQUIRE_APPROVAL beats lower-priority ALLOW.
- BLOCK wins.
- Equal-priority matching decisions succeed.
- Equal-priority disagreement fails.
- Explicit conflicts fail.
- Input order does not affect deterministic result.
- No applicable rules returns no client-specific decision.

### Frappe hook integration tests

Use a real `Appointment` document and trigger `validate` so the actual hook wiring executes.

Test:

- ALLOW leaves approval unnecessary.
- REQUIRE_APPROVAL sets fields.
- BLOCK raises validation error.
- Client ALLOW does not remove an existing shared approval requirement.

### Persistence tests

Use `insert()` to verify:

- ALLOW appointment persists.
- REQUIRE_APPROVAL persists approval fields.
- BLOCK prevents insertion.

## Coding-agent workflow

For every requested feature:

```text
Understand requirement
        ↓
Inspect capability registry
        ↓
Reuse existing capability?
        ↓
Configure existing behavior?
        ↓
Compose existing capabilities?
        ↓
If necessary, create local extension
        ↓
Write tests
        ↓
Record reusable learning
        ↓
Consider candidate promotion
```

The agent must inspect the capability base before coding.

## Guiding principle

The target is:

> vibe code against an accumulating software capability base

rather than:

> vibe code a new bespoke repository every time.

The valuable accumulated base includes not only source code, but tests, schemas, interfaces, integration knowledge, migration knowledge, deployment patterns, failure cases, and architecture decisions.

## Acceptance status — 2026-09-05

The packaged acceptance harness has been exercised end to end in a disposable rehearsal.
A structurally correct Beta composition passed the external evaluator, while the untouched
sandbox failed as expected. This validates the harness but is not the final fresh-agent proof
because the implementing assistant already knew the architecture.

Two bootstrap proof gates remain: real Frappe Bench lifecycle execution and an independent
fresh-agent acceptance run.
