from types import SimpleNamespace

from na_approvals.types import Decision

from beta_rules.appointment_rules import collect_rule_results


def test_appointments_over_90_minutes_require_approval():
    result = collect_rule_results(SimpleNamespace(duration_minutes=91))[0]

    assert result.decision == Decision.REQUIRE_APPROVAL
    assert result.reason.endswith("90 minutes")


def test_appointments_at_90_minutes_are_allowed():
    assert collect_rule_results(SimpleNamespace(duration_minutes=90)) == []
