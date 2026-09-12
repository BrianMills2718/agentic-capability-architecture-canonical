# Tentative: external integration platforms as ACA capability providers

**Status:** tentative design note; non-authoritative; not an architecture decision  
**Date:** 2026-09-12  
**Purpose:** capture a provider-resolution hypothesis for later ACA testing without changing the charter, semantic export catalog, or provider-selection rules.

## Thesis

Managed integration platforms such as Nango, Unified.to, Composio, Pipedream Connect, and Arcade should be evaluated as **candidate capability providers beneath ACA semantic identities**, not as replacements for ACA's capability model.

The durable ACA boundary should remain:

```text
required behavior
  -> provider-independent semantic capability identity
  -> provider resolution / selection or rejection
  -> honest typed public boundary
  -> explicit composition/configuration
  -> selected runtime/provider
  -> external system
  -> evidence
```

The integration platform may own authentication, credential refresh, connection lifecycle, provider-specific API execution, tool discovery, normalization, retries, or gateway behavior. It should not become the canonical semantic meaning of the capability merely because it exposes many provider-native tools.
## Why this fits the current ACA charter

ACA already requires agents to investigate native/runtime, ecosystem, external OSS/SaaS, standards/protocols, and internal providers before implementing shared behavior. It also explicitly says runtime infrastructure such as authorization, scheduling, retries, messaging, and observability should normally come from established systems when they satisfy the invariant.

External integration platforms therefore look less like "an integration architecture" and more like a **provider family** ACA should be able to reason about.

This is especially relevant to the current verified exports:

- `availability.query`
- `notification.email.send`
- `approval.resolve`
- `state.transition.plan`

For example, `availability.query` should remain the semantic behavior. Google Calendar, Microsoft 365, a normalized calendar API, or a managed integration platform can be alternative providers of that behavior. Likewise, `notification.email.send` should not become `gmail.send` simply because Gmail happens to be the first provider.

Provider-specific behavior is still legitimate when the requirement is genuinely provider-specific. The rule is not to hide meaningful provider semantics; it is to avoid making incidental provider names the durable abstraction when the required behavior is broader.
## Broader control-plane sourcing principle

The same sourcing rule should apply to ACA's **control plane**, not only to business/application capabilities. Before creating new shared infrastructure for authorization, durable execution, events, telemetry, tool metadata, catalogs, or integration plumbing, first test whether an established standard, runtime, or product already satisfies the invariant.

The tentative default should be:

```text
required control-plane invariant
  -> established standard / protocol?
  -> mature runtime or platform capability?
  -> established external/OSS implementation?
  -> existing internal capability?
  -> only then implement the residual gap
```

This does not mean ACA should adopt a particular vendor or turn standards into mandatory dependencies. It means generic infrastructure needs the same net-value gate ACA already applies to reusable application capabilities.

### Areas that should receive a build-vs-standard check

| Concern | Existing practices/systems to evaluate before custom infrastructure | ACA-specific remainder, if any |
| --- | --- | --- |
| Fine-grained authorization | Cedar, OpenFGA, OPA-style policy engines | application-specific resource/action model, delegated-agent semantics, evidence of the decision |
| Delegation and exact authorization | OAuth delegation/token-exchange concepts, rich/transaction authorization patterns | requester vs. connection-owner distinction and agent-specific approval semantics |
| OAuth and provider connections | OAuth/OIDC plus Nango/Unified/Composio/Pipedream-like managed connection infrastructure | semantic capability selection and any unavoidable provider-specific residual |
| Tool metadata/discovery | MCP tool schemas, annotations, and discovery | ACA semantic identity, verified binding, selection/rejection evidence |
| Events and asynchronous contracts | CloudEvents and AsyncAPI | domain event meaning and admission into governed knowledge |
| Durable waits/retries/scheduling | Temporal/Restate-style durable execution or runtime-native schedulers | domain workflow intent, approval points, escalation semantics |
| Observability | OpenTelemetry semantic conventions and standard trace/log/metric pipelines | ACA/consumer-specific attributes such as capability ID, requester, provider selection, policy decision |
| Generic software/service inventory | Backstage-style software catalogs and existing registries | ACA's capability/evidence graph: semantic behavior, executable boundary, net-value and reuse evidence |

ACA should resist becoming a generic authorization server, workflow engine, event bus, tracing vocabulary, service catalog, OAuth broker, or MCP transport merely because those concerns appear in capability compositions. The differentiated layer is the **agent-facing semantic capability/evidence loop**: stable behavior identity, honest executable boundaries, provider selection/rejection, net-value reasoning, explicit composition, residual-local semantics, and evidence that improves later decisions.

