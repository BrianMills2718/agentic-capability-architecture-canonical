# Upwork ATS Capability Experiment — Preliminary Result

**Status:** preliminary controlled experiment, `n=1` fresh Codex run per arm. Not proof of a general capability-layer advantage.

## Market source

On 2026-09-08 we selected a live public Upwork project as market-grounded pressure rather than inventing another architecture fixture:

- **Applicant Tracking System AI Automation**
- public listing: `https://www.upwork.com/freelance-jobs/apply/Applicant-Tracking-System-Automation_~022097067318014895521/`
- observed budget: $8,000 fixed price
- observed scope included candidate pipeline stages, appointment booking, overlap/double-booking prevention, reminder email, and post-appointment workflow.

The experiment used only a bounded behavior slice. It did **not** attempt to implement the full ATS, UI, email-deliverability infrastructure, deployment, CV intake, SMS, or integrations.

## Question

> Does the accumulated capability snapshot help a genuinely fresh coding agent implement the same behavior with less bespoke implementation than the same pre-code planning contract with no accumulated internal capabilities?

A second question emerged during the run:

> When real task pressure exposes a missing capability binding, can we strengthen capability knowledge without adding shared implementation, and does the next fresh agent then compose more of the task?

## Behavior-only task

Both arms received the same task and no capability-name hints. The slice required:

- `Applied -> Booked -> Attended` lifecycle behavior;
- actor/recipient validation;
- active appointment overlap prevention;
- idempotent already-booked/already-attended behavior;
- one booking confirmation after a successful booking;
- 24-hour and 2-hour reminder checks with duplicate suppression;
- no network dependency in tests;
- ATS-specific stages, timing, recipient choice, and record shape kept local.

The domain API was specified, but no internal package, semantic action, module path, or expected capability choice was named.

## Method

- Runner: Codex CLI `0.153.4`, fresh ephemeral sessions.
- Same prompt for every arm.
- Same `TASK.md`, `AGENT_RULES.md`, engagement schemas, and pre-code `CAPABILITY_PLAN.yml` contract.
- No web search or outside repositories.
- A hidden 11-test evaluator lived outside every agent workspace.
- Runs were sequential to prevent cross-workspace/concurrent-writer contamination.
- Control: identical engagement shape with an empty internal capability snapshot.
- Treatment v1: canonical snapshot before the availability export was published.
- Treatment v2: same task after the experiment caused us to publish the already-existing pure availability implementation as the verified `availability.query` boundary.

An earlier harness attempt was discarded because stale child Codex processes created concurrent writers. None of its results are included here.

## Results

All three final implementations passed the **same hidden evaluator: 11/11**.

| Measure | Control | Treatment v1 | Treatment v2 |
|---|---:|---:|---:|
| Hidden acceptance | 11/11 | 11/11 | 11/11 |
| Wall time | 242.85 s | 192.28 s | 185.27 s |
| Codex input tokens | 237,346 | 244,920 | 267,289 |
| Codex cached input tokens | 207,360 | 214,272 | 226,048 |
| Codex output tokens | 7,248 | 5,558 | 5,203 |
| Workflow source lines | 129 | 95 | 101 |
| Workflow AST statements | 76 | 57 | 52 |
| Workflow branch nodes | 20 | 12 | 11 |
| Agent-authored test lines | 221 | 163 | 143 |
| Workflow + test lines | 350 | 258 | 244 |
| Internal capabilities selected | 0 | 1 (`core`) | 2 (`core`, `scheduling`) |
| Explicit multi-component composition | no internal composition | `core` + native datetime | `core` + `scheduling` + native datetime |

Relative to control, treatment v2 was about **23.7% faster**, emitted **28.2% fewer output tokens**, used **31.6% fewer workflow AST statements**, **45% fewer branch nodes**, and authored **30.3% fewer workflow+test lines**.

However, treatment v2 consumed **12.6% more input tokens** and about **11.4% more total input+output tokens** than control. The current capability snapshot therefore has a real context/discovery cost; this experiment does not support a claim that the capability layer is token-cheaper overall.

## What the first treatment discovered

Treatment v1 selected `state.transition.plan` from Core and reused it for the ATS lifecycle.

It **rejected Scheduling** even though the runtime already contained a reusable pure availability implementation. That rejection was correct: Scheduling advertised broader `provides` labels but did not expose `availability.query` through a verified semantic export/public interface.

It also rejected `notification.email.send` because the current adapter imports Frappe while the task required a framework-neutral injected callback.

This was useful negative evidence. The task revealed a capability-knowledge defect, not a need for more scheduling code.

## Flywheel iteration

We made the smallest evidence-backed change:

- no new scheduling implementation;
- bound existing `availability.query` to `na_scheduling.availability.is_available`;
- declared `TimeWindow` / `find_conflicts` as supporting public interfaces;
- kept appointment lifecycle labels explicitly non-executable;
- clarified that portable workers should import vendored packages through their declared package names, not `snapshot.vendor...` layout paths.

A new fresh treatment then independently selected both:

- `state.transition.plan`
- `availability.query`

and used the declared public imports:

```python
from na_core.transitions import TransitionSpec, plan_transition
from na_scheduling.availability import TimeWindow, is_available
```

That is the most important result in this experiment: **real task pressure improved capability knowledge, and the next fresh agent consumed the stronger boundary without changing the task.**

## What this does not prove

This is one small slice and one run per arm. It does not establish statistical significance, commercial compounding, or superiority across job families/models.

Important limitations:

- one Codex sample per arm;
- model nondeterminism and sequential-run effects remain possible;
- the source Upwork job is much larger than the tested slice;
- no real client repository, credentials, deployment, UI, deliverability, or production operations were exercised;
- the capability snapshot increased input/context cost;
- v2 raw workflow line count was slightly higher than v1 even though statement/branch/test counts fell further;
- the notification capability remained a rejected fit, so this was not a three-capability composition.

## Next experiment

Replicate rather than broaden the architecture prematurely:

1. run at least 5 fresh sessions per arm for this same task;
2. repeat on 2–3 materially different current job families;
3. run the same matrix with a second coding-agent model (for example Claude Code);
4. report medians/distributions for success, wall time, input/output tokens, bespoke code, rework, and capability-selection accuracy;
5. test whether a smaller discovery-first snapshot/catalog can retain the code/time benefit while reducing input-token overhead.

Do not count a successful guided demo as this evidence. The task must remain behavior-only and the evaluator must remain outside the agent workspace during each run.
