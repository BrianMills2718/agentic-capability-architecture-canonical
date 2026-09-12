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

### Additional control-plane areas to source before building

Several adjacent concerns deserve the same treatment:

- **Workload/service identity:** evaluate SPIFFE/SPIRE or equivalent established workload-identity infrastructure before creating custom service certificates, service-token issuance, trust bundles, or agent/service identity bootstrapping. ACA may still need application-level meanings such as requester, connection owner, or delegated actor; those meanings should not require ACA to become a workload PKI.
- **Software supply-chain provenance and signing:** evaluate SLSA provenance, in-toto attestations, Sigstore/Cosign, or equivalent established mechanisms before defining a new cryptographic artifact-attestation format. ACA evidence may say that a capability/provider satisfied a semantic action under particular conditions; artifact authenticity/build provenance should use established supply-chain formats where possible.
- **Feature/configuration rollout:** evaluate OpenFeature and mature feature-flag/configuration systems before creating generic rollout percentages, per-user enablement, canary-provider routing, or experiment-targeting semantics. ACA can own the reason a provider/capability is under experiment without becoming a flag-delivery platform.
- **User/group provisioning:** evaluate SCIM for generic cross-domain user and group lifecycle synchronization before creating another provisioning protocol. Product-specific facts such as who owns a Second Brain or what delegated relationship is allowed remain domain semantics above that layer.

These examples are candidates for evaluation, not adopted dependencies. The question is always whether the standard or mature implementation satisfies the actual invariant with lower total cost and risk than a custom subsystem.

### Required prior-art check for new shared infrastructure

Any proposal for a new cross-project **schema, daemon, registry, gateway, identity mechanism, scheduler, policy engine, event envelope, telemetry vocabulary, signing/provenance format, or provisioning protocol** should include an explicit standards/prior-art section before implementation.

At minimum it should record:

1. the exact invariant the new component would own;
2. relevant standards/protocols and mature implementations considered;
3. why each plausible option fails or is uneconomic for the requirement;
4. the smallest adapter/configuration alternative to a new subsystem;
5. the smallest viable local implementation;
6. the ACA-specific semantic residual, if any;
7. migration/exit cost if an external implementation is selected;
8. evidence that would falsify the decision.

A missing prior-art search should be treated as an incomplete architecture proposal, not as evidence that a custom component is needed.

## Additional infrastructure that should stay standards-first

A few more control-plane areas deserve the same presumption against custom infrastructure:

| Concern | Existing practices/systems to evaluate first | ACA-specific remainder, if any |
| --- | --- | --- |
| Secrets and key custody | Vault/cloud KMS, short-lived credentials, SOPS-class encrypted configuration | which capability/provider needs a secret and what scope/rotation evidence applies |
| HTTP/RPC interface contracts | OpenAPI, JSON Schema, Protocol Buffers/gRPC where appropriate | ACA semantic action identity and evidence that a concrete interface actually satisfies it |
| Policy/configuration distribution | OPA bundle/discovery patterns, signed/versioned configuration delivery | ACA-specific policy meaning and the evidence that a particular consumer received/evaluated the intended version |
| Network-edge resilience | established proxies/service meshes and platform rate limiting, circuit breaking, retries, mTLS | capability-specific failure semantics and any domain rule that must not be hidden by generic retry behavior |

The practical rule is: ACA should reference or bind mature interface/control standards rather than create another IDL, secret store, policy-distribution daemon, proxy, or resilience layer. A custom adapter is justified only when it expresses a real semantic translation or evidence boundary that the underlying system does not provide.

### Contract discipline

When a capability crosses a process or repository boundary, prefer an established machine-readable contract format before creating an ACA-specific schema language. HTTP surfaces should generally start from OpenAPI + JSON Schema; RPC surfaces should consider an established IDL such as Protocol Buffers; asynchronous surfaces should continue to prefer AsyncAPI/CloudEvents. ACA may add semantic action IDs, provider-selection evidence, limitations, and compatibility metadata around those contracts, but should not duplicate their wire/interface semantics.

### Secret-handling discipline

Capability manifests and evidence should refer to logical secret requirements and scopes, never become the secret store. Prefer short-lived/dynamic credentials where available, external secret custody, explicit rotation/revocation, and machine-local resolution. Secret values should not enter capability catalogs, evidence records, prompts, generated documentation, or portable profiles.

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
## Concrete provider/OAuth proof

