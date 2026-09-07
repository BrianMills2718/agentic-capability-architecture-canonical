# Maintained capability publication seam

`CapabilityPublication` is the capability-architecture-owned mapping from stable semantic action IDs to reusable provider interfaces.

Ownership:
- the semantic compiler requests behavior by semantic action ID;
- this repository owns provider discovery, maturity/evidence, owner manifests, and selected reusable interfaces;
- `data-contracts` validates typed composition and reachability;
- runtime adapters execute selected providers and own effects.

The canonical publication document is `capability_publication_v1.yaml` and its schema is `capability_publication.schema.json`.

A publication entry must name exactly one capability owner and a selected implementation that is actually listed in that capability's `public_interfaces`.

## Deterministic resolution

`tools/resolve_behavior_requirements.py` resolves a compiler-owned `BehaviorRequirements v1` document against the publication. It is intentionally not a planner.

Compatibility rules are conservative:
1. `semantic_action` must match exactly.
2. Exactly one publication entry must exist for that action.
3. Every input named by the published semantic contract must be available in the requirement.
4. Every output required by the requirement must be provided by the published semantic contract.
5. Free-text invariants and provenance are preserved in the resolution result but are not treated as machine-verifiable semantic equivalence.

Typed failures:
- `UNKNOWN_SEMANTIC_ACTION`
- `AMBIGUOUS_PUBLICATION`
- `INPUT_CONTRACT_MISMATCH`
- `OUTPUT_CONTRACT_MISMATCH`

Publication integrity failures, such as an implementation not appearing in its owner manifest, are rejected separately by `tools/validate_capability_publication.py` before resolution.

The resolver emits provider-bound records containing the requirement ID, semantic action, capability owner, selected implementation, owner manifest, provenance, and requirement invariants. It does not execute providers.

The maintained validation commands are:

```bash
python tools/validate_capability_publication.py
python -m pytest -q tests/compatibility/test_behavior_requirement_resolution.py
```

Milestone-1 publication files remain as proof evidence. New integrations should depend on this maintained publication surface instead.
