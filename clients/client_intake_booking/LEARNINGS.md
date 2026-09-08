# Client Intake + Booking — Reuse Assessment

This project reuses `core`, `scheduling`, `approvals`, and `notifications` while keeping structured client-intake behavior in the local `intake_booking` extension.

## Current assessment

- Structured client intake is a first-use local concern; **no promotion candidate yet**.
- The project provides an early real-project use of shared scheduling, approval resolution, and notification transport, but it does not by itself justify broadening those capability contracts.
- The client-specific service types, 60-minute approval threshold, intake fields, and notification timing/copy remain local configuration or domain behavior.
- Automatic confirmation versus pending approval is a workflow/domain concern; reusable approval resolution must not be mistaken for the whole approval lifecycle.

Revisit promotion only after a materially different project needs the same intake semantics or exposes a stable smaller interface worth sharing.
