# Agent Operating Rules

## Current operating direction - 2026-09-22

Apply ACA through the [Agentic Engineering System](https://github.com/BrianMills2718/agentic-engineering-system-canonical) engineering
workflow, not as a parallel platform-building or benchmarking programme.
[ADR-018](docs/DECISIONS.md#adr-018--apply-aca-through-aes-product-engineering)
owns this local disposition; the [AES integration change](https://github.com/BrianMills2718/agentic-engineering-system-canonical/blob/d65df4a6df2015dc345f2cd04c0d6ce003df59c4/docs/decisions/0009-modular-product-design-without-parallel-aca-platform.md)
records the counterpart design policy and existing provider ownership.

Adopt a sufficient existing product/framework and its native modules first.
Keep cohesive reusable behavior behind clean boundaries, put product-specific
variation in configuration/policies, accept thin consumer adapters, and use
normal package/API publication and product/compatibility tests. Framework
independence and a new abstraction for every function are not required.

Do not resume standalone ACA experiments, create demo products, or build new
runtime/catalog/connector/semantic machinery from historical plans. A new
experiment or mechanism needs separate explicit authorization for a concrete
product decision or blocker. Ordinary testing, maintenance, and recovery of
already-produced evidence remain allowed. Existing capability code, manifests,
consumer compatibility, and evidence authority remain here; nothing is archived,
transferred, or promoted by this instruction. Company Planning and Enforced
Planning retain design and execution-governance ownership in AES.

This current direction takes precedence over older experiment-start instructions
below or in linked plans. Preserve those records without turning them into a
mandatory work queue.

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

## Rules kept in docs pages (read when the task touches them)

| When you are about to | Read |
| --- | --- |
| combine business rules, build scheduled/retryable or side-effecting behavior, write tests, or edit a shared capability | [docs/AGENT_IMPLEMENTATION_RULES.md](docs/AGENT_IMPLEMENTATION_RULES.md) (business-rule composition, triggered behavior completeness and idempotent side effects, testing and evidence rules, change discipline) |
| finish a project, record learnings, or do paid/client engagement work | [docs/AGENT_ENGAGEMENT_RULES.md](docs/AGENT_ENGAGEMENT_RULES.md) (knowledge capture, paid/client engagement workflow and its current trust boundary) |

## Before implementing any feature

Work in this order:

1. **Define the exact behavior.** Separate invariant/domain semantics from incidental implementation details.
2. **Inspect the verified internal action surface.** Run `python tools/capability_catalog.py list --json`; inspect relevant manifests, `semantic_exports`, public interfaces, source, and tests.
3. **Test net value against local implementation.** For each selected capability, name the smallest viable local alternative and the concrete advantage that justifies discovery and integration cost. A semantically correct capability may still be the wrong choice when an equally reliable local implementation is cheaper.
4. **Identify composition.** State which verified behaviors jointly satisfy the requirement and what must remain local.
5. **Reject false or uneconomic fits.** Record materially plausible candidates that do not fit, or do not create net value, and why.
6. **Source missing providers.** For unsatisfied behavior, investigate native/runtime, installed ecosystem, mature external OSS/SaaS, standards/protocols, and internal capabilities. **Off-the-shelf wins ties**, but sourcing is supporting policy rather than the architecture's main value.
7. **Implement only the residual.** If no existing capability honestly fits and creates net value, keep the behavior project-local unless later evidence justifies promotion.
8. **Plan product verification before coding.** Specify acceptance, configuration, error/effect, and existing-consumer compatibility checks for the actual change. A/B testing the value of modular architecture is not a delivery prerequisite.

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
