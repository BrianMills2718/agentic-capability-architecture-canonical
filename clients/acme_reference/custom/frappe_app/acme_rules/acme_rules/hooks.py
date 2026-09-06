app_name = "acme_rules"
app_title = "ACME Rules"
app_publisher = "ACME Reference"
app_description = "ACME-specific extensions"
app_email = ""
app_license = "Proprietary"

required_apps = ["na_scheduling", "na_approvals"]

doc_events = {
    "Appointment": {
        "validate": "acme_rules.appointment_rules.validate_appointment"
    }
}
