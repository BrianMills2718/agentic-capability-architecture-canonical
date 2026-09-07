from frappe.model.document import Document

from procurement_requests.policy import line_total, request_total


class PurchaseRequest(Document):
    def before_insert(self):
        import frappe

        if not self.requester:
            self.requester = frappe.session.user
        if not self.status:
            self.status = "Draft"

    def validate(self):
        for row in self.items or []:
            row.line_total = float(line_total(row.quantity, row.unit_price))
        self.total_amount = float(request_total(self.items or []))
