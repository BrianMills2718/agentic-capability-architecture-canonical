# Architecture (code2 format scope)

The repository's architecture authority is [ARCHITECTURE_CHARTER.md](../ARCHITECTURE_CHARTER.md), with [ARCHITECTURE.md](../ARCHITECTURE.md) and [DECISIONS.md](../DECISIONS.md); read those first. This page does not restate them.

Scoped here: [the import model](model.c4) covers one module, `tools.capability_catalog`, which builds the verified semantic-action catalog from capability manifests (`capability_registry.yml`, `capabilities/*/capability.yml`). Its requirement is the [capability-catalog spec](../../openspec/specs/capability-catalog/spec.md). Every other tool, capability, client and the Frappe reference are outside this scope and remain described by the documents above.
