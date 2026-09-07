# Service Desk — MVP

## Purpose

Provide a small support-request system that is useful on its own and prospectively tests the
primitive/capability architecture before implementation.

## Lifecycle

```text
New
→ Triaged
→ Assigned
→ In Progress
↔ Waiting on Requester
→ Resolved
→ Closed
```

## Roles

- Requester
- Support Dispatcher
- Support Agent

## Core fields

- requester
- subject
- category
- description
- priority
- attachment
- status
- assigned_to
- assigned_by
- assigned_at
- due_at
- started_at
- waiting_since
- resumed_at
- resolved_at
- closed_at
- resolution
- overdue_notified_at

## SLA defaults

```text
Urgent = 2 hours
High   = 8 hours
Normal = 24 hours
Low    = 72 hours
```

## Non-goals

- approvals
- appointment scheduling
- knowledge base
- omnichannel chat/email ingestion
- customer portal polish
- generic SLA engine
- generic ticketing framework
- generic comments system
