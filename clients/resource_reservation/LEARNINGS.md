# Shared Resource Reservation — Learnings

Current state: **prospective model plus local implementation scaffold; real-Frappe proof pending**.

Questions under test:

1. Is Scheduling actually reusable outside customer/appointment booking?
2. Is `availability.query` the stable cross-domain part while `Appointment` remains booking-specific?
3. Does the primitive graph need a new temporal primitive, or is availability better modeled as a higher-level Scheduling capability interface?
4. Can resource identity remain project-local while shared code owns interval semantics?
5. What database/concurrency contract is required to prevent simultaneous conflicting reservations?

Local implementation already suggests that resource identity and reservation records should remain project-native. The key unresolved issue is whether shared Scheduling genuinely provides a reusable non-appointment availability contract in real Frappe; that requires external proof before any promotion decision.
