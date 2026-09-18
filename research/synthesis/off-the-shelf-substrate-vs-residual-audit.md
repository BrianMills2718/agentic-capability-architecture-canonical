# Off-the-shelf substrate vs residual audit

Status: preliminary research synthesis; non-normative; provider fit not yet established.
First recorded: 2026-09-17. Corrected: 2026-09-18.

## Correction and planning route

The initial draft overemphasized enforcement/closeout as the minimum ACA technical core and spoke too definitively about a starting stack. The clarified goal is practical **independent capability composability** and fast usable-product delivery. Contractor acceptance and CI remain supporting controls, not the technical research question.

The proposed execution sequence, acceptance criteria, dependencies, owners, and stop rules now have one home: [ACA-PLAN-001](../../docs/plans/2026-09-18-minimal-composability.md). This note supplies sourcing leads, not another execution plan.

No live provider-fit evaluation was performed for the original audit. Statements below are candidate dispositions to investigate, not proof that a named product supplies the required invariants. The prior draft is retained in Git at commit `1493dd89702c3d933f26e9fdb7cb6017dae43a61`.

## Decision rule

> What capability cannot reasonably be delegated to an existing substrate without losing correct delivery and practical reuse?

Prefer one sufficient product, then a small integration. Novelty is not a goal. Count setup, hosting, paid features, adapter work, testing, review, licensing/embedding constraints, and maintenance. A standards document is not a running service; a workflow engine does not make every external action idempotent.

## Candidate sourcing map — not selected dependencies

| Need | Candidate to examine | What must be checked |
| --- | --- | --- |
| Workflow-heavy product | n8n | Actual slice, callable/reusable sub-workflows, exporting/importing, data mapping, credentials, waits, logs, licensing/plan and operational limits |
| Application-heavy product | Existing application/runtime and ordinary packages; current Frappe path where appropriate | Whether using the existing platform is cheaper than introducing a new workflow product |
| Tool access and connector authentication | Existing platform first; Composio or Pipedream only for a demonstrated gap | Exact tool availability, auth scope, custom capability binding, versions, terms, and provider guarantees |
| Callable structural interface | Native function types, OpenAPI/JSON Schema, MCP where useful | Required input/output/error facts and deployed version; not semantic equivalence or automatic safety |
| Adapters | Existing coding harness plus normal tests | Meaning, missing data, identity, transformations, extra calls, effects, and reimplementation cost |
| Durable execution | Selected runtime first; Temporal only if needed | Required retry/checkpoint/failure behavior and activity-side idempotency; not generic automatic rollback |
| Portable API workflow representation | Arazzo only if portability matters | Actual implementation support and execution needs; not an assumed runtime |
| Contractor acceptance | Existing GitHub/CI/engagement mechanisms | Trusted check configuration, appropriate access/review, and honest limits of structural tests |

Selected official references checked during planning are recorded in ACA-PLAN-001. Their documented features do not replace a product-fit test.

## Candidate ACA technical core

```text
profile of existing composable interfaces
        +
only the conformance tests needed for observed failures
```

This could be a short convention and tests, with no new service or schema. Do not invent a competing registry, transport, workflow language, or runtime. Generated adapters are an ordinary acceptable part of composition.

Existing capability references, planning artifacts, reuse receipts, and CI support this objective. They remain compatible but do not become a new governance product. A package plus a manifest is not sufficient evidence of easy independent composition.

## Cross-repo candidate dispositions

| Area | Preserve | Product-adoption posture |
| --- | --- | --- |
| ACA | Honest public boundaries, tested invariants, consumer compatibility and recorded evidence | Test the smallest composability profile; delegate execution and supporting machinery |
| Linguistic Core | Vocabulary, roles, versioned mappings and its independent construction goal | No mandatory expansion; consider a narrow semantic annotation only for an observed role/scope/loss failure |
| Requirement-to-Runtime Semantic Compiler | SystemSpec and world-model research/evidence | Optional consumer layer if precise requirement semantics are needed; not a mandatory intermediate step |
| Semantic Foundry | Semantic integration/reasoning and observation-versus-claim distinctions; existing tests and fixtures | Source commodity execution externally where fit is demonstrated; do not delete its runtime research from this recommendation |
| AES | Existing engineering-loop authorities and evidence boundaries | Consume results through current seams; no competing generic orchestration/governance platform |

Foundry's connector, transaction, saga, and event phases are relevant design/test donors, not evidence that their implementations should automatically become the product runtime. Conversely, the existence of an external workflow product is not proof that it preserves every Foundry invariant. Replacement requires a tested mapping and migration/rollback plan.

An ACA sourcing note cannot transfer another repository's authority, halt its independent research, or authorize removing code. Cross-repo changes follow the existing Vision decision route.

## Decision evidence still missing

The next work must identify the actual product slice and independently authored capabilities, check one plausible baseline, freeze the consumption/test conditions, deliver the composition, and measure a second consumer. If descriptions and ordinary tested adapters suffice, retain that result and stop adding ACA machinery. If not, fix the specific failure and measure the smallest change.

There is no observed result in this note establishing n8n fit, safe arbitrary composition, commercial compounding, or a required semantic layer.
