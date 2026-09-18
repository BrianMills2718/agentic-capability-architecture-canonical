# Off-the-shelf substrate vs residual audit

Status: research synthesis; non-normative.
Date: 2026-09-17.

## Decision rule

For every capability in ACA, Linguistic Core, Semantic Foundry, and the Requirement-to-Runtime Semantic Compiler, ask:

> What capability here cannot reasonably be delegated to a mature off-the-shelf substrate without losing the compounding/reuse outcome?

Prefer one product that covers the largest surface. Add a second product only after a concrete limitation appears. Build custom infrastructure only for the remaining residual.

This audit optimizes for **time to a usable product**, not architectural novelty.

## Recommended starting stack

1. **n8n** as the workflow/product shell: workflow composition, execution, connectors, transformations, logs, approvals, and MCP exposure/consumption.
2. **Claude Code or Codex** as planner/adapter author: inspect tools, generate glue, repair workflows, and implement project-local residual code.
3. **GitHub protected branches + CI** as the enforcement boundary for contractor delivery requirements.
4. Add **Pipedream or Composio** only if n8n's integration/tool surface is the limiting factor.
5. Add **Temporal** only if an authentic product requires stronger code-first durable execution semantics than the chosen workflow substrate supplies.
6. Use **OpenAPI/JSON Schema/MCP** for callable interface contracts; use **Arazzo** only when a portable API-workflow representation becomes valuable.

Do not introduce a custom ACA workflow engine, connector runtime, auth layer, transaction manager, saga engine, scheduler, or visual workflow system before this stack demonstrates a concrete gap.

## Current external substrate coverage

| Need | Existing substrate | Audit disposition |
| --- | --- | --- |
| Agent-callable tools | MCP | **delegate** |
| Input/output structural contracts | JSON Schema / OpenAPI / MCP | **delegate** |
| SaaS/API integrations + auth | n8n; Pipedream; Composio | **delegate** |
| Workflow construction/execution | n8n | **delegate first** |
| Agent-generated adapters/transforms | Claude Code / Codex + workflow code nodes | **delegate first** |
| Portable API workflow descriptions | Arazzo | **investigate only if portability is needed** |
| Durable retries/checkpoints/timers/signals | Temporal; workflow platforms | **delegate** |
| Generic transaction/saga orchestration | established workflow/runtime/database substrate | **delegate product responsibility** |
| Generic UI/catalog/search | existing workflow/developer portal products | **delegate unless product evidence says otherwise** |
| Contractor acceptance enforcement | GitHub CI / branch protection / schemas | **delegate mechanics; keep ACA policy** |

## ACA

### Keep

ACA should keep only the contract necessary to make paid work compound:

- a stable way to name the meaningful capabilities a product needs/provides;
- the delivery rule that a worker must inspect existing capabilities and either reuse or explicitly reject suitable candidates;
- explicit separation of selected composition from genuinely project-local residual behavior;
- an independently usable boundary for new reusable behavior when justified;
- closeout/evidence sufficient for the next project or agent to consume what was learned;
- cross-project receipts/knowledge that make Product N+1 start further ahead;
- acceptance checks ensuring the above happened.

This is the **enforceable delivery goal**. The enforcement mechanism is ordinary engineering machinery and is not itself a novelty claim.

### Delegate

- capability execution;
- connector/auth implementation;
- generic workflow orchestration;
- retries/scheduling/events;
- visual workflow editing;
- generic service catalog UI;
- generic package distribution;
- generic observability;
- adapter generation where a coding harness can produce and test the adapter.

### Investigate

- whether ACA needs a custom capability registry at all, versus a thin index over MCP/OpenAPI/n8n/Composio/Pipedream and repository-owned exports;
- whether capability identities add value beyond good tool descriptions and normal search;
- whether semantic/effect metadata materially improves fresh-agent composition;
- whether accumulated rejection/compatibility evidence pays for its maintenance cost.

### Candidate minimum ACA core

    CAPABILITY_PLAN / equivalent
      + capability identity references
      + reuse / reject / local-residual decisions
      + executable-boundary checks
      + CAPABILITY_CLOSEOUT / reuse receipt
      + CI acceptance policy

