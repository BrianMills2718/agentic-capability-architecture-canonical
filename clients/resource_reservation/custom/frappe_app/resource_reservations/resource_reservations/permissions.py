MANAGER_ROLE = "Reservation Manager"


def roles_for(user):
    import frappe
    return set(frappe.get_roles(user))


def require_requester_or_manager(doc, user):
    import frappe
    roles = roles_for(user)
    if "System Manager" in roles or MANAGER_ROLE in roles or doc.requester == user:
        return
    frappe.throw("Requester or Reservation Manager required", frappe.PermissionError)
