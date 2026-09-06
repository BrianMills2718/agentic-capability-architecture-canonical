# Shipment Exception Workflow

Follow the repository capabilities-first workflow and keep all project-specific behavior outside the shared capability layer.

## Required steps
1. Read `AGENT_RULES.md` and the repository capability registry before making a change.
2. Create `CAPABILITY_PLAN.yml` before implementation files.
3. Use the existing shared `core`, `scheduling`, `approvals`, and `notifications` capabilities when possible.
4. Compose a project-specific `shipment_exception` extension that enforces review for delayed or blocked shipments.
5. Validate the workflow with focused tests and the repository bootstrap gate.

## Acceptance criteria
- The project manifest declares the expected capability set.
- The custom extension keeps shipment-specific logic local.
- Delayed or blocked shipments resolve to a deterministic approval/block result.
- Follow-up notification behavior is wired through the shared notifications adapter.
- Each project records a reuse assessment in `clients/<project>/LEARNINGS.md`.
