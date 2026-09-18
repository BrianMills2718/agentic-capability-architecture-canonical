# Independent composition pilot — current results

Status: P3 dry-run preparation only; no live provider execution yet.
Recorded: 2026-09-18.

## Completed

- P1 product slice frozen.
- n8n selected as the first single-product workflow baseline.
- P2 minimal composability profile and protocol frozen.
- Evaluator fixtures frozen.
- Importable n8n fixture workflow created using only built-in Manual Trigger and Code nodes.
- Static workflow shape and evaluator invariants checked:
  - required n8n workflow fields present;
  - node names unique;
  - five-node fixture flow present;
  - normal review IDs remain cand-001/cand-002;
  - rejected candidate cannot hand off;
  - retry fixture permits at most one external effect.

## Not yet claimed

No live n8n execution, X API request, LLM scoring call, human approval event, CRM write, provider latency/cost observation, or second-consumer reuse has occurred.

## Current blocking dependencies

1. runnable n8n instance/deployment;
2. X developer/API credentials and sufficient search access;
3. selected scoring provider/model;
4. review destination;
5. sandbox CRM/local sink;
6. approved run/time/cost ceiling.

## Interpretation

Nothing observed so far requires a larger ACA layer. The fixture can be expressed as a normal n8n workflow and ordinary generated glue. The meaningful test remains live independent composition and then reuse by a second consumer.

Do not add semantic metadata, a registry service, or a custom runtime before a named live failure survives the repair sequence in the frozen protocol.
