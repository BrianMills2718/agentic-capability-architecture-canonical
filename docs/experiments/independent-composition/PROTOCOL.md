# Independent composition pilot protocol

Status: frozen P2 candidate; execution pending access/budget confirmation.
Plan: ACA-PLAN-001.
Product slice: Twitter Prospector.

## Question

Can a fresh coding agent compose independently authored capabilities into the frozen Twitter Prospector product using ordinary published interfaces plus generated adapters, without a bespoke ACA runtime?

## Baseline

Use:

- n8n as the workflow substrate;
- direct/native provider interfaces where available;
- X/Twitter API through n8n HTTP Request for collection;
- a selected LLM/API or deterministic scorer for relevance scoring;
- n8n-native wait/approval mechanism for human review;
- local/test CRM handoff;
- Claude Code or Codex as the composer/adapter author.

No additional ACA runtime metadata is supplied beyond the normal public contracts and this pilot's frozen behavior requirements.

## Capability independence

For the pilot, treat the following as separate capability boundaries even if the provider happens to host several of them:

1. candidate.search
2. candidate.score
3. human.review
4. crm.handoff.prepare

Prefer provider-native or already independently authored boundaries. Do not coordinate their schemas solely to make the final workflow easy.

Freeze exact interface/provider revisions before the composer starts.

## Fresh composer

Composer D receives:

- the frozen PRODUCT_SLICE behavior;
- public provider documentation;
- normal schemas/interfaces;
- credentials/access needed for the sandbox;
- normal examples;
- permission to inspect public/source interfaces and generate adapters.

Composer D does **not** receive:

- a prewritten final workflow;
- hidden evaluator expected outputs;
- private implementation/session context from capability authors;
- an ACA-specific target architecture.

## Frozen acceptance fixtures

Before execution, create fixtures covering:

1. **Normal composition** — three candidates collected, all scored, two routed to review, one shortlisted.
2. **Structural adapter** — collection output field names do not directly match scoring input names; agent must map them.
3. **Semantic mismatch** — one field with compatible JSON type but incompatible meaning (for example score confidence vs business relevance, or user ID vs account ID); composition must not silently equate them.
4. **Approval binding** — only explicit shortlist decision creates handoff.
5. **Retry/duplicate** — repeated handoff preparation for the same logical shortlist item must not create an unauthorized duplicate external effect; for the pilot use a local/test sink.
6. **Second-consumer readiness** — at least one retained boundary can later be invoked by a materially different workflow without importing Twitter Prospector private implementation.

## Measurements

Record:

- acceptance cases passed;
- time to first working workflow;
- agent turns and model/tool cost where available;
- lines/size of generated adapter/config code;
- number of provider/capability changes required;
- human interventions;
- semantic errors;
- operational/retry errors;
- documentation/interface defects;
- total setup/integration time;
- whether a second consumer can invoke the retained boundary.

Do not optimize for fewer lines or more reuse in isolation.

## Failure classification

Classify each failure before changing ACA:

- provider/access failure;
- missing actual behavior;
- structural schema mismatch;
- unclear documentation/example;
- semantic mismatch;
- operational/effect mismatch;
- agent planning/error;
- evaluator/fixture defect.

## Repair sequence

Apply the cheapest fix first:

1. ordinary docs/example correction;
2. generated adapter/validation;
3. provider-native configuration or metadata;
4. tiny composability-profile addition;
5. targeted semantic/effect experiment only if 1–4 fail.

Only step 4 creates a candidate ACA extension.

## Comparison rule

If the baseline works correctly within the frozen cost/effort ceiling, do **not** add richer ACA semantics simply to improve architectural elegance.

If an extension is added, freeze the failing task and compare:

- baseline interface;
- baseline + exactly one extension.

Use fresh runs under equivalent access and budgets.

## Safety

- no live outreach;
- no production CRM writes;
- no credential material committed to artifacts;
- sandbox/test destinations only;
- exact approved payload required before any external side effect;
- failures and rejected compositions are retained.

## Execution gates still open

Before running the pilot, record:

- X developer/API access;
- exact n8n deployment/plan;
- scoring provider/model;
- review channel;
- test CRM/local sink;
- run budget and time ceiling;
- fixture revisions;
- composer model/harness version.

Until those are fixed, this document freezes methodology but does not claim an executed experiment.