# Agentic Capability Architecture

Research and working implementation for an agent-native software architecture in which each project leaves behind reusable capability, tests, evidence, and architectural knowledge for the next project.

## North star

Instead of asking a coding agent to regenerate an application from scratch, give it a machine-readable capability base that lets it:

1. inspect what already exists;
2. reuse, configure, and compose proven behavior;
3. identify genuinely local gaps;
4. implement only those gaps;
5. validate compatibility and runtime behavior;
6. contribute new reuse evidence back to the capability base.

The larger hypothesis is that many applications may be compositions of a relatively small number of configurable semantic primitives plus higher-order capabilities, while important domain semantics remain local.

**Cross-repo role and lineage.** This is the **sole active capability-architecture
lineage**. It owns capability manifests, reusable public implementation
boundaries, provider/capability resolution, and reuse/maturity evidence. It does
not own upstream application meaning or introduce a second semantic IR.

The sibling repositories now have explicit non-active dispositions:
`brianmills-spec/agentic-capability-architecture` is historical/experimental
evidence, `brianmills-spec/composable-capability-architecture` is a historical
predecessor/evidence lineage, and
`brianmills-spec/capability-registry-discovery-proof-20260906` is a preserved
proof fixture. The unrecovered Downloads ZIP remains provenance debt, not
assumed functionality; track reconciliation in issue #27 and
`architecture/lineage_inventory.yml`.

For the wider authority matrix, semantic/compiler boundary, and cleanup policy,
see the [current ontology/semantic cluster architecture](https://github.com/BrianMills2718/vision/blob/main/wiki/synthesis/ontology-semantic-cluster-current-architecture-2026-09-07.md).

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
approvals       CANDIDATE
notifications   CANDIDATE
scheduling      CANDIDATE
```

## Semantic action catalog

Semantic actions are exported from capability manifests and resolved by exact ID; there is no hand-maintained publication registry. The first audited exports are `approval.resolve`, `state.transition.plan`, and `notification.email.send`, each pointing directly at an existing public function.

```bash
python tools/capability_catalog.py list --json
python tools/capability_catalog.py describe approval.resolve --json
```

Use the catalog for provider-independent lookup. Do not treat an action ID as a claim that the behavior is a universal primitive, and do not add wrapper functions when the existing public interface already matches the declared meaning.

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

## Capability-network research

The repository also contains the isolated fresh-agent registry-discovery challenge under `proof/fresh_agent_registry_discovery/challenge/`.

That challenge exposes multiple portable capabilities and asks an independent coding agent to discover and select the relevant ones before coding. It is intended to test whether the architecture works without conversational coaching.

## Start here

1. `docs/ARCHITECTURE_CHARTER.md` — governing one-page architecture.
2. `docs/ARCHITECTURE_ONE_DIAGRAM.md` — visual architecture overview.
3. `AGENTS.md` — rules for coding agents.
4. `capability_registry.yml` — current capability registry.
5. `python tools/capability_catalog.py list --json` — manifest-derived semantic action catalog (`make capability-list` is the thin shorthand).
6. `reuse_candidates.yml` — evidence pipeline for emerging reuse.
7. `docs/PRIMITIVE_CAPABILITY_THESIS.md` — deeper primitive/capability hypothesis.
8. `docs/WORKING_CONTEXT.md` and `docs/SESSION_CONTEXT_2026-09-06.md` — implementation history and strategic handoff.
9. `docs/PROOF_LEDGER_EXTENDED.md` — proof references.
10. `docs/DECISIONS.md` — durable repository-local architecture decisions.

## Status

This is an experimental research/code repository, not a claim that one universal primitive language or workflow engine has been validated.

The governing discipline is: **do not force everything to be reusable; make everything eligible to become reusable, then promote only after materially different uses provide evidence.**
