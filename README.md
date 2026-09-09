# Agentic Capability Architecture

A working architecture for **composable software functionality that compounds across projects**. It gives coding agents a machine-readable capability ecosystem: discoverable behaviors, typed public interfaces, explicit composition, project-local residuals, and evidence that feeds back into what later agents can reuse.

The core idea is not merely “reuse existing software.” It is to make reusable functionality **legible and composable to agents**, then make every real project strengthen that capability system for the next one.

> **Try the working system:** [`QUICKSTART.md`](QUICKSTART.md) generates an isolated engagement from a real task, gives the worker a capability snapshot, requires a capability/composition plan before coding, and validates the result.

## What the architecture makes possible

```text
required behavior
    ↓
capability identities + machine-readable metadata
    ↓
typed public interfaces
    ↓
discover / select / compose capabilities
    ↓
implement only genuine project-local residuals
    ↓
validate in real use
    ↓
record composition, compatibility, success, rejection, and failure evidence
    ↓
promote or strengthen reusable capability knowledge
    ↓
the next project starts from a stronger composable capability ecosystem
```

That flywheel is the differentiated architectural thesis. The system is designed so that a later project can increasingly be expressed as **composition plus a small residual**, rather than as a fresh application implementation.

## What exists today

- a capability registry and manifest-derived semantic action catalog;
- typed public capability boundaries tied to real implementations;
- reusable capability implementations and multiple proof applications;
- explicit project composition through capability manifests/plans;
- a paid-engagement generator that gives contractors/agents a portable hashed capability snapshot;
- mandatory `CAPABILITY_PLAN.yml` selection, rejection, interface, composition, and local-gap recording before implementation;
- validation that rejects unknown capabilities/interfaces, uncovered requirements, invalid compositions, and snapshot tampering;
- evidence, provenance, compatibility, rejection, maturity, and promotion machinery;
- tests and protected CI covering the repository contracts and proofs.

Provider sourcing is a supporting policy, not the architecture itself. Capabilities may come from internal code, platform-native behavior, external software/services, or standards. What matters architecturally is that the behavior can be represented honestly, bound through a usable interface, composed with other capabilities, validated, and learned from.

## Why this matters

Most coding-agent workflows still treat each new project as a mostly fresh synthesis problem. This architecture is testing a different model: **software delivery as cumulative composition**.

If it works, the important trend is not simply “more reuse.” It is that the percentage of a new project describable as validated capability composition rises over time, while bespoke residual implementation shrinks toward genuinely novel domain behavior.



Most coding-agent workflows repeatedly regenerate applications from requirements. This repository tests a different model: a **cumulative, composable capability ecosystem** in which software development should compound. A later project should increasingly reuse proven capabilities, interfaces, compatibility knowledge, and compositions instead of re-solving the same problems.

Ecosystem growth is not just more internal code. It can also mean better evidence for platform-native features, external OSS/SaaS, standards, rejected fits, compatibility constraints, or proof that a behavior should remain project-local. **Off-the-shelf wins ties.**

## What is not proven yet

This is a working technical system and research architecture, not proof of a universal composition language or a commercially compounding services business. The commercial hypothesis is being tested separately through paid engagements and comparable-cohort economics.

## For deeper technical context

