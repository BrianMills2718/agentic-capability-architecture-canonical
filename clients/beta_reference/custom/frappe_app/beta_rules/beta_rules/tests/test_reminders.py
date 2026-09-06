from types import SimpleNamespace
from unittest.mock import patch

from beta_rules.reminders import send_appointment_reminder


def test_appointment_reminder_uses_shared_email_transport():
    appointment = SimpleNamespace(start_time="2030-01-01 10:00:00")
    with patch("beta_rules.reminders.send_email") as send_email:
        send_appointment_reminder(
            recipients="customer@example.com",
            appointment=appointment,
        )

    send_email.assert_called_once_with(
        recipients="customer@example.com",
        subject="Appointment reminder",
        message="Reminder: your appointment starts at 2030-01-01 10:00:00.",
    )
