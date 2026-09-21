# Plan: minimal composability, off-the-shelf first

Plan ID: ACA-PLAN-001
Recorded: 2026-09-18
Status: **historical; bounded.** Executed 2026-09-18 to 2026-09-20; decision recorded in ADR-017 and P6_DECISION.md. Its evidence is bounded to one read-only, same-repository, same-language path. Superseded as the current execution plan by [ACA-PLAN-002](2026-09-21-evidence-repair-cross-repo-reuse.md); see the [2026-09-21 audit addendum](../experiments/independent-composition/AUDIT_ADDENDUM_2026-09-21.md) and the dated ADR-017 amendment.
Outcome owner: Brian Mills.
Execution owners: assigned coding workers; roles below are responsibilities, not a requirement to hire a separate person for each.
Execution status (as recorded 2026-09-20; preserved): P0-P6 complete. P3 produced reusable composition boundaries + live TwitterAPI.io evidence (41 tests). P5 second consumer (Engineering Signal Digest) exercised retained boundary successfully (22 tests, live "observability" query). P6 decision: ordinary interfaces + conformance tests are sufficient; no new ACA machinery justified. See ADR-017 and P6_DECISION.md.
Current qualification (2026-09-21, ACA-PLAN-002 A0): "complete" means the plan's decision step was recorded, not that the product slice was delivered (no human review, LLM scoring, live n8n, or real handoff occurred). "Sufficient" applies only to the exercised read-only path; the pilot did not exercise ADR-014 approval binding or durable idempotency, cross-repository reuse, discovery, or measured delivery economics. The live runs are prose records with no retained receipt.

## 1. Outcome and priorities

Deliver usable products quickly by composing capabilities, while making capabilities contributed by one hired developer or coding agent practical for the next project to consume. The desired technical property is **independent composability**, not compliance paperwork, a growing catalog, or novelty.

The smallest plausible new ACA surface is **a composability contract plus conformance tests**. Even these may reduce to a short profile of existing interfaces and ordinary tests. This is a candidate boundary to test, not authorization to delete current implementation or to invent a new standard.

Priorities, in order:

1. Correct, usable product delivery with acceptable operating and integration cost.
2. One sufficient off-the-shelf platform where possible; a small integration of existing products where necessary.
3. Capabilities that another project can actually invoke and compose, with tested adapters where needed.
4. Custom ACA machinery only for an observed, important gap that simpler descriptions, examples, configuration, or existing tooling do not resolve.

Contractor acceptance, required artifacts, protected branches, and CI are supporting delivery controls. We are **not** conducting research into whether a worker can be required to submit a manifest. A green manifest check is also not proof of practical composability.

## 2. Scope and non-goals

This plan covers capability shape, composition and adapter cost, a minimal standards-based contract candidate, a small independent-composition pilot, and a second consumer. It covers libraries/functions, APIs, services, and reusable workflows; it does not assume every product or capability must become an MCP server or an n8n workflow.

Do not build a new registry service, agent harness, workflow language/engine, connector/auth platform, scheduler, transaction manager, or generic evidence/governance framework for this pilot. Do not mandate Linguistic Core, Semantic Foundry, SystemSpec, Arazzo, Temporal, or a stack containing all candidate products.

No arbitrary pair of capabilities is assumed composable. Missing information, incompatible business semantics, unauthorized effects, and unsupported provider behavior can make rejection the correct result. A generated adapter may transform representations or call an explicit lookup capability; it cannot invent identity, consent, evidence, units, or guarantees.

The planning change performs no paid run, deployment, external business mutation, cross-repo edit, capability promotion, retirement, or migration. Existing consumers and research programs continue unchanged. Product adoption of a semantic research layer is separate from that repository's independent research/construction goals.

## 3. Starting evidence and corrections

The repository already has public capability boundaries, planning/closeout tooling, tests, and recorded decisions. Read `AGENTS.md`, `docs/ARCHITECTURE_CHARTER.md`, and `docs/DECISIONS.md` before implementation. In particular, ADR-011 avoids a second catalog authority, ADR-013 requires net value, ADR-014 preserves exact-action approval bindings, and ADR-015 preserves versioned receipt compatibility.

The prior `docs/NEXT_PROOF.md` emphasized planning-contract and accumulated-discovery experiments. Its historical formulation remains in that file; it is not the immediate prerequisite for this plan. Completed experiments and proof ledgers remain evidence for their recorded scopes, not new evidence for independent composition.

The first substrate audit was a preliminary recommendation, **not a verified provider-selection decision**. Its former minimum-core list overemphasized plans, receipts, and CI. The corrected audit routes to this plan and distinguishes the technical candidate from supporting controls.

