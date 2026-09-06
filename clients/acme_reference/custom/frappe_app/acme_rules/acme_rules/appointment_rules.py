from na_approvals.engine import apply_resolution, resolve
from na_approvals.types import Decision, RuleResult


def long_appointment_rule(doc):
    if (doc.duration_minutes or 0) > 120:
        return RuleResult(
            rule="acme.long_appointment",
            decision=Decision.REQUIRE_APPROVAL,
            priority=50,
            reason="ACME requires approval for appointments longer than 120 minutes",
        )
    return None


RULES = [long_appointment_rule]


def collect_rule_results(doc):
    return [result for rule in RULES if (result := rule(doc)) is not None]


def validate_appointment(doc, method=None):
    results = collect_rule_results(doc)
    resolution = resolve(results)

    if resolution is not None and resolution.decision == Decision.BLOCK:
        # Keep Frappe dependency at the adapter edge.
        import frappe
        frappe.throw("; ".join(resolution.reasons))

    apply_resolution(doc, resolution)
