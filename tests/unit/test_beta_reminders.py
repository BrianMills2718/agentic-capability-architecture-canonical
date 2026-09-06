from types import SimpleNamespace
from unittest.mock import patch

from beta_rules.reminders import send_appointment_reminder


def test_beta_appointment_reminder_uses_shared_email_transport():
    appointment = SimpleNamespace(customer="person@example.com", start_time="tomorrow")
    with patch("beta_rules.reminders.send_email") as send:
        send_appointment_reminder(appointment)
    send.assert_called_once_with(
        recipients="person@example.com",
        subject="Appointment reminder",
        message="Reminder: your appointment starts at tomorrow.",
    )
