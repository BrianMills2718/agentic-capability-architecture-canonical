# ACA Research Agenda — Prior Art First

Status: current research agenda candidate for ACA-PLAN-002.
Recorded: 2026-09-21.
Purpose: constrain ACA research to questions not already adequately solved by established software-engineering practice, standards, or products.

## Governing rule

ACA does **not** assume that software reuse, modularity, API contracts, service catalogs, contract testing, workflow orchestration, durable execution, package distribution, or product-line engineering are new problems.

Before adding an ACA mechanism:

1. identify the requirement precisely;
2. map it to established software-engineering practice and current standards/products;
3. adopt the existing mechanism when it is sufficient;
4. test whether coding agents can use it effectively;
5. invent only the smallest residual mechanism after a named, reproducible failure.

The research target is therefore **agentic use of established reuse mechanisms**, not replacement of those mechanisms.

## Prior-art convergence map

| Need | Established practice / standard / product | ACA posture now | Remaining research question |
| --- | --- | --- | --- |
| Modular reusable implementation | ordinary modules, libraries, packages, services, plugins | **Use directly** | Can agents identify the right reusable unit and avoid unnecessary extraction? |
| Systematic reuse across related products | software product lines, FODA/commonality-variability analysis | **Use concepts, do not recreate methodology** | Does agent-assisted reuse lower total marginal delivery effort in our product mix? |
| Variation between products | product-line variability management, configuration, extension points | **Keep local/configurable unless repeated evidence justifies extraction** | Can agents distinguish stable common behavior from consequential product-local variation? |
| HTTP API description | OpenAPI | **Prefer provider-native OpenAPI** | Can agents select and compose operations correctly without ACA-specific schemas? |
| Event/message API description | AsyncAPI | **Prefer provider-native AsyncAPI** | Can agents preserve event semantics and compatibility across consumers? |
| Agent/tool interface | MCP or native SDK/tool schemas | **Use when already available; do not mandate** | Do tool descriptions plus schemas provide enough context for correct agent selection/rejection? |
| API call sequencing description | Arazzo | **Reuse if a real machine-readable workflow-description need appears** | Does an agent actually benefit from workflow descriptions beyond ordinary code/docs? |
| Consumer/provider compatibility | consumer-driven contract testing, e.g. Pact pattern | **Adopt the pattern where useful** | Can agents generate/maintain useful consumer contracts without making them brittle? |
| Capability/service discovery | source control, package indexes, service catalogs; Backstage pattern at scale | **Retain lightweight manifest/catalog now; do not build a catalog service** | What minimum indexed evidence materially improves fresh-agent discovery and selection? |
| Package/artifact distribution | language package managers, Git revisions/tags, OCI/artifact repositories, hashes/SBOM conventions | **Use existing distribution** | What publication work is required before Product N assets become economical for N+1? |
| Workflow automation | application code, n8n and similar products | **Choose per product** | When is visual/operator-managed orchestration preferable for agent-produced systems? |
| Durable workflow execution | established runtimes such as Temporal and runtime-native job systems | **Source when the invariant requires it** | Can agents correctly recognize when durable execution is needed rather than reimplementing it? |
| Scheduling / retries / messaging / transactions | runtime/platform primitives, queues, DB constraints, outbox/idempotency patterns | **Never create generic ACA replacements** | Can agents bind these primitives correctly to product semantics and failure modes? |
| Human approval safety | ordinary authorization plus exact-action/payload binding; current ACA ADR-014 implementation | **Reuse existing binding invariant** | Can independent consumers compose it correctly under retries and payload changes? |
| Reuse economics | decades of systematic-reuse / software-product-line investment analysis | **Measure rather than rediscover theory** | Do agent-readable assets actually beat competent local implementation after publication/discovery/adaptation cost? |
| Governance / delivery controls | CI, protected branches, schemas, review, existing engagement tooling | **Use existing controls** | Which checks materially improve agent delivery rather than add compliance overhead? |
| Universal semantic IR / ontology | no demonstrated need for ACA | **Do not pursue as ACA core** | Only reopen after a concrete ambiguity survives native contracts, docs, examples, and adapters. |
| Custom ACA runtime | mature execution/runtime ecosystem already exists | **Out of scope by default** | Only reopen after a named execution invariant cannot be supplied economically by an established runtime. |

