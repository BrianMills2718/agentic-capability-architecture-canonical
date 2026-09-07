# Agentic Capability Architecture

Research and working implementation for an agent-native software architecture in which each project leaves behind reusable capability, tests, evidence, and architectural knowledge for the next project.

> **Canonical status:** this is the sole active capability-architecture lineage. Historical source/predecessor repos remain preserved for evidence, but new capability architecture development belongs here. See `architecture/lineage_inventory.yml` and issue #27.

## North star

Instead of asking a coding agent to regenerate an application from scratch, give it a machine-readable capability base that lets it:

1. inspect what already exists;
2. reuse, configure, and compose proven behavior;
3. identify genuinely local gaps;
4. implement only those gaps;
5. validate compatibility and runtime behavior;
6. contribute new reuse evidence back to the capability base.

The larger hypothesis is that many applications may be compositions of a relatively small number of configurable semantic primitives plus higher-order capabilities, while important domain semantics remain local.

## Shared composition seam

This repository owns reusable capability/primitive implementation metadata, maturity, evidence, dependencies, and resolution to implementation interfaces.

It does **not** own the portable typed composition contract. The shared boundary is `BrianMills2718/data-contracts`, whose composition layer validates action/contract flow while treating implementation references as opaque. The requirement-to-runtime semantic compiler can lower target-neutral system meaning into that boundary; this repository resolves the required behavior to existing providers.

The first proven cross-repo slice is:

```text
Semantic SystemSpec
    ↓
behavior requirements
    ↓
data-contracts composition validation
    ↓
capability resolution here
    ↓
existing provider interfaces
```

## Architecture at a glance

- [`docs/ARCHITECTURE_CHARTER.md`](docs/ARCHITECTURE_CHARTER.md) — concise governing architecture: primitives, capabilities, project-local behavior, evidence, agent planning, and the federated commons.
- [`docs/ARCHITECTURE_ONE_DIAGRAM.md`](docs/ARCHITECTURE_ONE_DIAGRAM.md) — one Mermaid diagram showing the end-to-end requirement → registry → composition → runtime → evidence → commons loop.

## Current layers

```text
semantic primitives
    ↓
evidence-backed capabilities
    ↓
typed project composition / state models
    ↓
project-native implementation adapters
```

## Current registered capabilities

```text
core            CORE
approvals       PROVEN
notifications   PROVEN
scheduling      CANDIDATE
```

## Real projects

The repository contains production-shaped Frappe implementations for:

1. Client Intake + Booking
2. Internal Procurement
3. IT Access Control
4. Facility Maintenance
5. Service Desk
6. Shared Resource Reservation

The latest seven-site proof demonstrated isolated project compositions and preserved older regression suites while adding the non-appointment Resource Reservation use case.

## Primitive-model research

See `docs/PRIMITIVE_CAPABILITY_THESIS.md` and the experimental files under `architecture/primitive_model/` where present.

The visual graph is not intended to be the architecture. The underlying typed model is the source; node/port, state-transition, deployment, and evidence diagrams are views over it.

Alternative build-time semantic-model experiments from historical lineages are preserved as research evidence and are not a second canonical composition contract.

## Capability-network research

The repository contains the isolated fresh-agent registry-discovery challenge under `proof/fresh_agent_registry_discovery/challenge/`.

Historical federated-capability-network context from the composable predecessor is provenance-preserved at `docs/research/COMPOSABLE_LINEAGE_NETWORK_GATE_2026-09-06.md`.

## Start here

1. `docs/ARCHITECTURE_CHARTER.md` — governing one-page architecture.
2. `architecture/lineage_inventory.yml` — canonical/superseded repo lineage and preserved evidence.
3. `docs/ARCHITECTURE_ONE_DIAGRAM.md` — visual architecture overview.
4. `AGENTS.md` — rules for coding agents.
5. `capability_registry.yml` — current capability registry.
6. `architecture/primitive_model/primitive_registry.yml` — experimental semantic primitive vocabulary and implementation evidence.
7. `reuse_candidates.yml` — evidence pipeline for emerging reuse.
8. `docs/PROOF_LEDGER_EXTENDED.md` — proof references.

## Status

This is an experimental research/code repository, not a claim that one universal primitive language or workflow engine has been validated.

The governing discipline is: **do not force everything to be reusable; make everything eligible to become reusable, then promote only after materially different uses provide evidence.**
