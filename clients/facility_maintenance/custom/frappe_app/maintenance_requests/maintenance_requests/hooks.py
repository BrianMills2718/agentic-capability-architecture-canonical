app_name = "maintenance_requests"
app_title = "Facility Maintenance"
app_publisher = "Composable Capability Base"
app_description = "Project-specific maintenance intake and SLA dispatch workflow"
app_email = ""
app_license = "Proprietary"

required_apps = ["na_notifications"]

after_install = "maintenance_requests.install.after_install"

scheduler_events = {
    "hourly": [
        "maintenance_requests.sla.notify_overdue_requests"
    ]
}
