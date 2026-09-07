import unittest
from unittest.mock import patch

try:
    import frappe
    from frappe.tests.utils import FrappeTestCase
    from procurement_requests.install import ensure_project_roles
    from procurement_requests import workflow
except ImportError:  # local bootstrap runs without Frappe installed
    frappe = None
    FrappeTestCase = unittest.TestCase
    ensure_project_roles = workflow = None


@unittest.skipIf(frappe is None, "real Frappe lifecycle test")
class TestInternalProcurementFlow(FrappeTestCase):
    def setUp(self):
        super().setUp()
        ensure_project_roles()
        self.requester = self.ensure_user("proc-requester@example.com", "Procurement Requester")
        self.manager = self.ensure_user("proc-manager@example.com", "Procurement Manager")
        self.finance = self.ensure_user("proc-finance@example.com", "Procurement Finance")
        self.officer = self.ensure_user("proc-officer@example.com", "Procurement Officer")
        frappe.db.set_single_value("Procurement Settings", "finance_threshold", 500)
        frappe.db.set_single_value("Procurement Settings", "currency", "USD")

    def ensure_user(self, email, role):
        if frappe.db.exists("User", email):
            user = frappe.get_doc("User", email)
        else:
            user = frappe.get_doc(
                {
                    "doctype": "User",
                    "email": email,
                    "first_name": email.split("@", 1)[0],
                    "send_welcome_email": 0,
                }
            )
            user.insert(ignore_permissions=True)
        if role not in frappe.get_roles(email):
            user.add_roles(role)
        return email

    def make_request(self, *, unit_price, quantity=1, requester=None):
        doc = frappe.get_doc(
            {
                "doctype": "Purchase Request",
                "requester": requester or self.requester,
                "department": "Operations",
                "justification": "Needed for project delivery",
                "preferred_vendor": "Example Vendor",
                "items": [
                    {
                        "doctype": "Purchase Request Item",
                        "description": "Equipment",
                        "quantity": quantity,
                        "unit_price": unit_price,
                    }
                ],
            }
        )
        doc.insert(ignore_permissions=True)
        doc.reload()
        return doc

    def test_under_threshold_needs_manager_only(self):
        request = self.make_request(unit_price=200, quantity=2)
        self.assertEqual(request.total_amount, 400)

        with patch("procurement_requests.workflow.notify_role") as notify_role, patch(
            "procurement_requests.workflow.notify_requester"
        ) as notify_requester:
            workflow.submit_request(request, actor=self.requester)
            request.reload()
            self.assertEqual(request.status, "Pending Manager Approval")

            workflow.approve_manager(request, actor=self.manager)
            request.reload()

        self.assertEqual(request.status, "Ready to Purchase")
        self.assertEqual(request.current_approval_stage or "", "")
        self.assertTrue(request.approved_at)
        self.assertEqual(request.approval_events[-1].stage, "Manager")
        self.assertEqual(request.approval_events[-1].action, "Approve")
        self.assertEqual(notify_role.call_count, 2)  # manager + procurement officer
        notify_requester.assert_called_once()

    def test_finance_threshold_requires_second_distinct_approval(self):
        request = self.make_request(unit_price=500)

        with patch("procurement_requests.workflow.notify_role"), patch(
            "procurement_requests.workflow.notify_requester"
        ):
            workflow.submit_request(request, actor=self.requester)
            request.reload()
            workflow.approve_manager(request, actor=self.manager)
            request.reload()

            self.assertEqual(request.status, "Pending Finance Approval")
            self.assertEqual(request.current_approval_stage, "Finance")

            with self.assertRaises(frappe.ValidationError):
                workflow.approve_finance(request, actor=self.manager)

            workflow.approve_finance(request, actor=self.finance)
            request.reload()

        self.assertEqual(request.status, "Ready to Purchase")
        self.assertTrue(request.approved_at)
        self.assertEqual(
            [(row.stage, row.action) for row in request.approval_events[-2:]],
            [("Manager", "Approve"), ("Finance", "Approve")],
        )

    def test_requester_cannot_approve_own_request_even_with_manager_role(self):
        requester_user = frappe.get_doc("User", self.requester)
        if "Procurement Manager" not in frappe.get_roles(self.requester):
            requester_user.add_roles("Procurement Manager")

        request = self.make_request(unit_price=100)
        with patch("procurement_requests.workflow.notify_role"):
            workflow.submit_request(request, actor=self.requester)
        request.reload()

        with self.assertRaises(frappe.ValidationError):
            workflow.approve_manager(request, actor=self.requester)

    def test_rejection_is_audited_and_notifies_once(self):
        request = self.make_request(unit_price=700)
        with patch("procurement_requests.workflow.notify_role"):
            workflow.submit_request(request, actor=self.requester)
        request.reload()

        with patch("procurement_requests.workflow.notify_requester") as notify_requester:
            workflow.reject_manager(request, actor=self.manager, reason="Not budgeted")
            request.reload()
            workflow.reject_manager(request, actor=self.manager, reason="Not budgeted")

        self.assertEqual(request.status, "Rejected")
        self.assertEqual(request.rejection_reason, "Not budgeted")
        self.assertTrue(request.rejected_at)
        event = request.approval_events[-1]
        self.assertEqual(event.stage, "Manager")
        self.assertEqual(event.action, "Reject")
        self.assertEqual(event.reason, "Not budgeted")
        notify_requester.assert_called_once()

    def test_procurement_fulfillment_actions_are_ordered_and_idempotent(self):
        request = self.make_request(unit_price=100)
        with patch("procurement_requests.workflow.notify_role"), patch(
            "procurement_requests.workflow.notify_requester"
        ):
            workflow.submit_request(request, actor=self.requester)
            request.reload()
            workflow.approve_manager(request, actor=self.manager)
            request.reload()

        with patch("procurement_requests.workflow.notify_requester") as notify_requester:
            workflow.mark_purchased(request, actor=self.officer)
            request.reload()
            workflow.mark_purchased(request, actor=self.officer)
            request.reload()
            workflow.mark_received(request, actor=self.officer)
            request.reload()
            workflow.mark_received(request, actor=self.officer)
            request.reload()
            workflow.close_request(request, actor=self.officer)
            request.reload()
            workflow.close_request(request, actor=self.officer)

        self.assertEqual(request.status, "Closed")
        self.assertTrue(request.purchased_at)
        self.assertTrue(request.received_at)
        self.assertTrue(request.closed_at)
        self.assertEqual(notify_requester.call_count, 2)  # purchased + received
        actions = [row.action for row in request.approval_events]
        self.assertEqual(actions.count("Mark Purchased"), 1)
        self.assertEqual(actions.count("Mark Received"), 1)
        self.assertEqual(actions.count("Close"), 1)
