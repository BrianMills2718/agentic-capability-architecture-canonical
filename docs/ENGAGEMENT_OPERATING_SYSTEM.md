# Engagement Operating System

This is the minimum operating layer for applying the cumulative, composable capability architecture to paid/client work without turning the canonical repository into a client-code monorepo or a premature services platform.

Its strongest current value is **structured planning and evidence capture**: the worker must make the capability/composition/local-gap boundary explicit before implementation, then leave generalized evidence after delivery.

## Core boundary

**Client work product stays in the engagement workspace.** The canonical repository supplies reusable background capability knowledge, public interfaces, evidence, and operating rules. A contractor may consume that material but does not push client-specific implementation, client source, secrets, or confidential information back into the canonical capability base.

The engagement loop is:

```text
paid task
  ↓
precise ENGAGEMENT.yml
  ↓
operator-generated capability snapshot
  ↓
CAPABILITY_PLAN.yml: discover → select/reject → compose → local gaps
  ↓
client-local implementation + tests
  ↓
delivery
  ↓
EVIDENCE_PROPOSAL.yml + METRICS.yml
  ↓
human sanitization review + close
  ↓
CANONICAL_EVIDENCE_PROPOSAL.yml
  ↓
human review / selective promotion
```

Promotion is never automatic. A successful engagement may strengthen evidence for an existing provider, record a rejected fit or compatibility limit, identify behavior that should remain local, or propose a reuse candidate. New shared code is only one possible outcome and still requires the repository's normal evidence/promotion discipline.

## Current trust boundary

This tooling is a **planning/evidence discipline for a cooperative worker**, not an adversarial sandbox or security product.

- The generated snapshot is intended to be treated as read-only by the worker.
- `SHA256SUMS` and the validator are shipped inside the same workspace. Validation detects ordinary changes relative to that shipped checksum, but a malicious worker who controls both the content and attestation can re-hash modified content. Do not describe the self-check as tamper-proof isolation.
- `control/engagement.py` validates the worker's contracts and declared internal exports/interfaces. It does not prove exhaustive provider research and cannot detect every semantic reimplementation in arbitrary returned code.
- Evidence sanitization is a human-reviewed declaration. The tool does not automatically redact credentials, contract identifiers, confidential prose, or client-owned code from free-text evidence fields.
- The client/IP boundary still depends on appropriate repository permissions, operational process, contracts, and human review.

These limitations are deliberate MVP boundaries. If adversarial contractor verification becomes necessary, the operator should retain independent snapshot/schema digests or signatures outside the worker workspace and add operator-side returned-work verification.

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

The generated kit contains `ENGAGEMENT.yml`, `TASK.md`, `AGENT_RULES.md`, `CAPABILITY_PLAN.yml`, `EVIDENCE_PROPOSAL.yml`, `METRICS.yml`, a portable capability snapshot with metadata/runtime source, and `control/engagement.py` plus its schemas so the contractor can run the planning checks without access to the canonical repository.

New workspaces use capability-plan schema version 2. Existing frozen workspaces retain their shipped validator and version-1 schema; to migrate one intentionally, set `CAPABILITY_PLAN.yml` to version 2 and add `local_alternative` to every selected item.

Before handing the workspace to a contractor, edit `ENGAGEMENT.yml` so the placeholder requirement becomes the smallest useful set of exact requirements and acceptance conditions. If you change the number of requirements, update `METRICS.yml` `requirements_total` to match; validation will reject drift. Avoid client secrets in engagement metadata when an alias/reference is sufficient.

Validate the intake:

```bash
python tools/engagement.py validate /private/work/job_001
```

## 2. Require composition planning before implementation

The contractor reads `ENGAGEMENT.yml`, `TASK.md`, the snapshot registry, and relevant capability metadata before coding. `CAPABILITY_PLAN.yml` must record:

- selected providers/capabilities and the requirements they satisfy;
- the smallest viable local alternative for each selection and why the selected capability creates concrete net value after discovery and integration cost;
- materially plausible candidates that were rejected and why;
- verified semantic actions/public interfaces for selected internal capabilities;
- explicit multi-component compositions;
- genuinely client/domain-local residual gaps.

For internal code, `semantic_exports` are the strongest executable action claim. A broad `provides` label is useful discovery metadata but is not sufficient evidence that a callable action exists.

When planning is complete, set `status: ready`. From inside the workspace the contractor can run:

```bash
python control/engagement.py validate . --require-ready
```

The operator can run the same check from the canonical checkout with:

```bash
python tools/engagement.py validate /private/work/job_001 --require-ready
```

The check validates schemas, requirement coverage, known internal capability/export/interface references, composition membership, and cooperative-workflow snapshot consistency. A pass does **not** prove that reuse was optimal; a correct plan may honestly conclude that behavior remains local.

## 3. Deliver locally

Implementation files, client tests, credentials, source data, and deployment material live in the engagement workspace/client repository, not here. Use snapshot public interfaces where they honestly fit. Do not edit shared capability source merely to make one client job work.

The operator/reviewer runs the engagement's acceptance commands and normal client-specific QA before delivery. The canonical `python tools/check_bootstrap.py` gate still governs any separate proposed change to this repository.

## 4. Record generalized evidence and economics

After delivery, complete `EVIDENCE_PROPOSAL.yml` using generalized statements only:

- successful reuse/composition observations;
- rejected fits;
- compatibility/runtime findings;
- possible capability candidates;
- behavior that should remain local.

`METRICS.yml` stays engagement-local and records revenue, contractor cost, human/agent hours, requirements reused, requirements composed, local lines changed, and rework events.

The main operating questions across a future comparable cohort are:

1. Is the percentage of requirements satisfied by validated composition rising?
2. Is local implementation/rework per comparable job falling?
3. Are human hours and contractor cost per comparable outcome falling?
4. Are gross contribution and delivery reliability improving?
5. Are agent selection/rejection/composition decisions becoming more accurate with accumulated evidence?

There is not yet a canonical cross-engagement time series proving these trends. The metrics contracts make the claim measurable; they do not establish it.

## 5. Human-review sanitization and closeout

The evidence template starts with both client-content flags set to `true`. A reviewer/contractor must inspect the free-text evidence, remove client-confidential/client-owned content, and explicitly set both to `false` before closeout.

Then run:

```bash
python tools/engagement.py close /private/work/job_001
```

Closeout creates:

- `CANONICAL_EVIDENCE_PROPOSAL.yml` — proposal-only generalized input for human review; it omits the task text, client reference, client code files, and financial metrics by construction, but copied free-text evidence still depends on human sanitization;
- `CLOSEOUT_SUMMARY.md` — engagement-local economics and reuse/composition rates.

A human reviewer decides whether to record a reuse observation, update compatibility/evidence metadata, or open a normal capability-promotion change. Never copy client-owned code into the shared base merely because it looks reusable.

## MVP operating posture

For the first engagements, keep the system intentionally manual around sales, hiring, review, evidence acceptance, and promotion. Do not add a marketplace, billing layer, worker portal, custom orchestration service, or automatic promotion engine until repeated paid work demonstrates the need.

This workflow supports an operational IP boundary but does not replace client/contractor agreements, access control, confidentiality procedures, or legal review for ownership and pre-existing/background technology.
