from types import SimpleNamespace

from beta_rules.appointment_rules import long_appointment_rule
from na_approvals.types import Decision


def test_beta_appointments_over_90_minutes_require_approval():
    result = long_appointment_rule(SimpleNamespace(duration_minutes=91))

    assert result.decision == Decision.REQUIRE_APPROVAL
    assert result.priority == 50


def test_beta_90_minute_appointment_has_no_local_decision():
    assert long_appointment_rule(SimpleNamespace(duration_minutes=90)) is None
