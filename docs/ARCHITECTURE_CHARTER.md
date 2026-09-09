# Agentic Capability Architecture — Charter

## Mission

Build a **cumulative, composable software-delivery ecosystem** in which agents can represent useful behavior as discoverable capabilities with honest typed boundaries, compose those capabilities into new systems, isolate only the genuinely project-local residual, and feed real-use evidence back into the ecosystem so later projects become increasingly composition-driven.

The durable asset is not a large private library and not a sourcing checklist. It is **machine-understandable capability knowledge plus compositional structure and evidence about what exists, what it actually does, how it binds, how it composes, where it fails, and what should remain local**.

The governing rules are:

> **Composition is the target shape.** A mature project should increasingly be describable as a composition of known capabilities plus only the genuinely novel residual.

> **Every project should strengthen the capability graph.** Successful compositions, rejected fits, interface limits, compatibility facts, and justified reusable behavior all improve later work.

> **Do not force everything to be reusable. Make everything eligible to become reusable, then promote only after materially different uses provide evidence.**

> **Off-the-shelf wins ties.** Provider sourcing is subordinate to the composability model: native/platform/external/internal implementations are all legitimate providers when they satisfy the same capability boundary honestly.

## Composability and cumulative growth contract

Every project is both a **consumer and a contributor** to the capability ecosystem. The architecture should make this compounding loop normal:

```text
discover / bind / compose known capabilities
        ↓
implement only the residual local gap
        ↓
validate the result in a real project
        ↓
record use, rejection, compatibility, provenance, and limitations
        ↓
promote genuinely reusable behavior when evidence warrants it
        ↓
better capability knowledge for the next project
```

The cumulative asset can grow even when no new internal package is created. A project improves the ecosystem when it strengthens evidence for an external/native capability, records a failed or rejected fit, clarifies an interface or compatibility constraint, preserves a useful local boundary, or contributes a reusable capability whose promotion is supported by materially different uses.

## Architecture

The ordinary application path is:

```text
requested application meaning / semantic requirement
        ↓
capability identity and provider resolution
        ↓
honest typed public boundaries
        ↓
explicit configuration / composition
        ↓
project-local residual behavior
        ↓
existing runtime/platform infrastructure
        ↓
execution, compatibility, and reuse evidence
```

Upstream application meaning is owned outside this repository by the appropriate semantic/application authority. This repository should not create a second semantic IR merely to perform capability selection.

### 1. Capability identity, discovery, and provider resolution

A semantic capability/action identity should name the **narrowest reusable behavior actually required/provided**, independently of provider, repository, or deployment. The currently audited internal semantic exports are deliberately narrow: `approval.resolve`, `state.transition.plan`, and `notification.email.send`. Broader research labels such as `policy.resolve`, `state.transition`, and `notification.send` are not canonical merely because an experiment used them.

Before creating shared implementation, investigate:

1. native runtime/platform capability;
2. installed ecosystem plugins/apps/packages;
3. mature external OSS/SaaS implementations;
4. existing standards/protocols;
5. internal registered capabilities;
6. only then, the residual project-local gap.

The architecture should record meaningful candidates, selection/rejection reasons, compatibility constraints, licensing/security/runtime considerations, and the evidence behind the decision when those facts materially affect future reuse.

### 2. Capabilities and honest public boundaries

A capability is reusable software or service behavior exposed through an honest public boundary, together with enough metadata and evidence for an agent to decide whether it fits.

A capability may be implemented by this repository, by Frappe/ERPNext, by another package, by a remote service, or by another standards-based provider. Ownership of the metadata/selection layer does not imply ownership of the implementation runtime.

Prefer existing typed public functions/APIs when they already express the correct behavior. Add adapters only for real translation, runtime, or compatibility needs; do not create wrapper facades merely for architectural symmetry.

### 3. Project-local behavior

Project-local behavior is a first-class architectural category, not failed abstraction. Domain rules such as procurement fulfillment, entitlement provisioning, support triage, resource identity, client-specific thresholds, and domain-specific notification timing/recipients should remain local when generalization would erase consequential meaning or increase coupling.

The preferred sequence is:

```text
source existing → configure → compose → implement residual local gap
```

Only repeated materially different demand should trigger extraction.

### 4. Runtime and infrastructure

Execution, persistence, authorization, scheduling, retries, messaging, transactions, observability, package distribution, and similar infrastructure should be supplied by established runtime/platform mechanisms when they satisfy the required invariant.

