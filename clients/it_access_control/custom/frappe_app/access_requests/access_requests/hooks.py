app_name = "access_requests"
app_title = "IT Access Control"
app_publisher = "Composable Capability Base"
app_description = "Project-specific access request and approval workflow"
app_email = ""
app_license = "Proprietary"

required_apps = ["na_approvals", "na_notifications"]

after_install = "access_requests.install.after_install"
