ROLES = ["Support Dispatcher", "Support Agent"]

def after_install():
    import frappe
    for role in ROLES:
        if not frappe.db.exists("Role", role):
            frappe.get_doc({"doctype": "Role", "role_name": role}).insert(ignore_permissions=True)