This repository should not build a generic workflow engine, authorization system, notification platform, scheduler, package manager, service catalog UI, agent transport protocol, provenance/signing system, or observability platform merely because those concerns appear in capability compositions.

### 5. Primitive-model research

The primitive vocabulary and composition files under `architecture/primitive_model/` are **experimental**.

A primitive is a proposed small semantic operation whose meaning may remain stable across materially different domains. A primitive label may still be useful as planning vocabulary even when execution is delegated to an existing runtime or product.

Do not promote a primitive merely because many applications can be described using a generic verb. Promotion requires evidence that the primitive adds value beyond ordinary typed capability interfaces—for example by catching real architecture errors, enabling useful compatibility checking, or improving capability selection/composition without hiding decisive domain semantics.

The primitive model is not the default runtime architecture and is not a claim that one small universal vocabulary has been validated.

## Evidence and maturity

Reuse maturity is evidence-driven:

```text
local / observed → candidate → proven → core
```

Evidence may include:

- materially different successful uses;
- failed or rejected fits;
- unit, integration, compatibility, and real-runtime proofs;
- independent-agent or independent-consumer use;
- runtime/platform diversity;
- migrations and interface stability;
- security review;
- operational incidents and limitations;
- licensing or deployment constraints.

Project count alone is insufficient. A capability can remain candidate/proven when extraction would increase coupling, the stable common surface is unclear, or all evidence comes from one runtime/domain family.

Human-readable documents should not hand-maintain volatile maturity tables when machine-readable manifests/catalogs can supply them. Views should be derived where practical and drift should be treated as a defect.

## Agent planning contract

Before writing project-specific code, an agent should be able to answer:

1. What exact requirement is being satisfied?
2. Which native, ecosystem, external, standards-based, and internal candidates are relevant?
3. Which candidates were rejected, and why?
4. Which semantic capability/action and honest public interface will be consumed?
5. What configuration or composition is required?
6. What behavior must remain project-local?
7. Which runtime/platform facility supplies execution and reliability guarantees?
8. What evidence/tests will prove the composition works?
9. What new sourcing/reuse observation should be recorded afterward?

The goal is to make agent planning increasingly **composition-dominated**: semantic capability identity, typed binding, and explicit composition should satisfy more of each project, while code generation contracts toward genuine residual gaps.

## Federated capability knowledge

The long-run model may be federated, but should reuse existing standards and registries rather than invent networking/distribution protocols prematurely:

```text
public/external capability sources
          ↓
organization capability knowledge
          ↓
team / project capability knowledge
          ↓
project-local behavior
```

A capability knowledge layer should eventually let agents reason about semantic identity/version, public interfaces, configuration, dependencies, runtime compatibility, licensing, provenance, tests, evidence, security constraints, known conflicts, rejected fits, and validated compositions.

The network effect is:

```text
real use or rejection
      ↓
evidence
      ↓
better capability binding and composition
      ↓
less bespoke implementation
      ↓
stronger evidence for future decisions
```

## Documentation and navigation

Cross-repo navigation is owned by the [Vision knowledge index](https://github.com/BrianMills2718/vision/blob/main/wiki/index.md). This repository owns local technical truth and exposes it through `docs/README.md`, manifests, code, schemas, tests, decisions, and the proof ledger.

Prefer links over duplicated status prose. Preserve historical proof/session documents with explicit labels rather than rewriting history as though later decisions were known at the time.

## Non-goals

The architecture does not currently aim to create:

- a universal workflow engine;
- a universal form/schema system;
- a universal semantic IR or primitive language;
- a visual graph editor as a source of truth;
- a generic developer portal/service catalog;
- a package registry or marketplace;
- a new MCP/A2A-like transport or agent registry;
- a general authorization, scheduling, messaging, observability, or provenance platform;
- internal replacements for mature runtime/platform/business capabilities merely to increase the apparent size of the capability base.

Frappe is the current runtime substrate, not the durable abstraction boundary.

## Success criterion

The architecture succeeds if the ecosystem **compounds**: later projects require less discovery and bespoke implementation because each completed project leaves behind better capability knowledge, evidence, and reusable behavior where justified—without hiding domain semantics or increasing coupling.

The desired trend is:

- more validated capability/evidence knowledge available to the next project;
- more requirements satisfied by existing suitable implementations, regardless of who owns them;
- fewer unnecessary internal abstractions and duplicate products;
- faster delivery and fewer regressions;
- stronger compatibility and rejection evidence;
- lower marginal effort per new project;
- clearer separation between reusable behavior and legitimately local semantics.

Success is not measured by the number of primitives, internal packages, or lines of shared code.