### Pre-build control-plane check

Before adding a new shared control-plane subsystem, answer:

1. What exact invariant is missing?
2. Which standard or mature implementation already addresses that invariant?
3. What concrete requirement is not satisfied by those options?
4. Can an adapter/configuration layer close that gap without creating another platform?
5. What is the smallest viable local implementation, and does shared infrastructure beat it after discovery, operations, security, and migration cost?
6. Which parts are genuinely ACA semantics versus generic infrastructure?
7. What evidence would falsify the decision to build or adopt the component?

If these questions do not expose a genuine residual, the default should be composition/adoption rather than new shared infrastructure.

## Important identity boundary for agent systems

A provider connection and the human currently requesting an action are not always the same identity.

A delegated or multi-user agent may have this shape:

```text
requester = person A
agent/profile/account owner = person B
external connection = person B's account
```

An integration platform can usually answer "which external account is connected?" It should not be assumed to answer the separate policy question "is this requester allowed to cause this account to perform this action?"

ACA should therefore preserve an explicit separation between:

1. **connection identity** — whose external credentials/account are used;
2. **requester identity** — who asked the agent to act;
3. **capability authority** — what that requester is permitted to do through that agent/account;
4. **action approval** — whether this exact consequential action/payload has been authorized where required.

A candidate provider that collapses these identities should be rejected or require an explicit adapter/policy boundary before use.
## Tentative provider hypotheses

These are starting hypotheses for testing, not rankings to preserve as doctrine.

### Nango-like provider infrastructure

Best fit when ACA wants to keep semantic actions and typed boundaries under its own control while outsourcing OAuth, token refresh, connection lifecycle, provider-specific API mechanics, and execution infrastructure.

Hypothesis: this is the cleanest fit for capabilities where ACA already has a stable semantic action and wants the external integration layer to remain mostly invisible above the provider boundary.

### Unified.to-like normalized APIs

Potentially strong fit when a stable ACA semantic capability maps cleanly to a normalized domain API across multiple vendors, for example availability, tasks, CRM records, or files.

Hypothesis: normalization can reduce adapter count, but only when the common model preserves the capability's decisive semantics. Provider passthrough should remain available for real vendor-specific behavior rather than widening the canonical ACA capability to match a lowest common denominator.

### Composio/Pipedream-like dynamic tool platforms

Potentially strong fit for broad provider coverage and runtime discovery. The risk is architectural leakage: provider-native tool names and schemas can become the agent's de facto capability ontology.

Hypothesis: use dynamic discovery as a provider-resolution/execution mechanism beneath ACA where possible, rather than allowing the provider catalog itself to replace semantic capability identity.
### Arcade-like governance gateways

Potentially useful when the problem is organization-wide agent/MCP governance rather than connector plumbing alone.

Hypothesis: evaluate separately from the provider-runtime question. A governance gateway may compose well with ACA, but it should not be assumed to replace application-specific delegated-authority rules, especially when requester identity differs from connection identity.

## Advice for ACA provider resolution

1. **Keep semantic action IDs provider-independent.** Do not make `gmail.*`, `monday.*`, or another vendor namespace the durable ACA identity unless the requirement is actually vendor-specific.
2. **Treat vendor catalogs as candidate-provider evidence, not semantic authority.** A large tool catalog can help sourcing/discovery without defining ACA's action ontology.
3. **Prefer honest existing interfaces.** If an external platform already exposes the right typed boundary, bind it directly. Add an adapter only for real translation, policy, compatibility, or evidence needs.
4. **Preserve local policy above provider execution.** Authentication to an external account is not equivalent to authorization for every human or agent that can reach the calling system.
5. **Preserve evidence.** Selection should retain provider/version, exact connection/configuration class, tests, limitations, incidents, and rejected-fit reasons where they matter for future reuse.
6. **Do not migrate broadly from a paper comparison.** Prove one or two semantic capabilities under authentic use before replacing working provider-specific infrastructure.
## Suggested first ACA experiment

Use existing verified semantic actions rather than inventing a new generic integration abstraction.

A good first pair is:

- `availability.query` — read-oriented, provider-neutral, already exported;
- `notification.email.send` — side-effecting, already exported, and useful for testing identity/approval/observability boundaries.

For each action, compare at least:

