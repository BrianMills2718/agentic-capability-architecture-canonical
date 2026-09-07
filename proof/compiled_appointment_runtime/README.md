# Compiled appointment real-site proof

This proof exercises the exact maintained compiler requirement on a fresh Frappe v15 site without changing any production client's business policy.

Why a proof-local adapter exists:
- the maintained compiler example requires approval only when appointment duration is **over 90 minutes**;
- the existing Client Intake + Booking project legitimately uses a different 60-minute threshold;
- changing that client merely to make this proof pass would destroy domain meaning.

The proof-local adapter therefore owns only domain/runtime mapping for the exact compiled requirement. It reuses the shared providers:
- `na_approvals.engine.resolve`
- `na_core.transitions.plan_transition`
- `na_notifications.email.send_email`
- shared `Appointment` persistence from `na_scheduling`

The real-site assertions cover:
1. a 120-minute appointment requires approval, confirms through the shared transition planner, persists approval/status state, queues email, and stores a provenance-bearing execution receipt as a standard Frappe `Comment`;
2. an exactly-90-minute appointment does **not** require approval, auto-confirms, and only then receives the reminder;
3. the long-appointment transition receipt preserves `role-binding:appointment-manager` while the auto-confirm path does not invent that role binding.

The receipt uses an existing Frappe `Comment` rather than introducing a shared receipt DocType. This is evidence storage for the proof, not a new reusable capability.

Workflow: `.github/workflows/compiled-appointment-real-site-proof.yml`.