## Established findings that change the agenda

### Software reuse is not a new ACA research field

The Software Engineering Institute's systematic reuse and software-product-line work already treats reuse as a technical **and economic** problem. FODA showed that identifying common elements is not enough; managing variation is central. Software product-line practice explicitly includes core assets, variability, adoption cost, evolution, and investment analysis.

ACA should reuse those concepts instead of inventing a new theory of "capabilities" to cover the same ground.

Official references:

- SEI, "Establishing a Basis for Software Reuse": https://www.sei.cmu.edu/history-of-innovation/establishing-a-basis-for-software-reuse/
- SEI, "Variability in Software Product Lines": https://www.sei.cmu.edu/library/variability-in-software-product-lines/
- SEI, "Software Product Lines Curriculum": https://www.sei.cmu.edu/library/software-product-lines-curriculum/
- SEI, "Investment Analysis of Software Assets for Product Lines": https://www.sei.cmu.edu/library/investment-analysis-of-software-assets-for-product-lines/

### Interface description is largely solved

Use the provider's existing contract rather than create an ACA wire format:

- OpenAPI for HTTP APIs: https://spec.openapis.org/oas/v3.1.1.html
- AsyncAPI for event/message APIs: https://www.asyncapi.com/docs/concepts/asyncapi-document
- MCP tool input/output schemas and annotations when an MCP boundary already exists: https://blog.modelcontextprotocol.io/posts/2026-07-28-release-candidate/

MCP behavioral annotations such as read-only, destructive, idempotent, and open-world are **hints**, not trusted enforcement contracts. Safety invariants still belong in deterministic authorization/runtime/application controls:

- https://blog.modelcontextprotocol.io/posts/2026-03-16-tool-annotations/

### Discovery and catalogs are established platform patterns

Backstage treats APIs as first-class catalog entities and as a primary mechanism for discovering functionality in large software ecosystems. ACA does not need to recreate Backstage. The present Git-backed manifest-derived catalog is intentionally much smaller.

Reference:

- https://backstage.io/docs/features/software-catalog/system-model/

The ACA question is narrower: **what minimum indexed information measurably helps coding agents discover/select/reject existing assets?**

### Consumer-driven compatibility testing is established

Pact's consumer-driven contract model captures the interactions consumers actually rely upon and verifies those expectations against providers. ACA should reuse this pattern rather than invent a generic "conformance protocol."

References:

- https://docs.pact.io/
- https://docs.pact.io/consumer
- https://docs.pact.io/provider

Use Pact itself only where it fits; ordinary language-native compatibility tests may be sufficient for in-process packages.

### Workflow description and execution already have mature options

Arazzo describes sequences of API calls and dependencies over API descriptions:

- https://spec.openapis.org/arazzo/latest.html

n8n supplies operator-facing workflow execution history and retries:

- https://docs.n8n.io/workflows/executions/all-executions/

Temporal supplies durable execution that resumes across crashes, network failures, and infrastructure outages:

- https://docs.temporal.io/

These are examples, not mandatory ACA dependencies. ACA must not build its own workflow engine simply because capabilities are composed.

## Removed from the ACA research agenda

The following are no longer active ACA research goals absent a new named failure:

- building a generic ACA workflow/runtime engine;
- building a new package registry or marketplace;
- building a new service/developer portal;
- building a new auth or connector platform;
- building a generic scheduler, queue, transaction manager, or idempotency service;
- inventing a universal API schema or transport;
- inventing a generic consumer-contract framework;
- inventing an API workflow-description language;
- inventing a universal semantic IR or primitive language as an ACA prerequisite;
- requiring Linguistic Core, Semantic Foundry, MCP, Arazzo, n8n, or Temporal across products;
- proving that software components/APIs can be reused in principle;
- treating "more reuse" as an outcome by itself.

Existing experimental repositories may continue their own research under their own authority. This agenda only limits what ACA treats as necessary core work.

