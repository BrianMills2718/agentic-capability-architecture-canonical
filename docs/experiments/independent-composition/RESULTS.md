# Independent composition pilot — current results

Status: P3 Python baseline with reusable composition boundaries.
Recorded: 2026-09-19.

## Completed

- P1 product slice frozen (Twitter Prospector behavior).
- n8n selected as first single-product workflow baseline (P1 decision).
- P2 minimal composability profile and protocol frozen.
- Evaluator fixtures frozen (5 acceptance cases, hard-failure rules).
- Importable n8n fixture workflow created using only built-in Manual Trigger and Code nodes.
- Static workflow shape and evaluator invariants checked.

**P3 Python baseline: Reusable composition boundaries**

Implemented four ordinary Python functions that can be composed independently:

1. **`structural_adapter(producer_output, mapping)`**
   - Maps producer field names to consumer input names
   - Raises KeyError if producer key missing
   - Preserves value types
   - Tests: positive mapping, negative missing key, edge empty mapping, type preservation

2. **`semantic_reject(data, forbidden_patterns)`**
   - Checks for forbidden semantic assumptions
   - Returns rejection reason if risk detected, None if safe
   - Pattern matching: `{"field": "user_id", "risk": "..."}`
   - Tests: user_id→crm_account_id rejection, confidence→business_relevance rejection, multi-pattern matching

3. **`approval_gated_handoff(candidate, review_decision)`**
   - Prepares handoff only if decision == 'shortlist'
   - Returns None for 'reject', 'unreviewed', unknown
   - Score (0.99 or otherwise) does not bypass gate
   - Tests: positive shortlist, negative reject/unreviewed/unknown, score does not bypass

4. **`IdempotentLocalSink`**
   - Records handoffs by logical_handoff_id
   - Repeated call for same ID: `new_record=False`, count unchanged
   - Different IDs each create separate records
   - Tests: first call creates, second deduplicates, multiple IDs increase count

Executable boundary: each function has public input/output contract, no hidden state except sink.

**Test suite: 31 focused tests (25 composition + 6 provider-adapter tests)**

Tests exercise functions directly with positive and negative controls:
- Positive: valid inputs produce expected outputs
- Negative: invalid/forbidden inputs are rejected correctly; score does not bypass approval gate
- Edge cases: empty inputs, multiple patterns, repeated calls
- Integration: each acceptance case invokes functions end-to-end; review decisions determine handoff

## P3 evidence: Python composition boundary validation

### Reusable Functions Tested

| Function | Positive tests | Negative tests | Controls |
| --- | --- | --- | --- |
| structural_adapter | field mapping, type preservation | missing key | edge empty |
| semantic_reject | reject user_id risk | accept when safe | multi-pattern |
| approval_gated_handoff | shortlist→handoff | reject/unreviewed/unknown→None | score irrelevant |
| IdempotentLocalSink | record deduplication | repeated calls same ID | different IDs tracked |

### Acceptance Case Results

| Case | Status | Verification |
| --- | --- | --- |
| normal-composition | pass | reviews derived from score threshold + explicit routing |
| structural-adapter | pass | field mapping without semantic error |
| semantic-mismatch | pass | user_id rejection, confidence rejection |
| approval-binding | pass | score 0.99 + reject decision = no handoff |
| retry-duplicate | pass | 2 invocations, 1 effect, via IdempotentLocalSink |

### Machine-Readable Receipt

All five cases produce JSON receipt to stdout:
```json
{
  "pilot": "ACA-PLAN-001 independent composition P3",
  "executor": "python_baseline",
  "cases_executed": 5,
  "cases_passed": 5,
  "overall_passed": true,
  "results": { ... }
}
```

## Provider-boundary progress

Inspection of the existing Twitter prospecting implementation found the active collection provider is **TwitterAPI.io**, not the native X API assumed in the original P1 provider-fit note. The observed ordinary provider contract is:

- base URL: `https://api.twitterapi.io`;
- read-only search endpoint: `/twitter/tweet/advanced_search`;
- authentication header: `X-API-Key`;
- local credential name: `TWITTERAPI_IO_API_KEY` (value not recorded here).

A minimal read-only adapter now exists at `twitterapi_io_collection.py`. It normalizes provider posts into the pilot collection shape while preserving provider post identity and source URL. Six fake-transport tests verify endpoint construction, credential-safe error handling, normalization, missing-credential behavior, and malformed-provider rejection. No live provider request is claimed yet.

## Not yet claimed

No live n8n execution, live TwitterAPI.io/X request, LLM scoring call, human approval event, CRM write, provider latency/cost observation, or second-consumer reuse has occurred.

## Integration substrate: assistant-to-n8n overhead vs. Python/API composition

The n8n workflow baseline (P1 selection) introduced:
- assistant-to-n8n orchestration overhead: how to author/deploy/invoke n8n workflows
- workflow JSON schema coordination (not a runtime issue)
- execution log interpretation gap (n8n logs vs. test logs diverge)
- semantic coupling: composition constraints embedded in n8n Code node syntax

The Python baseline demonstrates that composition logic can be:
- expressed as ordinary Python functions with standard contracts
- tested with direct function calls + negative controls
- verified without external orchestration runtime
- extended to wrap provider APIs directly (X, LLM, CRM)

**Decision: Python/API composition is the next execution route.**

Rather than orchestrating composition through n8n, next phase should:
1. Execute the existing TwitterAPI.io collection boundary live through the new read-only adapter and capture provider evidence
2. Implement scoring as a Python function calling the selected LLM (with deterministic test mode)
3. Implement review routing as a Python function (approval in tests only)
4. Keep CRM handoff on the idempotent local/test sink
5. Compose these functions in a lightweight Python orchestrator

This avoids:
- assistant-to-n8n control overhead (how to orchestrate an external system)
- workflow versioning/import coordination
- execution log divergence (single Python log trail)
- coupling composition semantics to specific orchestrator syntax

Retains:
- frozen n8n fixture for reference/validation
- compositional boundaries defined in protocol
- test coverage of all cases
- evidence trail

## Current unresolved P2/P3 gates

To run live composition:
1. Confirm the existing TwitterAPI.io credential still has read-only search access/quota by executing one bounded request
2. Selected scoring provider/model (with test mode)
3. Review approval mechanism/channel
4. Test CRM/local sink
5. Run budget and time ceiling

## Interpretation

P3 demonstrates that independent composition is achievable without ACA-specific metadata/runtime:
- Four reusable Python functions define composition boundaries
- Each function has explicit contract (not inferred)
- Tests use positive/negative controls, not fixture reassertion
- Semantic safety is enforced (not assumed)
- Approval binding is programmatic (not workflow magic)
- Idempotent side effects are real (tracked state, not counting duplicates)

The baseline proves the frozen behavior can be expressed and validated in pure Python. Next phase proves it can accept real provider data (X API, LLM, approval) and compose them without n8n.

Do not add semantic metadata, a registry service, or a custom ACA runtime before a named live failure survives the repair sequence in the frozen protocol.
