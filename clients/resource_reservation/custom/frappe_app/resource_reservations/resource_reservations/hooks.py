app_name = "resource_reservations"
app_title = "Resource Reservations"
app_publisher = "Composable Capability Base"
app_description = "Shared resource reservation using neutral Scheduling availability"
app_email = ""
app_license = "Proprietary"

required_apps = ["na_core", "na_scheduling", "na_notifications"]

after_install = "resource_reservations.install.after_install"
