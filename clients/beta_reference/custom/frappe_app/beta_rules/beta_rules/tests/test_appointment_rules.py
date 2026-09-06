from types import SimpleNamespace

from beta_rules.appointment_rules import long_appointment_rule
from na_approvals.types import Decision


def test_beta_long_appointment_requires_approval():
    result = long_appointment_rule(SimpleNamespace(duration_minutes=91))

    assert result.decision == Decision.REQUIRE_APPROVAL
    assert result.priority == 50


def test_beta_threshold_boundary_remains_allowed():
    assert long_appointment_rule(SimpleNamespace(duration_minutes=90)) is None
