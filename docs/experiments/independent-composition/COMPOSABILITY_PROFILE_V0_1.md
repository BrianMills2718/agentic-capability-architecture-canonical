# Minimal composability profile v0.1

Status: P2 contract candidate for ACA-PLAN-001.
Purpose: define the smallest information an independently authored capability should expose so a fresh coding agent can compose it without requiring an ACA-specific runtime.

This is a **profile over existing interfaces**, not a new transport, workflow language, registry, or ontology.

## Required surface

A capability is composition-ready for this pilot when the consumer can determine all of the following from its normal published interface, documentation, examples, and tests.

### 1. Invocation

- stable capability/interface identifier or stable published operation name;
- exact version/revision used by the composition;
- runnable invocation boundary;
- required authentication/connection mechanism, without embedding secrets.

Use the provider's native interface: MCP tool, OpenAPI operation, n8n sub-workflow, normal library function, service API, etc.

### 2. Structural contract

- machine-readable input shape;
- machine-readable output shape;
- required versus optional values;
- null/missing-value behavior where material.

Prefer the provider's existing JSON Schema/OpenAPI/MCP/native typed contract. ACA does not define a second schema.

### 3. Meaning needed for correct adaptation

Document only semantics that a reasonable fresh consumer could otherwise confuse, for example:

- units/currency;
- identifier namespace and tenant/account scope;
- time zone/time basis;
- cardinality/order;
- role meaning;
- whether a value is observed, predicted, requested, approved, or completed;
- information-loss constraints.

Ordinary field descriptions/examples are preferred. Linguistic Core or richer semantic annotations are **not required** unless an observed failure demonstrates that ordinary descriptions are insufficient.

### 4. Effects and operational constraints

For side-effecting or retryable operations, expose the material facts needed by a consumer:

- read-only versus state-changing;
- destructive or irreversible behavior where applicable;
- idempotency/retry expectation;
- authorization or human-approval requirement;
- important preconditions;
- externally visible effects.

Reuse native platform/MCP/OpenAPI/runtime metadata where it is sufficient. Do not create a universal effect ontology for the pilot.

### 5. Examples

At least one realistic positive example for a non-trivial capability.

Add a negative or edge example when silent misuse is plausible, such as:

- cents vs dollars;
- customer ID vs account ID;
- requested vs completed event;
- cross-tenant identifier;
- duplicate side effect.

### 6. Independent conformance

A retained capability must pass a consumer-side test showing that a fresh consumer can invoke it without importing the original product's private code or relying on private session state.

Adapters are allowed.

## Adapter rule

Generated adapters are expected and are **not a failure**.

An adapter may:

- rename/restructure fields;
- convert documented units/formats;
- perform deterministic validation;
- call an explicit lookup capability;
- preserve/propagate required metadata.

An adapter must not silently invent:

- identity;
- consent/authorization;
- missing evidence;
- units;
- business-state transitions;
- guarantees the provider does not make.

If the required mapping cannot be justified from published information or an explicit lookup, composition must fail/reject.

## Conformance checks for the pilot

The consumer/evaluator should test:

1. interface can be invoked at the pinned version;
2. positive example passes;
3. ordinary structural adapter passes;
4. one relevant semantic mismatch is either correctly adapted or rejected;
5. one side-effect/retry safety case behaves as declared;
6. original product-private implementation is not required by the second consumer.

## Explicit non-requirements

This profile does not require:

- an ACA capability registry;
- a shared base class;
- MCP;
- n8n;
- Arazzo;
- Linguistic Core identifiers;
- Semantic Foundry records;
- a universal workflow or effect language.

Those may be used when they already fit or if a later observed failure justifies them.

## Promotion rule

Do not add a new mandatory field to this profile because it seems theoretically useful.

Add one only when:

1. an authentic independent-composition run fails or incurs material recurring cost;
2. the failure is reproducible;
3. ordinary docs/examples/generated adapters or provider-native metadata do not solve it cheaply;
4. the added field/check measurably fixes the named failure.

This keeps ACA small by construction.