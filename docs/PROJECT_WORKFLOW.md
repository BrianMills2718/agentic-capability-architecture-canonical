# Project Workflow

This is the repeatable workflow a coding agent should use for every new project.

For global orientation, begin at the [Vision knowledge index](https://github.com/BrianMills2718/vision/blob/main/wiki/index.md). For repository-local authority, use [`README.md`](README.md) in this directory.

## 1. Understand the requirement

Translate the request into exact behavior, constraints, data, authorization, temporal/reliability needs, and consequential domain semantics before writing code.

Do not start by naming an internal capability. Start by stating the requirement independently of implementation.

## 2. Source before building

For each required behavior, investigate in this order:

1. **Native runtime/platform** — Frappe, ERPNext, or the selected runtime.
2. **Installed ecosystem** — established apps/plugins/packages already available in the environment.
3. **Mature external implementation** — established OSS or SaaS that should be integrated rather than recreated.
4. **Existing standard/protocol** — avoid inventing a schema, registry, workflow, authorization, messaging, agent, or provenance mechanism already standardized.
5. **Internal capability base** — inspect capability manifests, `capability_registry.yml`, real public interfaces, and relevant compatibility evidence.
6. **Residual local gap** — implement only what remains genuinely unmet.

When alternatives are materially plausible, record the important rejected candidates and why they do not fit. The goal is not to maximize internal reuse; it is to select the best existing implementation that honestly satisfies the requirement.

## 3. Classify each requirement

Classify each requested behavior as one of:

- **configure existing** — native/external/internal behavior already fits through configuration;
- **consume existing** — use an existing public capability/service interface directly;
- **compose existing** — combine multiple existing behaviors;
- **adapt existing** — a thin adapter is required for a real interface/runtime translation;
- **local extension** — genuinely project-specific residual behavior;
- **candidate capability** — new behavior that may later prove reusable.

A proof fixture that happens to implement a business capability is not automatically the preferred production provider if the runtime/ecosystem already has a mature implementation.

## 4. Create the project manifest first

Before implementation, create `clients/<project>/manifest.yml` declaring the internal capabilities the project intends to use.

Validate it:

```bash
python tools/validate_project.py clients/<project>/manifest.yml
```

The project manifest currently covers internal registered capability composition. External/native sourcing decisions that materially affect future work should be recorded in project planning/learnings until a dedicated machine-readable sourcing contract is justified.

## 5. Implement the smallest missing behavior

Do not modify a shared capability merely to satisfy one project's unusual rule.

Prefer:

```text
existing platform / package / service / capability
      +
project configuration
      +
small local extension
```

over a forked, duplicated, or speculative shared implementation.

Use existing typed public interfaces when they already express the correct boundary. Add wrappers only for real translation needs.

## 6. Use established runtime guarantees

Persistence, authorization, scheduling, retries, transactions, messaging, observability, package distribution, and similar infrastructure should use established runtime/platform mechanisms where they satisfy the required invariant.

A semantic label such as `notification.email.send`, `state.transition.plan`, or `actor.authorize` does not imply this repository should own an execution platform for that concern.

## 7. Test at the right layers

- Pure unit tests for rules/algorithms.
- Framework integration tests for Frappe hooks and lifecycle behavior.
- Persistence tests when final database state matters.
- Compatibility tests when shared behavior changes.
- For reminders, scheduled syncs, retries, expirations, or other automatic behavior, test the trigger/wiring as well as the callable function. A helper that can send a reminder is not enough unless something actually schedules or invokes it.
- Any scheduled/retryable external side effect must use durable idempotency/reliability appropriate to the failure mode. Run the job twice for the same logical event and assert the side effect happens once; where concurrency/crash behavior matters, use or test a mechanism that covers that failure mode. A time window alone is not deduplication.

## 8. Record learning and sourcing evidence

Every project must create `clients/<project>/LEARNINGS.md` before it is complete.

Record either:

- a reusable constraint, failure mode, integration pattern, sourcing lesson, rejected option, or candidate abstraction, or
- `No promotion candidate yet`, with a short explanation of why the new behavior should remain local.

This makes the reuse decision reviewable without forcing first-use code into the shared layer.

## 9. Promotion review

Do not promote on first use.

- first use → local,
- second materially different use → candidate/proven review,
- third use → explicit compatibility/composability test,
- mature/broadly depended upon → core.

Project count alone is insufficient. Consider domain/runtime diversity, interface stability, failed/rejected fits, independent consumers, security/operational evidence, and whether extraction actually reduces coupling.

## 10. Finish with validation

Run the exact repository-wide gate:

```bash
python tools/check_bootstrap.py
```

Targeted checks do not substitute for this command. A project is not complete until the full gate passes, and it is not complete if it works only by weakening or bypassing existing shared contracts.
