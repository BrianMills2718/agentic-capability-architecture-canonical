# Bootstrap Acceptance Test

## Goal

Prove that a coding agent can work against the capability base without being
verbally reminded of the architecture.

## Prompt to give a fresh coding agent

> Add a new project called `beta_reference`. It needs appointment scheduling,
> approvals for appointments over 90 minutes, and email reminders. Reuse what
> already exists where possible. Do not change existing project behavior.

Do not add extra architectural instructions to the prompt.

## Pass conditions

The agent should, because of repository context alone:

- read `AGENTS.md`,
- inspect `capability_registry.yml`,
- reuse Scheduling rather than create another appointment system,
- reuse Approvals rather than create a second rule resolver,
- notice Notifications exists and inspect whether it is sufficient,
- create a `beta_reference` manifest,
- keep the 90-minute threshold project-local unless the existing capability
  explicitly supports it as configuration,
- add tests,
- avoid editing ACME-specific code,
- preserve ACME behavior,
- record any candidate reusable learning,
- run local tests and project validation.

## Failure examples

The bootstrap is not done if the agent:

- creates a second Scheduling implementation without checking the registry,
- adds `if project == "beta"` to shared Scheduling,
- copies the approval resolver into the new client,
- weakens existing ACME behavior,
- creates shared abstractions merely because they might be useful someday,
- completes the work without tests or reusable knowledge capture.
