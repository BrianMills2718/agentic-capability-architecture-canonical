# Shared Resource Reservation — MVP

## Goal

Allow users to reserve an active shared resource for a time window while preventing
overlapping active reservations.

## Local records

### Reservable Resource

- resource_code
- title
- resource_type: Room | Equipment | Vehicle
- location
- active

### Resource Reservation

- requester
- resource
- purpose
- start_time
- duration_minutes
- status: Draft | Reserved | Cancelled
- reserved_at
- rescheduled_at
- cancelled_at

## Actions

### Reserve

```text
Draft
→ query availability for same resource/time window
→ if free: Reserved
→ notify requester
```

### Reschedule

```text
Reserved
→ query availability excluding self
→ if free: update start/duration
→ remain Reserved
→ notify requester
```

### Cancel

```text
Reserved
→ Cancelled
→ slot becomes available
→ notify requester
```

## Availability semantics

Use half-open time intervals:

```text
[start, end)
```

Therefore:

```text
10:00–11:00
11:00–12:00
```

do not overlap.

Resource identity remains project-local. The shared Scheduling layer should operate on time
windows; project code selects candidate reservations for the same resource.

## Non-goals

- approval workflow;
- customer appointment semantics;
- recurring reservations;
- capacity >1;
- waitlists;
- calendar UI;
- timezone conversion policy;
- generic asset management;
- generalized booking marketplace.
