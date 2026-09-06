from na_notifications.email import send_email


def send_appointment_reminder(*, recipients, appointment):
    return send_email(
        recipients=recipients,
        subject="Appointment reminder",
        message=(
            f"Reminder: your appointment starts at {appointment.start_time}."
        ),
    )
