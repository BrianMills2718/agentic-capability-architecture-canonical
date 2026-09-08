# Bootstrap Acceptance Test

> **Status: historical bootstrap fixture.** This test was designed to prove that a fresh agent could discover and reuse the repository's original internal capability base without conversational coaching. It is preserved as evidence of that bootstrap, not as the current general build-versus-buy test. The original acceptance later passed; see [`PROOF_LEDGER_EXTENDED.md`](PROOF_LEDGER_EXTENDED.md). Current sourcing policy is defined in `AGENTS.md` / `PROJECT_WORKFLOW.md`, and the remaining isolated registry-discovery proof is defined in [`NEXT_PROOF.md`](NEXT_PROOF.md).

## Goal at the time

Prove that a coding agent can work against the capability base without being verbally reminded of the architecture.

## Prompt given to a fresh coding agent

> Add a new project called `beta_reference`. It needs appointment scheduling,
> approvals for appointments over 90 minutes, and email reminders. Reuse what
> already exists where possible. Do not change existing project behavior.

No extra architectural instructions were added to the prompt.

## Historical pass conditions

The agent was expected, because of repository context alone, to:

- read `AGENTS.md`;
- inspect `capability_registry.yml`;
- reuse Scheduling rather than create another appointment system;
- reuse Approvals rather than create a second rule resolver;
- notice Notifications exists and inspect whether it is sufficient;
- create a `beta_reference` manifest;
- keep the 90-minute threshold project-local unless the existing capability explicitly supports it as configuration;
- add tests;
- avoid editing ACME-specific code;
- preserve ACME behavior;
- record any candidate reusable learning;
- run local tests and project validation.

## Historical failure examples

The bootstrap was not complete if the agent:

- created a second Scheduling implementation without checking the registry;
- added `if project == "beta"` to shared Scheduling;
- copied the approval resolver into the new client;
- weakened existing ACME behavior;
- created shared abstractions merely because they might be useful someday;
- completed the work without tests or reusable knowledge capture.

## Current interpretation

This test remains useful for understanding how the repository's agent instructions evolved, but its forced internal-provider choices should not be generalized. A current agent should first ask whether the required scheduling, approval, notification, or other behavior already exists in the selected runtime/platform, ecosystem, mature external software, or a standard interface before preferring an internal implementation.
