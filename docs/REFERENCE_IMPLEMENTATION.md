# Reference Implementation

## Purpose

This reference project proves the architecture with the smallest useful example.

### Shared capabilities

- `na_scheduling`: owns the reusable Appointment model.
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

`acme_rules/tests/test_appointment_hook.py` is a real Frappe integration suite. It
uses a real `Appointment` document, `doc.run_method("validate")`, and `doc.insert()`.
It should be run after the three apps are installed on a Frappe test site.

## Reference acceptance scenario

ACME's bespoke requirement is:

> Appointments longer than 120 minutes require approval.

This remains project-local. If a second materially different project needs the
same behavior, we should consider generalizing it. A third use should test that
the generalized form composes without breaking the first two.
