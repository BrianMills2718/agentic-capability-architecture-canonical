# Scheduling

Status: `candidate`

Scheduling now contains two layers whose maturity should not be conflated.

## Booking-oriented model

The shared Frappe `Appointment` model supports the existing appointment/booking consumers.

Declared capability interfaces:

- `appointment.create`
- `appointment.cancel`
- `appointment.reschedule`
- `availability.query`

`Appointment` remains intentionally booking-oriented. Project 6 did **not** reuse it as a
room/equipment/vehicle reservation record.

## Neutral temporal availability core

Project 6 introduced:

```text
na_scheduling.availability
```

with:

- `TimeWindow`
- `overlaps`
- `find_conflicts`
- `is_available`
- `validate_duration_minutes`

The shared interval convention is half-open:

```text
[start, end)
```

so back-to-back windows do not conflict.

## Real uses

Appointment/booking:

- `acme_reference`
- `client_intake_booking`

Shared-resource reservation:

- `resource_reservation`

The resource-reservation adapter selects active reservations for one project-local resource
and converts them to neutral `TimeWindow` values; Scheduling owns conflict semantics.

Seven-site Frappe v15 proof run `34046554727` passed:

```text
ACME                    6/6
Client Intake           4/4
Internal Procurement    5/5
IT Access Control       6/6
Facility Maintenance    4/4
Service Desk            5/5
Resource Reservation    5/5
```

## Why Scheduling remains candidate

Project 6 proves a genuinely reusable temporal core, but the current package still mixes:

```text
neutral time-window/conflict semantics
+
booking-specific Appointment model
```

Promote only after either a third materially different scheduling domain confirms the
boundary without shared changes, or repeated pressure justifies splitting the neutral
temporal layer from appointment-specific scheduling.
