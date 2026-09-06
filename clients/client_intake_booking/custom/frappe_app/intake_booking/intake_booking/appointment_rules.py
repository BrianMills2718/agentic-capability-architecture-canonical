from na_approvals.engine import apply_resolution, resolve
from na_approvals.types import Decision, RuleResult

APPROVAL_THRESHOLD_MINUTES = 60

def long_appointment_rule(doc):
    duration = int(getattr(doc, "duration_minutes", 0) or 0)
    if duration > APPROVAL_THRESHOLD_MINUTES:
        return RuleResult(rule="client_intake_booking.long_appointment", decision=Decision.REQUIRE_APPROVAL, priority=50, reason=f"Appointments over {APPROVAL_THRESHOLD_MINUTES} minutes require review")
    return None

RULES = [long_appointment_rule]

def collect_rule_results(doc):
    return [result for rule in RULES if (result := rule(doc)) is not None]

def validate_appointment(doc, method=None):
    resolution = resolve(collect_rule_results(doc))
    if resolution is not None and resolution.decision == Decision.BLOCK:
        import frappe
        frappe.throw("; ".join(resolution.reasons))
    apply_resolution(doc, resolution)
