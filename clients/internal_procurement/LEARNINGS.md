# Internal Procurement — Reuse Assessment

## What Project 2 reuses

This project deliberately reuses the shared `approvals` decision resolver and
`notifications` transport while excluding Scheduling entirely.

The finance threshold is evaluated through the shared approval vocabulary and
resolver. Procurement-specific states, roles, audit fields, and actions remain local.

## Second materially different use: approval_action_workflow

Project 1 used this pattern for a client consultation:

```text
Pending Approval
→ authorized staff action
→ record approver/time
→ Booked
→ notify once
```

Project 2 independently needs the same core mechanics in a different domain:

```text
Pending Manager Approval
→ authorize actor
→ validate stage
→ record approval event
→ advance state
→ notify next actor once

Pending Finance Approval
→ authorize different actor
→ validate stage
→ record approval event
→ advance state
→ notify requester/procurement once
```

The common intersection is now visible in real code:

- actor authorization,
- current-state/stage validation,
- a single auditable transition,
- actor + timestamp recording,
- idempotent repeated action handling,
- transition-triggered notification.

This is stronger evidence than Project 1 alone, but we should not extract a shared
workflow engine until the Project 2 lifecycle passes in real Frappe and we compare the
actual implementations side by side.

## What must remain local

Do not promote these procurement-specific concepts:

- Purchase Request / Purchase Request Item,
- $500 finance threshold,
- Manager / Finance / Procurement role names,
- procurement status names,
- purchase / receive / close actions,
- procurement notification copy.

## Current promotion assessment

`approval_action_workflow` should move from **observed** to **candidate** because this
is its second materially different implementation.

It is not yet `proven`/shared code. Promotion should happen only after the real-Frappe
Project 2 proof passes and the extracted API can serve both Project 1 and Project 2
without embedding either domain's terminology.