Planning baseline inspected: ACA PR #56 at commit `1493dd89702c3d933f26e9fdb7cb6017dae43a61`. Documentation inspection is not a fresh runtime/benchmark result.

## 4. Dependency-ordered delivery plan

| Step | Owner | Depends on | Deliverable | Exit condition |
| --- | --- | --- | --- | --- |
| P0 — Reconcile direction and navigation | Planning author; Brian reviews | User's clarified goal | This plan, ADR-016, updated next-proof route and corrected preliminary audit | One discoverable next plan; no claims that implementation or supplier fit is complete |
| P1 — Freeze one product slice and shortlist | Sourcing/implementation worker; Brian owns product fit | P0 | Brief, acceptance cases, and small provider-fit record | Selected baseline has evidence of required interfaces and an explicit access/cost path; unresolved needs named |
| P2 — Draft the minimal contract and pilot protocol | Contract author and evaluator | P1 | One-page contract candidate and frozen pilot protocol | Native contracts reused; costs, allowed context, independence, safety cases, and decision rules specified before runs |
| P3 — Deliver the baseline composition | Independent capability builders/providers; fresh composer | P2 | Running first product slice, tested adapters, run receipts | Behavior and safety acceptance passes or failures are retained and classified; useful result shown before further research |
| P4 — Repair only observed composition gaps | Implementer and evaluator | P3 failure or material integration overhead | Smallest justified repair and fresh comparison | Evidence determines whether the fix is documentation, tooling, a capability change, or a genuinely needed ACA extension |
| P5 — Reuse in a second process/product | Fresh consumer worker | A correct P3/P4 composition | Second consumer, reuse evidence, cost comparison | Distinct consumer exercises the retained boundary without importing the first product's private implementation |
| P6 — Select the minimum product boundary | Brian; author records decision | P3 and P5, plus P4 only if needed | Explicit adopt/defer/reject decision and lightweight contractor guidance | No new platform by default; any retained custom field/test has a demonstrated purpose |

P4 is conditional, not a mandatory research phase. If the baseline meets requirements economically, proceed directly to P5/P6. Do not complete an exhaustive landscape survey before delivering the bounded slice.

## 5. P1: product slice and proportionate sourcing

Use the Twitter Prospector review story as the initial candidate: collect/import records, score against configurable criteria, obtain human review, and prepare or perform an explicitly authorized handoff. The uploaded HTML is a fixture-backed UI example, not evidence of live collection, scoring quality, a CRM write, or cross-project reuse.

Start with authorized fixture data and a sandbox/local handoff if access is unresolved. Label that result as a bounded prototype; live API access, source coverage, quality, and actual product deployment remain separate acceptance items. Avoid building a new review UI when the chosen product already has an adequate one.

Prefer capabilities already produced for unrelated projects. If suitable ones are absent, assign two or three small capabilities to independent workers for distinct original briefs. Do not manufacture gratuitous new shared code merely to create an experiment.

The sourcing record must check the actual slice, not a marketing feature list: callable/versioned boundary, reusable workflow/function export, importing in another project, typed data/results, adapter escape hatch, necessary waits/retries/approvals, log access, deployment and credential isolation, applicable licensing/embedding terms, and total setup/operation cost. Product-level retry support is not automatically provider-side idempotency.

Evaluate one plausible complete platform first, then at most one materially different fallback before expanding the search. n8n is a candidate for workflow-heavy delivery; the existing application/runtime or ordinary typed packages may be cheaper for application/code-heavy work. Composio or Pipedream are optional connector/tool-access candidates, not mandatory layers. MCP/OpenAPI/JSON Schema are interfaces/specifications, not full execution products. Temporal and Arazzo are conditional options, not assumed dependencies.

Output: `docs/experiments/independent-composition/PROVIDER_FIT.md`, with dated official references, exact evaluated versions, documented versus exercised features, constraints, and selection/rejection rationale. No supplier is selected by this planning PR.

## 6. P2: minimal contract candidate

Output: `docs/contracts/MINIMAL_COMPOSABILITY_V0_1.md` (planned; not created by this change).

Draft a one-page consumption profile over the selected native interface, not a competing wire format. Reuse existing capability manifests and public exports when sufficient. Reference rather than duplicate schemas, versions, credential configuration, or provider-owned guarantees.

The profile must let a consumer locate and invoke the boundary, understand inputs and outputs, obtain necessary configuration, recognize errors, and identify composition-relevant restrictions. Put units, identity namespaces, cardinality/nullability, side effects, prerequisites, and retry behavior in ordinary existing descriptions where sufficient. Unknown guarantees must remain unknown; a shared role label or JSON type is not an equivalence proof.

Use native examples and tests where available. Do not withhold known safety facts from the baseline to make enriched ACA metadata look useful. Only add machine-readable semantic roles, effects, pre/postconditions, invariants, or mapping rules after a recorded failure justifies them and the selected standard cannot already express them adequately.