The sections below preserve the architecture, authority, proof, and lineage detail used by maintainers and agents. Repository-local documentation is indexed in [`docs/README.md`](docs/README.md). For cross-repository context, use the [Vision knowledge index](https://github.com/BrianMills2718/vision/blob/main/wiki/index.md) and [Agentic Capability Architecture project guide](https://github.com/BrianMills2718/vision/blob/main/wiki/projects/agentic-capability-architecture.md).

## Local role

This is the **sole active capability-architecture lineage**. It owns capability/provider metadata, honest reusable public implementation boundaries, conservative capability resolution, reuse/maturity evidence, and the local proof fixtures used to test those ideas.

Its core architectural purpose is **cumulative**: each project should consume the best capability knowledge already available and leave the ecosystem better for the next project through stronger evidence, clearer compatibility/provenance, better rejected-fit knowledge, or genuinely reusable capability when promotion is justified.

It does **not** own upstream application meaning, a second semantic IR, a universal workflow engine, a scheduler, authorization platform, notification platform, package registry, observability system, or a general replacement for capabilities already available in mature software.

The durable goal is to help a coding agent answer:

1. What behavior is actually required?
2. What suitable implementation already exists—native platform, ecosystem package, external OSS/SaaS, standard protocol, or internal capability?
3. Why does a candidate fit or fail?
4. What honest typed interface should be consumed?
5. What consequential behavior must remain project-local?
6. What evidence should be recorded so the next agent makes a better decision?

## Cumulative ecosystem model

Each project is both a **consumer and a contributor**. It should start by discovering and reusing the best existing implementation, implement only the genuine residual gap, then leave behind evidence and reusable knowledge that improve future decisions.

```text
requirement
    ↓
source/select existing capability
    ↓
configure / compose
    ↓
implement only the residual local gap
    ↓
validate in real use
    ↓
record evidence + provenance + compatibility + rejected fits
    ↓
promote reusable behavior when repeated use justifies it
    ↓
stronger capability ecosystem for the next project
```

Ecosystem growth therefore means more than a larger internal codebase. It includes better knowledge of native/platform features, external OSS/SaaS, standards, internal capabilities, honest interfaces, compatibility constraints, failures, and successful compositions. Sometimes the best cumulative contribution is evidence that an existing external capability should be reused—or that a behavior should remain project-local.

### Paid/client engagements

For contractor or client work, use `python tools/engagement.py new ...` to create an isolated engagement workspace. The contractor consumes a read-only capability snapshot, records a capability/composition plan before coding, keeps client work product local, and produces only sanitized generalized evidence for human review. See [`docs/ENGAGEMENT_OPERATING_SYSTEM.md`](docs/ENGAGEMENT_OPERATING_SYSTEM.md).

## Supporting sourcing policy

**Off-the-shelf wins ties.** Reuse does not mean “prefer our code.” Before creating shared implementation, investigate native runtime features, installed ecosystem options, mature external implementations, existing standards/protocols, and only then the internal capability base. Implement the residual local gap when none of those honestly satisfies the requirement.

The repository's strongest strategic direction is therefore a **capability intelligence and evidence layer**, not a growing private reimplementation of common application infrastructure.

The primitive vocabulary and composition models under `architecture/primitive_model/` remain experimental. A primitive name may be useful as semantic vocabulary without implying that this repository should own a runtime implementation for that operation.

## Local technical authority

Use [`docs/README.md`](docs/README.md) for the repository-local documentation map and authority order.

Key machine-readable/current sources include:

- `capabilities/*/capability.yml` — capability-local metadata and evidence;
- `capability_registry.yml` — synchronized capability index;
- `python tools/capability_catalog.py list --json` — manifest-derived semantic action catalog;
- `schemas/` — machine-readable contracts;
- `AGENTS.md` — coding-agent operating rules;
- `docs/ARCHITECTURE_CHARTER.md` — current local architecture charter;
- `docs/PROOF_LEDGER_EXTENDED.md` — current proof-status index.

Do not copy capability maturity/status tables into prose merely for convenience. Read machine-readable state directly. If manifests and registry disagree, that is a synchronization defect to fix rather than something this README should mask.

### Semantic action lookup

The current catalog is derived directly from capability manifests; there is no hand-maintained publication registry. The first audited exports are `approval.resolve`, `state.transition.plan`, and `notification.email.send`, each pointing directly at an existing public function. Lookup is exact and conservative.

```bash
python tools/capability_catalog.py list --json
python tools/capability_catalog.py describe approval.resolve --json
```

An action ID is a provider-independent behavior name, not a claim that the behavior is a universal primitive. Do not add a wrapper when the existing public interface already matches the declared meaning.

## Lineage

The sibling capability-architecture repositories are historical/evidence lineages rather than competing active architectures. The wider authority matrix and current dispositions are maintained in the [current ontology/semantic cluster architecture](https://github.com/BrianMills2718/vision/blob/main/wiki/synthesis/ontology-semantic-cluster-current-architecture-2026-09-07.md).

## Proof applications

Client Intake + Booking, Internal Procurement, IT Access Control, Facility Maintenance, Service Desk, Shared Resource Reservation, and the acceptance sandboxes are primarily **architecture proof fixtures**. They demonstrate reuse pressure, local semantics, compatibility, portability, and agent behavior. Where Frappe/ERPNext or another mature product already supplies the business capability, these fixtures are not a mandate to build a competing product.

## Status

This remains experimental architecture research. The validated claims are bounded implementation/proof claims, not proof of a universal primitive language or universal application-composition runtime. Current completed and pending proof claims are indexed in [`docs/PROOF_LEDGER_EXTENDED.md`](docs/PROOF_LEDGER_EXTENDED.md).