The first implementation-facing proof is specified in [`experiments/TEAM_BRAINS_PROVIDER_OAUTH_PROOF.md`](experiments/TEAM_BRAINS_PROVIDER_OAUTH_PROOF.md). It intentionally tests provider OAuth custody on one existing semantic capability before any broad integration-platform migration or broker deletion.

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

## Concrete audit of current ACA and Team-Brains custom infrastructure

This section applies the standards-first rule to code that exists today. It is a **retirement/simplification shortlist**, not authorization to delete or migrate anything. Each replacement requires an authentic consumer proof and rollback path.

| Current subsystem | Tentative disposition | Reason / boundary to preserve |
| --- | --- | --- |
| Team-Brains `knowledge/auth_broker/providers.py`, `store.py`, `server.py` | **Replace candidate — high confidence** | The code owns provider authorize URLs, token exchange/refresh/revoke quirks, scope drift, encrypted token storage, and connect links. Those are generic managed-integration/OAuth concerns. Preserve the local mapping from a brain owner to the selected connection and the local policy above execution. |
| Team-Brains `knowledge/mcp_server/mcp_oauth.py` | **Replace candidate — high confidence** | It implements an OAuth authorization server: dynamic client registration, PKCE, authorization codes, access/refresh tokens, revocation, expiry, rate limiting, Google identity verification, and persistence. If remote MCP login remains a product surface, prefer a mature OAuth/OIDC authorization server or identity-aware gateway; preserve only the roster/person binding and application authorization semantics. |
| Team-Brains Fernet/SQLite secret stores in `knowledge/storage/people.py` and `knowledge/auth_broker/store.py` | **Replace/centralize gradually** | Encryption-at-rest is useful, but key custody, rotation, audit, short-lived credentials, and secret lifecycle are generic secret-management concerns. A managed integration provider may eliminate most SaaS tokens; remaining service/profile secrets should move toward a real secret manager/KMS rather than expanding the SQLite vault. Keep non-secret person/provider identity mapping local. |
| `agents/plugins/inside-success-requester-identity/` | **Keep as the policy-enforcement point; simplify policy internals later** | This is product-specific and security-critical because requester identity is per message while the brain's MCP/provider credential is per process/profile. Keep authenticated requester extraction and fail-closed `pre_tool_call` enforcement. If policy grows, move relationship/rule evaluation to Cedar/OpenFGA/OPA-class infrastructure rather than enlarging Python allowlists. |
| Team-Brains `knowledge/mcp_server/tool_facets.py` | **Split, do not delete wholesale** | `effect`, requester tier, and outward-action meaning are local safety facts. Read-only/destructive/idempotent/open-world metadata overlaps standard MCP annotations and should project to those standards. Routing aliases/intents/cost/dependency hints are useful local projections but should not become a second canonical capability ontology beside ACA or a provider's discovery system. |
| `knowledge/proactive/actions.py` + `ledger.py` | **Keep semantic safety; separate generic execution mechanics** | Exact preview binding, approval expiry, live revalidation, owner-specific action semantics, and "already done" checks are differentiated safety/product logic. Generic state-machine persistence, attempt bookkeeping, idempotency plumbing, and retry execution should not grow into a proprietary workflow engine. |
| `knowledge/proactive/delivery.py` + `knowledge/mcp_server/daily_dloa.py` | **Freeze generic worker growth; evaluate durable execution before adding more workflows** | These files implement leases, retry clocks, schedules, attempt ceilings, recovery, serialized workers, and idempotent delivery. The current bounded SQLite implementation may be economical for a small pilot, but new workflow classes should trigger a Temporal/Restate/runtime-native comparison before duplicating more scheduler/queue machinery. Keep quiet hours, daily limits, proposal semantics, and owner-facing behavior local. |
| `knowledge/mcp_server/event_loop_telemetry.py` and timing hooks in `tool_errors.py` | **Bridge to OpenTelemetry; retire the custom telemetry store when practical** | Event-loop lag, tool latency, errors, and result size are observability signals rather than product semantics. Preserve the FastMCP `isError` compatibility shim until upstream behavior makes it unnecessary, but emit standard traces/metrics instead of expanding bespoke SQLite telemetry tables. |
| `knowledge/monitoring/reporter.py` / `notifier.py` | **Keep as presentation, not telemetry authority** | A Slack digest/alert is a useful product/operator view. Source the underlying measurements from standard telemetry/operational stores over time rather than turning the report path into a parallel observability system. |
| `knowledge/proactive/runtime.py` plus simple environment allowlists | **Keep simple for now** | One boolean plus an explicit person allowlist is cheaper and clearer than adopting a feature platform for a 15-person pilot. Move to OpenFeature/flag infrastructure only when contextual targeting, canaries, provider switching, or experiment cohorts materially proliferate. |
| Team-Brains person/provider identity registry in `knowledge/storage/people.py` | **Keep domain mapping; avoid becoming a directory service** | Mapping Slack/GitHub/Zoom/Monday identities to the canonical Second Brain person is product data. Joiner/leaver/group lifecycle can later come from SCIM/IdP sources; do not rebuild generic enterprise directory provisioning inside this table. |
| Static per-profile/service credentials such as `knowledge_mcp_tokens` and service passwords | **Investigate after auth/secrets decisions** | They currently encode useful owner/profile scoping, but new long-lived token maps should be avoided. Once provider auth and secret custody are simplified, evaluate short-lived workload/service identity rather than growing another static credential system. |