- the smallest viable local/direct-provider implementation;
- a Nango-style managed integration implementation;
- a Unified-style normalized implementation where the category genuinely fits;
- a Composio-style dynamic tool implementation.

Pipedream is a useful breadth/trigger candidate if the first set exposes provider-coverage or workflow gaps. Arcade is more useful as a separate governance-gateway candidate if centralized policy becomes the actual requirement.
## Evidence to collect

Record the comparison through the current ACA planning/evidence machinery rather than inventing a parallel scorecard. At minimum, the provider decision should make the following visible:

- exact semantic action being satisfied;
- selected provider and rejected plausible providers;
- smallest viable local alternative;
- concrete net-value reason after discovery, context, binding, and adaptation cost;
- amount and complexity of adapter/custom code required;
- credential/auth lifecycle removed or added;
- whether provider-specific semantics leak above the typed boundary;
- latency, reliability, failure semantics, retries, and rate-limit behavior;
- observability/audit information retained at the capability boundary;
- delegated requester/account-owner separation where applicable;
- idempotency and approval behavior for side effects;
- portability and provider-lock-in implications;
- real-use evidence strong enough to justify reuse beyond the experiment.

A candidate should lose even when semantically capable if its integration/context cost exceeds the smallest equally reliable local alternative. That is already ACA's net-value rule and should remain the decision gate here.
## Relationship to the current AES capability exchange

The current `tools/aes_capability_exchange.py` resolves exact requested semantic action IDs against the verified ACA catalog and reports uncovered gaps rather than guessing. That is a useful boundary to preserve.

A future external-provider extension should preferably look like:

```text
selection request for exact semantic action
  -> resolve verified internal export if one fits
  -> otherwise source external/native/standard candidates
  -> select or reject with evidence and limitations
  -> bind the chosen provider through an honest interface
  -> retain the semantic action ID above the provider boundary
```

Do not silently convert an uncovered semantic action into a provider-native tool name merely because a third-party catalog has a plausible fuzzy match. Discovery may propose candidates; selection should remain explicit and evidence-backed.

This may eventually justify extending the capability-exchange contract to represent external provider candidates, but this note does **not** recommend a schema change yet. First prove that one real consumer needs the exchange to carry those facts.
## Candidate future semantic identities

The following names are only examples for requirement analysis. They are **not** proposed canonical exports merely by appearing here:

```text
task.create
message.search
document.find
calendar.event.create
crm.contact.search
```

Promote a new semantic identity only when a real requirement cannot be honestly expressed through the existing catalog and when the proposed boundary survives provider/runtime variation without hiding consequential semantics.

In particular, avoid deriving the ACA vocabulary by mechanically stripping provider names from third-party tools. Semantic identity should come from stable required behavior, not from catalog normalization for its own sake.

## Tentative test order

From an ACA perspective, the initial order worth testing is:

1. **Nango** — strongest hypothesis when ACA owns the semantic action and wants managed auth/provider execution underneath it.
2. **Unified.to** — especially interesting where its normalized categories closely match an ACA semantic capability without semantic loss.
3. **Composio** — strongest hypothesis for dynamic provider/tool discovery; test whether it can remain subordinate to ACA identity rather than becoming the ontology.
4. **Pipedream Connect** — strong breadth/trigger fallback when coverage becomes the limiting factor.
5. **Arcade** — evaluate primarily when centralized agent/MCP governance is the requirement, not just integration plumbing.
## What would change my mind

Reject this framing if real experiments show that provider-native tool identity consistently produces better correctness, lower context cost, and lower integration burden than preserving an ACA semantic boundary; or if the semantic layer requires adapters so elaborate that it becomes a second integration product.

Likewise, reject a managed platform when direct provider integration is materially simpler, safer, cheaper, or more observable for the actual capability under test.

The goal is not to maximize use of ACA abstractions or third-party platforms. The goal is the ACA charter's stated outcome: composition should create net value and leave only the genuinely novel residual local.

## Explicit non-decision

This note does not:

- adopt Nango, Unified.to, Composio, Pipedream, or Arcade;
- change any current semantic export or capability manifest;
- authorize a new generic integration/gateway subsystem;
- claim that provider normalization is always desirable;
- claim that dynamic tool discovery is a substitute for semantic capability identity;
- recommend replacing working integrations without an authentic capability-level comparison;
- alter ACA's current authority hierarchy or architecture charter.

If a bounded experiment produces useful evidence, record the selection, rejection, compatibility, and failure evidence through the existing ACA mechanisms before considering an architectural decision.
