from resource_reservations import workflow


def _load(name):
    import frappe
    doc = frappe.get_doc("Resource Reservation", name)
    doc.check_permission("write")
    return doc


def _response(doc):
    return {
        "name": doc.name,
        "status": doc.status,
        "resource": doc.resource,
        "start_time": doc.start_time,
        "duration_minutes": doc.duration_minutes,
    }


def reserve_request(name):
    doc = _load(name)
    workflow.reserve(doc)
    doc.reload()
    return _response(doc)


def reschedule_request(name, start_time, duration_minutes):
    doc = _load(name)
    workflow.reschedule(
        doc,
        start_time=start_time,
        duration_minutes=duration_minutes,
    )
    doc.reload()
    return _response(doc)


def cancel_request(name):
    doc = _load(name)
    workflow.cancel(doc)
    doc.reload()
    return _response(doc)


try:
    import frappe
except ImportError:
    frappe = None

if frappe is not None:
    reserve_request = frappe.whitelist()(reserve_request)
    reschedule_request = frappe.whitelist()(reschedule_request)
    cancel_request = frappe.whitelist()(cancel_request)
