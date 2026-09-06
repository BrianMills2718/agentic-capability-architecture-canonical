import frappe
from frappe.model.document import Document


class Appointment(Document):
    def validate(self):
        if self.duration_minutes is not None and self.duration_minutes <= 0:
            frappe.throw("Appointment duration must be greater than zero")