Everything else is presumptively external.

## Linguistic Core

### Keep

Keep the repository's current narrow role:

- stable publishable predicate/relation vocabulary;
- roles and semantic identities;
- governed source mappings;
- directional/conditional/loss-aware semantic mappings;
- provenance and versioned source meaning.

This may become useful when two independently developed capability interfaces are structurally compatible but semantically ambiguous.

### Do not expand by default

Do not move into Linguistic Core: workflow semantics, runtime effects, retries/idempotency, provider discovery, authorization, transactions, or live world state.

### Investigate

Only after real composition failures, test whether LC annotations help with role mismatch, event-vs-intent confusion, semantic identity mismatch, or lossy adapter generation. If ordinary descriptions plus a strong model work reliably, do not add semantic annotation overhead.

## Requirement-to-Runtime Semantic Compiler

### Keep / prove

The strongest candidate differentiated responsibility is **natural-language requirement -> target-neutral SystemSpec / semantic intent**.

Keep this as research/product candidate only to the extent experiments show that the intermediate semantic contract improves correctness, reuse, predictability, or verification over direct agent-to-workflow/code generation.

### Delegate

Presumptively delegate generic workflow execution, generic scheduling, generic persistence, generic connector code, and target runtime reliability machinery. WTL/world-model/planning work should remain research unless an authentic product requires semantics that mature substrates cannot express.

### Investigate

Compare the same tasks and acceptance tests under:

    requirement -> Claude/Codex -> n8n/tools
    requirement -> SystemSpec -> Claude/Codex -> n8n/tools

Keep the semantic-compiler layer only where it creates measurable advantage or enables a requirement the direct path cannot safely satisfy.

## Semantic Foundry

Semantic Foundry contains valuable semantic-integration research, but its later phases cross into mature runtime-product categories.

### Keep as differentiated research

- heterogeneous semantic-resource integration;
- mapping/alignment claims;
- provenance and uncertainty;
- reasoning/translation research;
- proposal-vs-accepted-truth boundaries;
- observation/evidence versus semantic-claim separation;
- semantic federation and governed semantic write-back.

### Delegate as product infrastructure

Treat the following as **research fixtures / evidence, not owned product infrastructure**, unless provider sourcing identifies a concrete residual:

- Phase 15 generic external connectors;
- Phase 16 transaction execution/idempotency/rollback/compensation machinery;
- Phase 17 durable workflow/saga runtime;
- Phase 18 event-driven orchestration, duplicate handling, durable waits, approvals, and timeouts.

The semantic distinction those phases demonstrate may remain valuable even when execution is delegated. For example, 'transaction committed' must not automatically imply 'requirement satisfied.' Preserve that epistemic contract; delegate the transaction engine.

### Likely retained seam

    external runtime observation
      -> semantic/evidence interpretation
      -> proposal
      -> reviewed semantic write-back

That is different from owning the workflow runtime itself.

## AES

Keep AES focused on engineering loop integrity, evidence, evaluation, feedback, and replanning. Delegate commodity execution substrate rather than duplicating workflow/tool platforms.

## Immediate experiment

Build one authentic paid-work-shaped product using the smallest stack:

    Claude/Codex + n8n + existing connectors + GitHub CI

Require the ACA delivery contract, but use no custom ACA runtime.

Measure time to working product, bespoke code, reused capabilities, adapter size/count, new reusable boundaries left behind, semantic failure modes, runtime failure modes, and whether a fresh next project can reuse the contributed behavior.

Only add Composio/Pipedream, Semantic Compiler, Linguistic Core annotations, Semantic Foundry semantics, Temporal, or new ACA code in response to an observed failure.

## Decision heuristic

For every proposed custom subsystem:

    Can a mature product do it?
      yes -> use it
      partially -> use it + implement only the residual
      no -> prove the gap with an authentic product task, then build the minimum

The desired result of this audit may be a much smaller codebase. That is a success condition, not a loss of architectural ambition.