from frappe.model.document import Document


class AccessRequest(Document):
    def before_insert(self):
        import frappe

        if not self.requester:
            self.requester = frappe.session.user
        if not self.target_user:
            self.target_user = self.requester
        if not self.status:
            self.status = "Draft"
