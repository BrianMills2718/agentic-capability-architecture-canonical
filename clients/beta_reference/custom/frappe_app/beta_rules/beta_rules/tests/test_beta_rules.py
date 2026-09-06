from types import SimpleNamespace

from na_approvals.types import Decision

from beta_rules.appointment_rules import collect_rule_results
from beta_rules.hooks import scheduler_events


def test_appointments_over_90_minutes_require_approval():
    results = collect_rule_results(SimpleNamespace(duration_minutes=91))

    assert len(results) == 1
    assert results[0].decision == Decision.REQUIRE_APPROVAL
    assert results[0].priority == 50


def test_90_minute_appointments_remain_allowed_by_beta_rule():
    assert collect_rule_results(SimpleNamespace(duration_minutes=90)) == []


def test_reminders_are_registered_on_hourly_scheduler():
    assert scheduler_events["hourly"] == [
        "beta_rules.reminders.send_due_appointment_reminders"
    ]
