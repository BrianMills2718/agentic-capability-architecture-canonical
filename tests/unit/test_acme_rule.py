from types import SimpleNamespace

from acme_rules.appointment_rules import long_appointment_rule
from na_approvals.types import Decision


def test_acme_long_appointment_requires_approval():
    doc = SimpleNamespace(duration_minutes=180)
    result = long_appointment_rule(doc)
    assert result.decision == Decision.REQUIRE_APPROVAL
    assert result.priority == 50


def test_acme_normal_appointment_has_no_local_decision():
    doc = SimpleNamespace(duration_minutes=60)
    assert long_appointment_rule(doc) is None
