# Facility Maintenance — MVP

## Goal

Let an internal requester report a facility/equipment issue, dispatch it to a technician,
track an SLA deadline, complete the work, and notify the requester.

## Users

- Requester
- Maintenance Dispatcher
- Maintenance Technician

## Maintenance Request

Fields:

- requester
- location
- asset_tag
- category
- description
- priority
- photo
- status
- assigned_to
- assigned_by
- assigned_at
- due_at
- started_at
- completed_at
- closed_at
- resolution
- completion_photo
- overdue_notified_at

## Lifecycle

```text
New
  ↓ dispatch
Assigned
  ↓ technician starts
In Progress
  ↓ technician completes
Completed
  ↓ requester/dispatcher closes
Closed
```

There is deliberately no approval stage.

## SLA policy

Default project settings:

```text
Urgent  = 4 hours
High    = 24 hours
Normal  = 72 hours
Low     = 120 hours
```

The due timestamp is calculated server-side when the request is assigned.

An hourly scheduler checks Assigned/In Progress requests whose due time has passed.
One overdue notification is sent for a given breach and `overdue_notified_at` records it.

## Attachments

The MVP uses Frappe-native Attach fields for:

- initial issue photo
- completion photo

This is evidence about attachment needs, not yet a reason to create a shared Files capability.

## Notifications

Use shared `na_notifications`.

Send when:

- assigned → technician
- completed → requester
- overdue → technician + dispatchers
- closed → optional requester confirmation

## Permissions

- Requester can create and view.
- Dispatcher assigns and can close completed work.
- Technician can start/complete only work assigned to them.
- UI buttons are not authorization.
- Server actions must be idempotent or reject invalid state explicitly.

## Non-goals

Do not build:

- inventory/spare parts
- vendor management
- purchase orders
- approval workflow
- appointment calendar
- preventive-maintenance scheduling
- asset-management platform
- generic SLA engine
- generic form builder

## Acceptance

1. Structured maintenance request can be created.
2. Attach field is available for an issue photo.
3. Dispatcher assignment calculates due time from priority.
4. Repeated identical assignment does not duplicate notifications.
5. Wrong technician cannot start/complete another technician's work.
6. Assigned technician can start work.
7. Technician can complete work with a required resolution.
8. Completion records timestamp and notifies requester.
9. Completed request can be closed.
10. Overdue scheduler identifies late open work.
11. Overdue notification is durable/idempotent.
12. No Approvals app is installed on this project's test site.
13. No Scheduling app is installed on this project's test site.
14. Existing four project suites remain green.
