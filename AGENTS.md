# Agent Operating Rules

These rules apply to coding agents working in this repository or in an engagement workspace generated from it.

## Mission

The goal is not to maximize reuse and not to maximize code generation. The goal is to make software delivery increasingly **composition-dominated**:

```text
exact requirement
  -> honest capability identity
  -> verified public boundary
  -> selection / rejection
  -> composition
  -> genuinely local residual
  -> tests and evidence
```

A good result may reuse several capabilities, one capability, an external/platform capability, or none. Semantic fit is necessary but insufficient: select a capability only when its concrete implementation, verification, risk-reduction, compatibility, or repeated-use advantage exceeds its discovery, context, binding, and adaptation cost relative to the smallest viable local implementation. Preserve consequential project/domain behavior locally rather than forcing it into a generic abstraction.

## Machine-readable truth hierarchy

Do not treat every label in the repository as an executable guarantee.

1. **Verified semantic export** — `semantic_exports` resolved by `python tools/capability_catalog.py ...`; this is the strongest current callable action claim.
2. **Public interface** — `public_interfaces` declares a supported boundary; inspect source/tests before assuming semantics beyond a verified export.
3. **Capability scope** — `provides`, configuration, notes, and models help discovery but may be broader than the currently bound executable surface.
4. **Evidence/maturity metadata** — useful only when current and backed by actual use/test evidence.
5. **Prose/history** — context and rationale; never stronger than current code and machine-readable state.

If code and metadata disagree, surface that as a defect. Do not silently invent or infer a callable capability because a broad label sounds applicable.

## Navigation and authority

