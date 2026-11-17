# Agent implementation rules

Moved word for word from the root [AGENTS.md](../AGENTS.md) on 2026-11-17 to keep the root under the 12,000-byte instruction cap. These rules bind every agent working in this repository or an engagement workspace generated from it.

## Business-rule composition

When multiple rules can affect the same outcome:

- Rules should return decisions/facts rather than directly overwrite each other.
- Use explicit priorities when rules are allowed to compete.
- Use explicit conflicts when combinations are undefined or unsafe.
- Equal-priority disagreement should fail deterministically.
- Critical shared requirements must not be silently weakened by project-specific extensions.

Do not claim client reuse has validated multi-rule arbitration if every consumer passes only one rule. Tests of the shared package prove the implementation invariant; client evidence must prove that a real consumer needed/exercised it.

## Triggered behavior completeness

When a requirement describes behavior that must happen **later or automatically**—for example reminders, scheduled syncs, retries, expirations, or periodic reports—a callable helper is not a complete implementation.

Prefer an existing runtime-native trigger before inventing orchestration. The project must include an explicit trigger path, such as Frappe `scheduler_events`, cron/scheduled-job registration, a durable delayed-job mechanism, or another runtime mechanism that actually invokes the behavior.

Tests should prove both the business function and the trigger/wiring. A transport adapter like `send_email()` by itself does not satisfy a requirement for scheduled email reminders.

### Idempotent side effects

Scheduled and retryable jobs may run more than once. Any job that causes an external or user-visible side effect—email, SMS, payment, webhook, file delivery, notification, etc.—must be idempotent for the same logical event.

Do not treat a scheduler interval or time-window query as deduplication. Use durable state or a durable idempotency key/unique delivery record so restarts, retries, overlapping windows, concurrent workers, and delayed runs do not repeat the side effect.

When ordering matters, reason explicitly about the transaction boundary between durable state and the external side effect. Prefer established outbox/delivery patterns or runtime guarantees rather than inventing a bespoke reliability mechanism.

Tests must invoke the side-effecting job at least twice for the same eligible logical event and prove the external side effect occurs only once. Where concurrency/crash behavior matters, test it or use an infrastructure primitive whose guarantee covers that failure mode.

## Testing and evidence rules

Tests are part of the capability, not optional cleanup.

For reusable behavior, prefer:

1. pure unit tests for business logic;
2. framework integration tests for hooks/lifecycle behavior;
3. persistence tests for final state;
4. compatibility tests across known consumers when changing a proven/core capability;
5. negative-control tests for validators/gates—deliberately introduce the defect the gate claims to prevent and assert that it turns red.

Framework/Bench-only tests must still be collectable in the lightweight local bootstrap environment. If a test requires Frappe at import time, use `pytest.importorskip("frappe")` or otherwise defer the framework import.

Every bug fix that reveals a reusable failure mode should leave behind a regression test.

A green check proves only the invariant that check actually tests. Do not convert structural validity into a broader semantic or maturity claim.

## Change discipline

Before editing a shared capability, answer:

1. What exact requirement is being satisfied?
2. What verified capability/interface currently owns related behavior?
3. Which native, ecosystem, external, standards-based, and internal alternatives were considered?
4. Who currently uses this capability, and which distinctive invariants do those consumers actually exercise?
5. Can configuration/composition solve it without changing shared code?
6. Does the change alter an interface or semantic action meaning?
7. Does it introduce a new dependency?
8. What compatibility and negative-control tests should be added?
9. Is this truly shared behavior, or should it remain local?

Update `docs/DECISIONS.md` when making a repository-local architectural decision that future work should preserve. Update the Vision wiki only when cross-repo navigation/synthesis or a governing program decision changes.

