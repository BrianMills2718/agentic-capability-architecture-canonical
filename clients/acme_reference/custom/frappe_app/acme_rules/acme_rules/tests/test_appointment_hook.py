from unittest.mock import patch

import frappe
from frappe.tests.utils import FrappeTestCase
from frappe.utils import now_datetime

from na_approvals.types import Decision, RuleResult


COLLECT = "acme_rules.appointment_rules.collect_rule_results"


def result(rule, decision, priority=50, reason=None):
    return RuleResult(
        rule=rule,
        decision=decision,
        priority=priority,
        reason=reason or rule,
    )


class TestAppointmentApprovalHook(FrappeTestCase):
    def make_appointment(self):
        doc = frappe.new_doc("Appointment")
        doc.customer = "Integration Test Customer"
        doc.start_time = now_datetime()
        doc.duration_minutes = 60
        doc.status = "Pending"
        doc.approval_required = 0
        doc.approval_reason = ""
        return doc

    def test_allow_through_real_validate_hook(self):
        doc = self.make_appointment()
        with patch(COLLECT, return_value=[result("allow", Decision.ALLOW, 60)]) as collect:
            doc.run_method("validate")
        collect.assert_called_once_with(doc)
        self.assertEqual(doc.approval_required, 0)

    def test_require_approval_through_real_validate_hook(self):
        doc = self.make_appointment()
        with patch(COLLECT, return_value=[
            result("high_value", Decision.REQUIRE_APPROVAL, 90, "Approval required")
        ]):
            doc.run_method("validate")
        self.assertEqual(doc.approval_required, 1)
        self.assertEqual(doc.approval_reason, "Approval required")

    def test_block_through_real_validate_hook(self):
        doc = self.make_appointment()
        with patch(COLLECT, return_value=[
            result("compliance", Decision.BLOCK, 100, "Compliance hold")
        ]):
            with self.assertRaises(frappe.ValidationError):
                doc.run_method("validate")

    def test_allow_does_not_weaken_existing_shared_requirement(self):
        doc = self.make_appointment()
        doc.approval_required = 1
        doc.approval_reason = "Shared scheduling policy"
        with patch(COLLECT, return_value=[result("vip", Decision.ALLOW, 100)]):
            doc.run_method("validate")
        self.assertEqual(doc.approval_required, 1)
        self.assertEqual(doc.approval_reason, "Shared scheduling policy")

    def test_require_approval_persists_on_insert(self):
        doc = self.make_appointment()
        with patch(COLLECT, return_value=[
            result("long", Decision.REQUIRE_APPROVAL, 80, "Long appointment")
        ]):
            doc.insert(ignore_permissions=True)
        saved = frappe.get_doc("Appointment", doc.name)
        self.assertEqual(saved.approval_required, 1)
        self.assertEqual(saved.approval_reason, "Long appointment")

    def test_block_prevents_insert(self):
        doc = self.make_appointment()
        with patch(COLLECT, return_value=[
            result("compliance", Decision.BLOCK, 100, "Compliance hold")
        ]):
            with self.assertRaises(frappe.ValidationError):
                doc.insert(ignore_permissions=True)
        if doc.name:
            self.assertFalse(frappe.db.exists("Appointment", doc.name))
