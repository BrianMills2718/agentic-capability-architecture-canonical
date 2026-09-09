# Next Proof — Capability Flywheel Control Experiment

> **Supersedes the original bootstrap proof plan.** The original real-Frappe lifecycle and bounded fresh-agent acceptance gates have passed. Their evidence is indexed in [`PROOF_LEDGER_EXTENDED.md`](PROOF_LEDGER_EXTENDED.md). The next question is harder: whether accumulated capability knowledge creates measurable advantage beyond a good planning contract.

## Why the proof changed

The existing Shipment Exception fixture under `proof/fresh_agent_registry_discovery/challenge/` is useful for demonstrating the mechanics of a portable snapshot and pre-code composition plan, but its task currently names the shared notification choice, tells the agent not to recreate transition/notification logic, and exposes expected API shapes.

That means a pass primarily demonstrates instruction-following and composition mechanics. It cannot cleanly establish independent capability discovery or a compounding advantage.

Treat that fixture as **guided demo evidence**, not the decisive flywheel experiment.

## The two hypotheses to separate

**H1 — Planning-contract value:** forcing an agent to declare selections, rejections, compositions, interfaces, and local gaps before coding improves implementation quality even with no accumulated internal capability ecosystem.

**H2 — Accumulated-capability value:** giving the same planning discipline access to trustworthy accumulated capability knowledge/interfaces/evidence produces additional measurable improvement on comparable work.

The architecture's distinctive flywheel claim depends on H2 adding value beyond H1.

## Experimental design

Use the same behavior-only task and fresh independent agent sessions across at least two arms:

```text
CONTROL
behavior-only task
+ same planning contract
+ ordinary/blank project context

TREATMENT
same behavior-only task
+ same planning contract
+ capability snapshot / verified interfaces / evidence
```

Do not tell either arm the expected internal capability names, module names, composition, or implementation architecture.

The evaluator may define externally visible behavior and acceptance tests, but the task should not reveal the answer the capability layer is supposed to help discover.

Run multiple fresh sessions per task so one lucky/unlucky agent run is not treated as the result.

## Task-suite requirements

The initial suite should contain several materially different decision shapes:

1. **Real composition task** — two or more existing capabilities genuinely fit and must be composed with local semantics.
2. **Irrelevant-candidate task** — the snapshot includes a plausible but unnecessary capability that a good agent should reject.
3. **No-internal-reuse task** — the honest answer is mostly/project-local implementation.
4. **External/native-better task** — if external research is allowed, the best answer should be a platform/native or mature external provider rather than an internal capability.
5. **Distinctive-invariant task** — at least one task should exercise a capability's actual differentiating semantics (for example genuine multi-rule arbitration) if that capability is being evaluated for maturity.

Do not score “more reuse” as automatically better. Score semantic correctness and unnecessary bespoke work.

## What to measure

Record per run:

- task/evaluator success;
- tests passing on the first implementation attempt;
- agent turns;
- token usage where available;
- wall-clock time;
- human interventions/clarifications;
- bespoke/local lines of code;
- duplicated/reimplemented shared behavior;
- selected and rejected capability accuracy;
- composition accuracy;
- defects/rework;
- evidence quality at closeout.

Also record task identity, agent/model/runtime, exact capability snapshot revision, and a comparable-job classification so results can be interpreted rather than pooled blindly.

## Interpretation

Evidence for the capability flywheel requires the treatment arm to improve meaningful outcomes without hiding cost in extra metadata/review overhead.

A useful result might look like:

```text
same or better correctness
+ fewer duplicated implementations
+ fewer agent/human steps
+ less bespoke code
+ accurate composition/rejection
```

If the planning-contract control performs equally well, that is evidence that the pre-code reasoning discipline is valuable but the accumulated capability layer has not yet justified its additional complexity.

If both arms struggle, improve the task/planning contract before growing the capability base.

If the treatment consistently wins, then the repository has evidence for the main architectural thesis: software functionality can become an accumulated, agent-readable composition substrate that makes later projects easier.

## Integrity prerequisites before interpreting the experiment

Before relying on the result:

- only verified semantic exports should be treated as executable internal actions;
- the exact snapshot revision must be retained;
- machine evidence/maturity claims should not contradict observed consumer behavior;
- evaluator behavior must not be disclosed to the agent;
- tasks must not name the expected capability choices;
- run failures and negative results must be retained rather than discarded.

The experiment should decide what infrastructure to build next. Do not add a generalized planner, marketplace, primitive runtime, or broader capability catalog merely to prepare for a result that has not been observed.
