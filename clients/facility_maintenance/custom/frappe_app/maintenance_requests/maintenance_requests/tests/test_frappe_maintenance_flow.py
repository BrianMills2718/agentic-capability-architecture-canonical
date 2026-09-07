import unittest
from unittest.mock import patch

try:
    import frappe
    from frappe.tests.utils import FrappeTestCase
except ImportError:
    frappe = None
    FrappeTestCase = unittest.TestCase


@unittest.skipIf(frappe is None, "requires real Frappe")
class TestMaintenanceFlow(FrappeTestCase):
    def setUp(self):
        self.users = {}
        for key, role in [
            ("requester", None),
            ("dispatcher", "Maintenance Dispatcher"),
            ("tech", "Maintenance Technician"),
            ("othertech", "Maintenance Technician"),
        ]:
            email = f"_test_maint_{key}@example.com"
            if not frappe.db.exists("User", email):
                user = frappe.get_doc({
                    "doctype": "User",
                    "email": email,
                    "first_name": key.title(),
                    "send_welcome_email": 0,
                }).insert(ignore_permissions=True)
                if role:
                    user.add_roles(role)
            self.users[key] = email

    def make_request(self, priority="High"):
        frappe.set_user(self.users["requester"])
        return frappe.get_doc({
            "doctype": "Maintenance Request",
            "requester": self.users["requester"],
            "location": "Plant 1",
            "asset_tag": "PUMP-17",
            "category": "Equipment",
            "description": "Pump vibration is above normal.",
            "priority": priority,
        }).insert(ignore_permissions=True)

    def test_assignment_sets_due_time_and_is_idempotent(self):
        from maintenance_requests.workflow import assign

        doc = self.make_request("High")
        frappe.set_user(self.users["dispatcher"])

        with patch("maintenance_requests.notifications.send_email") as send_email:
            assign(doc, technician=self.users["tech"], actor=self.users["dispatcher"])
            doc.reload()
            first_due = doc.due_at
            first_assigned_at = doc.assigned_at
            self.assertEqual(doc.status, "Assigned")
            self.assertTrue(first_due > first_assigned_at)

            assign(doc, technician=self.users["tech"], actor=self.users["dispatcher"])
            doc.reload()

        self.assertEqual(doc.due_at, first_due)
        self.assertEqual(doc.assigned_at, first_assigned_at)
        send_email.assert_called_once()

    def test_wrong_technician_cannot_start(self):
        from maintenance_requests.workflow import assign, start

        doc = self.make_request()
        with patch("maintenance_requests.notifications.send_email"):
            assign(doc, technician=self.users["tech"], actor=self.users["dispatcher"])

        with self.assertRaises(Exception):
            start(doc, actor=self.users["othertech"])

    def test_assigned_technician_can_start_complete_and_requester_close(self):
        from maintenance_requests.workflow import assign, start, complete, close

        doc = self.make_request()

        with patch("maintenance_requests.notifications.send_email") as send_email:
            assign(doc, technician=self.users["tech"], actor=self.users["dispatcher"])
            start(doc, actor=self.users["tech"])
            complete(doc, resolution="Replaced failed bearing.", actor=self.users["tech"])

        doc.reload()
        self.assertEqual(doc.status, "Completed")
        self.assertEqual(doc.resolution, "Replaced failed bearing.")
        # One assignment notification + one completion notification.
        self.assertEqual(send_email.call_count, 2)

        close(doc, actor=self.users["requester"])
        doc.reload()
        self.assertEqual(doc.status, "Closed")
        self.assertTrue(doc.closed_at)

    def test_overdue_job_marks_notification_once(self):
        from frappe.utils import add_to_date, now_datetime
        from maintenance_requests import sla
        from maintenance_requests.workflow import assign

        doc = self.make_request("Urgent")
        with patch("maintenance_requests.notifications.send_email"):
            assign(doc, technician=self.users["tech"], actor=self.users["dispatcher"])

        frappe.db.set_value(
            "Maintenance Request",
            doc.name,
            {
                "due_at": add_to_date(now_datetime(), hours=-1),
                "overdue_notified_at": None,
            },
            update_modified=False,
        )

        with patch("maintenance_requests.notifications.send_email") as send_email:
            sla.notify_overdue_requests()
            first = frappe.db.get_value(
                "Maintenance Request", doc.name, "overdue_notified_at"
            )
            self.assertTrue(first)

            sla.notify_overdue_requests()
            second = frappe.db.get_value(
                "Maintenance Request", doc.name, "overdue_notified_at"
            )

        self.assertEqual(first, second)
        # One technician email; dispatcher-role email may add a second call if test users exist.
        self.assertGreaterEqual(send_email.call_count, 1)
        first_run_calls = send_email.call_count

        # A third pass must still be a no-op.
        with patch("maintenance_requests.notifications.send_email") as third_send:
            sla.notify_overdue_requests()
        third_send.assert_not_called()
