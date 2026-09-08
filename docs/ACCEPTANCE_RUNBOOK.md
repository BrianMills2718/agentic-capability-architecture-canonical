# Fresh-Agent Acceptance Runbook

> **Status: historical bootstrap fixture.** This runbook preserves the exact `beta_reference` acceptance procedure that hardened the original capability-first bootstrap. That acceptance has since passed; current proof status is in [`PROOF_LEDGER_EXTENDED.md`](PROOF_LEDGER_EXTENDED.md). Do not treat this task's forced reuse of internal Scheduling/Approvals/Notifications as the current general sourcing policy. Current agents must follow `AGENTS.md` / `PROJECT_WORKFLOW.md`, including native/platform, ecosystem, external, standards, internal, then local-gap sourcing. The remaining separate registry-discovery research question is described in [`NEXT_PROOF.md`](NEXT_PROOF.md).

This is the exact procedure for the original bootstrap acceptance test.

## What this test proves

A fresh coding agent should be able to enter the repository with no conversation history,
read the repository's normal instructions, reuse the existing capability base, isolate
project-specific behavior, test its work, and leave existing consumers unchanged.

The task is deliberately solvable without changing shared Scheduling, Approvals, or
Notifications runtime.

## Inputs

You need exactly two things:

1. `fresh_agent_acceptance_sandbox.zip` — give/extract this for the coding agent.
2. The control repository or `acceptance_test_control.zip` — keep this OUTSIDE the
   agent's workspace and use it only after the agent finishes.

Do not give the fresh agent this runbook, the evaluator, or the acceptance baselines.

## Fresh-agent prompt

The only user task to give the agent is:

> Add a new project called `beta_reference`. It needs appointment scheduling, approvals for appointments over 90 minutes, and email reminders. Reuse what already exists where possible. Do not change existing project behavior.

The same text is stored as `ACCEPTANCE_PROMPT.txt` inside the sandbox.

## Recommended run: Codex CLI

### macOS / Linux

```bash
rm -rf ~/capability-acceptance-run
mkdir -p ~/capability-acceptance-run
unzip fresh_agent_acceptance_sandbox.zip -d ~/capability-acceptance-run

cd ~/capability-acceptance-run/fresh_agent_acceptance_sandbox

git status --short
# Expected: no output

codex exec --ephemeral --sandbox workspace-write -C . - < ACCEPTANCE_PROMPT.txt
```

Do not append extra architectural instructions. Do not resume an old agent thread.

### Windows PowerShell

```powershell
$Run = "$HOME\capability-acceptance-run"
Remove-Item -Recurse -Force $Run -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Path $Run | Out-Null
Expand-Archive -Path .\fresh_agent_acceptance_sandbox.zip -DestinationPath $Run

Set-Location "$Run\fresh_agent_acceptance_sandbox"

git status --short
# Expected: no output

Get-Content -Raw .\ACCEPTANCE_PROMPT.txt | codex exec --ephemeral --sandbox workspace-write -C . -
```

If your installed Codex version has a Windows sandbox regression, use a normal fresh
interactive Codex session rooted at this directory and paste the exact prompt instead.
The acceptance criterion is freshness of the agent context and reliance on repository
instructions, not a particular CLI transport.

## Using another coding agent

Start a brand-new agent session with its working directory set to the extracted
`fresh_agent_acceptance_sandbox` directory. Paste ONLY the contents of
`ACCEPTANCE_PROMPT.txt` as the task. Do not attach this runbook or evaluator.

The agent must be allowed to read/write the sandbox and run the repository's local tests.

## After the agent finishes

First inspect what changed:

```bash
cd ~/capability-acceptance-run/fresh_agent_acceptance_sandbox
git status --short
git diff --stat
git diff
```

Then run the automated evaluator from OUTSIDE the sandbox.

### If you kept the full control repository

From the control repository:

```bash
python tools/evaluate_acceptance.py ~/capability-acceptance-run/fresh_agent_acceptance_sandbox
```

### If you use the standalone control ZIP

Extract `acceptance_test_control.zip`, then:

```bash
python acceptance_test_control/evaluate_acceptance.py ~/capability-acceptance-run/fresh_agent_acceptance_sandbox
```

On Windows PowerShell:

```powershell
python .\acceptance_test_control\evaluate_acceptance.py "$HOME\capability-acceptance-run\fresh_agent_acceptance_sandbox"
```

## Automated pass conditions

The evaluator requires the fresh agent to:

- create `clients/beta_reference/manifest.yml`;
- reuse `core`, `scheduling`, `approvals`, and `notifications`;
- isolate Beta-specific behavior in a project extension;
- encode the 90-minute rule locally;
- actually use the shared approval resolver;
- actually use the shared email notification capability;
- implement visible reminder scheduling/behavior;
- leave shared Scheduling/Approvals/Notifications runtime byte-for-byte unchanged;
- avoid duplicating the shared Appointment model or approval resolver;
- add Beta-specific tests;
- record a reusable learning/candidate note;
- preserve the existing ACME reference behavior;
- pass registry/project validation and the local test suite.

## Human review

An automated pass is necessary but not sufficient. Review `git diff` and confirm:

- the implementation is understandable and minimal;
- the 90-minute rule is genuinely project-specific;
- email reminders are actually wired rather than merely mentioned;
- no unnecessary framework abstraction was introduced;
- the agent followed the repository's reuse lifecycle;
- existing behavior remains intact.

## Pass/fail

**PASS:** evaluator passes AND human review passes.

**FAIL:** either one fails.

If it fails, preserve the failed sandbox. A failure is useful evidence about which
repository instructions, schemas, tests, or tooling need to become stronger.
