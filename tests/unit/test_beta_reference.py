from datetime import datetime, timedelta
from types import SimpleNamespace

from beta_rules.appointment_rules import long_appointment_rule
from beta_rules.reminders import reminder_is_due
from na_approvals.types import Decision


def test_beta_appointments_over_90_minutes_require_approval():
    result = long_appointment_rule(SimpleNamespace(duration_minutes=91))
    assert result.decision == Decision.REQUIRE_APPROVAL
    assert result.priority == 50


def test_beta_90_minute_appointments_remain_allowed_by_local_rule():
    assert long_appointment_rule(SimpleNamespace(duration_minutes=90)) is None


def test_beta_reminder_window_is_explicit():
    now = datetime(2026, 9, 6, 12, 0)
    assert reminder_is_due(now + timedelta(minutes=15), now)
    assert not reminder_is_due(now + timedelta(minutes=16), now)
