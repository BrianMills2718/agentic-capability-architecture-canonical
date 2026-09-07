from procurement_requests import workflow


def _load(name):
    import frappe

    doc = frappe.get_doc("Purchase Request", name)
    doc.check_permission("write")
    return doc


def submit_purchase_request(name):
    doc = _load(name)
    workflow.submit_request(doc)
    doc.reload()
    return _response(doc)


def manager_approve(name):
    doc = _load(name)
    workflow.approve_manager(doc)
    doc.reload()
    return _response(doc)


def manager_reject(name, reason):
    doc = _load(name)
    workflow.reject_manager(doc, reason=reason)
    doc.reload()
    return _response(doc)


def finance_approve(name):
    doc = _load(name)
    workflow.approve_finance(doc)
    doc.reload()
    return _response(doc)


def finance_reject(name, reason):
    doc = _load(name)
    workflow.reject_finance(doc, reason=reason)
    doc.reload()
    return _response(doc)


def mark_purchased(name):
    doc = _load(name)
    workflow.mark_purchased(doc)
    doc.reload()
    return _response(doc)


def mark_received(name):
    doc = _load(name)
    workflow.mark_received(doc)
    doc.reload()
    return _response(doc)


def close_purchase_request(name):
    doc = _load(name)
    workflow.close_request(doc)
    doc.reload()
    return _response(doc)


def _response(doc):
    return {
        "name": doc.name,
        "status": doc.status,
        "current_approval_stage": doc.current_approval_stage,
        "total_amount": doc.total_amount,
    }


try:
    import frappe
except ImportError:
    frappe = None

if frappe is not None:
    submit_purchase_request = frappe.whitelist()(submit_purchase_request)
    manager_approve = frappe.whitelist()(manager_approve)
    manager_reject = frappe.whitelist()(manager_reject)
    finance_approve = frappe.whitelist()(finance_approve)
    finance_reject = frappe.whitelist()(finance_reject)
    mark_purchased = frappe.whitelist()(mark_purchased)
    mark_received = frappe.whitelist()(mark_received)
    close_purchase_request = frappe.whitelist()(close_purchase_request)
