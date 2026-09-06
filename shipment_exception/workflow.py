from na_core.transitions import (
    TransitionResult,
    TransitionSpec,
    plan_transition,
)
from na_notifications.email import send_email


ACKNOWLEDGE_SPEC = TransitionSpec(
    stage="shipment_exception",
    action="acknowledge",
    allowed_from=frozenset({"Open"}),
    to_state="Acknowledged",
)
RESOLVE_SPEC = TransitionSpec(
    stage="shipment_exception",
    action="resolve",
    allowed_from=frozenset({"Acknowledged"}),
    to_state="Resolved",
)


def _require_actor(actor):
    if not actor or not str(actor).strip():
        raise ValueError("Transition actor is required")


def acknowledge(
    *,
    current_state,
    actor,
    occurred_at,
    already_applied,
    notify=send_email,
) -> TransitionResult:
    _require_actor(actor)
    result = plan_transition(
        current_state=current_state,
        spec=ACKNOWLEDGE_SPEC,
        actor=actor,
        occurred_at=occurred_at,
        already_applied=already_applied,
        reason="Shipment exception acknowledged",
    )
    if result.changed:
        notify(
            recipients="ops@example.test",
            subject="Shipment exception acknowledged",
            message=(
                f"Shipment exception acknowledged by {actor} at "
                f"{occurred_at}."
            ),
        )
    return result


def resolve(
    *,
    current_state,
    actor,
    occurred_at,
    resolution,
    already_applied,
    notify=send_email,
) -> TransitionResult:
    _require_actor(actor)
    if not resolution or not str(resolution).strip():
        raise ValueError("Resolution text is required")

    result = plan_transition(
        current_state=current_state,
        spec=RESOLVE_SPEC,
        actor=actor,
        occurred_at=occurred_at,
        already_applied=already_applied,
        reason=str(resolution),
    )
    if result.changed:
        notify(
            recipients="ops@example.test",
            subject="Shipment exception resolved",
            message=(
                f"Shipment exception resolved by {actor} at {occurred_at}: "
                f"{resolution}"
            ),
        )
    return result
