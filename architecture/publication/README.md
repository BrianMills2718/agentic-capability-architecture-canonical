# Maintained capability publication seam

`CapabilityPublication` is the capability-architecture-owned mapping from stable semantic action IDs to reusable provider interfaces.

Ownership:
- the semantic compiler requests behavior by semantic action ID;
- this repository owns provider discovery, maturity/evidence, owner manifests, and selected reusable interfaces;
- `data-contracts` validates typed composition and reachability;
- runtime adapters execute selected providers and own effects.

The canonical publication document is `capability_publication_v1.yaml` and its schema is `capability_publication.schema.json`.

A publication entry must name exactly one capability owner and a selected implementation that is actually listed in that capability's `public_interfaces`.

The generic validator is:

```bash
python tools/validate_capability_publication.py
```

Milestone-1 publication files remain as proof evidence. New integrations should depend on this maintained publication surface instead.
