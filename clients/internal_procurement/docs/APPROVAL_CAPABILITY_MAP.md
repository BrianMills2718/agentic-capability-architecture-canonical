# Approval Capability Map — Internal Procurement

## Purpose

Project two is the first materially different domain to test the existing Approvals capability.

The goal is to identify what is already reusable, what should remain procurement-local, and what becomes eligible for promotion after this second use.

## Current shared Approvals capability

The shared capability already provides the core decision layer:

```text
rule evaluation
      ↓
RuleResult
      ↓
deterministic resolver
      ↓
ALLOW / REQUIRE_APPROVAL / BLOCK
```

It already owns:

- decision vocabulary
- deterministic priority ordering
- explicit conflicts
- equal-priority disagreement errors
- BLOCK precedence
- protection against local rules silently weakening shared requirements

Those stay shared.

## How Procurement should use it

The shared rule engine should answer questions like:

```text
Does this request require another approval stage?
```

Project-local rules might include:

```text
manager_stage_required
    → REQUIRE_APPROVAL

finance_threshold
    if total_amount >= 500
    → REQUIRE_APPROVAL

prohibited_category
    → BLOCK
```

Rules return facts/decisions. They should not directly mutate the Purchase Request.

## The important distinction

The current shared Approvals capability is primarily a **decision resolver**.

Procurement introduces another concern:

```text
who may act
+ at which stage
+ what state transition occurs
+ audit record
+ notification
+ idempotency
```

That is an **approval workflow/action layer**.

Do not collapse these two abstractions together yet.

## Proposed project-two architecture

```text
Purchase Request
      ↓
project-local workflow service
      ↓
shared approval rule engine
      ↓
decision
      ↓
project-local stage transition
      ↓
audit event
      ↓
shared notification transport
```

Suggested local structure:

```text
procurement_requests/
├── procurement/
│   ├── doctype/
│   │   ├── purchase_request/
│   │   ├── purchase_request_item/
│   │   └── approval_event/
│   │
│   ├── approval/
│   │   ├── rules.py
│   │   ├── workflow.py
│   │   └── permissions.py
│   │
│   └── notifications.py
```

## Responsibility map

| Concern | Shared now? | Project-local now? | Promotion candidate? |
| --- | --- | --- | --- |
| Decision vocabulary | Yes | No | Already shared |
| Rule priority | Yes | No | Already shared |
| Explicit conflicts | Yes | No | Already shared |
| Deterministic resolver | Yes | No | Already shared |
| Purchase amount threshold | No | Yes | No |
| Manager/finance role names | No | Yes | No |
| Approval stage names | No | Yes | Possibly |
| Actor authorization | No | Yes | Yes |
| State transition engine | No | Yes | Yes |
| Approval audit record | No | Yes | Yes |
| Idempotent approval action | No | Yes | Yes |
| Transition-triggered notification | Transport shared | Trigger local | Yes |
| Purchase/receive/close flow | No | Yes | No |

## Boundary we should preserve

Do **not** add workflow state management into `na_approvals` yet.

Today the shared capability answers:

```text
What decision do the applicable rules produce?
```

Project two additionally needs:

```text
Who can perform the next action?
What state should this document move to?
What must be recorded?
Who must be notified?
```

Those are separate concerns until reuse proves otherwise.

## Why project two matters for `approval_action_workflow`

Project one already gave us this candidate:

```text
approval_action_workflow
```

Project two is the second materially different use.

Project one:

```text
Pending Approval
→ Approve & Book
→ Booked
```

Project two:

```text
Pending Manager Approval
→ manager approves
→ Pending Finance Approval

Pending Finance Approval
→ finance approves
→ Approved
```

The reusable intersection we are looking for is:

```text
authorized actor
      ↓
validate current state
      ↓
perform action once
      ↓
record actor + timestamp
      ↓
advance state
      ↓
trigger notification once
```

If that intersection survives both domains, it is strong evidence for extraction.

## Candidate shared shape after project two

Do **not** implement this interface yet. It is only a target shape to compare against actual code.

```python
transition = ApprovalTransition(
    action="approve",
    from_stage="manager",
    allowed_roles={"Manager"},
    to_stage="finance",
)

result = execute_transition(
    document=request,
    transition=transition,
    actor=current_user,
)
```

Potential generic result:

```text
TransitionResult
- action
- previous_state
- next_state
- actor
- timestamp
- changed
```

## Promotion decision after project two

If both projects actually implement the same underlying transition mechanics, promote:

```text
approval_action_workflow
candidate → proven
```

Extract only the generic mechanics.

Do **not** promote:

- purchase request fields
- manager/finance terminology
- $500 threshold
- procurement lifecycle
- purchase-specific messages

## Third-use test

The eventual third project should be able to use the extracted action/workflow layer without changing its core API.

That third materially different use is the compatibility test that tells us whether the abstraction is truly composable rather than merely shared between two projects.
