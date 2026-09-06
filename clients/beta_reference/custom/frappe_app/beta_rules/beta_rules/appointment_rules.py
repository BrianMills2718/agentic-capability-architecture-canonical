from na_approvals.engine import apply_resolution, resolve
from na_approvals.types import Decision, RuleResult


def long_appointment_rule(doc):
    if (doc.duration_minutes or 0) > 90:
        return RuleResult(
            rule="beta.long_appointment",
            decision=Decision.REQUIRE_APPROVAL,
            priority=50,
            reason="Beta requires approval for appointments longer than 90 minutes",
        )
    return None


RULES = [long_appointment_rule]


def validate_appointment(doc, method=None):
    resolution = resolve(
        [result for rule in RULES if (result := rule(doc)) is not None]
    )
    apply_resolution(doc, resolution)
