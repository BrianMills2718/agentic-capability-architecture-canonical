# Engagement Operating System

This is the minimum operating layer for using the cumulative, composable capability ecosystem on paid/client work without turning the canonical repository into a client-code monorepo or a premature services platform.

## Core boundary

**Client work product stays in the engagement workspace.** The canonical repository supplies reusable background capability knowledge, interfaces, evidence, and operating rules. A contractor may consume that material but does not push client-specific implementation, client source, secrets, or confidential information back into the canonical capability base.

The engagement loop is:

```text
paid task
  ↓
precise ENGAGEMENT.yml
  ↓
read-only capability snapshot
  ↓
CAPABILITY_PLAN.yml: discover → select/reject → compose → local gaps
  ↓
client-local implementation + tests
  ↓
delivery
  ↓
EVIDENCE_PROPOSAL.yml + METRICS.yml
  ↓
sanitize + close
  ↓
CANONICAL_EVIDENCE_PROPOSAL.yml
  ↓
human review / selective promotion
```

Promotion is never automatic. A successful engagement may strengthen evidence for an existing provider, record a rejected fit or compatibility limit, identify behavior that should remain local, or propose a reuse candidate. New shared code is only one possible outcome and still requires the repository's normal evidence/promotion discipline.

## 1. Create the contractor kit

Start with a task file containing the client-visible requirement and acceptance conditions. Generate an isolated workspace:

```bash
python tools/engagement.py new job_001 \
  --task /path/to/TASK.md \
  --output /private/work/job_001 \
  --client-reference internal-alias \
  --external-research \
  --acceptance-command "python -m pytest"
```

The generated kit contains `ENGAGEMENT.yml`, `TASK.md`, `AGENT_RULES.md`, `CAPABILITY_PLAN.yml`, `EVIDENCE_PROPOSAL.yml`, `METRICS.yml`, a hashed read-only `snapshot/` with portable capability metadata/runtime source, and `control/engagement.py` plus its schemas so the contractor can validate the kit without access to the canonical repository.

Before handing the workspace to a contractor, edit `ENGAGEMENT.yml` so the placeholder requirement becomes the smallest useful set of exact requirements and acceptance conditions. If you change the number of requirements, update `METRICS.yml` `requirements_total` to match; validation will reject drift. Avoid client secrets in the engagement metadata itself when an alias/reference is sufficient.

Validate the intake:

```bash
python tools/engagement.py validate /private/work/job_001
```

## 2. Require planning before implementation

The contractor reads `ENGAGEMENT.yml`, `TASK.md`, and the snapshot before coding. `CAPABILITY_PLAN.yml` must record:

- selected providers/capabilities and the requirements they satisfy;
- materially plausible candidates that were rejected and why;
- semantic actions/public interfaces for selected internal capabilities;
- explicit multi-component compositions;
- genuinely client/domain-local residual gaps.

When planning is complete, set `status: ready`. From inside the isolated workspace the contractor can run:

```bash
python control/engagement.py validate . --require-ready
```

The operator can run the same check from the canonical checkout with `python tools/engagement.py validate /private/work/job_001 --require-ready`. If the contractor environment lacks the validator dependencies, install only `control/requirements.txt` in an isolated environment.

Validation rejects unknown internal capabilities/actions/interfaces, unknown requirement IDs, uncovered requirements, invalid compositions, and any modification to the hashed capability snapshot.

## 3. Deliver locally

Implementation files, client tests, credentials, source data, and deployment material live in the engagement workspace/client repository, not here. Use the read-only snapshot through its public interfaces where appropriate. Do not edit shared capability source to make one client job work.

The operator/reviewer runs the engagement's acceptance commands and normal client-specific QA before delivery. The canonical `python tools/check_bootstrap.py` gate still governs any separate proposed change to this repository.

## 4. Record generalized evidence and economics

After delivery, complete `EVIDENCE_PROPOSAL.yml` using generalized statements only:

- successful reuse/composition observations;
- rejected fits;
- compatibility/runtime findings;
- possible capability candidates;
- behavior that should remain local.

`METRICS.yml` stays engagement-local and records the business flywheel: revenue, contractor cost, human/agent hours, requirements reused, requirements composed, local lines changed, and rework events. These fields are deliberately separate from canonical evidence intake.

The main operating questions across the first 5–10 engagements are:

1. Is the percentage of requirements satisfied by existing providers rising?
2. Is the percentage satisfied through composition rising?
3. Is local implementation/rework per comparable job falling?
4. Are human hours and contractor cost per comparable outcome falling?
5. Are gross contribution and delivery reliability improving?

## 5. Sanitize and close

The evidence template starts with both client-content flags set to `true`. A reviewer/contractor must sanitize the evidence and explicitly set both to `false` before closeout. Then run:

```bash
python tools/engagement.py close /private/work/job_001
```

Closeout creates:

- `CANONICAL_EVIDENCE_PROPOSAL.yml` — generalized proposal-only input for human review; it intentionally excludes task text, client reference, client code, and financial metrics;
- `CLOSEOUT_SUMMARY.md` — engagement-local economics and reuse/composition rates.

A human reviewer decides whether to record a reuse observation, update compatibility/evidence metadata, or open a normal capability-promotion change. Never copy client-owned code into the shared base merely because it looks reusable.

## MVP operating posture

For the first engagements, keep the system intentionally manual around sales, hiring, review, and promotion. Do not add a marketplace, billing layer, worker portal, custom orchestration service, or automatic promotion engine until repeated paid work demonstrates the need.

This technical isolation/evidence workflow supports an IP boundary but does not replace appropriate client/contractor agreements or legal review for ownership, confidentiality, and pre-existing/background technology.
