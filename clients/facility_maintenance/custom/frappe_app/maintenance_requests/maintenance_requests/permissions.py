DISPATCHER_ROLE = "Maintenance Dispatcher"
TECHNICIAN_ROLE = "Maintenance Technician"

def roles_for(user):
    import frappe
    return set(frappe.get_roles(user))

def require_role(user, role):
    import frappe
    roles = roles_for(user)
    if role not in roles and "System Manager" not in roles:
        frappe.throw(f"{role} role required", frappe.PermissionError)

def require_assigned_technician(doc, user):
    import frappe
    roles = roles_for(user)
    if "System Manager" in roles:
        return
    if TECHNICIAN_ROLE not in roles or doc.assigned_to != user:
        frappe.throw("Only the assigned technician can perform this action", frappe.PermissionError)

def require_requester_or_dispatcher(doc, user):
    import frappe
    roles = roles_for(user)
    if "System Manager" in roles or DISPATCHER_ROLE in roles or doc.requester == user:
        return
    frappe.throw("Requester or Maintenance Dispatcher role required", frappe.PermissionError)
