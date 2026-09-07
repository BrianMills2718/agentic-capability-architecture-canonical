from service_desk_requests import workflow

def _load(name):
    import frappe
    doc = frappe.get_doc("Support Request", name)
    doc.check_permission("write")
    return doc

def _response(doc):
    return {"name": doc.name, "status": doc.status, "assigned_to": doc.assigned_to, "due_at": doc.due_at}

def triage_request(name, category, priority):
    doc=_load(name); workflow.triage(doc, category=category, priority=priority); doc.reload(); return _response(doc)
def assign_request(name, agent):
    doc=_load(name); workflow.assign(doc, agent=agent); doc.reload(); return _response(doc)
def start_request(name):
    doc=_load(name); workflow.start(doc); doc.reload(); return _response(doc)
def wait_request(name):
    doc=_load(name); workflow.wait_for_requester(doc); doc.reload(); return _response(doc)
def resume_request(name):
    doc=_load(name); workflow.resume(doc); doc.reload(); return _response(doc)
def resolve_request(name, resolution):
    doc=_load(name); workflow.resolve(doc, resolution=resolution); doc.reload(); return _response(doc)
def close_request(name):
    doc=_load(name); workflow.close(doc); doc.reload(); return _response(doc)

try:
    import frappe
except ImportError:
    frappe=None
if frappe is not None:
    for fn in [triage_request, assign_request, start_request, wait_request, resume_request, resolve_request, close_request]:
        globals()[fn.__name__] = frappe.whitelist()(fn)
