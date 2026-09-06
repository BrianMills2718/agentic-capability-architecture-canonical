import sys
import types
from datetime import datetime, timedelta
from types import SimpleNamespace

from beta_rules import reminders


def test_reminder_job_is_idempotent_for_an_appointment(monkeypatch):
    sent = []
    delivered = set()
    appointment = SimpleNamespace(
        name="APT-00001",
        customer="person@example.com",
        start_time=datetime(2026, 9, 6, 4, 0),
    )

    class Delivery:
        name = "APT-00001"

        def insert(self, ignore_permissions=False):
            delivered.add(appointment.name)

    fake_frappe = types.ModuleType("frappe")
    fake_frappe.get_all = lambda *args, **kwargs: [appointment]
    fake_frappe.get_doc = lambda values: Delivery()
    fake_frappe.DuplicateEntryError = RuntimeError
    fake_frappe.db = SimpleNamespace(
        exists=lambda doctype, filters: appointment.name in delivered
    )
    fake_utils = types.ModuleType("frappe.utils")
    fake_utils.add_to_date = lambda value, minutes: value + timedelta(minutes=minutes)
    fake_utils.now_datetime = lambda: datetime(2026, 9, 6, 3, 30)
    fake_frappe.utils = fake_utils
    monkeypatch.setitem(sys.modules, "frappe", fake_frappe)
    monkeypatch.setitem(sys.modules, "frappe.utils", fake_utils)
    monkeypatch.setattr(
        reminders,
        "send_email",
        lambda **kwargs: sent.append(kwargs),
    )

    assert reminders.send_due_appointment_reminders() == 1
    assert reminders.send_due_appointment_reminders() == 0
    assert len(sent) == 1
