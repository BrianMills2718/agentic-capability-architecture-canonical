import unittest
from unittest.mock import patch

try:
    import frappe
    from frappe.tests.utils import FrappeTestCase
    from frappe.utils import add_to_date, now_datetime
except ImportError:
    frappe = None
    FrappeTestCase = unittest.TestCase


@unittest.skipIf(frappe is None, "requires real Frappe")
class TestResourceReservationFlow(FrappeTestCase):
    def setUp(self):
        self.requester = "_test_reservation_requester@example.com"
        if not frappe.db.exists("User", self.requester):
            frappe.get_doc({
                "doctype": "User",
                "email": self.requester,
                "first_name": "Reservation",
                "last_name": "Requester",
                "send_welcome_email": 0,
            }).insert(ignore_permissions=True)

        for code, kind in [("ROOM-A", "Room"), ("ROOM-B", "Room")]:
            if not frappe.db.exists("Reservable Resource", code):
                frappe.get_doc({
                    "doctype": "Reservable Resource",
                    "resource_code": code,
                    "title": code,
                    "resource_type": kind,
                    "active": 1,
                }).insert(ignore_permissions=True)

    def make_reservation(self, resource="ROOM-A", start_time=None, duration=60):
        frappe.set_user(self.requester)
        return frappe.get_doc({
            "doctype": "Resource Reservation",
            "requester": self.requester,
            "resource": resource,
            "purpose": "Team use",
            "start_time": start_time or add_to_date(now_datetime(), hours=24),
            "duration_minutes": duration,
        }).insert(ignore_permissions=True)

    def test_reserve_is_idempotent_and_records_confirmation(self):
        from resource_reservations.workflow import reserve

        doc = self.make_reservation()
        with patch("resource_reservations.notifications.send_email") as send:
            reserve(doc, actor=self.requester)
            doc.reload()
            first_reserved_at = doc.reserved_at
            reserve(doc, actor=self.requester)

        doc.reload()
        self.assertEqual(doc.status, "Reserved")
        self.assertEqual(doc.reserved_at, first_reserved_at)
        send.assert_called_once()

    def test_same_resource_overlap_rejected_but_other_resource_allowed(self):
        from resource_reservations.workflow import reserve

        start = add_to_date(now_datetime(), hours=48)
        first = self.make_reservation("ROOM-A", start, 60)
        with patch("resource_reservations.notifications.send_email"):
            reserve(first, actor=self.requester)

        overlapping = self.make_reservation("ROOM-A", add_to_date(start, minutes=30), 60)
        with patch("resource_reservations.notifications.send_email"):
            with self.assertRaises(Exception):
                reserve(overlapping, actor=self.requester)
        overlapping.reload()
        self.assertEqual(overlapping.status, "Draft")

        other = self.make_reservation("ROOM-B", add_to_date(start, minutes=30), 60)
        with patch("resource_reservations.notifications.send_email"):
            reserve(other, actor=self.requester)
        other.reload()
        self.assertEqual(other.status, "Reserved")

    def test_back_to_back_same_resource_is_allowed(self):
        from resource_reservations.workflow import reserve

        start = add_to_date(now_datetime(), hours=72)
        first = self.make_reservation("ROOM-A", start, 60)
        second = self.make_reservation("ROOM-A", add_to_date(start, minutes=60), 60)
        with patch("resource_reservations.notifications.send_email"):
            reserve(first, actor=self.requester)
            reserve(second, actor=self.requester)
        second.reload()
        self.assertEqual(second.status, "Reserved")

    def test_reschedule_conflict_does_not_mutate_reservation(self):
        from resource_reservations.workflow import reserve, reschedule

        start = add_to_date(now_datetime(), hours=96)
        first = self.make_reservation("ROOM-A", start, 60)
        second = self.make_reservation("ROOM-A", add_to_date(start, hours=2), 60)
        with patch("resource_reservations.notifications.send_email"):
            reserve(first, actor=self.requester)
            reserve(second, actor=self.requester)

        second.reload()
        old_start = second.start_time
        old_duration = second.duration_minutes
        with patch("resource_reservations.notifications.send_email"):
            with self.assertRaises(Exception):
                reschedule(
                    second,
                    start_time=add_to_date(start, minutes=30),
                    duration_minutes=60,
                    actor=self.requester,
                )
        second.reload()
        self.assertEqual(second.start_time, old_start)
        self.assertEqual(second.duration_minutes, old_duration)
        self.assertEqual(second.status, "Reserved")

    def test_cancel_releases_slot_and_is_idempotent(self):
        from resource_reservations.workflow import cancel, reserve

        start = add_to_date(now_datetime(), hours=120)
        first = self.make_reservation("ROOM-A", start, 60)
        with patch("resource_reservations.notifications.send_email"):
            reserve(first, actor=self.requester)
            cancel(first, actor=self.requester)
            first.reload()
            first_cancelled_at = first.cancelled_at
            cancel(first, actor=self.requester)

        first.reload()
        self.assertEqual(first.status, "Cancelled")
        self.assertEqual(first.cancelled_at, first_cancelled_at)

        replacement = self.make_reservation("ROOM-A", start, 60)
        with patch("resource_reservations.notifications.send_email"):
            reserve(replacement, actor=self.requester)
        replacement.reload()
        self.assertEqual(replacement.status, "Reserved")
