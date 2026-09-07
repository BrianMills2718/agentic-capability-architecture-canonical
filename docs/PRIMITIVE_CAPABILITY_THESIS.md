# Primitive and Capability Thesis

## Hypothesis

A surprisingly large share of agent-built software may be describable as compositions of a relatively small number of configurable, extensible, semantically meaningful primitives, combined into larger evidence-backed capabilities and project-specific compositions.

This is a hypothesis to test, not a settled architecture.

## Primitive vs capability

A **primitive** is a bounded semantic operation with stable execution meaning, such as a state transition or deterministic rule resolution.

A **capability** is higher-order: implementation plus public interface, configuration, dependencies, tests, extension points, compatibility evidence, and maturity.

A **project** composes capabilities and keeps irreducibly local semantics local.

```text
primitive
   ↓
capability
   ↓
project composition
   ↓
domain implementation
```

## Good primitive criteria

A useful primitive should be semantically meaningful, bounded, configurable without hiding consequential behavior, testable independently, composable through typed contracts, explicit about failure/idempotency/effects, and stable across materially different domains.

## Proposed hybrid model

```text
node/port graph
    +
state/action/transition semantics
    +
trigger/event semantics
    +
capability/evidence layer
    +
project-local domain actions
```

Typed ports should express more than JSON compatibility: semantic type, schema/version, cardinality, state expectations, sensitivity/scope, and compatibility constraints where relevant.

State/action/transition semantics are needed because a graph alone does not say whether an action is legal now, who may perform it, whether retries are no-ops, what changed, or how effects are audited.

## Standards and prior art

UML, SysML v2, KerML, BPMN, and ISO/IEC/IEEE 42010 are treated as prior art and possible interchange/viewpoint sources, not presumed runtime kernels.

The current architecture particularly values ISO-42010-style multiple views over one source model: capability, state, composition, deployment, evidence, provenance, security, and agent-planning views can all project the same underlying system.

## Falsification posture

The primitive hypothesis should narrow or fail if prospective projects require constant primitive invention, if typed composition adds no planning/reuse value, if agents do better with ordinary capability APIs, or if supposedly generic primitives repeatedly hide decisive domain semantics.
