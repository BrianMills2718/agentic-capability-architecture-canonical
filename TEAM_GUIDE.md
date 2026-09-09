# Team Guide: Why Point an Agent at This Repository?

This is the shortest explanation for collaborators who want to understand what the repository is for before reading the research history.

## The 30-second version

Most coding-agent workflows start each project with a requirement plus whatever happens to be in that project's repository. The agent then rediscovers interfaces, rewrites familiar behavior, and leaves most of what it learned trapped in that project.

This repository tests a different operating model:

> **Make useful software behavior persistent and legible to agents as typed capabilities, let agents compose those capabilities before writing new code, keep genuinely domain-specific behavior local, and feed real-use evidence back so the next project starts from a stronger capability system.**

The goal is not to maximize reuse. The goal is to maximize **correct composition** while shrinking bespoke implementation toward the genuinely novel residual.

## Why this is relevant to your coding agent

When you point an agent at this repository, the agent should gain more than source code. It gets an explicit decision surface for answering:

1. What reusable behavior is actually available?
2. Which behavior has a verified executable interface?
3. Which capabilities fit this requirement, and which should be rejected?
4. Which capabilities should be composed together?
5. What must remain project-local because it carries real domain meaning?
6. What evidence from this project should improve the next agent's decision?

The intended loop is:

```text
requirement
  -> capability identity
  -> verified public boundary
  -> selection / rejection
  -> composition
  -> project-local residual
  -> tests and real-use evidence
  -> stronger capability knowledge
  -> next project starts ahead
```

That loop is the main value proposition.

## What is actually differentiated here?

The individual ingredients are not novel by themselves. Reusing libraries, preferring mature software, typed APIs, registries, CI, package managers, and build-vs-buy decisions are all established software practice.

The differentiated hypothesis is the **combination and operating discipline**:

- semantic capability identities that are independent of one project;
- machine-readable manifests and verified executable exports for agent discovery;
- typed public boundaries that can be bound without copying implementation details into each project;
- an explicit pre-code capability plan covering selections, rejections, compositions, and local gaps;
- project-local semantics treated as a first-class outcome rather than a failure to abstract;
- every project acting as both a consumer of prior capability knowledge and a contributor of new evidence;
- evidence-backed promotion instead of assuming that code which looks generic is reusable;
- a success criterion based on later projects becoming increasingly **composition-dominated**, not on growing a large internal library.

We should **not** claim that this is historically unique or a world-first architecture without a dedicated landscape review. The potentially novel part is the integrated agent-facing capability/evidence loop and the attempt to measure whether it creates a compounding advantage.

## What is verified today

There is real working software here:

- a capability registry and capability manifests;
- a manifest-derived semantic action catalog;
- audited semantic exports bound to public implementation interfaces;
- reusable capability code plus multiple proof applications;
- an engagement generator that creates a portable worker workspace;
- `CAPABILITY_PLAN.yml` for explicit pre-code composition reasoning;
- schemas, validation, tests, and protected CI;
- evidence and closeout artifacts intended to feed generalized learning back into the capability system.

Use `python tools/capability_catalog.py list --json` to inspect the currently verified executable semantic exports. Treat `semantic_exports` as the callable guarantee. A broader `provides` label describes capability scope and is **not by itself evidence that a callable action exists**.

## What is not verified yet

Several important claims remain hypotheses:

- We have not yet shown, with controlled fresh-agent experiments, how much the accumulated capability layer improves success, speed, token use, or bespoke code versus the same agent with only a good planning contract.
- We do not yet have a 5–10 engagement comparable cohort proving that reuse/composition improves commercial unit economics.
- Candidate capability maturity evidence is still being hardened; a green structural check should not be read as proof that every capability claim is semantically true.
- The engagement workspace is a planning/evidence discipline for a cooperative worker. Its shipped hashes and self-check are not an adversarial security boundary, and evidence sanitization still requires human review.

These are useful limits because they define the next experiments rather than weakening the architecture thesis.

## Machine-readable truth hierarchy

When an agent encounters conflicting signals, use this order:

1. **Verified semantic export** — `semantic_exports` resolved by `tools/capability_catalog.py`; intended executable action boundary.
2. **Public interface** — a declared interface in a capability manifest; inspect the pinned source and tests before relying on semantics not covered by an export.
3. **Capability scope** — `provides`, configuration, notes, and models; useful discovery metadata, not necessarily an invokable function.
4. **Evidence and maturity fields** — useful only to the extent they are current and backed by the cited use/test evidence.
5. **Prose/history** — context, rationale, and prior experiments; never stronger than current machine/code truth.

If the machine state and code disagree, treat that as a repository defect to surface rather than silently choosing whichever is convenient.

## What to ask your agent to do

For a real task, a good instruction is:

> Read `AGENTS.md` and the relevant task. Before coding, inspect the capability catalog and relevant manifests. Treat only verified semantic exports as callable action guarantees. Write down what you will reuse, what you reject, what you will compose, and what must stay local. Do not maximize reuse for its own sake. Implement only after the composition/local-gap boundary is explicit, then leave tests and evidence that would help the next agent make a better decision.

For a hands-on guided demonstration, follow [`QUICKSTART.md`](QUICKSTART.md).

## How we will know whether the thesis is right

The decisive experiment is not whether an agent can follow these instructions. It is whether, on comparable tasks and fresh sessions, the accumulated capability system causes measurable improvement over a control.

The metrics that matter include:

- task success and first-pass test success;
- agent turns, tokens, and wall-clock time;
- human interventions;
- bespoke/local code written;
- duplicated implementation;
- defects and rework;
- capability-selection and composition accuracy;
- the share of later projects satisfied through validated composition.

If those do not improve as capability knowledge accumulates, the flywheel thesis is wrong or incomplete. If they do, the repository is evidence for a different way of organizing agent-directed software development.