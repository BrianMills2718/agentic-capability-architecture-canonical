# P6 Decision: Minimum Sufficient ACA Boundary

**Plan ID:** ACA-PLAN-001
**Phase:** P6 — Select the minimum product boundary
**Date:** 2026-09-20
**Recorded by:** Brian Mills

---

## Decision

**Ordinary independently invokable provider interfaces plus documented semantics/effects/examples and consumer-side conformance tests are sufficient for composition.** No new ACA runtime, registry, connector platform, authentication layer, workflow engine, semantic compiler, Linguistic Core, or Semantic Foundry is justified by the observed cases.

The `COMPOSABILITY_PROFILE_V0_1` is a **lightweight evaluation checklist**, not a required wire format or runtime artifact.

Generated adapters are normal and expected.

---

## Evidence Supporting This Decision

### P3 First Consumer (Twitter Prospector)

- **Composition Boundaries:** Four ordinary Python functions + one provider adapter
- **Interface Type:** Directly invokable functions with documented input/output contracts; `search_candidates(query, *, api_key=None, timeout_seconds=30.0, opener=urllib.request.urlopen) -> list[dict[str, Any]]` with normalized candidate dicts
- **Test Coverage:** 41 focused tests: 25 composition unit tests + 6 provider adapter tests + 10 live pipeline tests (positive and negative controls)
- **Live Evidence:** TwitterAPI.io collection successful (live API call on "agentic" and frozen query "agentic engineering" OR "AI developer tools"), deterministic scoring, approval gating, in-memory test-local deduplication sink
- **Acceptance Cases:** All 5 frozen cases passed without ACA machinery
- **Safety Enforcement:** Programmatic approval binding, semantic rejection, in-memory deduplication tracking
- **No Runtime Required:** Pure Python functions, no workflow engine or orchestration platform needed

### P5 Second Consumer (Engineering Signal Digest)

- **Boundary Reused:** `search_candidates(query)` from first product, used directly without modification
- **Consumer Type:** Materially different product (signal collection vs. prospect scoring)
- **Test Coverage:** 22 focused tests, all passed
- **Private Implementation Needed:** None; second consumer is self-contained
- **Adapter Code Size:** 45 lines of structural mapping + validation (lightweight, readable)
- **Live Execution:** Query "observability" successful, 20 items, 14 unique authors, identity preservation correct
- **Conformance Proof:** All six COMPOSABILITY_PROFILE_V0_1 conformance checks passed

### Composition Mechanics Observed

| Concern | Approach | Sufficiency |
|---------|----------|-------------|
| **Invocation** | Stable function name + pinned Git revision | ✓ Sufficient |
| **Input/Output Contracts** | Existing JSON schema / Python type hints | ✓ Sufficient |
| **Field Semantics** | Ordinary documentation + examples | ✓ Sufficient |
| **Effects & Constraints** | Published docstrings + negative tests | ✓ Sufficient |
| **Adaptation** | Generated Python code (manual or LLM-assisted) | ✓ Sufficient |
| **Safety (Approval)** | Programmatic binding (existing AES `approval.action` pattern) | ✓ Sufficient |
| **Safety (Idempotency)** | Durable state tracking (existing pattern) | ✓ Sufficient |
| **Evidence/Provenance** | Git revision + test logs | ✓ Sufficient |

### What Was Not Needed

- **ACA Registry Service:** Function names and Git revisions are discoverable in source/docs
- **Semantic Compiler or IR:** Ordinary field mappings are deterministic without a universal schema
- **Linguistic Core:** Field meanings communicated through documentation + examples
- **Semantic Foundry:** Capability identity established through name + published interface
- **New Workflow Engine:** Composition logic expressed as ordinary Python functions or existing orchestrators (n8n was evaluated; Python was sufficient and simpler)
- **MCP, Arazzo, or SystemSpec:** Native interfaces work directly; no interlingua needed
- **Governance Platform:** Repository lifecycle, CI checks, and existing engagement tools sufficient
- **Shared Base Class:** Composition works through explicit input/output contracts

---

## P4 Repairs Classified

All observed failures resolved without ACA extension:

| Failure | Classification | Resolution | Result |
|---------|-----------------|-----------|--------|
| Query parsing (multi-word) | Agent/tool invocation mistake | Retry with correct quoting | No code change |
| Score selectivity (95% routed to review) | Configuration problem | Threshold tuning (0.5 → 0.65) | Configuration-only adjustment |
| UUID identity invention (second consumer design) | Design review catch (not live) | Use boundary's `source_candidate_id` directly | Preserves composition semantics |

