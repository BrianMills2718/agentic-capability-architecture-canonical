# Maintained capability publication seam

`CapabilityPublication` is the capability-architecture-owned mapping from stable semantic action IDs to reusable provider interfaces.

Ownership:
- the semantic compiler requests behavior by semantic action ID and declares target-neutral payload contracts plus input-source provenance;
- this repository owns provider discovery, maturity/evidence, owner manifests, selected reusable interfaces, and versioned opaque composition implementation identities;
- `data-contracts` lowers provider resolution into `ActionPack`/`CompiledManifest` and validates typed composition and reachability;
- runtime adapters execute selected providers and own effects.

The canonical publication document is `capability_publication_v1.yaml` and its schema is `capability_publication.schema.json`.

A publication entry must name exactly one capability owner, a selected implementation actually listed in that capability's `public_interfaces`, and a valid versioned `composition_implementation_ref` for the composition layer.

## Deterministic resolution

`tools/resolve_behavior_requirements.py` resolves a compiler-owned `BehaviorRequirements v1` document against the publication. It is intentionally not a planner.

Compatibility rules are conservative:
1. `semantic_action` must match exactly.
2. Exactly one publication entry must exist for that action.
3. Every input named by the published semantic contract must be available in the requirement.
4. Every requirement input must carry a target-neutral payload `contract_id` and explicit source (`external` or named prior requirement output).
5. Every output required by the requirement must be provided by the published semantic contract and carry a payload `contract_id`.
6. Free-text invariants and provenance are preserved but are not treated as machine-verifiable semantic equivalence.

Typed resolver failures include:
- `UNKNOWN_SEMANTIC_ACTION`
- `AMBIGUOUS_PUBLICATION`
- `INPUT_CONTRACT_MISMATCH`
- `INPUT_SOURCE_MISSING`
- `OUTPUT_CONTRACT_MISMATCH`

The resolver emits `Provider Resolution Result v1`, including runtime interface identity, versioned composition implementation identity, payload contract IDs, explicit input sources, provenance, and invariants. It does not execute providers.

## One-command pre-execution gate

When the maintained `data-contracts` package containing the provider-resolution adapter is installed, run:

```bash
python tools/run_behavior_pipeline.py path/to/behavior_requirements.yaml \
  --resolution-output /tmp/provider_resolution.yaml
```

That command performs provider resolution and then invokes `data-contracts` lowering/reachability validation. It does not invoke runtime implementations.

`data-contracts` treats only inputs marked `external` as initial seeds. Inputs declared as `requirement_output` must resolve to the named producer output with the exact same payload contract ID; missing producers, bad output names, contract mismatches, and dependency cycles fail before execution.

Maintained local validation commands are:

```bash
python tools/validate_capability_publication.py
python -m pytest -q tests/compatibility/test_behavior_requirement_resolution.py
```

Milestone-1 publication files remain as proof evidence. New integrations should depend on this maintained publication surface instead.
