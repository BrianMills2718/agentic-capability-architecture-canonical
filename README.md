# Agentic Capability Architecture

A working architecture for **composable software functionality that compounds across projects**. It gives coding agents a machine-readable capability system: semantic capability identities, verified executable exports, typed public boundaries, explicit composition, project-local residuals, and evidence that can improve what later agents know how to reuse.

The main idea is **not** “use off-the-shelf software when possible.” That is only a sourcing rule. The architectural thesis is to make useful functionality **legible, bindable, composable, and cumulative for agents** so that a later project can increasingly be expressed as composition plus only the genuinely novel residual.

> **If you are a teammate:** read [`TEAM_GUIDE.md`](TEAM_GUIDE.md) first. It explains why this matters to your coding agent, what is and is not novel, what is actually verified, and what remains a hypothesis.
>
> **Try the working system:** [`QUICKSTART.md`](QUICKSTART.md) generates an isolated engagement from a real task, gives the worker a capability snapshot, requires a capability/composition plan before coding, and validates the workflow.

## The value proposition

Most coding-agent workflows start each project from requirements plus whatever context happens to be in that repository. The agent rediscovers familiar behavior, rewrites interfaces, and leaves much of what it learned trapped in the project.

This repository tests a different model:

```text
required behavior
    ↓
semantic capability identity
    ↓
verified executable / typed public boundary
    ↓
select + reject + compose
    ↓
project-local residual behavior
    ↓
real tests / runtime evidence
    ↓
compatibility + rejection + composition knowledge
    ↓
stronger capability system for the next project
```

The goal is **not maximum reuse**. It is **correct composition**: reuse what truly fits, compose multiple capabilities when they jointly satisfy the requirement, keep consequential domain semantics local, and leave evidence that makes the next agent's decision better.

## Why point a coding agent at this repository?

The useful thing here is not simply a shared code library. An agent gets an explicit decision surface for answering:

1. What reusable behavior exists?
2. Which behavior has a verified executable interface?
3. Which candidates fit this requirement, and which should be rejected?
4. Which capabilities should be composed together?
5. What must remain project-local because it carries real domain meaning?
6. What evidence from this project should improve future composition decisions?

For paid/client work, `tools/engagement.py` turns those questions into a pre-code `CAPABILITY_PLAN.yml` and a closeout/evidence loop rather than leaving them as informal advice.

## What may be novel here — and what is not

The ingredients are not individually novel. Reusing libraries, typed APIs, service catalogs, package ecosystems, CI, build-vs-buy decisions, and preferring mature software over reinvention are established software practices.

The differentiated hypothesis is the **integrated agent-facing loop**:

- provider-independent semantic capability identities;
- machine-readable capability knowledge with explicit executable exports;
- typed boundaries that agents can bind and compose;
- a required pre-code plan that separates selected capabilities, rejected candidates, compositions, and local gaps;
- project-local behavior treated as a valid architectural outcome rather than failed abstraction;
- every project feeding success, failure, compatibility, and rejected-fit evidence back into the capability system;
- evidence-backed promotion rather than assuming generic-looking code is reusable;
- success measured by later projects becoming increasingly **composition-dominated**, not by the size of an internal library.

We do **not** claim this is historically unique or a world-first architecture without a dedicated landscape review. The potentially novel contribution is the combination, the agent operating contract, and the attempt to make the capability/evidence flywheel measurable and falsifiable.

## Machine-readable truth hierarchy

Agents should not treat every label in the repository as equally strong evidence.

1. **`semantic_exports` / `capability_catalog.py`** — verified executable action boundary. This is the strongest current callable claim.
2. **`public_interfaces`** — declared public boundary; inspect source/tests for semantics not covered by an export.
3. **`provides` and capability metadata** — capability scope/discovery information. A `provides` label is **not by itself a guarantee that a callable action exists**.
4. **evidence/maturity fields** — useful only to the extent they are current and backed by real use/test evidence.
5. **prose and historical proof material** — context, never stronger than current code/machine truth.

If code and metadata disagree, surface the disagreement as a defect. Do not silently infer a capability that the executable boundary does not support.

### Semantic action lookup

The current audited semantic action catalog is derived from capability manifests and exact public interfaces:

```bash
python tools/capability_catalog.py list --json
python tools/capability_catalog.py describe state.transition.plan --json
python tools/capability_catalog.py check
```

The audited exports currently include `approval.resolve`, `state.transition.plan`, and `notification.email.send`. Broader capability scope may exist in manifests, but agents should not treat it as an executable action until it has an honest bound export/interface.

## What exists today

