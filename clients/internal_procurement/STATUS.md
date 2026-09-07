# Internal Procurement — Status

Current phase: **local implementation / pre-Frappe proof**.

Implemented:

- Purchase Request and child line-item DocTypes.
- Server-side line and request totals.
- Project-local Procurement Settings with finance threshold.
- Manager-only approval below threshold.
- Manager → Finance staged approval at/above threshold.
- Self-approval prevention and role enforcement.
- Rejection with audit event and reason.
- Ready to Purchase → Purchased → Received → Closed actions.
- Project-local approval/transition audit trail.
- Notifications through the shared Notifications capability.
- Desk buttons for requester, manager, finance, and procurement actions.
- Sequential idempotency for repeated approvals and fulfillment actions.

Next proof gate:

- Run the project on its own real Frappe v15 site alongside separate ACME and Client Intake sites.
- Keep all existing project regression suites green.
