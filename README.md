# Agentic Capability Architecture

Research and working implementation for an agent-native capability **selection, reuse, and evidence** architecture.

> **Global navigation:** start at the [Vision knowledge index](https://github.com/BrianMills2718/vision/blob/main/wiki/index.md), then use the [Agentic Capability Architecture project guide](https://github.com/BrianMills2718/vision/blob/main/wiki/projects/agentic-capability-architecture.md).
>
> This README describes this repository's local role. It intentionally does not maintain a competing global “start here” tree.

## Local role

This is the **sole active capability-architecture lineage**. It owns capability/provider metadata, honest reusable public implementation boundaries, conservative capability resolution, reuse/maturity evidence, and the local proof fixtures used to test those ideas.

It does **not** own upstream application meaning, a second semantic IR, a universal workflow engine, a scheduler, authorization platform, notification platform, package registry, observability system, or a general replacement for capabilities already available in mature software.

The durable goal is to help a coding agent answer:

1. What behavior is actually required?
2. What suitable implementation already exists—native platform, ecosystem package, external OSS/SaaS, standard protocol, or internal capability?
3. Why does a candidate fit or fail?
4. What honest typed interface should be consumed?
5. What consequential behavior must remain project-local?
6. What evidence should be recorded so the next agent makes a better decision?

## Governing stance

**Off-the-shelf wins ties.** Reuse does not mean “prefer our code.” Before creating shared implementation, investigate native runtime features, installed ecosystem options, mature external implementations, existing standards/protocols, and only then the internal capability base. Implement the residual local gap when none of those honestly satisfies the requirement.

The repository's strongest strategic direction is therefore a **capability intelligence and evidence layer**, not a growing private reimplementation of common application infrastructure.

The primitive vocabulary and composition models under `architecture/primitive_model/` remain experimental. A primitive name may be useful as semantic vocabulary without implying that this repository should own a runtime implementation for that operation.

## Local technical authority

Use [`docs/README.md`](docs/README.md) for the repository-local documentation map and authority order.

Key machine-readable/current sources include:

- `capabilities/*/capability.yml` — capability-local metadata and evidence;
- `capability_registry.yml` — current checked-in registry/catalog surface;
- `schemas/` — machine-readable contracts;
- `AGENTS.md` — coding-agent operating rules;
- `docs/ARCHITECTURE_CHARTER.md` — current local architecture charter;
- `docs/PROOF_LEDGER_EXTENDED.md` — current proof-status index.

Do not copy capability maturity/status tables into prose merely for convenience. Read machine-readable state directly. If manifests and registry disagree, that is a synchronization defect to fix rather than something this README should mask.

## Lineage

The sibling capability-architecture repositories are historical/evidence lineages rather than competing active architectures. The wider authority matrix and current dispositions are maintained in the [current ontology/semantic cluster architecture](https://github.com/BrianMills2718/vision/blob/main/wiki/synthesis/ontology-semantic-cluster-current-architecture-2026-09-07.md).

## Proof applications

Client Intake + Booking, Internal Procurement, IT Access Control, Facility Maintenance, Service Desk, Shared Resource Reservation, and the acceptance sandboxes are primarily **architecture proof fixtures**. They demonstrate reuse pressure, local semantics, compatibility, portability, and agent behavior. Where Frappe/ERPNext or another mature product already supplies the business capability, these fixtures are not a mandate to build a competing product.

## Status

This remains experimental architecture research. The validated claims are bounded implementation/proof claims, not proof of a universal primitive language or universal application-composition runtime. Current completed and pending proof claims are indexed in [`docs/PROOF_LEDGER_EXTENDED.md`](docs/PROOF_LEDGER_EXTENDED.md).
