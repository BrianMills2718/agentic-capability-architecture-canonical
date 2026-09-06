# Agent Rules

1. Read `AGENTS.md` and `capability_registry.yml` before making project changes.
2. Create `CAPABILITY_PLAN.yml` before implementation files are written.
3. Reuse shared capabilities first; do not modify shared code for a single project's rule.
4. Keep project-specific business logic in the project's `custom/` layer.
5. Use the approval resolver and notification adapters rather than duplicating decision logic.
6. Write tests that validate the business rule and the orchestration path.
7. Record learning in `clients/<project>/LEARNINGS.md` before the project is considered complete.
8. Finish with `python tools/check_bootstrap.py`.