**Interpretation:** No failures survived the repair sequence that could not be fixed by documentation, configuration, or generated adapters. No evidence of missing ACA machinery.

---

## Contractor Guidance: Minimum Necessary Practices

When publishing reusable capability boundaries for composition:

### 1. Publish Usable Boundaries

- Expose stable, independently invokable entry points (functions, APIs, workflows)
- Pin exact versions / Git revisions in documentation
- Do not require consumers to know about private internal implementation

### 2. Document Composition-Relevant Semantics

Include in README or docstring only:
- **Input:** Required vs. optional fields, units/scope (e.g., "currency_code is ISO-4217"), cardinality, null behavior
- **Output:** Guaranteed shape and guarantees; what is observed/predicted/requested/completed; information loss constraints
- **Effects:** Read-only vs. state-changing; side effects if any; idempotency contract; preconditions; authorization requirements
- **Examples:** At least one realistic case; add a negative example if silent misuse is plausible

Ordinary field descriptions are preferred. Do not add semantic metadata, role labels, or richer contracts until an **observed** failure demonstrates insufficient clarity and ordinary documentation does not solve it cheaply.

### 3. Test Adapter Integration

Write consumer-side conformance tests showing:
- Boundary can be invoked at the pinned version (positive case)
- Structural mapping works (your output shape → consumer input shape)
- One relevant semantic mismatch is either correctly adapted or rejected (negative control)
- Side effect / retry safety case behaves as declared (if applicable)
- Consumer implementation does not require importing your private code or session state

### 4. Record Composition Decisions Honestly

In project closeout (LEARNINGS.md), record:
- Which boundaries are offered for reuse, and why
- Which capabilities were selected/rejected for this project, and why (apply ADR-013)
- What adapter code was needed, and why
- Tests and live evidence of reuse
- Incompleteness, limitations, or failure modes observed

Do not claim reusability without evidence from a materially different consumer.

### 5. Preserve Reject Evidence

If another project cannot reuse your boundary or finds it unsuitable, record:
- Exact reason (mismatch, incompatibility, insufficient advantage over local implementation, etc.)
- Any adapted use or workaround
- Whether the boundary should remain as-is or be marked as unsuitable for future search

Bad reuse evidence (missing field, wrong semantics) is as valuable as good evidence for the next agent's decisions.

---

## Stop Condition: Future ACA Extensions

Do not add new ACA infrastructure (registry, compiler, semantic metadata, governance layer, workflow engine, connector platform) until:

1. **A named failure exists:** A reproducible composition case that cannot be resolved
2. **Repair sequence exhausted:** Documentation, configuration, generated adapters, or provider-native metadata do not fix it
3. **Cost is material:** The fix would provide measurable value exceeding the cost of the extension itself and its future maintenance
4. **Evidence is in the repository:** The failure is documented in `docs/experiments/independent-composition/`, `RESULTS.md`, or `LEARNINGS.md` with:
   - Exact failing case (frozentest input, expected output, observed output)
   - Failures of each repair step
   - Estimate of recurring cost if not fixed

This rule prevents infrastructure growth on hypothetical future problems. Real failures take priority over general elegance.

---

## Decisions Explicitly Made

### 1. COMPOSABILITY_PROFILE_V0_1 Remains a Checklist, Not a Runtime Spec

The profile is useful as an **evaluation guide** for workers:
- "Does my boundary pass these six checks?"
- "Which fields do I document?"
- "What conformance tests should I write?"

It is **not** a wire format that flows through a platform or a required input to an ACA runtime. Future workers should read it as advice on what to expose, not as a manifest schema they must fill out.

### 2. n8n Is Product Infrastructure, Not ACA Machinery

n8n was selected in P1 and represented by a frozen fixture-based workflow baseline. Live n8n orchestration was not completed due to assistant-to-n8n control/auth integration overhead. P3 execution pivoted to Python/API composition, which required no additional platform layer and proved sufficient for the frozen behavior and acceptance cases.

n8n is:
- **Optional:** Not required for composition; Python functions proved sufficient for the observed cases
- **A delivery platform:** Not an ACA dependency; another product could use a different orchestrator or no orchestrator at all
- **Product-level choice:** If future work selects n8n as a deployment substrate, n8n's existing capabilities (HTTP request, code node, approval nodes) integrate well with provider APIs and generated adapters

