# Agentic Capability Architecture — Charter

## Mission

Build a software-delivery system in which coding agents **reuse and strengthen existing capability rather than regenerate every application from scratch**. Each real project should leave behind working software, tests, compatibility evidence, reusable observations, and better instructions for the next agent.

The governing rule is:

> **Do not force everything to be reusable. Make everything eligible to become reusable, then promote only after materially different uses provide evidence.**

## Architectural layers

```text
semantic primitives
    ↓
evidence-backed capabilities
    ↓
typed project composition / state models
    ↓
project-local domain behavior
    ↓
runtime adapters and infrastructure
```

### 1. Primitives

A primitive is a **small, bounded semantic operation** whose execution meaning can remain stable across materially different domains. Examples under investigation include `state.transition`, `actor.authorize`, `policy.resolve`, `actor.assign`, `time.deadline`, `event.scan`, `notification.send`, and `artifact.attach`.

A primitive is not merely a helper function. A useful primitive should have explicit inputs/outputs, constraints, state/effect semantics, failure behavior, retry/idempotency behavior, and typed composition boundaries. The current execution hypothesis combines typed node/port composition with explicit state/action/transition and trigger semantics.

### 2. Capabilities

A capability is a **higher-order reusable unit**: implementation + public interfaces + configuration + dependencies + tests + extension points + compatibility evidence + maturity. Current examples include Core, Approvals, Notifications, and Scheduling.

Capabilities may compose primitives or other capabilities. A capability interface does **not** automatically become a primitive; promotion depends on semantic stability and repeated cross-domain evidence.

### 3. Project-local behavior

Project-local behavior is a first-class architectural category, not failed abstraction. Domain rules such as procurement fulfillment, entitlement provisioning, support triage, resource identity, client-specific thresholds, and domain-specific notification timing/recipients should remain local when generalization would erase consequential meaning or increase coupling.

Agents should follow this order:

```text
reuse → configure → compose → implement local gap
```

Only repeated materially different demand should trigger extraction.

## Evidence and promotion

Reuse maturity is evidence-driven:

```text
local / observed → candidate → proven → core or canonical
```

Evidence may include materially different project uses, unit/integration tests, compatibility suites, real-runtime proofs, migrations, known conflicts and limitations, independent-agent acceptance, security review, and operational incidents/lessons.

Tests are executable institutional memory. Project count alone is insufficient: a capability can remain candidate/proven when extraction would increase coupling or the stable common surface is still unclear.

## Agent planning contract

Before writing project-specific code, an agent should be able to answer:

1. What requirement is being satisfied?
2. Which registered capabilities/primitives are semantically relevant?
3. Which available capabilities are explicitly rejected, and why?
4. Which public interfaces will be consumed?
5. What configuration or composition is required?
6. What behavior must remain project-local?
7. What evidence/tests will prove the composition works?
8. What new reuse observation, if any, should be recorded afterward?

The goal is to make agent planning increasingly **selection-and-composition dominated**, with code generation focused on genuine gaps.

## Federated capability commons

The long-run model is federated rather than monolithic:

```text
PUBLIC CAPABILITY COMMONS
          ↓
ORGANIZATION REGISTRIES
          ↓
TEAM / PROJECT REGISTRIES
          ↓
PROJECT-LOCAL BEHAVIOR
```

A registry should eventually let agents query capability identity/version, semantics, public interfaces, configuration, dependencies, runtime compatibility, licensing, provenance, tests, evidence, security constraints, known conflicts, and validated compositions.

The network effect is:

```text
real use → evidence → better agent selection → more reuse → stronger capabilities → faster future projects
```

The central reusable asset is therefore not just code. It is **machine-understandable capability plus evidence about when and how it works**.

## Non-goals

The architecture does not currently aim to create a universal workflow engine, universal form/schema system, visual graph editor as the source of truth, one semantic vocabulary for every domain, or a global capability marketplace before independent-consumer demand exists.

Frappe is the current runtime substrate, not the durable abstraction boundary. UML, SysML v2, KerML, BPMN, and ISO/IEC/IEEE 42010 are prior art and possible interchange/viewpoint sources, not assumed runtime kernels.

## Success criterion

The architecture succeeds if later projects require less architectural discovery and less bespoke implementation **without hiding domain semantics or increasing coupling**. The desired trend is more requirements satisfied by existing primitives/capabilities, faster delivery, fewer regressions, stronger compatibility evidence, and lower marginal effort per new project—not simply more shared code.
