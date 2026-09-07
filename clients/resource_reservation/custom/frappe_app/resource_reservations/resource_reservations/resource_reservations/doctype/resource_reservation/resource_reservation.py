import frappe
from frappe.model.document import Document

from na_scheduling.availability import validate_duration_minutes


class ResourceReservation(Document):
    def validate(self):
        try:
            validate_duration_minutes(self.duration_minutes)
        except ValueError:
            frappe.throw("Reservation duration must be greater than zero")
