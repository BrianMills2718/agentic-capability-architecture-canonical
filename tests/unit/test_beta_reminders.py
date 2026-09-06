from datetime import datetime, timedelta
from types import SimpleNamespace
from unittest.mock import Mock, patch

from beta_rules.reminders import is_due, send_appointment_reminder


def test_reminder_is_due_only_within_lead_time():
    now = datetime(2026, 1, 1, 12, 0)
    appointment = SimpleNamespace(
        status="Confirmed",
        start_time=now + timedelta(minutes=60),
    )
    assert is_due(appointment, now)
    assert not is_due(
        SimpleNamespace(status="Cancelled", start_time=appointment.start_time),
        now,
    )


def test_reminder_delivery_is_durable_and_idempotent():
    appointment = SimpleNamespace(
        name="APT-00001",
        customer="person@example.com",
        start_time=datetime(2026, 1, 1, 12, 30),
        status="Confirmed",
    )
    delivery = Mock()
    frappe = SimpleNamespace(
        db=SimpleNamespace(exists=Mock(side_effect=[False, True])),
        get_doc=Mock(return_value=delivery),
        utils=SimpleNamespace(now_datetime=Mock(return_value=appointment.start_time)),
    )

    with patch("beta_rules.reminders.send_email") as send_email:
        assert send_appointment_reminder(appointment, frappe, now=datetime(2026, 1, 1, 12)) is True
        assert send_appointment_reminder(appointment, frappe, now=datetime(2026, 1, 1, 12)) is False

    delivery.insert.assert_called_once_with(ignore_permissions=True)
    delivery.db_set.assert_called_once_with("sent_at", appointment.start_time)
    send_email.assert_called_once()