- a capability registry and capability manifests;
- a manifest-derived semantic action catalog with audited public implementation boundaries;
- reusable capability implementations and multiple proof applications;
- explicit capability composition plus project-local extension boundaries;
- a paid-engagement generator that creates a portable worker capability snapshot;
- `CAPABILITY_PLAN.yml` for pre-code selection, rejection, composition, interfaces, and local-gap reasoning;
- validation for schema/requirement coverage, known internal exports/interfaces, and cooperative-workflow snapshot consistency;
- evidence, provenance, compatibility, rejection, maturity, and promotion records;
- tests and protected CI covering repository contracts and proof applications.

The engagement workflow is currently a **planning and evidence discipline for a cooperative worker**, not an adversarial sandbox or automatic IP-redaction system. The shipped checksum/self-check detects ordinary changes relative to the shipped snapshot, but because the worker receives the hash file and validator it is not a tamper-proof trust boundary. Evidence sanitization also still requires human review. See [`docs/ENGAGEMENT_OPERATING_SYSTEM.md`](docs/ENGAGEMENT_OPERATING_SYSTEM.md).

## The cumulative/composable flywheel

Each project is both a **consumer and a contributor**. A project consumes existing capability knowledge, composes what fits, implements only its residual local behavior, then contributes evidence back.

```text
requirement
    ↓
represent relevant capabilities honestly
    ↓
bind verified interfaces
    ↓
compose selected capabilities
    ↓
implement residual local semantics
    ↓
validate in real use
    ↓
record success + failure + rejection + compatibility evidence
    ↓
promote or strengthen reusable capability knowledge when justified
    ↓
next project starts from a stronger composable capability ecosystem
```

That is the **cumulative, composable capability ecosystem** this repository is testing.

## Supporting sourcing policy

**Off-the-shelf wins ties.** Provider sourcing matters, but it is not the main invention. A capability may be implemented by native platform behavior, an installed package, external OSS/SaaS, a standard, or internal code. The architecture cares that the behavior is represented honestly, exposed through a usable boundary, composable with other behavior, and backed by evidence.

Before creating shared implementation, investigate native/runtime features, installed ecosystem options, mature external implementations, existing standards/protocols, and internal capabilities. Implement a local gap when none of those honestly satisfies the requirement.

## What is not proven yet

This is a working technical system and research architecture, not proof that the capability flywheel pays for its overhead.

The central experiment still needs to show that, on comparable tasks and fresh sessions, an agent with the accumulated capability system materially outperforms a control agent with only a good planning contract. Relevant measures include task success, first-pass tests, turns/tokens/time, human intervention, bespoke code, duplicated implementation, rework, and composition accuracy.

The commercial hypothesis is also unproven: there is not yet a comparable 5–10 paid-engagement cohort showing that composition increases while marginal delivery effort and cost fall.

## For deeper technical context

Repository-local documentation is indexed in [`docs/README.md`](docs/README.md). The current charter is [`docs/ARCHITECTURE_CHARTER.md`](docs/ARCHITECTURE_CHARTER.md), the one-diagram view is [`docs/ARCHITECTURE_ONE_DIAGRAM.md`](docs/ARCHITECTURE_ONE_DIAGRAM.md), and current proof status is indexed in [`docs/PROOF_LEDGER_EXTENDED.md`](docs/PROOF_LEDGER_EXTENDED.md).

For cross-repository context, use the [Vision knowledge index](https://github.com/BrianMills2718/vision/blob/main/wiki/index.md) and [Agentic Capability Architecture project guide](https://github.com/BrianMills2718/vision/blob/main/wiki/projects/agentic-capability-architecture.md).

## Local role and boundaries

This is the **sole active capability-architecture lineage**. It owns capability/provider metadata, honest reusable public implementation boundaries, conservative capability resolution, reuse/maturity evidence, engagement planning contracts, and the local proof fixtures used to test those ideas.

It does **not** own upstream application meaning, a universal workflow engine, a scheduler, authorization platform, notification platform, package registry, observability system, or a universal primitive runtime. The primitive vocabulary/composition work under `architecture/primitive_model/` remains experimental.

Shared capabilities must not absorb consequential client/project semantics merely to increase reuse. The intended mature project shape is:

```text
known capability composition
        +
small genuinely novel project-local residual
```

## Proof applications

Client Intake + Booking, Internal Procurement, IT Access Control, Facility Maintenance, Service Desk, Shared Resource Reservation, and the acceptance sandboxes are primarily **architecture proof fixtures**. They demonstrate reuse pressure, local semantics, compatibility, portability, and agent behavior. They are not a mandate to rebuild mature business platforms.

## Status

This remains experimental architecture research with real working code and bounded proof results. The validated claims are implementation/proof claims, not proof of a universal composition language, a universal application runtime, or commercial compounding. Current completed and pending proof claims are indexed in [`docs/PROOF_LEDGER_EXTENDED.md`](docs/PROOF_LEDGER_EXTENDED.md).