# Working Context

> **Status: historical accumulated implementation context.** This file records the reasoning and examples that shaped the early capability-first bootstrap. Terms such as “current,” “chosen direction,” and the workflow shown below should be read in that historical context. For current architecture use [`ARCHITECTURE_CHARTER.md`](ARCHITECTURE_CHARTER.md); for current agent/project sourcing use `../AGENTS.md` and [`PROJECT_WORKFLOW.md`](PROJECT_WORKFLOW.md); for current proof status use [`PROOF_LEDGER_EXTENDED.md`](PROOF_LEDGER_EXTENDED.md). In particular, current sourcing begins with native/platform, ecosystem, mature external, and standards-based options before internal capability reuse.

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

For every requested feature, the early bootstrap used:

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

The current workflow broadens inspection beyond the internal capability base; see `PROJECT_WORKFLOW.md`.

## Guiding principle

The target was described as:

> vibe code against an accumulating software capability base

rather than:

> vibe code a new bespoke repository every time.

The valuable accumulated base includes not only source code, but tests, schemas, interfaces, integration knowledge, migration knowledge, deployment patterns, failure cases, and architecture decisions.

The current charter generalizes this idea further: the accumulated asset is capability **knowledge and evidence**, and the selected implementation may be native, ecosystem, external, standards-based, internal, or local.

## Fresh-agent proof learning — iteration 1

The first independent GitHub Copilot cloud-agent run correctly reused Scheduling, Approvals, and Notifications and kept the 90-minute rule local, but it exposed two self-guidance gaps: it did not record a reuse assessment, and it implemented an email reminder callable without an actual scheduled trigger. The bootstrap then mechanically required a per-project `LEARNINGS.md` reuse assessment and explicitly required automatic/triggered requirements to include real framework wiring and tests.

## Fresh-agent proof learning — iteration 2

The second fresh agent fixed the first run's missing learning record and missing scheduled trigger, but full-suite evaluation exposed a test-module basename collision between unit and compatibility directories. The repository then adopted pytest importlib mode for modular test isolation, protected that contract with a regression test, and explicitly required agents to run the exact full bootstrap gate before declaring work complete.

## Fresh-agent proof learning — iteration 3

A green developer-shell test run is not sufficient evidence if nested app tests are omitted or local packages happen to be installed. The bootstrap was strengthened to dynamically discover every Frappe app, supply all app roots through a clean test environment, execute nested app tests, and structurally validate Frappe module-package markers before wheel builds.

### Local-vs-Bench test collection rule

Nested app tests are part of the local repository-wide test discovery. Tests that genuinely require a real Frappe site must remain collectable without Frappe installed, using `pytest.importorskip("frappe")` or deferred framework imports. This lets the local gate prove test discovery/import wiring while the real Bench proof establishes lifecycle behavior for the tested revision.

## Current semantic capability boundary

The current application/composability architecture uses precise semantic action IDs only as provider-independent lookup keys. Capability manifests remain the implementation source of truth and point exports at real public interfaces. The initial audited set is `approval.resolve`, `state.transition.plan`, and `notification.email.send`; catalog/list/describe views are derived from those manifests, exact matching is the current resolver policy, and no wrapper or second publication registry is added unless a real interface mismatch or matching requirement appears.