The n8n fixture and documentation remain as **historical product-fit evaluation evidence** in `docs/experiments/independent-composition/n8n/`. This evidence is preserved; n8n is not deleted or deprecated by this decision. The fixture represents a plausible workflow shape but does not constitute live runtime proof.

### 3. search_candidates() Is Eligible for Lifecycle Review, Not Automatically Promoted

Evidence from this pilot:
- ✓ Two materially different consumers (prospect scoring vs. signal collection)
- ✓ Generalized behavior exercised (both call `search_candidates(query)`)
- ✓ Live second consumer evidence (successful execution without first-product imports)
- ✓ No modifications required to serve both consumers

This qualifies as **`candidate` → eligible for `proven` review** under repository lifecycle policy (AGENTS.md § Reuse lifecycle).

**Promotion decision:** Defer to explicit review via repository procedures. This report documents the evidence; a separate promotion PR will decide `proven` or `candidate` status. If first consumer experiences live failures, or third consumer reveals unanticipated field requirements, demotion remains possible.

### 4. Preserve Historical n8n/Provider-Fit Evidence

All prior work and decisions are retained:
- `docs/experiments/independent-composition/n8n/twitter-prospector-fixture-baseline.json`
- `docs/experiments/independent-composition/n8n/README.md`
- `research/synthesis/off-the-shelf-substrate-vs-residual-audit.md`
- P1/P2 provider-fit evaluation in `docs/experiments/independent-composition/PROVIDER_FIT.md`

These remain as historical record and competitive analysis. Do not rewrite or delete them as though a later choice invalidates earlier research. The pivot from n8n orchestration to Python/API composition is recorded in `PROTOCOL.md` as an execution amendment; it does not delete the n8n baseline evidence.

---

## ADR Candidate

This decision informs an addition to `docs/DECISIONS.md`:

> **ADR-017 — Composition-ready boundaries use ordinary interfaces plus conformance tests**
>
> **Status:** accepted from P3/P5 pilot evidence
>
> **Decision:** A capability is composition-ready when it exposes a stable, independently invokable boundary (function, API, workflow) with documented input/output contracts, field semantics where non-obvious, effects/constraints, and at least one realistic example. A fresh consumer demonstrates conformance via a focused test showing invocation at the pinned version, structural mapping, one semantic concern correctly adapted or rejected, and side-effect safety if applicable.
>
> **Why:** Two materially different consumers successfully composed from a single retained boundary using ordinary Python functions and a lightweight adapter. No ACA registry, semantic metadata layer, workflow engine, connector platform, or shared base class was required in the observed runs. Ordinary documentation and test-driven integration proved sufficient.
>
> **Consequence:** Do not mandate semantic metadata, universal schema, registry, or governance machinery until an observed, reproducible composition failure survives the repair sequence (docs/examples/adapters/provider-native features) and material cost justifies the new layer. Composition-ready guidance focuses on usable boundaries, examples, and conformance tests, not on infrastructure.

---

## Files and Artifacts

### Created
- `docs/experiments/independent-composition/P6_DECISION.md` (this file)

### Updated
- `docs/plans/2026-09-18-minimal-composability.md` — P6 status and completion note
- `docs/DECISIONS.md` — ADR-017 addition (if approved)

### Preserved (Not Modified)
- All P3 and P5 evidence files (RESULTS.md, SECOND_CONSUMER.md, test suites)
- n8n fixture and evaluation history
- PROTOCOL.md amendment record

---

## Summary

The evidence from P3 and P5 demonstrates that **independent composition is achievable without new ACA machinery**. Boundaries that expose stable, invokable interfaces plus clear documentation and tested adapters are sufficient.

Future ACA work should focus on:
1. **Better capability discoverability** (how do agents find suitable boundaries?)
2. **Clearer composition evidence** (documenting what worked and why)
3. **Reuse cost/benefit observation** (collect time/effort data to assess whether later projects save time/cost)

Not on:
- New registries, compilers, or semantic layers
- Governance machinery predating real failures
- Mandatory infrastructure before evidence justifies it

This approach preserves the ACA mission (composition-driven delivery with evidence of reuse) while respecting the cost of building new platforms.

---

**Next action:** P6 complete. Future ACA extensions require named, reproducible composition failure that survives documented repair sequence and repositories reviewed to justify the new layer.
