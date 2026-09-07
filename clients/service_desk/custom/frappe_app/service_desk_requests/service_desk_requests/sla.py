from datetime import timedelta

DEFAULT_HOURS = {"Urgent": 2, "High": 8, "Normal": 24, "Low": 72}

def hours_for_priority(priority, settings=None):
    if settings is None:
        return DEFAULT_HOURS[priority]
    field = {"Urgent":"urgent_hours","High":"high_hours","Normal":"normal_hours","Low":"low_hours"}[priority]
    value = getattr(settings, field, None)
    return int(value if value not in (None, "") else DEFAULT_HOURS[priority])

def calculate_due_at(assigned_at, priority, settings=None):
    return assigned_at + timedelta(hours=hours_for_priority(priority, settings))

def notify_overdue_requests():
    import frappe
    from frappe.utils import now_datetime
    from service_desk_requests.notifications import notify_overdue
    now = now_datetime()
    names = frappe.get_all(
        "Support Request",
        filters={
            "status": ["in", ["Assigned", "In Progress"]],
            "due_at": ["<", now],
            "overdue_notified_at": ["is", "not set"],
        },
        pluck="name",
    )
    for name in names:
        doc = frappe.get_doc("Support Request", name)
        notify_overdue(doc)
        doc.db_set("overdue_notified_at", now, update_modified=False)
