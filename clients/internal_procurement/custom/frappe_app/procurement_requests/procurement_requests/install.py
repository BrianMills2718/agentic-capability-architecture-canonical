PROJECT_ROLES = (
    "Procurement Requester",
    "Procurement Manager",
    "Procurement Finance",
    "Procurement Officer",
)


def after_install():
    ensure_project_roles()


def ensure_project_roles():
    """Create the project-local roles used by server-side workflow authorization."""
    import frappe

    for role_name in PROJECT_ROLES:
        if frappe.db.exists("Role", role_name):
            continue
        frappe.get_doc({"doctype": "Role", "role_name": role_name}).insert(
            ignore_permissions=True
        )
