# Project Workflow

This is the repeatable workflow a coding agent should use for every new project.

## 1. Understand the requirement

Translate the request into business capabilities and constraints before writing code.

## 2. Inspect the existing base

Read:

- `AGENTS.md`
- `capability_registry.yml`
- relevant capability manifests and READMEs
- known compatibility tests

## 3. Classify each requirement

For each requested behavior, classify it as one of:

- **reuse** — already provided by a capability,
- **configure** — existing capability supports it through settings,
- **compose** — combine multiple existing capabilities,
- **local extension** — genuinely project-specific new behavior,
- **candidate capability** — new behavior that may later prove reusable.

## 4. Create the project manifest first

Before implementation, create `clients/<project>/manifest.yml` declaring the capabilities the project intends to use.

Validate it:

```bash
python tools/validate_project.py clients/<project>/manifest.yml
```

## 5. Implement the smallest missing behavior

Do not modify a shared capability merely to satisfy one project's unusual rule.

Prefer:

```text
shared capability
      +
project configuration
      +
small local extension
```

over a forked or duplicated capability.

## 6. Test at the right layers

- Pure unit tests for rules/algorithms.
- Framework integration tests for Frappe hooks and lifecycle behavior.
- Persistence tests when final database state matters.
- Compatibility tests when shared behavior changes.
- For reminders, scheduled syncs, retries, expirations, or other automatic behavior, test the trigger/wiring as well as the callable function. A helper that can send a reminder is not enough unless something actually schedules or invokes it.

## 7. Record learning

Every project must create `clients/<project>/LEARNINGS.md` before it is complete.

Record either:

- a reusable constraint, failure mode, integration pattern, or candidate abstraction, or
- `No promotion candidate yet`, with a short explanation of why the new behavior should remain local.

This makes the reuse decision reviewable without forcing first-use code into the shared layer.

## 8. Promotion review

Do not promote on first use.

- first use → local,
- second materially different use → candidate/proven review,
- third use → explicit compatibility/composability test,
- mature/broadly depended upon → core.

## 9. Finish with validation

Run:

```bash
python tools/check_bootstrap.py
```

A project is not complete if it works only by weakening or bypassing existing shared contracts.
