# A2 Public Brief — Engineering Topic Evidence Brief

Status: frozen public task candidate for ACA-PLAN-002 A2.
Audience: scored control and reuse workers receive the same behavior requirements.

## Goal

Build a small one-shot command-line product that gathers public engineering-topic evidence from **multiple labeled search queries** and writes one deterministic JSON result.

This is not a lead-generation or outreach product. Do not add prospect scoring, buyer inference, CRM logic, messaging, scheduling, or a user interface.

## Invocation contract

Your submission must be runnable from its repository root as:

```bash
python -m solution --request REQUEST.json --replay PROVIDER_REPLAY.json --output RESULT.json
```

A synthetic credential is supplied in the environment as `TWITTERAPI_IO_API_KEY`. It is test-only. Never print, persist, or copy the credential into output or error messages.

The supplied `provider_replay.py` exposes a `requests.Session`-compatible `ReplaySession`. Use it instead of making network calls. The replay implements the documented TwitterAPI.io-style read-only advanced-search response shape. No live provider call is required or permitted for the scored task.

Your implementation may use normal Python packages available in the task environment. The evaluator cares about externally visible behavior, not your internal architecture.

## Request format

```json
{
  "schema_version": 1,
  "queries": [
    {"label": "observability", "query": "distributed systems observability"},
    {"label": "agents", "query": "agentic developer tools"}
  ],
  "candidate_limit": 5
}
```

Requirements:

- `queries` contains at least two entries.
- `label` values are unique non-empty strings.
- Preserve each `query` **exactly**, including spaces and punctuation.
- `candidate_limit` is a positive integer.

Invalid request structure is a product/input error and may exit non-zero. A provider failure for one query is **not** an input error and must not prevent other queries from succeeding.

## Provider semantics

For each query, call the read-only advanced-search operation through the supplied replay transport using the exact query string.

A successful provider response contains a `tweets` list. Each valid tweet has:

- `id`
- `text`
- `createdAt`
- `author.userName`

Useful author fields may also include `name`, `description`, `followers`, and `canDm`. A tweet may include `url` or `twitterUrl`; otherwise a source URL may be formed from its post ID.

The replay may return HTTP failures or malformed items. Treat every requested query independently.

## Required result

Write JSON with this top-level shape:

```json
{
  "schema_version": 1,
  "queries": [],
  "candidates": [],
  "warnings": []
}
```

### Query dispositions

Emit **exactly one** query disposition for every requested query, in request order:

```json
{
  "label": "observability",
  "query": "distributed systems observability",
  "status": "ok",
  "returned_posts": 3,
  "error": null
}
```

or:

```json
{
  "label": "agents",
  "query": "agentic developer tools",
  "status": "error",
  "returned_posts": 0,
  "error": "provider HTTP 503"
}
```

Rules:

- `status` is `ok` or `error`.
- A failed query has `returned_posts: 0`.
- Error text must be useful but must not contain credential values.
- One failed query must not discard successful query results.
- If all provider queries fail, still produce the result document with one error disposition per query and no candidates.

### Candidate aggregation

Aggregate valid source evidence by case-insensitive author handle.

Each candidate must contain:

```json
{
  "candidate_id": "x-user:builder",
  "profile": {
    "handle": "builder",
    "name": "Builder",
    "bio": "Distributed systems engineer",
    "followers": 1200,
    "profile_url": "https://x.com/builder"
  },
  "posts": [
    {
      "post_id": "101",
      "url": "https://x.com/i/status/101",
      "text": "Tracing across async services is finally usable.",
      "created_at": "2026-09-20T12:00:00Z"
    }
  ],
  "matched_query_labels": ["observability"]
}
```

Rules:

- `candidate_id` is `x-user:<casefolded handle>`.
- The first valid profile occurrence in request/query order owns profile fields.
- Aggregate evidence for the same handle across successful queries.
- Deduplicate posts by `post_id`.
- If the same `post_id` reappears with conflicting text/URL/author evidence, keep the first valid occurrence and emit a warning.
- `matched_query_labels` contains each successful query label that contributed retained evidence, in request order with no duplicates.
- Sort each candidate's posts by `created_at` descending, then `post_id` ascending.
- A malformed tweet (missing required post ID, text, or author handle) is skipped and produces a warning rather than failing the whole successful query.

### Candidate ranking and limit

The product's ranking is deliberately **not prospecting-specific**.

Rank aggregated candidates by:

1. latest retained post `created_at`, descending;
2. casefolded author handle, ascending.

Then return at most `candidate_limit` candidates.

This ranking rule is part of the Product N+1 behavior. Do not substitute a provider/package's domain-specific ranking merely because it already exists.

## Warnings

`warnings` is a JSON list of human-readable strings.

Warnings must make material data loss or degraded execution visible, including:

- skipped malformed provider items;
- conflicting duplicate post evidence;
- failed provider queries.

Do not include the synthetic credential or request headers in warnings.

Exact prose is not prescribed; the evaluator checks that the relevant condition is represented and that secrets are absent.

## Determinism

Given the same request and replay fixture, repeated runs must produce semantically identical JSON.

Do not use current time, random IDs, process IDs, network calls, or unordered-set iteration in output.

## Public sample

A harmless sample replay fixture is provided as `public_sample.json`. It is an example, not the held-out evaluator. The scored evaluator uses different synthetic data.

A typical sample request is:

```json
{
  "schema_version": 1,
  "queries": [
    {"label": "systems", "query": "distributed systems observability"},
    {"label": "agents", "query": "agentic developer tools"},
    {"label": "down", "query": "synthetic provider failure"}
  ],
  "candidate_limit": 3
}
```

## Completion

A valid submission includes:

- the runnable `solution` module/package;
- any submission-local tests you choose to write;
- no network dependency for the scored run;
- no credentials or private Product N source committed to the consumer repository.

The evaluator will run the immutable first submission against held-out synthetic provider data.