Generated adapters are allowed and expected. Keep their input/output mapping, extra lookups, dependencies, and tests inspectable. Cheap correct glue is a success, not evidence that a universal ontology is required. An adapter that recreates a provider's substantive behavior must be reported as reimplementation, not integration.

## 7. P2/P3: independent-composition protocol

Output: `docs/experiments/independent-composition/PROTOCOL.md` (planned).

**Independence.** Builders A/B/(optional C) solve distinct original briefs. They may share selected public standards and normal engineering instructions, but not destination-specific interfaces, a prearranged solution, each other's private session context, or the final evaluator packet. Prefer already independently authored capabilities. Record the provenance of each boundary; jointly designed fixtures must not be described as independent.

Freeze capability and task revisions before fresh composer D starts. D receives the new product's behavior-only requirements, public interfaces, normal documentation/examples, runnable access, and ordinary allowed source/tests. D may search, inspect source, generate adapters, reject a bad fit, or implement a justified local gap. Do not handicap a normal coding harness by giving it schemas without runnable tools or withholding public documentation. Keep the evaluator's specific cases/expected outputs separate; the required business and safety rules themselves are public requirements.

**Small pilot.** Start with one end-to-end composition and one distinct second consumer, not a new benchmark platform. Use one fresh baseline composer run to deliver and diagnose. If P4 introduces an extension, freeze it and compare baseline versus that extension on the same snapshots and held-out cases, with three fresh runs per condition within an approved budget. Repeated confirmation for higher-risk use is a separate decision; small pilots do not prove universal reliability or commercial compounding.

**Fairness.** Keep model/harness version, access, tools, budgets, acceptance cases, and enforcement discipline equivalent. Change one interface convention or metadata addition at a time. If executable behavior also changes, report it as a different intervention. Retain failures, source/network outages, budget exhaustion, and evaluator defects; do not count infrastructure failure as proof of a semantic defect.

**Budget/access gate.** Before execution, record the actual environment, authorized services/data, model-run limit, monetary cap, human-time cap, and artifact destination in the protocol. No spend amount or production authorization is inferred from this planning request. If unavailable, report the dependency and continue only with explicitly bounded local work; do not invent live evidence.

For work on Brian's machines, use the authorized Remote MCP/`ask-agent` route and isolated workspaces where available. A truly fresh participant must not resume a session that has seen evaluator answers. Use existing agent/session and test tooling, not a custom orchestration harness.

## 8. Acceptance cases and measurements

Freeze concrete fixtures and expected outcomes before runs. Include a normal end-to-end case, an ordinary schema transformation, a genuine semantic mismatch, a boundary that must be rejected, and an operational failure/retry. Choose relevant cases rather than requiring every capability to implement every possible effect.

| Check | Pass condition |
| --- | --- |
| Correct behavior | All frozen required behavior cases pass; fixture demonstration and live acceptance remain distinct |
| Reusable boundary | A clean independent consumer invokes the pinned capability without original-product imports, private session state, or undeclared configuration |
| Identity and meaning | Mappings preserve required units, tenant/identity scope, roles, cardinality, and missing-data semantics; unsupported transformations are rejected |
| Effects and approval | No unauthorized effects; approval is bound to the exact approved action/payload; changed payloads cannot inherit stale approval |
| Retry/partial failure | Declared retry behavior is exercised; duplicate-effect or ambiguous-outcome cases fail safely instead of silently repeating writes |
| Adapter correctness | Mapping and lookup behavior has positive and negative tests; generated glue does not fabricate data or silently duplicate provider logic |
| Evidence honesty | Run, dependency, input, output and artifact revisions are retained; a green structural check is not outcome or general-reuse proof |

A destructive action, credential exposure, cross-tenant operation, silent semantic corruption, or unapproved mutation is a hard failure regardless of speed. Use sandbox destinations and fake credentials; no real outreach or CRM writes in the pilot without separate explicit approval.

Measure accepted behavior; adapter/debugging and human-review time; model/tool cost and tokens where available; bespoke business code versus adapters/configuration; capability/source edits; time to first working slice; time and effort for the second consumer; and first-use documentation/packaging/maintenance cost. Lines of code and reuse counts are descriptive, not optimization targets. Unobserved cost is marked unknown, not zero.

P2 must freeze the acceptable total effort/cost ceiling for the chosen slice. P6 chooses the simpler baseline if a richer contract does not resolve a named required failure or yield a material improvement under that ceiling. Count metadata authoring, testing, review, operations, and future maintenance, not just consumer-side token savings.

## 9. P4: failure-led repairs and stop rules

Classify the smallest reproducible failure before choosing a layer:

