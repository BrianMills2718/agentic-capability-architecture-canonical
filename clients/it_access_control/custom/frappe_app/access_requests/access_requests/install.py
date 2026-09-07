PROJECT_ROLES = (
    "Access Requester",
    "Access Manager",
    "Security Approver",
    "Access Provisioner",
)


def after_install():
    ensure_project_roles()


def ensure_project_roles():
    import frappe

    for role_name in PROJECT_ROLES:
        if frappe.db.exists("Role", role_name):
            continue
        frappe.get_doc({"doctype": "Role", "role_name": role_name}).insert(
            ignore_permissions=True
        )
