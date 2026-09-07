import frappe
from frappe.model.document import Document

from na_scheduling.availability import validate_duration_minutes


class Appointment(Document):
    def validate(self):
        if self.duration_minutes is not None:
            try:
                validate_duration_minutes(self.duration_minutes)
            except ValueError:
                frappe.throw("Appointment duration must be greater than zero")
