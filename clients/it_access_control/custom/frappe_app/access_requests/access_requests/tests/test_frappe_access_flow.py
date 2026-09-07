import unittest
from unittest.mock import patch

try:
    import frappe
    from frappe.tests.utils import FrappeTestCase
    from access_requests.install import ensure_project_roles
    from access_requests import workflow
except ImportError:
    frappe = None
    FrappeTestCase = unittest.TestCase
    ensure_project_roles = workflow = None


@unittest.skipIf(frappe is None, "real Frappe lifecycle test")
class TestITAccessControlFlow(FrappeTestCase):
    def setUp(self):
        super().setUp()
        ensure_project_roles()
        self.requester = self.ensure_user("access-requester@example.com", "Access Requester")
        self.target = self.ensure_user("access-target@example.com", "Access Requester")
        self.manager = self.ensure_user("access-manager@example.com", "Access Manager")
        self.security = self.ensure_user("access-security@example.com", "Security Approver")
        self.provisioner = self.ensure_user("access-provisioner@example.com", "Access Provisioner")
        frappe.db.set_single_value(
            "Access Control Settings",
            "security_approval_levels",
            "Sensitive\nPrivileged",
        )

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

    def make_request(self, *, access_level="Standard", requester=None, target=None):
        doc = frappe.get_doc(
            {
                "doctype": "Access Request",
                "requester": requester or self.requester,
                "target_user": target or self.target,
                "system_name": "Analytics Platform",
                "access_level": access_level,
                "justification": "Needed for project delivery",
            }
        )
        doc.insert(ignore_permissions=True)
        doc.reload()
        return doc

    def test_standard_access_needs_manager_only(self):
        request = self.make_request()
        with patch("access_requests.workflow.notify_role"), patch(
            "access_requests.workflow.notify_requester_and_target"
        ):
            workflow.submit_request(request, actor=self.requester)
            request.reload()
            workflow.approve_manager(request, actor=self.manager)
            request.reload()

        self.assertEqual(request.status, "Ready to Provision")
        self.assertTrue(request.approved_at)
        self.assertEqual(
            [(row.stage, row.action) for row in request.approval_events[-2:]],
            [("Submission", "Submit"), ("Manager", "Approve")],
        )

    def test_sensitive_access_requires_distinct_security_approval(self):
        request = self.make_request(access_level="Sensitive")
        with patch("access_requests.workflow.notify_role"), patch(
            "access_requests.workflow.notify_requester_and_target"
        ):
            workflow.submit_request(request, actor=self.requester)
            request.reload()
            workflow.approve_manager(request, actor=self.manager)
            request.reload()

            self.assertEqual(request.status, "Pending Security Approval")

            manager_user = frappe.get_doc("User", self.manager)
            if "Security Approver" not in frappe.get_roles(self.manager):
                manager_user.add_roles("Security Approver")

            with self.assertRaises(frappe.ValidationError):
                workflow.approve_security(request, actor=self.manager)

            workflow.approve_security(request, actor=self.security)
            request.reload()

        self.assertEqual(request.status, "Ready to Provision")
        self.assertTrue(request.approved_at)
        self.assertEqual(
            [(row.stage, row.action) for row in request.approval_events[-2:]],
            [("Manager", "Approve"), ("Security", "Approve")],
        )

    def test_requester_or_target_cannot_self_approve(self):
        requester_user = frappe.get_doc("User", self.requester)
        if "Access Manager" not in frappe.get_roles(self.requester):
            requester_user.add_roles("Access Manager")

        request = self.make_request()
        with patch("access_requests.workflow.notify_role"):
            workflow.submit_request(request, actor=self.requester)
        request.reload()

        with self.assertRaises(frappe.ValidationError):
            workflow.approve_manager(request, actor=self.requester)

        target_user = frappe.get_doc("User", self.target)
        if "Access Manager" not in frappe.get_roles(self.target):
            target_user.add_roles("Access Manager")
        with self.assertRaises(frappe.ValidationError):
            workflow.approve_manager(request, actor=self.target)

    def test_rejection_is_audited_and_idempotent(self):
        request = self.make_request(access_level="Privileged")
        with patch("access_requests.workflow.notify_role"):
            workflow.submit_request(request, actor=self.requester)
        request.reload()

        with patch("access_requests.workflow.notify_requester_and_target") as notify:
            workflow.reject_manager(request, actor=self.manager, reason="Not required")
            request.reload()
            workflow.reject_manager(request, actor=self.manager, reason="Not required")

        self.assertEqual(request.status, "Rejected")
        self.assertEqual(request.rejection_reason, "Not required")
        self.assertEqual(request.approval_events[-1].action, "Reject")
        notify.assert_called_once()

    def test_provision_and_revoke_are_ordered_and_idempotent(self):
        request = self.make_request()
        with patch("access_requests.workflow.notify_role"), patch(
            "access_requests.workflow.notify_requester_and_target"
        ):
            workflow.submit_request(request, actor=self.requester)
            request.reload()
            workflow.approve_manager(request, actor=self.manager)
            request.reload()

        with patch("access_requests.workflow.notify_requester_and_target") as notify:
            workflow.mark_provisioned(request, actor=self.provisioner)
            request.reload()
            workflow.mark_provisioned(request, actor=self.provisioner)
            request.reload()
            workflow.revoke_access(request, actor=self.provisioner)
            request.reload()
            workflow.revoke_access(request, actor=self.provisioner)

        self.assertEqual(request.status, "Revoked")
        self.assertTrue(request.provisioned_at)
        self.assertTrue(request.revoked_at)
        self.assertEqual(notify.call_count, 2)
        actions = [row.action for row in request.approval_events]
        self.assertEqual(actions.count("Provision"), 1)
        self.assertEqual(actions.count("Revoke"), 1)

    def test_target_cannot_provision_own_access(self):
        target_user = frappe.get_doc("User", self.target)
        if "Access Provisioner" not in frappe.get_roles(self.target):
            target_user.add_roles("Access Provisioner")

        request = self.make_request()
        with patch("access_requests.workflow.notify_role"), patch(
            "access_requests.workflow.notify_requester_and_target"
        ):
            workflow.submit_request(request, actor=self.requester)
            request.reload()
            workflow.approve_manager(request, actor=self.manager)
            request.reload()

        with self.assertRaises(frappe.ValidationError):
            workflow.mark_provisioned(request, actor=self.target)
