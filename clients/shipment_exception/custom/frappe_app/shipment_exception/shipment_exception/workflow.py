from na_approvals.engine import apply_resolution, resolve
from na_approvals.types import Decision, RuleResult


def shipment_exception_rule(shipment):
    exception_type = str(getattr(shipment, "exception_type", "") or "").lower()
    delay_hours = int(getattr(shipment, "delay_hours", 0) or 0)
    risk_level = str(getattr(shipment, "risk_level", "normal") or "normal").lower()
    blocked = bool(getattr(shipment, "blocked", False))

    if blocked:
        return RuleResult(
            rule="shipment_exception.blocked",
            decision=Decision.BLOCK,
            priority=90,
            reason="Shipment is blocked pending compliance review.",
        )

    if exception_type in {"damaged", "missing", "late"} or delay_hours >= 24 or risk_level in {"high", "critical"}:
        return RuleResult(
            rule="shipment_exception.review",
            decision=Decision.REQUIRE_APPROVAL,
            priority=60,
            reason="Shipment exception requires manager approval before release.",
        )

    return None


def collect_rule_results(shipment):
    result = shipment_exception_rule(shipment)
    return [result] if result is not None else []


def evaluate_shipment_exception(shipment):
    return resolve(collect_rule_results(shipment))


def apply_shipment_exception(shipment):
    resolution = evaluate_shipment_exception(shipment)
    if resolution is not None and resolution.decision == Decision.BLOCK:
        raise ValueError("; ".join(resolution.reasons))
    apply_resolution(shipment, resolution)
    return resolution


def notify_exception_team(shipment, send_email=None):
    if send_email is None:
        from na_notifications.email import send_email

    if getattr(shipment, "approval_required", 0):
        send_email(
            recipients=["ops@example.com"],
            subject="Shipment exception requires review",
            message=f"Shipment {getattr(shipment, 'shipment_id', 'unknown')} requires approval.",
        )
        return True
    return False
