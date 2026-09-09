# Agentic Capability Architecture

A working prototype for building software with AI agents and contractors by **discovering, selecting, and composing existing capabilities before writing new code**. The goal is cumulative software delivery: each completed project should make later comparable projects easier to build.

## Try the working system

Start with [`QUICKSTART.md`](QUICKSTART.md). It gives you a reproducible hands-on demo using the included Shipment Exception task. You will generate an isolated engagement workspace, inspect its capability snapshot and planning contract, and then hand that workspace to a coding agent.

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install 'PyYAML>=6,<7' 'jsonschema>=4,<5'
python tools/engagement.py new colleague_demo \
  --task proof/fresh_agent_registry_discovery/challenge/TASK.md \
  --output ../colleague_demo
python tools/engagement.py validate ../colleague_demo
```

The generated workspace contains `TASK.md`, `ENGAGEMENT.yml`, `AGENT_RULES.md`, `CAPABILITY_PLAN.yml`, `METRICS.yml`, `EVIDENCE_PROPOSAL.yml`, a self-contained validator, and a hashed snapshot of available capability metadata and runtime source.

## What it does

```text
requirement
  -> discover available capabilities/providers
  -> select and reject candidates explicitly
  -> compose through declared public interfaces
  -> implement only the residual local gap
  -> test and deliver
  -> record evidence, compatibility, failures, and reusable learning
  -> improve the ecosystem for the next project
```

The system is designed so a worker does **not** begin from a blank repository. It receives reusable capability knowledge and must complete a capability/composition plan before implementation. Client-specific work stays isolated; reusable learning is proposed separately for human review.

## What exists today

- a machine-readable capability registry and manifest-derived semantic action catalog;
- reusable capability implementations with honest public interfaces;
- capability selection/rejection and composition planning;
- isolated engagement generation for contractor/client work;
- snapshot integrity and self-contained engagement validation;
- commercial/delivery metrics and sanitized evidence closeout;
- multiple project/proof fixtures that pressure-test reuse and local semantics;
- repository-wide validation, package-build checks, tests, and a protected `bootstrap` CI gate.

## Why this matters

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

## Governing stance

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
