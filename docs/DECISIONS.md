# Architecture Decisions

Cross-repo semantic/interface policy is governed by the [Vision Semantic Boundary and Interface Policy](https://github.com/BrianMills2718/vision/blob/main/wiki/synthesis/adr-2026-09-07-semantic-boundary-and-interface-policy.md). This file records repository-local decisions that future work should preserve.

## ADR-001 — Separate shared, configured, and custom behavior

**Decision:** Use explicit shared capability, project configuration, and project custom-extension boundaries.

**Reason:** Prevents reusable code from accumulating project-specific conditions.

---

## ADR-002 — Reuse must be demonstrated

**Decision:** New code is not automatically considered reusable. Use lifecycle states: local → candidate → proven → core.

**Reason:** Premature abstraction creates complexity without demonstrated reuse.

---

## ADR-003 — Agents inspect before building

**Decision:** Coding agents must investigate existing implementations before creating new behavior. Inspection includes native runtime/platform features, installed ecosystem packages, mature external implementations, existing standards/protocols, and internal registered capabilities.

**Reason:** The capability base only compounds if agents select existing suitable behavior before generating bespoke code; “reuse” must not mean “prefer our implementation regardless of what already exists.”

---

## ADR-004 — Tests are institutional memory

**Decision:** Reusable behavior requires tests, and discovered failure modes should become regression tests.

**Reason:** Future agents and developers need executable constraints, not only comments.

---

## ADR-005 — Business-rule conflicts are explicit

**Decision:** Rules affecting the same outcome should report decisions to a deterministic resolver. Priorities represent allowed competition; explicit conflicts represent undefined combinations.

**Reason:** Business behavior must not depend on incidental hook/install order.

---

## ADR-006 — Project extensions must not silently weaken shared safety rules

**Decision:** A project-specific ALLOW decision cannot automatically erase a stricter shared/core REQUIRE_APPROVAL or BLOCK decision.

**Reason:** Local customization should not bypass shared invariants accidentally. Where durable state represents multiple requirement sources, provenance should be preserved rather than relying on an unqualified Boolean alone.

---

## ADR-007 — Off-the-shelf wins ties

**Decision:** When an established platform feature, package, external product/service, or standard satisfies the required invariant approximately as well as a custom implementation, use or integrate the established option. Build shared implementation only for a genuine unmet gap or where the custom boundary provides a demonstrated architectural benefit.

**Reason:** Reimplementing commodity workflow, scheduling, authorization, notifications, package distribution, observability, service cataloging, agent transport, or business application functionality increases maintenance cost without strengthening the distinctive capability-selection/evidence layer.

**Consequence:** Proof applications may deliberately exercise these concerns, but their presence in the repository is not a product commitment to compete with mature off-the-shelf systems.

---

## ADR-008 — Capability intelligence is the strategic trunk

**Decision:** Prioritize semantic capability identity, honest public interfaces, sourcing/selection, explicit local gaps, compatibility/rejection evidence, and accumulated reuse knowledge over expanding a private implementation catalog.

**Reason:** The durable advantage is better agent decisions about available capability, not ownership of every implementation.

**Consequence:** Primitive/composition research remains probationary until it demonstrates incremental value beyond good capability metadata and typed interfaces.

---

## ADR-009 — The Vision wiki is the single global navigation authority

**Decision:** Cross-repo “where do I start / where does this belong?” navigation is owned by `BrianMills2718/vision/wiki/index.md`. Repository READMEs identify local role and point to local authority maps but do not maintain competing global navigation trees.

**Reason:** Multiple active-looking indexes and repeated current-status lists drift and make fresh-agent discovery less reliable.

**Consequence:** `docs/README.md` is a repository-local document map only. Historical proof/session documents remain preserved but must not be presented as current navigation authority.

---

## ADR-010 — Do not duplicate volatile machine state in prose

**Decision:** Capability maturity, public interfaces, dependencies, and other machine-readable state should be read from or derived from manifests/catalogs where practical. Prose may explain interpretation but should not maintain a second manual status table.

**Reason:** Independent hand-maintained summaries become stale and can agree with each other while disagreeing with evidence or executable state.

**Consequence:** If machine-readable sources disagree, treat that as a synchronization/validation defect to fix explicitly rather than choosing a prose winner.

---

## ADR-011 — Semantic action catalog is derived from capability manifests

**Decision:** Capability manifests are the source of truth for semantic exports. An exported action ID must already be listed in the capability's `provides` and must point at a declared `public_interfaces` boundary. Catalog/list/describe views are generated from those manifests; no second publication registry is maintained. Existing public functions serve directly when their semantics already match, so no wrapper is added for `approval.resolve`, `state.transition.plan`, or `notification.email.send`.

**Reason:** This preserves provider-independent semantic lookup without duplicating provider metadata or creating adapter code for architectural symmetry. Exact matching is sufficient until a real requirement demonstrates the need for graded matching or planning.

**Consequence:** `tools/capability_catalog.py` is a derived view/check surface. A duplicate action ID, a non-public target, or an action not present in `provides` is a validation failure.


## ADR-012 — Publish availability.query as the scheduling availability boundary

**Status:** accepted

**Decision:** Bind the existing `availability.query` capability identity to the pure-Python `na_scheduling.availability.is_available` public interface, with `TimeWindow` and `find_conflicts` declared as supporting public interfaces. Keep `appointment.create`, `appointment.cancel`, and `appointment.reschedule` as broader scope labels only until honest callable boundaries exist.

**Why:** A fresh-agent experiment derived from a current public ATS/booking job independently required overlap prevention. The scheduling implementation already contained the reusable behavior, but the agent correctly rejected Scheduling because the manifest exposed no verified executable interface. This was a capability-knowledge defect, not an implementation gap. Publishing the existing stable boundary improves discoverability without adding shared code.

**Constraint:** This does not promote Scheduling beyond `candidate`, does not make availability a universal primitive, and does not claim appointment lifecycle actions exist.

---

## ADR-013 — Capability selection requires net value over a local alternative

**Status:** accepted

**Decision:** Semantic fit is necessary but insufficient for capability selection. For every selected capability, the pre-code capability plan must name the smallest viable local implementation and explain the concrete implementation, verification, risk-reduction, compatibility, or repeated-use advantage that exceeds discovery, context, binding, and adaptation cost.

**Rejected alternative:** Select every capability whose semantics fit and rely on later engagement metrics to reveal whether consumption was economical.

**Reason:** The order-approval experiment showed that a correctly selected and composed capability can still increase wall time and context cost for a small fixed rule set. Treating fit as sufficient would reward reuse count instead of lower marginal delivery effort and reliability.

**Consequence:** A capability that fits but offers no concrete advantage over an equally reliable local implementation should be recorded as a rejected candidate and the behavior should remain local. This does not reduce capability value to source-line savings: reused verification, difficult invariants, material risk reduction, compatibility, and amortization across repeated actions are legitimate advantages.
