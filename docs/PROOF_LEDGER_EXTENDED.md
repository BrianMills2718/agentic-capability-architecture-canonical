# Proof Ledger

This is the repository's **current proof-status index**. Historical proof plans, iteration logs, PR descriptions, and session notes may describe what was pending at the time they were written; reconcile current completed/pending claims here first.

GitHub Actions run IDs are retained so claims can be checked against the original proof repositories where access remains available.

## Bootstrap and agent behavior

- `34001408766` — baseline real Frappe lifecycle proof; 6 tests OK.
- `34010580867` — genuinely fresh coding-agent acceptance hidden evaluator; acceptance passed for its bounded authored task/harness claim.

The original bootstrap's two decisive gates are therefore closed. See `DEFINITION_OF_DONE.md` for the ongoing per-project completion standard.

## Real project proofs

- `34012529168` — Client Intake + Booking staff approval lifecycle; ACME regression 6/6, Client Intake 4/4.
- `34015479165` — Internal Procurement on isolated site; Procurement 5/5 while prior suites remained green.
- `34017058788` — IT Access Control added another materially different **consumer** of the approvals package. Current client call sites still pass at most one rule result at a time, so this run does **not** prove that real projects need or exercise the resolver's distinctive multi-rule arbitration/conflict semantics.
- `34020413484` — Facility Maintenance five-site proof; Maintenance 4/4.
- Later Service Desk proof added a sixth isolated composition and prospective primitive-model pressure.
- `34046554727` — Shared Resource Reservation seven-site proof; non-appointment scheduling domain added while prior suites remained green.

## Cross-repository portability

- `34047230770` — independent consumer repository resolved portable capabilities, verified package hashes, installed dependency closure, and passed 7/7 consumer tests.

## Evidence interpretation

Passing tests prove bounded implementation claims, not universal architectural correctness or capability maturity.

The strongest recurring evidence so far is:

- state-transition planning generalized across multiple domains;
- Notifications remained small while serving multiple distinct domains;
- client-specific Frappe apps can remain isolated on separate sites/databases;
- capability portability can work outside the source monorepo;
- prospective modeling produced at least one useful ownership correction before implementation;
- Resource Reservation showed that a capability interface such as availability checking need not automatically become a primitive;
- the approvals package is genuinely consumed by several projects, but its broader multi-rule arbitration abstraction remains package-tested rather than client-validated.

These project proofs are architecture evidence, not a reason to recreate mature business products that already exist in Frappe/ERPNext or other established systems.

## Preliminary controlled market-derived experiment

A 2026-09-08 controlled fresh-agent experiment used a behavior-only slice derived from a live public Upwork ATS project. Control and capability-snapshot treatments all passed the same hidden 11-test evaluator. Capability-aware runs were faster and produced materially less/shallower bespoke code, but consumed more input context.

The first treatment also exposed a concrete capability-knowledge gap: a reusable pure availability implementation already existed, but Scheduling had no verified executable `availability.query` boundary, so the fresh agent correctly rejected it. After publishing that existing boundary without adding shared implementation, a new fresh agent selected and composed both `state.transition.plan` and `availability.query` on the unchanged task.

A second-model Claude Code pair also passed the same hidden evaluator in both arms. Both hit the same fixed 300-second ceiling, so it did not replicate the Codex speed signal; however, the capability-aware treatment left a materially smaller/shallower implementation and completed its evidence/metrics closeout while the control did not.

This remains a tiny sample—one control/treatment pair per model—and is **preliminary**, not proof of a general capability-layer advantage. See [`experiments/UPWORK_ATS_CAPABILITY_EXPERIMENT.md`](experiments/UPWORK_ATS_CAPABILITY_EXPERIMENT.md).

## Pending decisive proof

The most important unresolved question is **not** whether a fresh agent can follow a task that names the expected capability choices. It is whether accumulated capability knowledge materially improves agent performance over a control.

The existing Shipment Exception challenge under `proof/fresh_agent_registry_discovery/challenge/` is useful as a guided mechanics fixture, but its task currently names the shared notification choice, instructs the agent not to recreate shared transition/notification logic, and exposes expected API shapes. A pass therefore demonstrates bounded instruction-following/composition mechanics, not independent discovery advantage.

The next decisive experiment should use fresh sessions and behavior-only task specifications with at least two arms:

```text
control:   planning contract + ordinary/blank project context
comparison: same planning contract + accumulated capability snapshot
```

Measure task success, first-pass tests, agent turns/tokens/time, human intervention, bespoke code, duplicated implementation, rework, selection accuracy, and composition accuracy. Include irrelevant capabilities that should be rejected and at least one task where the honest answer is no internal reuse.

That experiment is what can support or falsify the compounding capability-flywheel claim.
