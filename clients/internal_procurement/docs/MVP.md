# Internal Procurement — MVP Definition

## Goal

Build a small internal purchase-request workflow that meaningfully stress-tests the existing capability base without prematurely creating a generic procurement platform.

The MVP should prove that the system can support a multi-actor, multi-stage business workflow with money, child records, role-based actions, auditability, and notifications.

## Primary users

- **Requester** — submits a purchase request and tracks its status.
- **Manager** — approves or rejects the initial request.
- **Finance** — approves or rejects requests that exceed the finance threshold.
- **Procurement** — marks approved requests as purchased and later received/closed.

Executive approval is intentionally deferred from the first MVP unless the existing two-stage flow proves too easy to stress the architecture.

## Core records

### Purchase Request

Fields:

- requester
- department
- justification
- preferred_vendor
- status
- total_amount
- current_approval_stage
- submitted_at
- approved_at
- rejected_at
- rejection_reason
- purchased_at
- received_at

### Purchase Request Item

Child rows:

- description
- quantity
- unit_price
- line_total

Server-owned calculation:

```text
line_total = quantity × unit_price
total_amount = sum(line_total)
```

Client-side totals are display helpers only. The server is authoritative.

## Approval policy

### Tier 1 — below $500

```text
Draft
→ Pending Manager Approval
→ Approved
```

### Tier 2 — $500 or more

```text
Draft
→ Pending Manager Approval
→ Pending Finance Approval
→ Approved
```

The threshold is project configuration, not a shared-capability default.

## Lifecycle

```text
Draft
  ↓ submit
Pending Manager Approval
  ├─ reject → Rejected
  └─ approve
       ├─ total < $500 → Approved
       └─ total ≥ $500 → Pending Finance Approval
                              ├─ reject → Rejected
                              └─ approve → Approved
                                               ↓
                                        Ready to Purchase
                                               ↓
                                           Purchased
                                               ↓
                                           Received
                                               ↓
                                            Closed
```

For MVP simplicity, `Approved` may transition immediately to `Ready to Purchase`.

## Required actions

Requester:

- create draft
- edit draft
- submit
- view status

Manager:

- approve manager stage
- reject manager stage

Finance:

- approve finance stage
- reject finance stage

Procurement:

- mark purchased
- mark received
- close request

## Notification behavior

Reuse the existing shared Notifications capability.

Send notifications for:

- submission → manager
- manager approval requiring finance → finance
- rejection → requester
- final approval → requester and procurement
- purchased → requester
- received/closed → requester

Templates stay project-local for now.

## Audit requirements

Every approval/rejection transition records:

- actor
- timestamp
- decision
- stage
- optional reason

Do not rely only on the current status field as the audit trail.

For the MVP, this may live in a project-local `Approval Event` child DocType.

## Permissions

The server enforces action permissions. UI button visibility is not authorization.

At minimum:

- Requesters cannot approve their own requests.
- Managers can act only on the manager stage.
- Finance can act only on the finance stage.
- Procurement cannot bypass approvals.
- Repeated transitions are idempotent or explicitly rejected.

## Reuse requirements

Reuse:

- `core`
- `approvals`
- `notifications`

Scheduling is intentionally **not** included. Project two should prove that the capability base is useful outside the booking domain.

## What stays project-local

Keep these local until repetition proves otherwise:

- Purchase Request DocTypes
- procurement status names
- $500 threshold
- manager/finance role mapping
- purchase/receive/close actions
- procurement email templates
- purchase-specific audit fields

## Explicit non-goals

Do not build these yet:

- vendor management
- purchase orders
- inventory
- accounts payable
- invoice matching
- budgets
- three-way matching
- executive approval
- ERP integrations
- generic workflow designer
- generic form builder

## MVP acceptance tests

The project is MVP-complete when all of the following pass:

1. A requester can create a request with multiple line items.
2. Server-side totals are correct.
3. A request under $500 needs manager approval only.
4. A request at/above $500 needs manager then finance approval.
5. A manager cannot approve the finance stage.
6. Finance cannot act before manager approval.
7. The requester cannot approve their own request.
8. Rejection records actor, stage, timestamp, and reason.
9. Final approval notifies the correct users.
10. Procurement can mark an approved request purchased, received, then closed.
11. Repeated approval/action calls do not duplicate notifications or corrupt state.
12. The project runs on its own Frappe site and does not install another client's custom app.
13. Existing Client Intake + Booking and ACME regression tests remain green.
14. New reusable observations are recorded without prematurely promoting them.
