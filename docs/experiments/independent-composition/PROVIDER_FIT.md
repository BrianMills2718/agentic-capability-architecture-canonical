# P1 provider-fit record — Twitter Prospector baseline

Status: selected pilot baseline; live access not yet exercised.
Recorded: 2026-09-18.
Plan: ACA-PLAN-001 P1.

## Selection

**Selected first baseline: n8n as the single workflow/orchestration product.**

Use provider APIs and credentials through n8n's existing nodes or generic HTTP Request node. Do not add Composio, Pipedream, Temporal, Arazzo, Linguistic Core, Semantic Foundry, or new ACA runtime code unless an observed pilot failure justifies them.

The selection optimizes for the smallest product count, fast delivery, inspectable workflow execution, and cheap adapter/transform escape hatches.

## Why n8n fits the frozen slice

| Need | n8n route | P1 assessment |
| --- | --- | --- |
| Configure query/criteria | workflow inputs/configuration | fit |
| Search X/Twitter | generic HTTP Request to X API using user-owned developer credentials | fit in principle; live credential/API-plan validation pending |
| Normalize candidate records | expressions / mapping / Code node | fit |
| Score relevance | LLM node/API call or deterministic scoring sub-workflow | fit |
| Human review | wait/approval pattern; simple approval-capable integrations exist; generic Wait path available for more complex review | fit |
| Prepare CRM handoff | native CRM node when available or HTTP Request/local sink | fit |
| Execution history | n8n execution history | fit |
| Reusable workflow pieces | sub-workflows / callable workflow boundaries | fit for pilot |
| Agent-generated glue | normal code/expression nodes authored by Claude Code/Codex | fit |
| Source control | n8n source-control features exist on higher plans; pilot may instead retain exported workflow artifacts in Git | plan/cost dependent, not required for first local pilot |

## External dependencies

The workflow platform does not remove the underlying service dependencies:

1. **X/Twitter API access.**
   - Requires a developer app/API credentials and an X API plan that permits the needed search endpoint.
   - This is the main unresolved access dependency.
2. **Model access** if LLM scoring is used.
   - Provider/model is not fixed by ACA.
3. **CRM target** for any live handoff.
   - Pilot should use a local/test target unless a live destination is separately approved.

## X/Twitter provider note

n8n does not need a dedicated X node for this pilot because its HTTP Request capability can call an arbitrary API. The pilot should bind directly to the current X API contract rather than introduce a second integration product solely for X.

### Composio fallback

Composio is the preferred first fallback if direct X authentication/tool handling becomes materially costly. Current Composio documentation exposes a versioned Twitter/X toolkit with recent/full-archive search and other actions, but it requires a customer-owned X developer app/credentials. Therefore it simplifies tool/auth integration but does **not** eliminate the core X access dependency.

### Pipedream disposition

Do not select Pipedream for the X portion of this pilot without fresh confirmation. Current Pipedream community support statements say X is not currently supported after X asked for removal, despite stale integration pages remaining searchable. This makes it a weaker baseline for this specific slice.

## Why no second product yet

Adding Composio before direct n8n/X validation would create:

- another account and billing surface;
- another schema/version boundary;
- another source of execution logs;
- another integration seam;

without yet proving a problem that n8n + direct API access cannot solve.

The pilot therefore starts:

```text
X API
  -> n8n collection
  -> normalize
  -> score
  -> human review
  -> local/test CRM handoff
```

Claude Code/Codex may generate expressions, Code-node adapters, request mappings, and tests.

## Unresolved P1 gates

P1 provider fit is selected, but **live fit is not yet proven**. Before P3 execution, P2 must record:

- exact X endpoint(s) and required API access;
- available X credentials/account plan;
- selected n8n deployment/plan;
- selected scoring model or deterministic scoring mechanism;
- sandbox review channel;
- sandbox CRM/handoff destination;
- cost/time ceiling;
- frozen acceptance fixtures.

If X API access is unavailable or uneconomic, re-source the collection capability instead of expanding ACA.

## P1 decision

Proceed to P2 with **n8n-only workflow substrate as the baseline**, subject to X access validation.

ACA contributes no runtime component at this stage. Its role is limited to the independent-composition contract/protocol that P2 will freeze and test.
