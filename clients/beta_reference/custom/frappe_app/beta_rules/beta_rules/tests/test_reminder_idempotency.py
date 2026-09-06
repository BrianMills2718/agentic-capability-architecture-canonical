from unittest.mock import patch

import pytest

frappe = pytest.importorskip("frappe", reason="real Frappe lifecycle test")
from frappe.tests.utils import FrappeTestCase
from frappe.utils import add_to_date, now_datetime

from beta_rules.reminder_scheduler import schedule_reminders


class TestReminderIdempotency(FrappeTestCase):
    def test_repeated_scheduler_runs_send_one_reminder(self):
        appointment = frappe.get_doc(
            {
                "doctype": "Appointment",
                "customer": "reminder@example.com",
                "start_time": add_to_date(now_datetime(), minutes=30),
                "duration_minutes": 30,
                "status": "Confirmed",
            }
        ).insert(ignore_permissions=True)

        with patch("beta_rules.reminder_scheduler.send_email") as send_email:
            schedule_reminders()
            schedule_reminders()

        send_email.assert_called_once()
        self.assertTrue(
            frappe.db.exists(
                "Appointment Reminder Sent", {"appointment": appointment.name}
            )
        )
