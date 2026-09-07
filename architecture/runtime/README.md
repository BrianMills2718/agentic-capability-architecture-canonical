# Runtime adapter boundary

This layer consumes an already-resolved, composition-validated provider sequence. It does not discover capabilities, reinterpret semantic actions, or replace selected providers.

For each step a runtime adapter may:
1. materialize runtime/provider arguments from validated payloads;
2. invoke the selected public provider interface;
3. normalize provider outputs back to declared payload contracts;
4. persist or delegate external effects where the runtime owns them;
5. emit a `Runtime Execution Receipt v1` preserving requirement and source provenance.

The adapter must not silently substitute a different provider or convert a provider failure into semantic success. Persistence, authorization, transactions, and external-effect guarantees remain runtime/domain responsibilities unless explicitly provided by the selected capability contract.

`runtime_execution.schema.json` defines the portable receipt shape. The first proof is intentionally appointment-specific and exercises the actual approval resolver, transition planner, and notification sender with only the external Frappe mail boundary substituted.
