# P3 dry-run n8n baseline

This directory contains an importable n8n workflow artifact for the frozen Twitter Prospector fixture.

## What it proves

The artifact is intended to prove only that the frozen P1 behavior can be represented as an ordinary n8n workflow using built-in Manual Trigger and Code nodes:

```text
manual trigger
  -> load frozen candidates
  -> score fixture candidates
  -> simulate frozen human-review decisions
  -> build local-only handoff + assurance receipt
```

It performs no network call, no live X search, no model call, no production CRM write, and no outreach.

## Why the review step is simulated

P3 live execution is still gated on an actual n8n instance and the selected review channel. The dry-run uses the already-frozen reviewer dispositions so the workflow shape and evaluator can be prepared without inventing live evidence.

When live access exists, replace:

- `Load Frozen Candidates` with direct X API collection through HTTP Request;
- `Score Fixture Candidates` with the selected scoring provider/sub-workflow;
- `Simulate Human Review Fixture` with an n8n wait/approval path;
- the local handoff with the selected sandbox CRM destination.

Do not change the frozen evaluator cases to make the implementation pass.

## Import shape

The workflow uses n8n's normal workflow JSON fields: `name`, `nodes`, `connections`, and `settings`. It intentionally uses only built-in nodes.

## Expected final receipt

The final node emits one run receipt containing all candidate records, one shortlisted handoff record for `cand-001`, explicit flags that no production CRM write/outreach occurred, and explicit non-claims.

## Live gates

Execution against real providers still requires:

1. n8n instance/deployment access;
2. X developer/API credentials and suitable endpoint access;
3. scoring provider/model;
4. review destination;
5. sandbox CRM/local sink;
6. run budget/time ceiling.
