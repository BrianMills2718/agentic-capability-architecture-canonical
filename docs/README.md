# Local Documentation Map

> **Global navigation authority:** start at the [Vision knowledge index](https://github.com/BrianMills2718/vision/blob/main/wiki/index.md), then follow the [Agentic Capability Architecture project guide](https://github.com/BrianMills2718/vision/blob/main/wiki/projects/agentic-capability-architecture.md).
>
> This file organizes **repository-local technical documentation only**. It is not a second global “start here” page.

## Authority order

When documents disagree, resolve the conflict in this order:

1. executable code, schemas, tests, and machine-readable manifests for facts they directly define;
2. accepted/current architecture decisions and the architecture charter;
3. the current proof ledger and explicit current status files;
4. operational runbooks;
5. experimental/research documents;
6. historical proof logs, session context, superseded plans, and preserved source material.

Human-readable status summaries should not duplicate volatile machine state when a manifest/catalog can supply it. A disagreement between machine-readable authorities is a defect to fix, not a reason for README prose to choose a winner silently.

## Current architecture and operating rules

| Document | Role |
| --- | --- |
| [`ARCHITECTURE_CHARTER.md`](ARCHITECTURE_CHARTER.md) | Current local architecture mission, boundaries, sourcing order, evidence model, and non-goals. |
| [`DECISIONS.md`](DECISIONS.md) | Repository-local durable decisions. Cross-repo semantic/interface policy lives in the Vision ADR linked from the global wiki. |
| [`PROJECT_WORKFLOW.md`](PROJECT_WORKFLOW.md) | Required project implementation/reuse workflow. |
| [`REUSE_PROMOTION.md`](REUSE_PROMOTION.md) | Current internal promotion discipline and the broader evidence factors that sit above the minimum reuse-count checks. |
| [`ARCHITECTURE_ONE_DIAGRAM.md`](ARCHITECTURE_ONE_DIAGRAM.md) | Explanatory view only; not an independent source of architecture truth. |
| [`DEFINITION_OF_DONE.md`](DEFINITION_OF_DONE.md) | Current per-project/material-change completion standard and interpretation of the completed bootstrap. |

`ARCHITECTURE.md` is retained as a compatibility pointer to the charter rather than a second architecture specification.

## Current proof and status

| Document | Role |
| --- | --- |
| [`PROOF_LEDGER_EXTENDED.md`](PROOF_LEDGER_EXTENDED.md) | **Current proof-status index.** Completed and pending proof claims should be reconciled here first. |
| [`FRAPPE_TEST_STATUS.md`](FRAPPE_TEST_STATUS.md) | Current record of the baseline real-Frappe lifecycle proof result. |
| [`NEXT_PROOF.md`](NEXT_PROOF.md) | Current formulation of the remaining isolated registry-discovery research question; it also supersedes the old bootstrap proof plan. |

## Operational runbooks and checks

| Document | Role |
| --- | --- |
| [`FRAPPE_INTEGRATION_RUNBOOK.md`](FRAPPE_INTEGRATION_RUNBOOK.md) | Current local real-Bench regression invocation; the executable script owns the app/site matrix. |
| [`EXPORT_CHECKLIST.md`](EXPORT_CHECKLIST.md) | Current post-bootstrap export/handoff checklist. |

## Experimental and research material

| Document / directory | Role |
| --- | --- |
| [`PRIMITIVE_CAPABILITY_THESIS.md`](PRIMITIVE_CAPABILITY_THESIS.md) | Falsifiable research thesis; not settled architecture. |
| [`../architecture/primitive_model/`](../architecture/primitive_model/) | Experimental primitive/composition models and evidence. |

Primitive labels may be useful semantic vocabulary without implying that this repository should own a runtime implementation of each primitive.

## Historical evidence and preserved context

These files are intentionally retained because they explain how the current rules were learned. Their own headers should identify them as historical/fixture material where they could otherwise be mistaken for current status.

| Document | Status |
| --- | --- |
| [`FRESH_AGENT_PROOF.md`](FRESH_AGENT_PROOF.md) | Historical iteration log; current outcome is summarized at its top and in the proof ledger. |
| [`ACCEPTANCE_RUNBOOK.md`](ACCEPTANCE_RUNBOOK.md) | Historical runbook for the original `beta_reference` bootstrap acceptance fixture. |
| [`ACCEPTANCE_TEST.md`](ACCEPTANCE_TEST.md) | Historical acceptance fixture/specification; its forced internal-provider choices are not the current general sourcing policy. |
| [`ACCEPTANCE_REHEARSAL_RESULT.md`](ACCEPTANCE_REHEARSAL_RESULT.md) | Historical rehearsal evidence, reconciled with the later completed proofs. |
| [`FRAPPE_CI_PROOF.md`](FRAPPE_CI_PROOF.md) | Baseline historical proof narrative; the successful run remains evidence for its recorded revision. |
| [`REFERENCE_IMPLEMENTATION.md`](REFERENCE_IMPLEMENTATION.md) | Early reference/proof fixture, not a product roadmap. |
| [`SESSION_CONTEXT_2026-09-06.md`](SESSION_CONTEXT_2026-09-06.md) | Historical dated architecture checkpoint. |
| [`WORKING_CONTEXT.md`](WORKING_CONTEXT.md) | Historical accumulated implementation context; current sourcing/architecture documents override its early capability-first workflow. |
| [`SOURCE_MATERIALS.md`](SOURCE_MATERIALS.md) | Preserved source/provenance notes with an explicit authority boundary. |

## Machine-readable authorities

- `../capabilities/*/capability.yml` — capability-local metadata and evidence.
- `../capability_registry.yml` — current checked-in registry/catalog surface. Clean-mainline direction is to derive catalog views from capability manifests and real public interfaces rather than multiply hand-authored authorities.
- `../reuse_candidates.yml` — candidate evidence queue.
- `../schemas/` — machine-readable contracts.
- `../AGENTS.md` — coding-agent operating rules.

## Documentation rule

Cross-repo topology and navigation belong in the Vision wiki. Local documents should explain local contracts, procedures, evidence, and implementation details; they should link outward rather than copy the global map. Historical records should be preserved and labeled, not silently rewritten as if they always reflected later decisions.