| Failure | First response | Escalation only if needed |
| --- | --- | --- |
| Missing/unclear docs, field mapping, example | Correct ordinary description/example or generated adapter | Tiny profile/conformance rule |
| Wrong units, identity, scope, role or information loss | Explicit field semantics and tested mapping/lookup; reject missing evidence | Targeted LC or mapping-profile experiment, with exact version and separate ownership |
| Missing actual behavior | Source another provider or implement the local residual | New reusable boundary only when justified |
| Retry, auth, approval, partial commit, provider limitation | Existing runtime/provider mechanism and provider-specific tests | Narrow domain effect contract; not a new transaction/workflow engine |
| Requirement meaning is underspecified | Clarify the requirement and acceptance cases | SystemSpec experiment only if a precise semantic IR is needed |
| Discovery/context overhead | Better native search/indexing/context packaging | Minimal metadata change; not a new catalog service |

Stop expanding ACA when the baseline is correct and economical for the chosen product/consumer. Stop an extension when it fails to improve the relevant outcome. Stop execution on a safety/access/budget violation. If a capability is inherently unsuitable, reject it; do not force composition to demonstrate reuse. Re-scope rather than adding every semantic repository or workflow product to rescue an oversized pilot.

## 10. P5/P6: second consumer and lightweight adoption

The first working product is shown before any broad research expansion. Then give a fresh worker a materially different workflow or product requirement that exercises at least one retained capability's meaningful behavior. Use its normal published boundary without silently coordinating new changes with the original builder. Record any necessary versioned change and its cost.

The delivered reusable asset may be a native sub-workflow, normal package, service API, tested adapter, or composition. It need not be a new internal package. Preserve project-specific business rules and rights boundaries. Client-owned code, credentials, and confidential evidence are not promoted into ACA; export only material Brian is entitled to reuse, with review where needed.

Use the existing engagement plan/closeout/evidence seams and existing CI to check the adopted profile. Add only the missing checks, including one negative test per claimed gate. Trusted acceptance configuration must not be controlled solely by an untrusted worker's self-attested snapshot. These controls do not automatically judge design quality or guarantee general reusability.

P6 produces `docs/experiments/independent-composition/RESULTS.md` and a decision in `docs/DECISIONS.md`: baseline sufficient; native convention/configuration sufficient; small ACA extension justified; or result inconclusive with a bounded next action. New evidence is indexed through `docs/PROOF_LEDGER_EXTENDED.md`. Schema changes remain additive/versioned; ADR-014/015 invariants and existing consumers remain intact.

Do not delete or migrate existing ACA, LC, compiler, Foundry, or AES implementations from an audit recommendation alone. Retirement needs its own dependency inventory, replacement acceptance, compatibility/migration checks, and rollback decision. Cross-repo ownership changes require the existing Vision decision route.

## 11. Source trail and remaining uncertainty

Internal basis: [operating rules](../../AGENTS.md), [charter](../ARCHITECTURE_CHARTER.md), [decisions](../DECISIONS.md), [prior proof formulation](../NEXT_PROOF.md), and [preliminary sourcing audit](../../research/synthesis/off-the-shelf-substrate-vs-residual-audit.md).

Official documentation checked on 2026-09-18 supplies starting leads, not provider-fit proof:

- [n8n Execute Sub-workflow](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.executeworkflow/): native sub-workflow invocation and input mapping. This does not establish independent cross-project portability or the full product fit.
- [MCP tools, version 2025-11-25](https://modelcontextprotocol.io/specification/2025-11-25/server/tools): input/output schemas and behavioral annotations; annotations are not unconditional trusted guarantees. This is a checked version, not a claim that it is the latest deployed version.
- [Composio direct execution](https://docs.composio.dev/docs/tools-direct/executing-tools): a documented tool boundary and versioning considerations; the page points agent builders toward sessions. P1 must verify the selected current path rather than copy a legacy example.
- [GitHub protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches): required reviews/checks and bypass considerations, not semantic acceptance automation.

Open items belong to P1/P2: exact product/data access, provider/plan/version, concrete independently authored capabilities, run budget, deployment target, frozen tests, and numerical cost/effort ceiling. They are execution dependencies, not reasons to invent more architecture now.

## 12. Planning completion and next action

This change is complete as a planning artifact when its routes and precedence are consistent, prior evidence is preserved, the diff is documentation-only, and the repository completion gate `python tools/check_bootstrap.py` is verified through local execution or the existing CI. Record pending/unavailable checks honestly; no experiment is marked complete by merging the plan.

**Next action after planning review: P1 — freeze the smallest useful product slice and verify one off-the-shelf baseline.** Then draft the one-page contract and protocol. Do not start by implementing a new ACA schema, conformance framework, or runtime.
