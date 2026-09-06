# Agent Operating Rules

These rules apply to coding agents working in this repository.

## Before implementing any feature

1. Read `docs/WORKING_CONTEXT.md`.
2. Read `capability_registry.yml`.
3. Search existing capabilities for the requested behavior.
4. Prefer configuration over new code.
5. Prefer composition of existing capabilities over adding new behavior.
6. Never put client-specific behavior directly into a shared capability.
7. If behavior is unique to one project, put it in that project's `custom/` layer.
8. If behavior appears reusable, mark it as a candidate; do not automatically promote it.
9. Shared behavior must have tests before it is treated as reusable.
10. Record plausible reusable behavior in `reuse_candidates.yml` rather than promoting it immediately.
11. Every completed project MUST include `clients/<project>/LEARNINGS.md` with a reuse assessment. If nothing should be promoted yet, say so explicitly and explain why. Silence is not a reuse assessment.
12. Preserve compatibility with existing consumers unless a breaking change is explicit.

## Reuse lifecycle

Use these states:

- `local` — used by one project only.
- `candidate` — suspected to be reusable, but not demonstrated.
- `proven` — used successfully by at least two materially different projects.
- `core` — mature, broadly relied upon capability.

Do not promote something merely because it looks generic.

A useful default test for promotion is:

- First use: keep it local.
- Second materially different use: extract or mark as candidate/proven.
- Third use: treat as a compatibility/composability test.

## Architecture rules

Keep these layers separate:

```text
shared capability
        ↓
project/client configuration
        ↓
project/client custom extension
```

Do not use `if client == ...` inside shared capability code.

Prefer explicit interfaces, dependency declarations, configuration schemas, and rule-resolution semantics over hidden coupling.

## Business-rule composition

When multiple rules can affect the same outcome:

- Rules should return decisions/facts rather than directly overwrite each other.
- Use explicit priorities when rules are allowed to compete.
- Use explicit conflicts when combinations are undefined or unsafe.
- Equal-priority disagreement should fail deterministically.
- Critical shared requirements must not be silently weakened by project-specific extensions.

Example decisions:

- `ALLOW`
- `REQUIRE_APPROVAL`
- `BLOCK`

## Triggered behavior completeness

When a requirement describes behavior that must happen **later or automatically**—for example reminders, scheduled syncs, retries, expirations, or periodic reports—a callable helper is not a complete implementation.

The project must include an explicit trigger path, such as:

- Frappe `scheduler_events`,
- a cron/scheduled-job registration,
- a durable delayed-job mechanism, or
- another framework-native trigger that actually invokes the behavior.

Tests should prove both the business function and the trigger/wiring. A transport adapter like `send_email()` by itself does not satisfy a requirement for scheduled email reminders.

## Testing rules

Tests are part of the capability, not optional cleanup.

For reusable behavior, prefer:

1. Pure unit tests for business logic.
2. Framework integration tests for Frappe hooks/lifecycle behavior.
3. Persistence tests for the final document/database state.
4. Compatibility tests across known consumers when changing a proven/core capability.

Every bug fix that reveals a reusable failure mode should leave behind a regression test.

## Knowledge capture

When a project reveals a reusable fact, record it.

Useful reusable assets include:

- Code
- Tests
- Schemas
- Configuration options
- Interfaces
- Integration adapters
- Deployment recipes
- Migration knowledge
- Failure cases
- Architecture decisions
- Agent instructions

Do not assume future agents will infer an important constraint from old code.

Every project must finish with `clients/<project>/LEARNINGS.md`. Record either:

- a plausible reuse candidate / reusable constraint / integration lesson, or
- an explicit `No promotion candidate yet` assessment with the reason the behavior should remain local.

This requirement is about preserving evidence, not forcing premature abstraction.

## Change discipline

Before editing a shared capability, answer:

1. Who currently uses this?
2. Can this be handled through configuration instead?
3. Does the change alter an interface?
4. Does it introduce a new dependency?
5. What compatibility tests should be added?
6. Is this truly shared behavior, or should it remain local?

Update `docs/DECISIONS.md` when making an architectural decision that future work should preserve.

## Machine-readable workflow helpers

- `python tools/new_project.py <name> --capabilities core,scheduling,...` creates a clean project layer.
- `python tools/record_reuse_candidate.py ...` records a reuse observation without changing shared code.
- `python tools/validate_schemas.py` validates the repository contracts.
- `python tools/check_reuse_evidence.py` prevents unsupported promotion labels.
