from types import SimpleNamespace

from beta_rules.appointment_rules import long_appointment_rule
from beta_rules import hooks
from beta_rules.reminders import reminder_message
from na_approvals.types import Decision


def test_beta_appointments_over_90_minutes_require_approval():
    result = long_appointment_rule(SimpleNamespace(duration_minutes=91))

    assert result.decision == Decision.REQUIRE_APPROVAL
    assert result.priority == 50


def test_beta_appointment_at_90_minutes_has_no_local_decision():
    assert long_appointment_rule(SimpleNamespace(duration_minutes=90)) is None


def test_beta_reminders_are_scheduled_hourly():
    assert hooks.scheduler_events == {
        "hourly": ["beta_rules.reminders.send_due_reminders"]
    }


def test_beta_reminder_message_includes_appointment_details():
    appointment = SimpleNamespace(start_time="2030-01-01 10:00", duration_minutes=45)

    assert reminder_message(appointment) == (
        "Reminder: your appointment starts at 2030-01-01 10:00 and lasts 45 minutes."
    )
