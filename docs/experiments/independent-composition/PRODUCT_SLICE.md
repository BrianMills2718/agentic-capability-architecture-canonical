# P1 product slice — Twitter Prospector

Status: frozen pilot slice for ACA-PLAN-001 P1.
Recorded: 2026-09-18.
Source basis: Brian's concrete Twitter Prospector review prototype supplied in the planning conversation.

## Outcome

Deliver one bounded prospecting workflow that:

1. accepts explicit prospect criteria and an X/Twitter query;
2. collects candidate posts/accounts;
3. scores candidate relevance against the configured criteria;
4. routes sufficiently relevant candidates to human review;
5. records shortlist/reject decisions with reasons;
6. prepares approved candidates for downstream CRM handoff;
7. retains step-level execution evidence and explicit non-claims.

The first pilot is a sandbox/demo workflow. It does not send outreach or perform a production CRM mutation without separate approval.

## Frozen behavior

The reference run shape is:

```text
criteria
  -> collect candidates
  -> score relevance
  -> human review
  -> shortlist handoff
       |
       +---- feedback may inform later criteria
```

A review result may inform a later run, but this pilot does not automatically rewrite targeting criteria.

## Acceptance cases

### A1 — collection

Given a configured X/Twitter search query, the workflow returns concrete candidate records with stable run-local IDs and original source text/URLs or provider identifiers sufficient for review.

### A2 — scoring

Every collected candidate receives:

- one numeric relevance score;
- explicit supporting signals/reasons;
- the scoring input revision/prompt/model configuration needed to interpret the result.

The score is a prioritization signal, not an automatic commercial-value claim.

### A3 — review routing

Candidates at or above a configured review threshold become reviewable. Human review can record at least:

- shortlist;
- reject;
- reason.

A score alone cannot create an approved handoff.

### A4 — handoff

Only an explicit shortlist decision may produce the handoff payload. For the pilot, handoff may be a local table/file/test CRM destination. A real external CRM mutation requires a separately authorized execution step.

### A5 — evidence

The run must retain enough data to answer:

- what criteria/query were used;
- what candidates were returned;
- what scores/reasons were produced;
- what the human decided;
- what was prepared for handoff;
- what each observation does not prove.

### A6 — reusable boundaries

The pilot should expose or retain independently invokable boundaries for at least:

- candidate collection/search;
- candidate scoring;
- review/approval;
- CRM handoff preparation.

These may be native nodes, APIs, sub-workflows, MCP tools, normal functions, or generated adapters. They do not need an ACA-specific runtime wrapper.

## Explicit non-goals

The slice does not need:

- automatic outreach;
- a bespoke ACA workflow engine;
- an ACA connector platform;
- a new ontology;
- universal prospect scoring semantics;
- proof of X API coverage/reliability;
- proof that relevance score predicts conversion;
- proof that shortlisted candidates have commercial value.

## P1 completion rule

P1 is complete when one off-the-shelf baseline is selected for the pilot with:

- a concrete route for every acceptance case;
- named external dependencies and access constraints;
- no custom platform component required before P2;
- unresolved gaps explicitly recorded.