## Active ACA research questions

### R1 — Agent discovery and selection

Can a fresh coding agent, given a behavior-only product requirement and ordinary access to a trustworthy capability index plus native contracts, correctly:

- find relevant existing assets;
- reject plausible but wrong assets;
- prefer native/external providers when better;
- identify the smallest local residual;
- avoid reimplementing an existing capability merely because generating code is easy?

This is the strongest candidate for ACA-specific value.

### R2 — Economic compounding

Does access to accumulated capability work improve accepted product delivery after counting:

- publication/extraction cost;
- discovery/context cost;
- installation and dependency cost;
- adaptation/debugging;
- model/tool usage;
- human intervention;
- maintenance and compatibility burden?

Compare against the **smallest competent local/provider-native implementation**, not against a deliberately weak control.

### R3 — Minimum capability knowledge

What is the smallest additional indexed information that changes agent behavior beneficially beyond native contracts and source search?

Candidate information includes:

- stable capability/action identity;
- exact public boundary and revision;
- known consumers;
- compatibility/runtime constraints;
- evidence and failed/rejected fits;
- provider/deployment/licensing constraints.

Do not add a field unless an experiment shows that its absence caused a material error or recurring cost.

### R4 — Publication readiness from Product N to Product N+1

When useful behavior exists inside Product N, what prevents N+1 from consuming it?

Measure separately:

- architecture/publication debt;
- packaging/distribution;
- dependency leakage;
- hidden configuration;
- private initialization;
- interface instability;
- missing examples/tests;
- genuine domain coupling.

A poor Product N architecture is evidence about publication readiness, not automatically evidence that reuse is uneconomic.

### R5 — Agent-driven compatibility maintenance

Can agents use ordinary consumer-contract/compatibility techniques to evolve reusable boundaries safely?

Test:

- provider version changes;
- consumer assumptions;
- breaking versus compatible changes;
- migration effort;
- whether generated compatibility tests detect real regressions without becoming brittle.

### R6 — Effectful composition safety

For side-effecting behavior, can agents correctly compose established safety primitives instead of rebuilding them?

The current first canary is:

- exact-action/payload approval binding;
- durable idempotency;
- restart/retry/concurrency behavior;
- ambiguous-result handling.

This is a bounded safety question, not authorization for an ACA transaction runtime.

### R7 — Evidence flywheel

Does preserving successful use, failed fits, incompatibilities, costs, and limitations improve later agent decisions?

The key outcome is not the size of the catalog. It is whether later workers:

- make fewer false selections;
- rediscover less;
- duplicate less behavior;
- deliver faster or with fewer regressions;
- know when *not* to reuse.

## Current experimental sequence

ACA-PLAN-002 is the current execution vehicle.

1. **Prior-art convergence gate** — map each proposed ACA mechanism to established practice/product/standard; remove solved mechanisms from the agenda.
2. **Evidence repair** — narrow earlier P3/P5/P6 claims to what was actually exercised.
3. **Brownfield publication audit** — test whether a pre-existing Product N capability can leave its source product without consumer-specific redesign.
4. **Control vs reuse** — run equivalent fresh workers on a nontrivial behavior and measure total economics.
5. **Effect-safety canary** — separately test an established approval/idempotency composition.
6. **Decision** — adopt/defer/reject the reusable asset or tiny missing metadata based on measured results.

The read-only one-query case is plumbing only. It cannot decide the architecture.

## Stop rules

Stop ACA research on a mechanism when an established standard/product/practice already satisfies the requirement at acceptable cost.

Reopen only when all of the following are true:

1. a named product/composition case fails;
2. the failure is reproducible;
3. ordinary source/docs/examples/configuration/adapters and the relevant established standard/product are insufficient;
4. the failure creates material recurring cost, correctness, safety, or delivery risk;
5. the proposed ACA addition is smaller than the recurring problem and can be tested against a control.

## Success criterion

ACA succeeds if **agents exploit existing software assets and established engineering mechanisms more effectively over time**, so later products require less rediscovery and bespoke implementation at equal or better correctness.

ACA does not succeed by owning more infrastructure.
