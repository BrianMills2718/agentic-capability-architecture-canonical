from datetime import datetime
from types import ModuleType, SimpleNamespace

import beta_rules.reminders as reminders
from beta_rules.reminders import reminder_key


def test_reminder_key_is_stable_for_an_appointment():
    appointment = SimpleNamespace(name="APT-00001")

    assert reminder_key(appointment) == "beta-reference:appointment:APT-00001:reminder"


def test_due_reminder_is_idempotent(monkeypatch):
    appointment = SimpleNamespace(
        name="APT-00001",
        customer="person@example.com",
        start_time="2026-09-06 04:00:00",
    )
    delivered = set()
    sent = []

    class FakeDB:
        def exists(self, doctype, filters):
            return filters["idempotency_key"] in delivered

    class FakeDoc:
        def insert(self, ignore_permissions=False):
            delivered.add(self.idempotency_key)

    fake_frappe = ModuleType("frappe")
    fake_frappe.db = FakeDB()
    fake_frappe.get_all = lambda *args, **kwargs: [appointment]

    def get_doc(values):
        doc = FakeDoc()
        doc.__dict__.update(values)
        return doc

    fake_frappe.get_doc = get_doc
    fake_utils = ModuleType("frappe.utils")
    fake_utils.now_datetime = lambda: datetime(2026, 9, 6, 3, 30)
    monkeypatch.setitem(__import__("sys").modules, "frappe", fake_frappe)
    monkeypatch.setitem(__import__("sys").modules, "frappe.utils", fake_utils)
    monkeypatch.setattr(reminders, "send_email", lambda **kwargs: sent.append(kwargs))

    reminders.send_due_reminders()
    reminders.send_due_reminders()

    assert len(sent) == 1