For cross-repo orientation, start at the [Vision knowledge index](https://github.com/BrianMills2718/vision/blob/main/wiki/index.md) and follow the [Agentic Capability Architecture project guide](https://github.com/BrianMills2718/vision/blob/main/wiki/projects/agentic-capability-architecture.md).

Inside this repository, use `docs/README.md` for the local documentation map and authority order. `TEAM_GUIDE.md` explains the collaborator-facing value proposition; `docs/ARCHITECTURE_CHARTER.md` owns the current local architecture stance.

Do not treat dated proof plans, session context, experimental PR descriptions, or historical implementation notes as current architecture when a current decision, manifest, code boundary, or proof ledger says otherwise.

## Before implementing any feature

Work in this order:

1. **Define the exact behavior.** Separate invariant/domain semantics from incidental implementation details.
2. **Inspect the verified internal action surface.** Run `python tools/capability_catalog.py list --json`; inspect relevant manifests, `semantic_exports`, public interfaces, source, and tests.
3. **Test net value against local implementation.** For each selected capability, name the smallest viable local alternative and the concrete advantage that justifies discovery and integration cost. A semantically correct capability may still be the wrong choice when an equally reliable local implementation is cheaper.
4. **Identify composition.** State which verified behaviors jointly satisfy the requirement and what must remain local.
5. **Reject false or uneconomic fits.** Record materially plausible candidates that do not fit, or do not create net value, and why.
6. **Source missing providers.** For unsatisfied behavior, investigate native/runtime, installed ecosystem, mature external OSS/SaaS, standards/protocols, and internal capabilities. **Off-the-shelf wins ties**, but sourcing is supporting policy rather than the architecture's main value.
7. **Implement only the residual.** If no existing capability honestly fits and creates net value, keep the behavior project-local unless later evidence justifies promotion.
8. **Plan evidence before coding.** State what tests/runtime observation would prove the composition works and what result would falsify the reuse hypothesis.

Then apply these repository rules:

- Prefer configuration and composition over new shared code when semantics already fit.
- Never put client-specific behavior directly into a shared capability.
- If behavior is unique to one project, keep it in that project's `custom/` layer.
- If behavior appears reusable, record it as a candidate; do not automatically promote it.
- Shared behavior must have tests before it is treated as reusable.
- Record plausible reusable behavior in `reuse_candidates.yml` rather than promoting it immediately.
- Every completed project MUST include `clients/<project>/LEARNINGS.md` with a reuse assessment. If nothing should be promoted, say so and explain why.
- Preserve compatibility with existing consumers unless a breaking change is explicit.

## Reuse lifecycle

Use these states:

- `local` — used by one project only.
- `candidate` — suspected to be reusable, but not demonstrated.
- `proven` — used successfully by at least two materially different projects **with the generalized behavior actually exercised**.
- `core` — mature, broadly relied upon capability.

Do not promote something merely because it looks generic or because several projects import the package.

A useful default review sequence is:

- First use: keep it local.
- Second materially different use: candidate/proven review.
- Third use: explicit compatibility/composability test.

Project count alone is not evidence that the common surface is correct. Failed fits, rejected reuse, incidents, portability limits, interface churn, and cases where a client only uses a trivial subset are also evidence. If a capability's distinctive invariants are not exercised by consumers, record that as negative/insufficient promotion evidence rather than inflating maturity.

## Architecture rules

The durable target is:

```text
requested semantic behavior
        ↓
verified capability boundaries
        ↓
composition/configuration
        ↓
project-local residual semantics
        ↓
runtime/platform infrastructure
        ↓
real-use evidence
```

Shared capabilities must not depend on client/project code. Do not use `if client == ...` inside shared capability code.

Prefer explicit interfaces, dependency declarations, configuration schemas, and deterministic semantics over hidden coupling.

A semantic primitive label does not imply that this repository should own a runtime engine for it. Prefer native/runtime/standard infrastructure for execution, persistence, authorization, scheduling, retries, messaging, and observability when those systems satisfy the requirement.

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

## Knowledge capture

Useful reusable assets include:

- semantic requirement/capability identity;
- selected and rejected providers with reasons;
- verified public interfaces and code;
- tests and compatibility evidence;
- schemas/configuration;
- integration adapters;
- deployment recipes;
- migration knowledge;
- failure cases and incidents;
- architecture decisions;
- agent instructions.

Do not assume future agents will infer an important constraint from old code.

Every project must finish with `clients/<project>/LEARNINGS.md`. Record either a plausible reuse candidate/reusable constraint/integration lesson or an explicit `No promotion candidate yet` assessment.

This requirement preserves evidence; it does not force abstraction.

## Paid/client engagement workflow

For contractor, agency, or client-paid work, do not put the engagement implementation directly in this canonical repository. Generate an isolated workspace with `python tools/engagement.py new ...`. Client work product stays local to the engagement.

Before implementation, the worker must make `CAPABILITY_PLAN.yml` ready and explicitly record selected providers, each selection's smallest viable local alternative and net-value reason, rejected providers, composition, exact internal exports/interfaces, and residual local gaps.

For internal selections, treat only verified semantic exports/public interfaces as executable boundaries. A broad `provides` label is not enough.

At closeout, generalized evidence may be proposed through `EVIDENCE_PROPOSAL.yml`; client-confidential material and client-owned code are prohibited from canonical evidence intake. `python tools/engagement.py close ...` produces proposal-only output for human review and never promotes code automatically.

### Current trust boundary

The engagement tooling is a **planning and evidence discipline for a cooperative worker**, not an adversarial sandbox/security product.

- The snapshot checksum and validator are shipped in the same workspace. They detect ordinary changes relative to that shipped state, but a malicious worker who controls both can re-attest modified content.
- The self-check validates contracts and declared internal exports/interfaces; it does not prove exhaustive provider research or detect every semantic reimplementation.
- Evidence “sanitization” is a human-reviewed declaration. The tool does not automatically redact credentials, confidential text, or client-owned code from free-text fields.

Do not describe these controls more strongly than they are.

Business metrics (`METRICS.yml`) remain engagement-local. They exist to test whether reuse/composition rates rise and marginal delivery effort falls across materially similar work; there is not yet a canonical cohort time series proving that claim.

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

## Completion gate

Before declaring any project complete, run:

```bash
python tools/check_bootstrap.py
```

Targeted tests, syntax checks, package builds, or schema checks are useful during development but do **not** substitute for this final gate. If the full command fails, the project is not complete.

## Machine-readable workflow helpers

- `python tools/capability_catalog.py list --json` — list verified manifest-derived semantic exports.
- `python tools/capability_catalog.py describe <action-id> --json` — exact action lookup.
- `python tools/capability_catalog.py check` — validate export integrity.
- `python tools/new_project.py <name> --capabilities core,scheduling,...` — create a clean project layer.
- `python tools/record_reuse_candidate.py ...` — record a reuse observation without changing shared code.
- `python tools/engagement.py new|validate|close ...` — run the paid/client planning/evidence loop.
- `python tools/validate_schemas.py` — validate repository contracts.
- `python tools/check_reuse_evidence.py` — enforce configured promotion thresholds for promoted statuses; do not infer broader evidence quality from a pass.
