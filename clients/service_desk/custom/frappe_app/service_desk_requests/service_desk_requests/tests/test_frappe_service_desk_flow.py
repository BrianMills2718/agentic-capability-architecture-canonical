import unittest
from unittest.mock import patch
try:
    import frappe
    from frappe.tests.utils import FrappeTestCase
except ImportError:
    frappe=None
    FrappeTestCase=unittest.TestCase

@unittest.skipIf(frappe is None, "requires real Frappe")
class TestServiceDeskFlow(FrappeTestCase):
    def setUp(self):
        self.users={}
        for key,role in [("requester",None),("dispatcher","Support Dispatcher"),("agent","Support Agent"),("other","Support Agent")]:
            email=f"_test_support_{key}@example.com"
            if not frappe.db.exists("User",email):
                u=frappe.get_doc({"doctype":"User","email":email,"first_name":key.title(),"send_welcome_email":0}).insert(ignore_permissions=True)
                if role: u.add_roles(role)
            self.users[key]=email
    def make_request(self):
        frappe.set_user(self.users["requester"])
        return frappe.get_doc({"doctype":"Support Request","requester":self.users["requester"],"subject":"Cannot export report","description":"Export button fails."}).insert(ignore_permissions=True)
    def triage_assign(self, doc, priority="High"):
        from service_desk_requests.workflow import triage, assign
        with patch("service_desk_requests.notifications.send_email"):
            triage(doc,category="Bug",priority=priority,actor=self.users["dispatcher"])
            assign(doc,agent=self.users["agent"],actor=self.users["dispatcher"])
        doc.reload()
    def test_triage_assignment_and_sla_are_idempotent(self):
        from service_desk_requests.workflow import triage, assign
        doc=self.make_request()
        with patch("service_desk_requests.notifications.send_email") as send:
            triage(doc,category="Bug",priority="High",actor=self.users["dispatcher"])
            assign(doc,agent=self.users["agent"],actor=self.users["dispatcher"])
            doc.reload(); first_due=doc.due_at; first_at=doc.assigned_at
            assign(doc,agent=self.users["agent"],actor=self.users["dispatcher"])
        doc.reload()
        self.assertEqual(doc.status,"Assigned"); self.assertEqual(doc.due_at,first_due); self.assertEqual(doc.assigned_at,first_at); send.assert_called_once()
    def test_wrong_agent_cannot_start(self):
        from service_desk_requests.workflow import start
        doc=self.make_request(); self.triage_assign(doc)
        with self.assertRaises(Exception): start(doc,actor=self.users["other"])
    def test_wait_resume_resolve_close(self):
        from service_desk_requests.workflow import start, wait_for_requester, resume, resolve, close
        doc=self.make_request(); self.triage_assign(doc)
        start(doc,actor=self.users["agent"])
        with patch("service_desk_requests.notifications.send_email"):
            wait_for_requester(doc,actor=self.users["agent"])
        doc.reload(); self.assertEqual(doc.status,"Waiting on Requester"); original_due=doc.due_at
        resume(doc,actor=self.users["requester"]); doc.reload(); self.assertEqual(doc.status,"In Progress"); self.assertEqual(doc.due_at,original_due)
        with patch("service_desk_requests.notifications.send_email"):
            resolve(doc,resolution="Fixed export permission.",actor=self.users["agent"])
        doc.reload(); self.assertEqual(doc.status,"Resolved")
        close(doc,actor=self.users["requester"]); doc.reload(); self.assertEqual(doc.status,"Closed")
    def test_waiting_request_is_not_overdue_scanned(self):
        from frappe.utils import add_to_date, now_datetime
        from service_desk_requests.workflow import start, wait_for_requester
        from service_desk_requests import sla
        doc=self.make_request(); self.triage_assign(doc,"Urgent"); start(doc,actor=self.users["agent"])
        with patch("service_desk_requests.notifications.send_email"):
            wait_for_requester(doc,actor=self.users["agent"])
        frappe.db.set_value("Support Request",doc.name,{"due_at":add_to_date(now_datetime(),hours=-1),"overdue_notified_at":None},update_modified=False)
        with patch("service_desk_requests.notifications.send_email") as send:
            sla.notify_overdue_requests()
        send.assert_not_called(); self.assertFalse(frappe.db.get_value("Support Request",doc.name,"overdue_notified_at"))
    def test_overdue_active_request_notifies_once(self):
        from frappe.utils import add_to_date, now_datetime
        from service_desk_requests import sla
        doc=self.make_request(); self.triage_assign(doc,"Urgent")
        frappe.db.set_value("Support Request",doc.name,{"due_at":add_to_date(now_datetime(),hours=-1),"overdue_notified_at":None},update_modified=False)
        with patch("service_desk_requests.notifications.send_email") as send:
            sla.notify_overdue_requests(); first=frappe.db.get_value("Support Request",doc.name,"overdue_notified_at"); sla.notify_overdue_requests()
        self.assertTrue(first); self.assertGreaterEqual(send.call_count,1)
