# Try the Working Capability System

This repository is not only an architecture document. It contains a working capability registry, audited semantic exports, reusable capability implementations, project examples, validation/proof tooling, and an engagement workflow that creates portable contractor/agent workspaces.

If you want the conceptual explanation first, read [`TEAM_GUIDE.md`](TEAM_GUIDE.md). If you want to see the mechanics, continue here.

## What you should understand by the end

The important behavior is not “the agent found a library.” You should be able to see an agent:

1. inspect machine-readable capability knowledge;
2. distinguish verified executable exports from broader capability scope;
3. select and reject capabilities explicitly;
4. compose more than one capability when appropriate;
5. keep consequential task/domain behavior local;
6. leave tests and evidence that can improve the next project.

That is the capability flywheel this repository is testing.

## Important demo caveat

The included Shipment Exception task is currently a **guided mechanics demonstration**. Its task text names expected transition/notification behavior and therefore is **not** a clean experiment proving that an agent independently discovered the best composition.

Use it to understand the engagement/capability workflow. Do not cite a successful run as evidence that the accumulated capability system beats a blank/control repository. The controlled fresh-agent experiment remains separate work.

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

## 1. Inspect the verified executable capability surface

```bash
python tools/capability_catalog.py list --json
python tools/capability_catalog.py describe state.transition.plan --json
python tools/capability_catalog.py check
```

The semantic catalog is the strongest current machine-readable callable claim. In capability manifests:

- `semantic_exports` means an action is intentionally bound to a public implementation boundary;
- `public_interfaces` declares public surfaces;
- `provides` is broader capability-scope metadata and is **not by itself a callable guarantee**.

If you are evaluating agent behavior, verify that the agent respects that distinction.

## 2. Generate an engagement kit

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
OK: engagement contracts, snapshot checksum consistency, and capability plan are valid
```

“Snapshot checksum consistency” means the snapshot still matches the checksum file shipped in the same workspace under the expected cooperative workflow. It is **not** an adversarial attestation boundary because the worker receives the checksum and validator too.

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

The worker receives a portable snapshot of capability metadata and runtime source instead of being told to start from a blank repository. The portable registry also copies each capability's `semantic_exports` and `public_interfaces` so the agent can see the strongest executable boundaries without inferring them from broad scope labels.

`CAPABILITY_PLAN.yml` starts in `draft` state. Before implementation, the worker should record:

- selected providers/capabilities;
- the smallest viable local alternative for each selection and the concrete net advantage of consuming the capability;
- materially plausible rejected candidates and reasons;
- exact verified semantic actions/public interfaces being consumed;
- explicit multi-component compositions;
- genuine project-local residual gaps.

A plan with little or no reuse can be correct if the capability system does not honestly fit or if an equally reliable local implementation is cheaper. The point is to make that boundary explicit, not to force reuse.

## 4. Give the workspace to a coding agent

Open `../colleague_demo` as the coding agent's working directory and give it this instruction:

> Read `TASK.md`, `AGENT_RULES.md`, `snapshot/capability_registry.yml`, and relevant `snapshot/metadata/*` before coding. Treat only verified semantic exports as callable action guarantees. Complete `CAPABILITY_PLAN.yml` first: state what you selected, the smallest viable local alternative and net advantage for each selection, what you rejected, what you are composing, and what must stay local. Do not maximize reuse for its own sake. Then implement the task, run tests, and leave generalized evidence that would help the next agent.

The agent can run the self-check:

```bash
python control/engagement.py validate . --require-ready
```

That check is a planning/schema conformance tool for a cooperative worker. It is not a sandbox and it does not prove that the worker exhaustively searched every provider or avoided every possible reimplementation.

## 5. Review the agent's composition reasoning

Before looking at the code, inspect `CAPABILITY_PLAN.yml` and ask:

- Did the agent use exact verified exports/interfaces rather than infer functions from broad labels?
- Did each selected capability provide a concrete advantage over the smallest equally reliable local implementation after discovery and integration cost?
- Did it reject irrelevant capabilities instead of selecting everything available?
- Did it identify a real composition when multiple capabilities jointly satisfy the requirement?
- Did it keep task-specific timing, recipients, persistence, authorization, schema, and other consequential semantics local where appropriate?
- Did the plan make the boundary clear enough that implementation mostly follows from it?

That review is more important than the raw number of reused functions.

## 6. What the mechanism is intended to demonstrate

```text
requirement
  -> capability identity
  -> verified boundary
  -> select / reject
  -> compose
  -> implement residual local behavior
  -> test
  -> record success/failure/compatibility evidence
  -> improve the next composition decision
```

The same engagement workflow is intended for paid work, where `METRICS.yml` records delivery economics and `EVIDENCE_PROPOSAL.yml` records proposed generalized learning. Evidence sanitization remains a human-reviewed declaration; the current tool does not automatically redact secrets or client-owned code.

See [`docs/ENGAGEMENT_OPERATING_SYSTEM.md`](docs/ENGAGEMENT_OPERATING_SYSTEM.md) for the exact trust boundary and closeout posture.

## 7. Full repository validation

For maintainers or anyone who wants to verify the complete repository rather than only the engagement controller:

```bash
python tools/check_bootstrap.py
```

That includes documentation/schema/registry checks, capability/project validation, Frappe package builds, and the repository test suite. Some Frappe lifecycle tests intentionally require a real Bench test site and are skipped in the lightweight local environment.

## What this does not prove yet

This demonstrates a working technical mechanism and bounded proof fixtures. It does **not** yet prove the key economic/productivity claim.

The decisive next experiment is a controlled comparison across fresh sessions and comparable tasks: planning contract alone versus planning contract plus accumulated capability snapshot. Measure success, first-pass tests, turns/tokens/time, human intervention, bespoke code, duplication, rework, and composition accuracy.

The separate startup/business hypothesis is tracked in `BrianMills2718/capability-services`.
