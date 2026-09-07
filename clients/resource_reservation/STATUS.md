# Shared Resource Reservation — Status

Current phase: **prospective implementation scaffold complete locally; real-Frappe proof pending**.

Implemented locally:

- project-first primitive/capability model;
- project-local Reservable Resource and Resource Reservation Frappe app structure;
- availability/overlap logic for half-open time windows;
- reserve, reschedule, and cancel workflow adapters;
- Notifications integration boundary;
- local permission and contract tests.

Current local verification:

```text
5 passed
5 expected real-Frappe lifecycle skips
resource_reservations wheel builds successfully
```

Not yet proven:

- installation on an isolated real Frappe site;
- concurrency behavior under simultaneous reservation attempts;
- non-appointment reuse of the shared Scheduling capability in a real runtime.

Therefore this project **must not** be counted among the five completed/proven real projects yet.
