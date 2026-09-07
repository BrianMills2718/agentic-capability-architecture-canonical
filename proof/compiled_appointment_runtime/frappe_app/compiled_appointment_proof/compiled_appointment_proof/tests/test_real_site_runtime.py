import json
import unittest

import frappe
from frappe.tests.utils import FrappeTestCase
from frappe.utils import add_to_date, now_datetime

from compiled_appointment_proof.adapter import execute_compiled_appointment


class TestCompiledAppointmentRealSite(FrappeTestCase):
    def make_appointment(self, *, duration: int):
        doc = frappe.get_doc({
            "doctype": "Appointment",
            "customer": f"compiled-{duration}@example.test",
            "start_time": add_to_date(now_datetime(), hours=24),
            "duration_minutes": duration,
            "status": "Pending",
            "approval_required": 0,
            "approval_reason": "",
        })
        doc.insert(ignore_permissions=True)
        return doc

    def test_over_90_persists_transition_receipt_and_queued_notification(self):
        appointment = self.make_appointment(duration=120)
        before_queue = frappe.db.count("Email Queue")

        result = execute_compiled_appointment(
            appointment_name=appointment.name,
            actor="Administrator",
            recipient="compiled-customer@example.test",
        )

        saved = frappe.get_doc("Appointment", appointment.name)
        self.assertEqual(saved.status, "Confirmed")
        self.assertEqual(saved.approval_required, 1)
        self.assertIn("exceeds 90 minutes", saved.approval_reason)

        comment = frappe.get_doc("Comment", result["receipt_comment"])
        payload = json.loads(comment.content)
        self.assertEqual(comment.reference_doctype, "Appointment")
        self.assertEqual(comment.reference_name, appointment.name)
        self.assertEqual(
            [receipt["semantic_action"] for receipt in payload["receipts"]],
            ["policy.resolve", "state.transition", "notification.send"],
        )
        self.assertEqual(
            payload["receipts"][1]["provenance"]["role_binding"],
            "role-binding:appointment-manager",
        )
        self.assertGreater(frappe.db.count("Email Queue"), before_queue)

    def test_exactly_90_does_not_require_approval(self):
        appointment = self.make_appointment(duration=90)
        result = execute_compiled_appointment(
            appointment_name=appointment.name,
            actor="Administrator",
            recipient="compiled-90@example.test",
        )
        saved = frappe.get_doc("Appointment", appointment.name)
        self.assertEqual(saved.approval_required, 0)
        self.assertEqual(saved.status, "Pending")
        self.assertEqual(result["receipts"][0]["outputs"]["decision"], "ALLOW")


if __name__ == "__main__":
    unittest.main()
