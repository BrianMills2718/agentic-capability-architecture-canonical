# Architecture Decisions

## ADR-001 — Separate shared, configured, and custom behavior

**Decision:** Use three explicit layers: shared capability, project configuration, project custom extension.

**Reason:** Prevents reusable code from accumulating project-specific conditions.

---

## ADR-002 — Reuse must be demonstrated

**Decision:** New code is not automatically considered reusable. Use lifecycle states: local → candidate → proven → core.

**Reason:** Premature abstraction creates complexity without demonstrated reuse.

---

## ADR-003 — Agents inspect before building

**Decision:** Coding agents must inspect the registry and existing capabilities before implementing new behavior.

**Reason:** The capability base only compounds if reuse is considered before coding.

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

**Reason:** Local customization should not bypass shared invariants accidentally.
