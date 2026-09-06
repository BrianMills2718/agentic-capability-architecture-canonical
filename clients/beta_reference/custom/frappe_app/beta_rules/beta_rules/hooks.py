app_name = "beta_rules"
app_title = "Beta Rules"
app_publisher = "Beta Reference"
app_description = "Beta-specific scheduling extensions"
app_email = ""
app_license = "Proprietary"

required_apps = ["na_scheduling", "na_approvals", "na_notifications"]

doc_events = {
    "Appointment": {
        "validate": "beta_rules.appointment_rules.validate_appointment"
    }
}

scheduler_events = {
    "hourly": [
        "beta_rules.reminders.send_due_appointment_reminders"
    ]
}
