# Capability discovery and semantic export seam

The maintained source of truth is the capability manifest plus the capability's real public implementation surface.

Each capability may declare a small `semantic_exports` section that binds a stable semantic action ID to one already-public implementation and its named input/output contract surface. `tools/capability_catalog.py` derives the agent-facing catalog from those manifests.

Ownership:
- the semantic compiler requests behavior by semantic action ID and declares target-neutral payload contracts plus input-source provenance;
- capability manifests own capability identity, maturity/evidence, dependencies, public interfaces, and semantic exports;
- the resolver matches semantic requirements against the manifest-derived catalog;
- `data-contracts` owns typed boundary validation; the provider-resolution critical path may use the minimal graph validator where richer composition semantics are not required;
- runtime adapters execute selected providers and own persistence/effects.

## Source-of-truth rule

Do not maintain capability identity or implementation selection independently in multiple registry formats.

The compatibility document `capability_publication_v1.yaml` and its schema are retained while existing Milestone-1 evidence and consumers are supported, but they are no longer the preferred authoring surface on this subtraction branch. The derived catalog has been proven equivalent for the resolver-critical fields used by the current appointment and Shipment Exception cases.

Generate/inspect the current catalog with:

```bash
python tools/capability_catalog.py list --json
python tools/capability_catalog.py describe state.transition --json
python tools/capability_catalog.py publication --json
```

The final `publication` command exists only as a compatibility view for the current resolver/tests; it is generated from manifests and should not become another hand-maintained source.

## Deterministic resolution

`tools/resolve_behavior_requirements.py` resolves a compiler-owned `BehaviorRequirements v1` document against the manifest-derived catalog by default. It can still accept an explicit legacy publication YAML for compatibility testing.

Compatibility rules are conservative:
1. `semantic_action` must match exactly.
2. Exactly one exported implementation must exist for that action.
3. Every input named by the exported semantic contract must be available in the requirement.
4. Every requirement input carries a target-neutral payload `contract_id` and explicit source (`external` or named prior requirement output).
5. Every output required by the requirement must be provided by the export and carry a payload `contract_id`.
6. Free-text invariants and provenance are preserved but are not treated as machine-verifiable semantic equivalence.

Typed resolver failures include:
- `UNKNOWN_SEMANTIC_ACTION`
- `AMBIGUOUS_PUBLICATION`
- `INPUT_CONTRACT_MISMATCH`
- `INPUT_SOURCE_MISSING`
- `OUTPUT_CONTRACT_MISMATCH`

The resolver emits a provider-bound result containing runtime interface identity, payload contract IDs, explicit input sources, provenance, and invariants. That result is an internal handoff, not a new implementation/discovery protocol.

## Interface policy

Core implementations remain ordinary typed software. CLI is the portable local automation surface; Make targets are thin repository entrypoints; MCP should be added only when standardized AI-client discovery/invocation, managed authorization, remote service boundaries, or cross-client distribution justify it.

A future MCP adapter should derive its tools from the same capability metadata rather than introduce another registry.
