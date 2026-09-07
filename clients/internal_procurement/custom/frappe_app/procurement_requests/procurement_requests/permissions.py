REQUESTER_ROLE = "Procurement Requester"
MANAGER_ROLE = "Procurement Manager"
FINANCE_ROLE = "Procurement Finance"
OFFICER_ROLE = "Procurement Officer"


def roles_for(user):
    import frappe

    return set(frappe.get_roles(user))


def require_role(user, role):
    import frappe

    roles = roles_for(user)
    if role not in roles and "System Manager" not in roles:
        frappe.throw(f"{role} role is required")


def require_request_owner_or_system_manager(request, user):
    import frappe

    if user == request.requester:
        return
    if "System Manager" in roles_for(user):
        return
    frappe.throw("Only the requester can submit this purchase request")


def require_not_requester(request, user):
    import frappe

    if user == request.requester:
        frappe.throw("A requester cannot approve their own purchase request")


def users_with_role(role):
    import frappe

    users = frappe.get_all(
        "Has Role",
        filters={"role": role, "parenttype": "User"},
        pluck="parent",
    )
    return sorted(set(users))
