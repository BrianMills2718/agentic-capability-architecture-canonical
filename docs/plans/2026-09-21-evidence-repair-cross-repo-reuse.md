# Plan: repair the evidence and test cross-repository reuse

Plan ID: ACA-PLAN-002
Recorded: 2026-09-21
Status: historical / standalone execution stopped by Brian on 2026-09-22; see ADR-018 and docs/NEXT_PROOF.md. Preserve existing artifacts and recover already-produced evidence without claiming missing receipts or starting further trials. This is a direction change, not a passed-all-stages or economic-sufficiency claim.
Outcome owner: Brian Mills.
Planning baseline: canonical `main` at `9bdf123776e6f1379c1a4b1b0ea3ed618d4348b3`.
Predecessor: [ACA-PLAN-001](2026-09-18-minimal-composability.md), including merged PRs #59–61.
Governing research agenda: [ACA Research Agenda — Prior Art First](../RESEARCH_AGENDA.md).

## 1. Decision this work must inform

Does useful capability work from Product N let a fresh worker deliver a materially different Product N+1 more correctly or economically than ordinary engineering without that accumulated asset?

Separate three claims: **technical consumption** (the retained boundary actually works outside its originating product), **net delivery value** (reuse beats or otherwise justifies its cost against a competent local/provider-native alternative), and **discovery/selection** (a worker can find or reject it without being told the answer). One success does not establish all three.

Keep the current default: ordinary provider interfaces, existing packages/products, generated adapters, and focused tests before custom ACA infrastructure. Missing proof of general sufficiency is not evidence that a new runtime is needed. Retain existing manifest-derived discovery, evidence, and lifecycle controls while testing whether they help; do not expand them by default.

The endpoint is a bounded delivery decision, not another platform or universal composability proof. No further Twitter prospect scoring or manual prospect review is needed for this work.

## 2. Starting evidence and necessary qualifications

This plan distinguishes source facts from hypotheses. Line references below refer to the planning baseline unless another repository/revision is specified.

