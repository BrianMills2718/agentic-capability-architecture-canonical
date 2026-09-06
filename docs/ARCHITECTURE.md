# Architecture

## Layers

### 1. Shared capabilities

Reusable code with:

- explicit purpose,
- public interface,
- configuration schema,
- dependency declarations,
- tests,
- compatibility expectations.

### 2. Project/client configuration

Settings that change shared behavior without forking shared code.

### 3. Project/client custom extension

Behavior unique to one project.

Custom extensions may depend on shared capabilities but should not modify their source directly.

## Desired dependency direction

```text
client custom code
       ↓
shared capabilities
       ↓
core/runtime
```

Shared capabilities should not depend on client/project code.

## Composition rule

Prefer explicit APIs/contracts over one capability reaching into another capability's internals.

## Rule engine pattern

For competing business rules:

```text
framework hook
      ↓
dispatcher
      ↓
rule evaluations
      ↓
deterministic resolver
      ↓
single final mutation
```

Rules report decisions. The resolver owns final state changes.

## Compatibility

A change to a proven or core capability should be treated as potentially affecting every known consumer.

Compatibility tests should be added when:

- interfaces change,
- dependencies change,
- configuration semantics change,
- rule precedence changes,
- migrations alter stored data,
- framework lifecycle hooks change.
