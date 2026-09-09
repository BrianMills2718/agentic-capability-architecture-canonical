# Upwork Order-Approval Capability Experiment — Preliminary Result

**Status:** preliminary controlled experiment, one fresh Codex control and one fresh Codex treatment. Not promotion evidence or proof of a general capability-layer advantage.

## Market source

On 2026-09-08 we selected a live public Upwork project as a second, materially different source of market pressure:

- **AI Workflow Automation Developer for Order Processing and Operations**
- public listing: `https://www.upwork.com/freelance-jobs/apply/Workflow-Automation-Developer-for-Order-Processing-and-Operations_~022079631969043129867/`
- observed scope included validation against business rules, inventory/customer checks, draft-order creation, human approval for exceptions, follow-up email, auditability, duplicate prevention, and recovery from external failures.

The experiment used only a bounded framework-neutral rule/approval slice. It did **not** implement document extraction, AI/LLM behavior, ERP/CRM integrations, Slack/Teams, persistence, production monitoring, or deployment.

## Question

> On a market-derived task that genuinely requires several independent business rules to compete, does the accumulated capability system cause a fresh agent to use the shared approval-resolution and transition semantics correctly, and does that reduce delivery effort versus the same planning contract with no internal capabilities?

This task was chosen specifically because it can falsify the current Approvals abstraction: unlike prior client fixtures that passed at most one rule to `resolve()`, this slice requires BLOCK dominance, ranked BLOCKs, and equal-rank agreeing approval rules.

## Behavior-only task

Both arms received the same domain API and no capability names. The slice required:

- `Received -> Drafted`, `NeedsApproval`, or `Blocked` routing;
- a customer-hold BLOCK rule;
- an inventory-shortage BLOCK rule;
- high-value and price-exception REQUIRE_APPROVAL rules at the same rank;
- BLOCK dominance over approval conditions;
- highest-ranked BLOCK selection;
- deterministic aggregation of equal-rank agreeing approval rules;
- explicit human approval from `NeedsApproval -> Drafted`;
- idempotent processed/approved retries;
- injected notifications with no network/Frappe dependency;
- order-specific rules, ranks, states, recipients, and copy kept local.

A hidden 11-test evaluator remained outside both agent workspaces.

## Method

- Runner: Codex CLI `0.153.4`, fresh ephemeral sessions.
- Same prompt, task, agent rules, schemas, and planning contract for both arms.
- No web/network access during implementation.
- Control: empty internal capability snapshot.
- Treatment: canonical snapshot at `0f21c9341f7ee33e6eeee73ea3c51f29c65c19dd`.
- Both runs completed normally within a 240-second execution ceiling.

## Results

Both implementations passed the **same hidden evaluator: 11/11**.

| Measure | Control | Treatment |
|---|---:|---:|
| Hidden acceptance | 11/11 | 11/11 |
| Wall time | 211.96 s | 227.56 s |
| Codex input tokens | 222,317 | 319,707 |
| Codex cached input tokens | 191,872 | 283,904 |
| Codex output tokens | 6,319 | 6,619 |
| Workflow source lines | 113 | 122 |
| Workflow AST statements | 75 | 73 |
| Workflow branch nodes | 24 | 20 |
| Agent-authored test lines | 182 | 164 |
| Workflow + test lines | 295 | 286 |
| Internal capabilities selected | 0 | 2 (`approvals`, `core`) |
| Explicit internal composition | no | yes (`approvals` + `core`) |

The treatment was about **7.4% slower**, consumed **43.8% more input tokens**, emitted **4.7% more output tokens**, and wrote **8.0% more workflow lines**. It did use **16.7% fewer branch nodes**, **2.7% fewer AST statements**, and **3.1% fewer workflow+test lines**.

This is therefore **not a delivery-efficiency win** in this sample.

## What the treatment did correctly

The fresh treatment agent independently selected:

- `approval.resolve` from Approvals;
- `state.transition.plan` from Core.

It built all four domain rules as local `RuleResult` values and delegated their competition to the shared resolver. That exercised behavior that prior client fixtures had not exercised in real composition:

- BLOCK winning over REQUIRE_APPROVAL even when approval rules have higher numeric rank;
- highest-ranked BLOCK selection when multiple BLOCK rules apply;
- deterministic aggregation of two equal-rank REQUIRE_APPROVAL rules;
- shared transition planning for routing and explicit human approval.

The agent also correctly rejected `notification.email.send` because that adapter requires Frappe while this task required a framework-neutral injected callback.

The control implemented the same resolution semantics locally and passed the same hidden tests.

## Interpretation

This experiment supplies **fit evidence** for the Approvals resolver: its distinctive multi-rule semantics mapped honestly to a real market-derived business problem and worked in composition with Core.

But fit is not the same as economic value. In this sample, the shared abstraction did not reduce wall time, token use, or workflow source lines. The smaller branch count is consistent with delegating arbitration to tested shared code, but the snapshot/discovery/interface overhead more than erased that benefit in the observed run.

The correct current conclusion is:

> `approval.resolve` has now demonstrated a credible multi-rule market-derived use, but the repository has **not** shown that consuming it is cheaper than implementing a small fixed rule set locally.

Keep Approvals at `candidate`. Do not promote it based on this experiment.

## What this adds to the wider experiment

The ATS experiment showed a stronger treatment signal: less bespoke surface and faster Codex delivery, plus a concrete capability-knowledge flywheel iteration around `availability.query`.

This order-approval experiment is an important counterexample: composition can be semantically correct without being economically beneficial on a small bounded task.

That makes the research question sharper. The architecture needs to learn **when the accumulated capability layer pays for its discovery/integration cost**, not merely whether capabilities can be composed.

## Next experiments

1. Repeat this order-approval pair across fresh sessions before drawing any model-level conclusion.
2. Test a larger approval workflow where arbitration semantics recur across several actions; the fixed discovery cost may amortize differently.
3. Continue measuring snapshot/context overhead explicitly.
4. Prefer a discovery-first compact catalog/index before shipping full capability source when the agent does not need all implementations.
5. Do not count this market-derived experiment as a materially different production/client use for promotion thresholds.