### ACA code that should remain differentiated

The audit does **not** suggest replacing ACA's semantic layer with Backstage, MCP, or an integration vendor.

- `tools/capability_catalog.py` should remain the strong semantic-action verifier: it admits a capability only when the manifest's export resolves to a real declared public callable. Generic software catalogs do not provide that ACA-specific claim.
- `tools/aes_capability_exchange.py` is currently a small exact-ID selection contract and gap reporter. Keep it small. If it later becomes a remote/federated protocol, carry the ACA payload over an established transport such as MCP/A2A/HTTP rather than inventing networking, discovery, authentication, or federation semantics here.
- `tools/engagement.py` should keep the pre-code selection/rejection/net-value/evidence discipline. Its checksum explicitly remains a cooperative consistency check; if adversarial artifact provenance is ever required, use Sigstore/SLSA/in-toto-class infrastructure instead of evolving `SHA256SUMS` into a home-grown attestation system.
- Capability manifests should continue to own ACA semantic metadata, but public API shapes should reuse OpenAPI/JSON Schema/Protocol Buffers or the provider's honest native interface where those standards already fit.

### Suggested simplification sequence

1. **Provider/OAuth proof:** run the planned `availability.query` / `notification.email.send` comparison. Measure how much of `auth_broker` and provider token storage disappears with Nango/Unified/Composio/direct-provider alternatives.
2. **Remote MCP authentication review:** separately compare `mcp_oauth.py` with a mature OAuth/OIDC authorization-server or identity-proxy deployment. Do not couple this decision to the SaaS connector vendor.
3. **Authorization seam:** keep the requester-identity plugin as the enforcement point, but define the four identities (`requester`, `connection owner`, `capability authority`, exact-action approval) as a clean contract so a policy engine can replace hand-maintained rule evaluation without changing Hermes identity extraction.
4. **Durable-execution proof:** before adding another scheduled/retryable proactive workflow, implement one representative DLOA/reminder flow on a durable runtime and compare code size, failure recovery, idempotency, inspectability, and operating burden with the SQLite lease worker.
5. **Telemetry bridge:** emit tool/action/provider spans and metrics through OpenTelemetry while retaining existing reports. Retire custom telemetry persistence only after equivalent diagnostics are demonstrated.
6. **Secret reduction:** after provider migration choices are known, inventory the credentials that remain and move only the durable residue into managed secret/KMS infrastructure.
7. **Defer scale-only infrastructure:** SCIM, SPIFFE/SPIRE, OpenFeature, and a generic service catalog should stay candidates until participant count, deployment topology, or operational requirements make their advantage concrete.

The migration rule should be **strangler-style, capability by capability**: prove an external/standard implementation on one authentic path, route that path through it, preserve rollback, then delete overlapping custom code only after retained evidence shows the replacement is better. Do not launch a simultaneous rewrite of auth, policy, workflows, telemetry, and integrations.

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
