# Reference Implementation

> **Status: preserved proof fixture / early example.** This document demonstrates the original shared/config/local pattern. It is not a production recommendation to rebuild appointment scheduling or approval workflow when Frappe/ERPNext or another mature provider already satisfies the real requirement. For current architecture and sourcing rules, use `ARCHITECTURE_CHARTER.md` and `PROJECT_WORKFLOW.md`.

## Purpose

This reference project proves the architecture with a small controlled example.

### Shared capabilities

- `na_scheduling`: owns the reusable Appointment model in this proof fixture.
- `na_approvals`: owns deterministic approval-rule resolution.

### Project-specific extension

- `acme_rules`: hooks `Appointment.validate` and contributes ACME-only rules.

### Composition

```text
na_scheduling
      │
      │ Appointment.validate
      ▼
acme_rules
      │
      │ emits RuleResult values
      ▼
na_approvals
      │
      ▼
deterministic Resolution
```

`na_scheduling` does not import or mention ACME.

## What is proven locally

The root `pytest` suite tests:

- ALLOW vs REQUIRE priority,
- REQUIRE vs ALLOW priority,
- BLOCK precedence,
- equal-priority agreement,
- equal-priority disagreement,
- explicit conflicts,
- deterministic ordering,
- monotonic ALLOW behavior,
- ACME's local long-appointment rule,
- project manifest registration,
- absence of ACME-specific behavior from shared Scheduling code.

## What requires a Frappe environment

`acme_rules/tests/test_appointment_hook.py` is a real Frappe integration suite. It uses a real `Appointment` document, `doc.run_method("validate")`, and `doc.insert()`.

The baseline real-Frappe proof has since passed; current evidence is indexed in `PROOF_LEDGER_EXTENDED.md` and `FRAPPE_TEST_STATUS.md`.

## Reference acceptance scenario

ACME's bespoke requirement is:

> Appointments longer than 120 minutes require approval.

This remains project-local in the fixture. Repeated demand may justify a reusable semantic boundary, but extraction should be evaluated against existing platform/ecosystem/external implementations first. A second or third use is evidence pressure, not an automatic instruction to build a new shared product.