| Source | What it supports | What remains open |
| --- | --- | --- |
| [P3 implementation](../experiments/independent-composition/python_baseline.py), [live runner](../experiments/independent-composition/live_pipeline.py), and [results](../experiments/independent-composition/RESULTS.md) | Fixture regression behavior and recorded live read-only collection/routing | Held-out independent composition; a completed live human-review/handoff product; delivery economics |
| [Second consumer](../experiments/independent-composition/engineering_signal_digest.py) and [report](../experiments/independent-composition/SECOND_CONSUMER.md) | A separate worker session reused the unchanged collection boundary for a different downstream task | Discovery was guided; the consumer shared a repository/directory/language; isolated distribution and version-change behavior were not established |
| `python_baseline.py:45–68,71–128`; `live_pipeline.py:67` | Field-presence rejection, a shortlist string gate, and in-memory deduplication | These are not a general semantic compatibility checker, ADR-014 exact-action binding, or restart-safe effect execution |
| [P6 decision](../experiments/independent-composition/P6_DECISION.md):27–52 and [ADR-017](../DECISIONS.md#adr-017--composition-ready-boundaries-use-ordinary-interfaces-plus-conformance-tests) | No additional ACA platform was needed in the observed runs | The evidence table still overstates approval-binding and durable-state coverage; a policy default must be separated from an empirical sufficiency claim |
| [Original Product N client](https://github.com/Inside-Success/twitter-prospecting/blob/ab2cfba0e8c43f0198716dee4414dedf2212d478/apps/twitter_prospecting/twitter_client.py):35–91 | A pre-existing `TwitterApiIoClient` calls the same search provider/endpoint as the new P3 wrapper | Whether its publication/dependency boundary is economical to consume; rights and exact historical provenance must be verified before distribution |
| [Proof ledger](../PROOF_LEDGER_EXTENDED.md):23–53; ADR-012/013 | Earlier portability and controlled experiments already exist; prior economic results are mixed | Neither universal failure nor universal success of capability knowledge follows; reuse those instruments before building more |

Do not replace the prior overclaim with another one. P5 had a fresh session; do not describe it as the same-session implementation. Consuming a small read-only capability is real reuse, even if it is weak evidence for a broader architecture. Source inspection was allowed by the original protocol. Three fresh runs per condition were required only for a proposed ACA extension comparison, not for every baseline. The original protocol also explicitly allowed small pilots.

No reason is yet established to say that the original Product N client *could not* be reused. Duplication of its provider integration is an observation; packaging failure is a hypothesis to test. Similarly, n8n control friction does not establish n8n workflow unsuitability. No new n8n setup is planned.

### Prior-art convergence gate — completed by this planning change

Before execution, ACA's research surface was re-mapped against established software-reuse/product-line engineering, OpenAPI/AsyncAPI/MCP-native interface descriptions, Backstage-style catalog/discovery patterns, Pact-style consumer contracts, Arazzo API-workflow descriptions, and established orchestration/durable-execution products such as n8n and Temporal. See [RESEARCH_AGENDA.md](../RESEARCH_AGENDA.md) for the source trail and resulting agenda.

This gate removes already-solved mechanism-building from the experiment. The remaining questions are agent-specific: discovery/selection, publication readiness, economic compounding, compatibility maintenance, effectful composition, and whether accumulated evidence improves later decisions. A0 therefore starts with evidence repair rather than another technology build.

## 3. Scope, roles, and authorization

Scope is evidence repair, one pre-existing boundary, one separate consumer product, a bounded control/reuse comparison, and a separately scoped local effect-safety canary. Python is acceptable on both sides; another language or platform is not required merely to make the experiment look harder.

No ACA runtime, registry service, connector/auth platform, workflow engine, scheduler, agent harness, universal schema, semantic compiler, or compulsory LC/Foundry/MCP/Arazzo layer. Do not retire existing implementations or promote a capability as part of this plan. No production outreach, CRM writes, infrastructure provisioning, or secret disclosure.

Responsibilities may be filled by existing coding-agent sessions, not new hires:

- **Coordinator:** preserve revisions, prepare equivalent environments, measure execution, and retain every outcome. Does not write the scored consumer implementations or steer them toward an answer.
- **Publisher:** qualify the pre-existing Product N asset and expose its legitimate boundary without tailoring substantive behavior to the consumer's hidden tests.
- **Evaluator/reviewer:** prepare behavioral acceptance and hidden cases independently of scored workers; verify claims and gate each PR. Must disclose any shared context or compromised isolation.
- **Fresh workers:** separate sessions for each scored run; no shared memory/resume lineage with the publisher, evaluator, prior pilot, or other arm. They may inspect allowed public source/tests and write their own tests.

This document authorizes no experimental spend or source-repository change by itself. Before execution, adopt or amend the proposed caps in section 9 and record actual repository/data rights, approved destinations, and scope. Use normal PR review; do not merge a broad conclusion merely because the author reports green tests.

**Subscription-first resource policy.** Use Brian's existing authorized subscriptions and included local/CLI access for ChatGPT/OpenAI, Claude, Codex, GitHub, TwitterAPI.io, and other already-paid tools wherever the required workflow can be exercised through them. Do not substitute metered model APIs merely because they are convenient. Existing subscription fees are sunk account costs, not experiment cash spend; record the dependency and any usage limits, while treating incremental cash as zero only when no additional charge is actually incurred. Metered API/provider calls are allowed only when included/subscription access cannot execute the required path and the run manifest explicitly authorizes the incremental cap. Do not buy another subscription or infrastructure service for this experiment.

## 4. Dependency-ordered execution

| Stage | Owner | Output | Exit gate |
| --- | --- | --- | --- |
| A-1 — Prior-art convergence | Planning author + reviewer | `docs/RESEARCH_AGENDA.md` and narrowed research surface | Existing standards/practices/products are adopted as defaults; no solved mechanism remains on the ACA invention agenda. **Completed by the planning PR.** |
| A0 — Repair evidence claims | Coordinator + reviewer | Dated audit addendum, corrected navigation/status, bounded ADR-017/P6 amendment, reuse observation | Every material claim maps to a retained source or is explicitly unverified; no historical success erased or invented |
| A1 — Qualify and publish Product N boundary | Publisher + reviewer | Brownfield portability audit, exact source/dependency revision, ownership/rights check, consumer-blind publication-only normalization if needed, ordinary distribution recipe, original-consumer regression | A clean environment imports/invokes the actual retained implementation without private application setup or silently replacing it; publication debt is measured separately from reuse cost |
| A2 — Freeze representative task, evaluator, environment, and budget | Evaluator + coordinator | Public brief/examples, nontriviality gate, separate held-out evaluator, run manifest and comparison rules | The scored task exercises at least one distinctive retained invariant beyond a single GET/field rename; isolation and instrument negative controls pass before any scored run |
| A3 — Deliver control/reuse pair | Two fresh workers | Separate consumer repos, commits, execution logs and metrics | Both submissions evaluated unchanged; failures/timeouts/rejections retained |
| A4 — Evaluate and, if useful, repeat once | Independent reviewer | Paired comparison including first-use cost; at most one additional fresh pair | Outcome is bounded positive, no advantage, failure, or inconclusive; no post-hoc threshold tuning |
| A5 — Effect-safety canary | Fresh integrator + reviewer | Existing approval binding composed with a local durable test destination | Required before any new effectful-readiness claim; not a prerequisite to a read-only decision |
| A6 — Close out | Coordinator + Brian/reviewer | Ledger entry, reuse/rejection evidence, scoped adoption decision | Tests, exact revisions, limitations, spend and next product action are linked; no automatic promotion |

A0–A4 are the first tranche. A5 is a bounded follow-up only when effectful reuse is in scope; otherwise record it as deferred, not passed. A6 can close the read-only tranche without A5. Stop at a genuine rights, access, safety, or approved-budget gate instead of compensating with new infrastructure.

### A0 — Correct the record, not the history

Create a dated addendum under `docs/experiments/independent-composition/` and reconcile `docs/README.md`, `docs/NEXT_PROOF.md`, `docs/PROOF_LEDGER_EXTENDED.md`, the predecessor plan's current-status header, `PROTOCOL.md`, `RESULTS.md`, `SECOND_CONSUMER.md`, and `P6_DECISION.md`. Preserve historical entries and distinguish what was known on each date.

Amend ADR-017 to retain the default preference for ordinary/native contracts while limiting the pilot's evidence to the exercised boundary and conditions. Retain ADR-011 manifest authority, ADR-013 net value, ADR-014 exact-action approval, and ADR-015 evidence compatibility. Record that full product completion, general composability, and economic compounding remain unestablished; do not re-open unrelated successful bootstrap proofs.

Correct the durable-sink/approval-pattern table, all-six-checks claim, current navigation, stale counts, and null-handling claim. Demonstrate suspected code defects using small local probes or regression tests, not prose alone. Keep original `CASES.json`, `EVALUATION.json`, and n8n artifacts unchanged. Label the field-presence semantic check and in-memory sink as bounded fixtures, not production contracts.

Add the P3 wrapper as a reuse observation in `reuse_candidates.yml`, using the lowest honest lifecycle status supported by the evidence; do not newly register or promote it. Link positive use, limitations, rejection information, and provenance. A later registered export must resolve a real public boundary using existing manifest/catalog conventions; do not invent a second source of metadata truth.

Recover original logs/receipts only where actually available. A transcription from chat is marked as such; missing raw output stays missing. Do not generate a new JSON object and present it as an original historical execution receipt. Never fill unknown cost with zero.

### A1 — Reuse the existing implementation rather than rewrite it

First candidate: `Inside-Success/twitter-prospecting`'s existing `TwitterApiIoClient` and the minimal declared types/dependencies needed to invoke its public collection behavior. The inspected revision is `ab2cfba0e8c43f0198716dee4414dedf2212d478`; verify relevant file history, tests, remote revision and reuse rights before selecting it. A pre-existing class name is not by itself proof of independent provenance or a portable boundary.

Treat architecture quality as a measured variable rather than silently optimizing it away. First attempt a **brownfield portability check** against the Product N revision as it exists. Record exactly what blocks external consumption: package shape, imports, private initialization, dependency declaration, hidden configuration, ambiguous types, or substantive coupling. Then, if needed, permit one **consumer-blind publication-only normalization** pass: packaging/export path, dependency metadata, public type placement, installation recipe, and documentation may change, but provider behavior, collection semantics, error policy, and consumer-specific output fields may not be redesigned. The publisher must not see the held-out evaluator or scored consumer implementation. This separates `Product N was not publication-ready` from `published reuse has poor economics`.

Choose the smallest distribution form that already fits: a pinned existing package, a repository dependency/export, or a normal built artifact with a hash. Inspect the repository's earlier cross-repo export proof before adding packaging code. Record source repository, original commit, brownfield failure/friction, any publication-only diff, artifact hash, dependency lock and public invocation example. Publication cost remains part of first-use economics even when the normalization makes later reuse easy.

Do not copy a whole application, rely on sibling imports/PYTHONPATH from the originating checkout, or build another HTTP client and call it an adapter. The distributed implementation may include necessary public data models; it must not require private product sessions, review code, secrets, or hidden application initialization. An exported source bundle is acceptable when its provenance is explicit; undisclosed copied/reimplemented logic is not.

Record publication/documentation/test cost separately. Cap normalization/extraction at **60 active engineering minutes** within the preparation budget. If the candidate requires substantive behavioral redesign, consumer-specific schema shaping, or more than that bounded publication work, preserve the result as **architecture/publication debt** rather than continuing until it becomes reusable. That is useful ACA evidence, not an experimental failure. If a real dependency or licensing problem prevents a clean boundary, preserve the failure and stop this candidate's trial. Select at most one alternative pre-existing capability under a newly frozen brief; do not secretly substitute the P3 wrapper to make a Product N reuse claim pass.

Any source-repository modification needs its own PR, original-product regression checks, and rights confirmation. Freeze the published artifact before scored consumer sessions. Subsequent producer behavior changes create a new condition, not an invisible fix.

### A2 — Freeze a useful product and a trustworthy instrument

Use a **difficulty ladder**, and do not let the trivial rung decide ACA.

- **T0 — plumbing sanity only:** one read-only query proves the artifact installs and invokes outside Product N. T0 can validate packaging, provenance, and transport, but it is explicitly **non-decisive** for ACA economics or general composability.
- **T1 — primary scored comparison:** a one-shot engineering topic brief executes multiple explicit topic queries and must preserve independent per-query success/failure status, partial success, normalized source-backed evidence, duplicate suppression across queries, malformed-item warnings, deterministic candidate limiting/truncation, and stable provenance. This intentionally targets the already-authored `TwitterApiIoClient.collect(...)` / `SearchCollection` behavior at Product N revision `ab2cfba...`, especially its per-query failure isolation and aggregation semantics, rather than only `search(query)`.
- **T2 — effect-safety canary:** the separate A5 approval/idempotency test. T2 is required before effectful-readiness claims but is not part of the read-only economics score.

The T1 consumer remains **not a prospecting workflow**: no lead ranking, buyer inference, outreach, CRM, scheduler, or new UI. The public brief must define truncation, malformed data, duplicate conflict and error behavior before runs. Consumer acceptance is expressed behaviorally, so the control may implement equivalent semantics directly from provider/native tools while the reuse arm may consume or reject the published Product N asset.

T1 must exercise a distinctive invariant that would be lost by replacing the asset with a trivial one-request wrapper. If the qualified Product N boundary cannot expose such meaningful behavior without substantive redesign, stop and record the architecture as insufficiently reusable rather than manufacturing a harder task or optimizing the producer to the evaluator. If this use case still offers no plausible advantage over a small direct integration, that is exactly what the control/reuse comparison is meant to measure.

Freeze a shared behavior-only brief, provider-native documentation snapshot, harmless public examples, clean environment/dependency baseline, replay data, runtime/model/harness identifiers, worker permissions, timer/cost policy, comparator, and independent acceptance tests. List required business/safety facts publicly; hide only evaluator-specific inputs and expected outputs.

Use ordinary test tooling and an existing HTTP/session injection seam or small replay endpoint. The controlled runs use the **same fixed provider responses and synthetic credentials**. The reuse arm must call the real retained client through this transport; replacing the entire capability with a fake `search_candidates` is not integration evidence. A live provider smoke test is optional and reported separately, never required to compare fluctuating search results.

Acceptance includes full query preservation (including spaces), correct mapping/provenance, duplicate posts/authors across queries, conflicting duplicates, missing/null fields, empty results, **at least two queries with one success and one provider failure**, retained execution/disposition for every requested query, partial-result survival, bounded timeout/error reporting, warning preservation, candidate-limit/truncation behavior, secret-safe outputs, and declared data-loss semantics. Deliberately break identity mapping, drop a requested query from the disposition list, turn one-query failure into whole-run failure, silently swallow a malformed-item warning, exceed the candidate limit, and bypass the retained provider; the relevant evaluator checks must turn red. Consumer acceptance itself remains behavior-based so the control is not penalized for not importing ACA code.

Hold the evaluator outside both workers' accessible repositories, git history, mounted paths and session context. Use existing sandbox/permission controls; do not invent a security platform. If only instruction-level isolation is feasible, record that weaker condition and do not claim enforced blinding. Check shell access, tests, dependency installation, cost visibility and multi-word argument transport with a non-scored trivial preflight. A worker unable to execute tests is not equivalent to a fully enabled worker.

### A3/A4 — Fair comparison and limited confirmation

| Condition | Available material | Freedom |
| --- | --- | --- |
| C — Ordinary engineering | Same public brief, provider docs, examples, standard packages, tools and planning discipline | Implement the smallest correct local/provider-native integration |
| R — Accumulated asset available | Everything in C, plus a read-only snapshot of the qualified Product N boundary, its normal docs/tests and existing publication/index information | Discover, inspect, compose, or explicitly reject the asset when its net value is poor |

The behavior brief must not name the expected function, adapter mapping, final architecture or evaluator answers. The treatment snapshot can naturally name its public interfaces; that is not the same as instructing the worker which one must be chosen. Give each worker a separate consumer repo outside ACA/Product N. Pin the source dependency rather than importing a sibling checkout. Do not expose other workers' outputs or historical pilot results.

Keep model version, harness, permissions, common package cache, transport, environment, budget and completion criteria equivalent. Run one pair first. If neither arm has a valid setup/safety result, stop and repair the instrument. Otherwise allow one repeat pair with fresh sessions and reversed execution order under the remaining cap. Do not repeat until the desired result appears. Setup-invalid runs and any replacements remain in the record; replacements require budget headroom and cannot erase the failed attempt.

During scored runs, allow normal public-source inspection and self-tests, but no coordinator-authored patches, hidden-test answers or selective hints. Freeze submissions at the time/cost ceiling. Evaluate each immutable submission once against the same held-out suite. Later assisted repairs are separate diagnostic work with separate cost; do not retroactively score them as a blind first pass.

Report discovery, installation, adaptation, debugging and total accepted-delivery time separately. This small index/task tests only *bounded selection*. It does not establish large-catalog discovery or isolate the causal value of metadata versus code. A third metadata-only arm is deferred unless that distinction becomes a real product decision.

## 5. Measurements and predeclared decision rule

Retain per run: input/brief/evaluator/source/environment hashes; model and harness version; session ID and granted permissions; wall time, active worker time and outages separately; human interventions/minutes; tokens and measured model/tool/provider cost; chosen/rejected capabilities and reasons; original-source changes; consumer adapter versus residual code; first-submission and final acceptance; observed safety failures; output/log paths and provenance. A success flag printed by the application is not an independent safety check.

Use ordinary runner output and existing engagement metrics/receipt formats where they fit, not a new measurement service. Fixed ceilings must be enforceable through existing controls or conservative reservations; if spend cannot be bounded, do not start that run. Mark unavailable actual metering as unknown rather than presenting estimates as invoices.

Let `P` be incremental publication/packaging/documentation/verification cost, `C_i` control delivery cost, and `R_i` reuse delivery cost for equivalent accepted behavior. Report:

`first-use net saving = C_1 - (P + R_1)`

`later-use saving = C_i - R_i`

For a positive representative later-use saving `S`, report the **estimated** break-even number of comparable uses `ceil(P / S)`. Calculate time and money separately unless an explicit conversion rate was agreed before runs. Do not amortize across imaginary future projects or use a failed/timeout submission as the cost of correct delivery.

Proposed practical threshold, to be adopted before results: a **promising marginal delivery advantage** requires both fresh pairs to meet all mandatory correctness/safety tests, reuse accepted-delivery time at least 20% lower in each pair, and no increase in measured marginal model/tool dollars or human intervention time. Report packaging-inclusive first-use value even if negative. Any break-even claim needs plausible comparable follow-on demand and is provisional.

A repeated correctness/risk-reduction advantage can justify scoped reuse even without a time win, but report it separately and include the cost premium; do not re-label it as an efficiency result. One pair supports a smoke/pilot finding only. Two pairs are still a tiny sample, not statistical proof or evidence of general compounding.

Tie, higher reuse cost without offsetting value, appropriate rejection, or inadequate evidence are valid outcomes. Follow ADR-013: prefer the simpler local/provider-native choice rather than rescue the experiment with more metadata. No universal conclusion follows from failure of this one asset either.

## 6. Effect-safety canary — distinct, local, and limited

Run A5 only before relying on broader effectful composition claims. Reuse existing `approval.action.bind` / `approval.action.verify` behavior and a normal durable local test destination. Start with the already published approval binding, not the P3 shortlist helper. No new authorization system or transaction engine.

The proposed destination is a temporary SQLite-backed test record. Put the logical operation key, exact approved action/target/payload digest, and the local effect record in the same appropriate transaction boundary; use the database's uniqueness/transaction facilities. The test effect is that local record, not a real email, payment or CRM write.

Exercise: payload A approved then changed to B; changed action/target/operation key; absent or rejected approval; retry in a new process; two processes racing on one operation; crash before commit; commit followed by lost acknowledgement; and same key with conflicting content. Assert the actual persisted effect count and content independently of application receipts. A changed payload fails closed; a valid retry produces at most one local effect and does not silently hide a conflicting operation.

Use explicit synthetic approval fixtures for mechanics and label them synthetic. They do not prove human identity/authentication or replace real approval for future production actions. Do not ask Brian to review Twitter prospects to test this invariant.

A passing local canary establishes only the stated database/approval boundary. Remote-effect exactly-once behavior remains unproven: a real destination needs its own provider idempotency/reconciliation or established delivery mechanism. An ambiguous remote result must not lead to an automatic blind repeat. Run one deliberate breaking-contract control against the pinned approval interface to demonstrate that the consumer compatibility test actually detects drift.

## 7. Failure handling and stop conditions

Classify before repairing: provider/access; missing behavior; structural mismatch; documentation/example problem; semantic mismatch; operational/effect mismatch; agent mistake; evaluator defect. Count agent mistakes, review time, harness failures and publication work in delivery cost even when they do not justify an ACA abstraction.

Repair order: normal documentation/example, generated adapter, provider-native configuration/metadata, then at most a tiny justified ACA change. Do not impose a new interface or metadata requirement on scored runs after seeing their result. A later extension requires a separately frozen failing case and an approved comparison under the original plan's extension discipline.

Stop on unauthorized effects, secrets exposure, rights uncertainty, exceeded caps, broken blinding, non-equivalent environments, or unsupported target guarantees. Retain the failure. Fix the cheapest relevant layer, not the most architecturally interesting one.

## 8. Artifacts, PRs, and recoverability

Use a small evidence directory under `docs/experiments/cross-repo-reuse/` when execution starts. A public brief, boundary provenance/recipe, protocol/run manifest, immutable run summaries/output receipts, evaluation report and conclusion are sufficient. The evaluator stays inaccessible during scored work; publish it with hashes afterward when rights permit. Do not require a new artifact schema for every file.

Use existing `CAPABILITY_PLAN.yml`, `METRICS.yml`, `LEARNINGS.md`, evidence proposals and receipt versions where appropriate to each consumer/engagement. Keep client-owned code and confidential artifacts out of canonical intake. A portable evidence reference names repository, exact revision and path; a machine-local `/tmp` filename alone is not durable evidence.

Proposed review units: **PR-A** evidence/status corrections; **PR-B** source publication and fixture/instrument preparation (source-owner changes separate where required); **PR-C** immutable comparison results and decision; **PR-D**, only if run, effect-safety evidence. These are review boundaries, not a requirement to accumulate work before committing.

Before changes inspect git status/diffs; preserve unknown modifications. Use isolated branches/worktrees and small coherent commits. Push recoverable checkpoints before long runs, risky environment work, restarts or handoff. Do not reset, clean, delete or recreate an existing worktree without inspecting its state and obtaining approval for discarding unknown work.

Use GitHub for repository truth and review. Use Remote MCP only for necessary machine state/execution: `devices_list`, confirm `execution_ready`, then `devices_ping`; run WSL through `C:\Users\thela\bin\wsl-safe.ps1`. Use scripts/files for complex arguments instead of repeatedly trying broken nested quoting. Record `ask-agent` sessions; resume only within the same assigned task, never to impersonate a fresh participant. Agent permission denials must be reported, not disguised as executed checks.

Each material PR runs focused negative controls and `python tools/check_bootstrap.py`, with exact interpreter/environment and skipped checks recorded. Reuse a known suitable venv or create an isolated environment without deleting unknown directories. A separate reviewer verifies the claim-to-evidence mapping; green schema checks alone are not approval of the architecture claim. Changes to protected `main` go through PRs, never bypass.

## 9. Proposed execution envelope and Brian's involvement

These are **proposed caps**, not claimed measurements or spending permission. Freeze acceptance of them in the run manifest before experimentation.

**Default cost route is Brian's existing subscriptions.** Use included ChatGPT/OpenAI, Claude/Codex, GitHub, provider, and local-compute access where authorized and technically sufficient. Record the plan/tool dependency and usage limits, but do not assign a fictitious per-run cash charge when no incremental charge occurs. Conversely, do not call the experiment free: active engineering time, context/tokens where observable, subscription dependency, and publication work are still measured. Metered API usage is fallback-only and must fit the incremental cap below.

| Work | Active engineering ceiling | Incremental metered/provider cash cap after subscription-first routing |
| --- | --- | --- |
| A0–A2 preparation plus evaluation/closeout | 2 hours total, including A1's 60-minute publication-normalization limit | $5 total |
| First control/reuse pair | 30 minutes per worker; 2 workers | $2 per worker; $4 total |
| Optional confirmation pair | Same; at most 2 additional fresh workers | $4 total |
| Optional local effect canary | 45 minutes | $2 total |
| Entire envelope | Under 5 active engineering hours; blocked wall time separate | **$15 incremental maximum**, with a target of $0 when subscriptions/local replay suffice |

No new subscriptions, hosting purchases or infrastructure deployments. Controlled trials use fixed local/replay provider responses and therefore require zero live-provider calls. Any optional read-only live smoke should use Brian's existing authorized provider subscription/allowance where available; if it would incur incremental metered spend, verify and approve a separate per-call cap within the $15 maximum. If the incremental price cannot be verified/enforced, omit the live smoke.

Brian's input is limited to adopting the execution envelope, resolving genuine code/data ownership or access decisions, and reviewing a consequential scope/adoption decision. Target at most 20 minutes of Brian's time, recorded separately. Exceeding a cap requires an explicit decision to stop, narrow scope or authorize more; do not silently turn the pilot into a research program.

## 10. Completion and immediate next action

Planning is complete when this plan is linked from current navigation, source claims are grounded, scope/caps/decisions are explicit, and the documentation-only PR passes the repository completion gate. Merging the planning PR does not mark A0–A6 complete or amend historical decision evidence by itself.

Execution closes with one useful delivered consumer or an honestly retained failed/rejected reuse result, independently checked compatibility/evidence, measured economics or explicit unknowns, and a scoped adoption/defer/reject decision. Register/propose a boundary only with honest provenance and observed use; no automatic `proven`/`core` promotion. Index the outcome in the existing proof ledger.

**Historical next-step instruction superseded by ADR-018.** Do not resume this sequence automatically; current work returns to AES product engineering.
