app_name = "intake_booking"
app_title = "Client Intake Booking"
app_publisher = "Composable Capability Base"
app_description = "Project-specific client intake and booking orchestration"
app_email = ""
app_license = "Proprietary"

required_apps = ["na_scheduling", "na_approvals", "na_notifications"]

doc_events = {
    "Appointment": {
        "validate": "intake_booking.appointment_rules.validate_appointment"
    }
}
