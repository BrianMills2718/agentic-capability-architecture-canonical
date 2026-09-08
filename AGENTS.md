# Agent Operating Rules

These rules apply to coding agents working in this repository.

## Navigation and authority

For cross-repo orientation, start at the [Vision knowledge index](https://github.com/BrianMills2718/vision/blob/main/wiki/index.md) and follow the [Agentic Capability Architecture project guide](https://github.com/BrianMills2718/vision/blob/main/wiki/projects/agentic-capability-architecture.md).

Once working inside this repository, use `docs/README.md` for the local documentation map and authority order. Do not treat dated proof plans, session context, experimental PR descriptions, or historical implementation notes as current architecture when a current decision, manifest, or proof ledger says otherwise.

## Before implementing any feature

First establish what already exists. **Internal reuse is only one candidate source; off-the-shelf wins ties.** Investigate in this order:

1. **Native runtime/platform:** does Frappe, ERPNext, or the selected runtime already provide the behavior?
2. **Installed ecosystem:** is an established plugin/app/package already available in the chosen environment?
3. **Mature external implementation:** is there established OSS or SaaS that should be integrated instead of recreated?
4. **Existing standard/protocol:** are you about to invent a schema, registry, workflow, authorization, messaging, agent, or provenance mechanism already standardized?
5. **Internal capability base:** inspect `capability_registry.yml`, capability manifests, `python tools/capability_catalog.py list --json`, and existing public interfaces for an honest semantic match.
6. **Project-local gap:** only then implement the residual behavior locally. Promote it later only when materially different reuse provides evidence.

Then apply these repository rules:

1. Read `docs/README.md` and the current architecture/decision documents it identifies.
2. Read the relevant capability manifests and public interfaces before relying on registry prose or old proof material.
3. Record meaningful alternatives that were rejected and why when the sourcing decision is not obvious.
4. Prefer configuration over new code.
5. Prefer composition of existing suitable capabilities over adding new behavior.
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

Project count alone is not evidence that the common surface is correct. Failed fits, rejected reuse, incidents, portability limits, and interface churn are also evidence.

## Architecture rules

Keep these layers separate:

```text
requested semantic behavior
        ↓
selected existing capability / public boundary
        ↓
project/client configuration
        ↓
project/client custom extension
        ↓
runtime/platform infrastructure
```

Shared capabilities must not depend on client/project code. Do not use `if client == ...` inside shared capability code.

Prefer explicit interfaces, dependency declarations, configuration schemas, and deterministic rule-resolution semantics over hidden coupling.

A semantic primitive label does not imply that this repository should own a runtime engine for it. Prefer native/runtime/standard infrastructure for execution, persistence, authorization, scheduling, retries, messaging, and observability when those systems satisfy the requirement.

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

Prefer an existing runtime-native trigger before inventing orchestration. The project must include an explicit trigger path, such as:

- Frappe `scheduler_events`,
- a cron/scheduled-job registration,
- a durable delayed-job mechanism,
- a mature workflow/runtime service when its guarantees are required, or
- another framework-native trigger that actually invokes the behavior.

Tests should prove both the business function and the trigger/wiring. A transport adapter like `send_email()` by itself does not satisfy a requirement for scheduled email reminders.

### Idempotent side effects

Scheduled and retryable jobs may run more than once. Any job that causes an external or user-visible side effect—email, SMS, payment, webhook, file delivery, notification, etc.—must be idempotent for the same logical event.

Do not treat a scheduler interval or time-window query as deduplication. Use durable state or a durable idempotency key/unique delivery record so restarts, retries, overlapping windows, concurrent workers, and delayed runs do not repeat the side effect.

When ordering matters, reason explicitly about the transaction boundary between durable state and the external side effect. Prefer established outbox/delivery patterns or runtime guarantees rather than inventing a bespoke reliability mechanism.

Tests must invoke the side-effecting job at least twice for the same eligible logical event and prove the external side effect occurs only once. Where concurrency/crash behavior matters, test or use an infrastructure primitive whose guarantee covers that failure mode.

## Testing rules

Tests are part of the capability, not optional cleanup.

For reusable behavior, prefer:

1. Pure unit tests for business logic.
2. Framework integration tests for hooks/lifecycle behavior.
3. Persistence tests for the final document/database state.
4. Compatibility tests across known consumers when changing a proven/core capability.

Framework/Bench-only tests must still be collectable in the lightweight local bootstrap environment. If a test requires Frappe at import time, use `pytest.importorskip("frappe")` (or otherwise defer the framework import) so `python tools/check_bootstrap.py` can discover the test and skip it locally while real Bench CI executes it.

Every bug fix that reveals a reusable failure mode should leave behind a regression test.

## Knowledge capture

When a project reveals a reusable fact, record it.

Useful reusable assets include:

- semantic requirement/capability identity;
- selected and rejected providers with reasons;
- code and public interfaces;
- tests and compatibility evidence;
- schemas and configuration options;
- integration adapters;
- deployment recipes;
- migration knowledge;
- failure cases and operational incidents;
- architecture decisions;
- agent instructions.

Do not assume future agents will infer an important constraint from old code.

Every project must finish with `clients/<project>/LEARNINGS.md`. Record either:

- a plausible reuse candidate / reusable constraint / integration lesson, or
- an explicit `No promotion candidate yet` assessment with the reason the behavior should remain local.

This requirement is about preserving evidence, not forcing premature abstraction.

## Paid/client engagement isolation

For contractor, agency, or client-paid work, do not put the engagement implementation directly in this canonical repository. Generate an isolated workspace with `python tools/engagement.py new ...`. The snapshot is reusable background capability material; client work product stays local to the engagement.

Before implementation, the worker must make `CAPABILITY_PLAN.yml` ready and explicitly record selected providers, rejected providers, multi-capability composition, and residual local gaps. At closeout, generalized evidence may be proposed only through a sanitized `EVIDENCE_PROPOSAL.yml`; client-confidential material and client-owned code are prohibited from canonical evidence intake. `python tools/engagement.py close ...` produces proposal-only output for human review and never promotes code automatically.

Business metrics (`METRICS.yml`) remain engagement-local. They exist to test whether reuse/composition rates rise and marginal delivery effort falls across materially similar work.

## Change discipline

Before editing a shared capability, answer:

1. What exact requirement is being satisfied?
2. Which native, ecosystem, external, standards-based, and internal alternatives were considered?
3. Who currently uses this capability?
4. Can this be handled through configuration or an existing product/interface instead?
5. Does the change alter an interface or semantic action meaning?
6. Does it introduce a new dependency?
7. What compatibility tests should be added?
8. Is this truly shared behavior, or should it remain local?

Update `docs/DECISIONS.md` when making a repository-local architectural decision that future work should preserve. Update the Vision wiki only when cross-repo navigation/synthesis or a governing program decision changes; do not copy local technical detail into the global navigation layer.

## Completion gate

Before declaring any project complete, run the exact repository-wide command:

```bash
python tools/check_bootstrap.py
```

Targeted tests, syntax checks, package builds, or schema checks are useful during development but do **not** substitute for this final gate. The gate discovers nested app tests and supplies app import paths itself, so do not rely on packages that happen to be installed in your current shell. If the full command fails, the project is not complete.

## Machine-readable workflow helpers

- `python tools/new_project.py <name> --capabilities core,scheduling,...` creates a clean project layer.
- `python tools/record_reuse_candidate.py ...` records a reuse observation without changing shared code.
- `python tools/engagement.py new|validate|close ...` runs the isolated paid/client engagement operating loop.
- `python tools/validate_schemas.py` validates the repository contracts.
- `python tools/capability_catalog.py list --json` lists manifest-derived semantic exports; `describe <action-id> --json` performs exact lookup.
- `python tools/check_reuse_evidence.py` prevents unsupported promotion labels.
