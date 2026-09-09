# Try the Working Capability System

This repository is not only an architecture document. It contains a working capability registry, reusable capability implementations, project examples, validation/proof tooling, and a paid-engagement operating system that creates isolated contractor/agent workspaces.

The quickest way to understand the system is to generate one engagement and inspect what it gives the worker.

## Prerequisites

- Python 3.11+
- Git
- access to this private GitHub repository

Create an isolated Python environment and install the two dependencies used by the engagement controller:

```bash
python -m venv .venv
. .venv/bin/activate            # Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install 'PyYAML>=6,<7' 'jsonschema>=4,<5'
```

## 1. Inspect the capability ecosystem

```bash
python tools/capability_catalog.py list --json
python tools/capability_catalog.py describe state.transition.plan --json
```

The current catalog is derived from capability manifests and points semantic actions to real public interfaces.

## 2. Generate a real engagement kit

The repository already contains a Shipment Exception task that makes a useful demonstration because it needs state-transition behavior, notification behavior, idempotency, and project-local semantics.

From the repository root:

```bash
python tools/engagement.py new colleague_demo \
  --task proof/fresh_agent_registry_discovery/challenge/TASK.md \
  --output ../colleague_demo
```

Validate the generated workspace:

```bash
python tools/engagement.py validate ../colleague_demo
```

You should see:

```text
OK: engagement contracts, snapshot integrity, and capability plan are valid
```

## 3. Open the generated workspace

The new `../colleague_demo/` directory contains:

```text
TASK.md
ENGAGEMENT.yml
AGENT_RULES.md
CAPABILITY_PLAN.yml
EVIDENCE_PROPOSAL.yml
METRICS.yml
control/engagement.py
control/requirements.txt
snapshot/capability_registry.yml
snapshot/SHA256SUMS
snapshot/metadata/...
snapshot/vendor/...
```

The important point is that the worker receives a portable, hashed snapshot of available capability knowledge and runtime source instead of being told to start from a blank repository.

`CAPABILITY_PLAN.yml` starts in `draft` state. Before implementation, the worker must inspect the task and snapshot and record:

- selected capabilities/providers;
- relevant rejected candidates and reasons;
- exact public interfaces/actions being consumed;
- explicit compositions;
- genuine project-local residual gaps.

## 4. Give the workspace to a coding agent

Open `../colleague_demo` as the coding agent's working directory and tell it:

> Implement `TASK.md` and follow `AGENT_RULES.md` exactly. Complete `CAPABILITY_PLAN.yml` before implementation. Do not modify the capability snapshot.

The agent can validate its own plan without access to the source repository:

```bash
python control/engagement.py validate . --require-ready
```

That self-contained validation rejects unknown capabilities/interfaces, uncovered requirements, invalid compositions, and snapshot tampering.

## 5. What this demonstrates

The demonstration is meant to show the operating thesis, not merely generate files:

```text
requirement
  -> discover available capability knowledge
  -> select / reject
  -> compose through declared interfaces
  -> implement only the residual local behavior
  -> test the result
  -> record generalized evidence
```

Client/project implementation remains outside this canonical capability repository. The same engagement controller is intended for real paid work, where `METRICS.yml` records delivery economics and `EVIDENCE_PROPOSAL.yml` captures sanitized reusable learning.

## 6. Full repository validation

For maintainers or anyone who wants to verify the complete repository rather than only the engagement controller:

```bash
python tools/check_bootstrap.py
```

That includes documentation/schema/registry checks, capability/project validation, Frappe package builds, and the repository test suite. Some Frappe lifecycle tests intentionally require a real Bench test site and are skipped in the lightweight local environment.

## What this does not prove yet

This proves a working technical mechanism and bounded architecture/proof fixtures. It does **not** yet prove that a commercial services business will achieve increasing reuse, lower marginal delivery cost, or product-market fit. That is the purpose of the paid-engagement pilot tracked separately in `BrianMills2718/capability-services`.
