app_name = "procurement_requests"
app_title = "Internal Procurement"
app_publisher = "Composable Capability Base"
app_description = "Project-specific purchase request and staged approval workflow"
app_email = ""
app_license = "Proprietary"

required_apps = ["na_approvals", "na_notifications"]

after_install = "procurement_requests.install.after_install"
