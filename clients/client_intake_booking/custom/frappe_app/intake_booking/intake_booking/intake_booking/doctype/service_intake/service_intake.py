from frappe.model.document import Document


class ServiceIntake(Document):
    def after_insert(self):
        from intake_booking.workflow import process_new_intake

        process_new_intake(self)
