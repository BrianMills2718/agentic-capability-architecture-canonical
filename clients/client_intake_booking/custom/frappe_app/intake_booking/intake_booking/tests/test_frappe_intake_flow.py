import unittest
from unittest.mock import patch

try:
    import frappe
    from frappe.tests.utils import FrappeTestCase
    from frappe.utils import add_to_date, now_datetime
    from intake_booking.api import submit_intake
except ImportError:
    frappe = None
    FrappeTestCase = unittest.TestCase
    add_to_date = now_datetime = submit_intake = None


@unittest.skipIf(frappe is None, "real Frappe lifecycle test")
class TestClientIntakeFlow(FrappeTestCase):
    def make_intake(self, *, email, duration):
        return frappe.get_doc({
            "doctype": "Service Intake",
            "client_name": "Integration Client",
            "email": email,
            "service_type": "Consultation",
            "request_summary": "Discuss an engagement",
            "requested_start_time": add_to_date(now_datetime(), hours=24),
            "requested_duration_minutes": duration,
            "status": "Submitted",
        })

    def test_desk_style_insert_books_short_consultation(self):
        intake = self.make_intake(email="desk@example.com", duration=60)
        with patch("intake_booking.workflow.send_email") as send_email:
            intake.insert()
        intake.reload()
        appointment = frappe.get_doc("Appointment", intake.appointment)
        self.assertEqual(intake.status, "Booked")
        self.assertEqual(appointment.status, "Confirmed")
        self.assertFalse(bool(appointment.approval_required))
        send_email.assert_called_once()

    def test_desk_style_insert_leaves_long_consultation_pending(self):
        intake = self.make_intake(email="desk-long@example.com", duration=90)
        with patch("intake_booking.workflow.send_email"):
            intake.insert()
        intake.reload()
        appointment = frappe.get_doc("Appointment", intake.appointment)
        self.assertEqual(intake.status, "Pending Approval")
        self.assertTrue(bool(appointment.approval_required))
        self.assertEqual(appointment.status, "Pending")

    def test_authenticated_api_uses_same_doctype_workflow(self):
        with patch("intake_booking.workflow.send_email") as send_email:
            result = submit_intake(
                client_name="API Client",
                email="api@example.com",
                service_type="Project Discovery",
                request_summary="Discuss a discovery engagement",
                requested_start_time=add_to_date(now_datetime(), hours=48),
                requested_duration_minutes=60,
            )
        intake = frappe.get_doc("Service Intake", result["intake"])
        self.assertEqual(result["appointment"], intake.appointment)
        self.assertEqual(result["status"], "Booked")
        send_email.assert_called_once()
