import frappe

from access_requests import workflow


def _request(name):
    doc = frappe.get_doc("Access Request", name)
    doc.check_permission("write")
    return doc


@frappe.whitelist()
def submit_access_request(name):
    return workflow.submit_request(_request(name))


@frappe.whitelist()
def manager_approve(name):
    return workflow.approve_manager(_request(name))


@frappe.whitelist()
def manager_reject(name, reason):
    return workflow.reject_manager(_request(name), reason=reason)


@frappe.whitelist()
def security_approve(name):
    return workflow.approve_security(_request(name))


@frappe.whitelist()
def security_reject(name, reason):
    return workflow.reject_security(_request(name), reason=reason)


@frappe.whitelist()
def mark_provisioned(name):
    return workflow.mark_provisioned(_request(name))


@frappe.whitelist()
def revoke_access(name, reason=None):
    return workflow.revoke_access(_request(name), reason=reason)
