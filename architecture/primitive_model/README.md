# Experimental Primitive Composition Model

This directory is a bounded experiment, not a new production runtime.

It asks whether the real projects, including a prospective Service Desk test can be represented from one small
machine-readable model combining:

- typed nodes and ports;
- explicit state models and transitions;
- triggers;
- primitive/capability/local-action nodes;
- implementation adapters;
- evidence links;
- deployment/isolation information;
- explicit local semantics and known gaps.

The experiment intentionally permits `local_action` nodes. A model that can only succeed by
renaming every domain-specific behavior as a generic primitive would be evidence against the
hypothesis rather than evidence for it.

Files:

- `primitive_registry.yml` — candidate primitive vocabulary.
- `primitive_model.schema.json` — structural schema.
- `projects/*.yml` — current models of the real projects.
- `prospective_snapshots/service_desk_preimplementation.yml` — exact Service Desk model before implementation.
- `../../tools/validate_primitive_models.py` — semantic validator.
- `../../tools/render_primitive_views.py` — generates multiple views from the same source.
- `../../docs/PRIMITIVE_MODEL_EXPERIMENT_RESULT.md` — evaluation and conclusions.

## Prospective Service Desk result

Service Desk was the first project whose model was authored before implementation. It
validated with 15 nodes, 12 typed edges, 7 transitions, no local-action nodes, and no new
primitive vocabulary.

The model exposed that `state.transition` was incorrectly owned by Approvals. The canonical
implementation moved to `na_core.transitions`, with `na_approvals.transitions` retained as a
compatibility re-export. Six-site Frappe run `34044617169` passed all consumers.

This strengthens the model as an **agent planning and architecture** layer, but it remains
experimental rather than an executable universal graph runtime.
