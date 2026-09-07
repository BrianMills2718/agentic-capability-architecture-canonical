REQUESTER_ROLE = "Access Requester"
MANAGER_ROLE = "Access Manager"
SECURITY_ROLE = "Security Approver"
PROVISIONER_ROLE = "Access Provisioner"


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
    frappe.throw("Only the requester can submit this access request")


def require_not_requester_or_target(request, user):
    import frappe

    if user in {request.requester, request.target_user}:
        frappe.throw("Requester/target user cannot approve this access request")


def require_not_target(request, user):
    import frappe

    if user == request.target_user:
        frappe.throw("Target user cannot provision their own access")
