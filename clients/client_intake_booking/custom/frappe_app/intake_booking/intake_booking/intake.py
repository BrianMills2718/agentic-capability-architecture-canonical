from dataclasses import dataclass

SERVICE_TYPES = frozenset({"Consultation", "Project Discovery", "Support"})
ALLOWED_DURATIONS = frozenset({30, 60, 90, 120})

@dataclass(frozen=True)
class IntakeSubmission:
    client_name: str
    email: str
    service_type: str
    request_summary: str
    requested_start_time: str
    requested_duration_minutes: int

def normalize_submission(*, client_name, email, service_type, request_summary, requested_start_time, requested_duration_minutes=30) -> IntakeSubmission:
    client_name = str(client_name or "").strip()
    email = str(email or "").strip().lower()
    service_type = str(service_type or "").strip()
    request_summary = str(request_summary or "").strip()
    requested_start_time = str(requested_start_time or "").strip()
    try:
        duration = int(requested_duration_minutes)
    except (TypeError, ValueError) as exc:
        raise ValueError("requested duration must be an integer number of minutes") from exc
    if not client_name:
        raise ValueError("client name is required")
    if "@" not in email or email.startswith("@") or email.endswith("@"):
        raise ValueError("a valid email address is required")
    if service_type not in SERVICE_TYPES:
        raise ValueError(f"unsupported service type: {service_type}")
    if not request_summary:
        raise ValueError("request summary is required")
    if not requested_start_time:
        raise ValueError("requested start time is required")
    if duration not in ALLOWED_DURATIONS:
        raise ValueError(f"unsupported duration: {duration}")
    return IntakeSubmission(client_name, email, service_type, request_summary, requested_start_time, duration)

def confirmation_copy(*, client_name: str, pending_approval: bool) -> tuple[str, str]:
    if pending_approval:
        return ("Consultation request received", f"Hi {client_name}, your consultation request was received and is pending review.")
    return ("Consultation booked", f"Hi {client_name}, your consultation has been booked.")
