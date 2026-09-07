"""Domain-neutral state-transition planning primitives.

This module deliberately owns no authorization, routing policy, persistence, or
domain status vocabulary. Consumers supply those semantics and durable evidence.
"""

from dataclasses import dataclass
from typing import Any


class InvalidTransition(ValueError):
    """Raised when an action is attempted from an invalid state."""


@dataclass(frozen=True)
class TransitionSpec:
    """Description of one bounded state-changing action."""

    stage: str
    action: str
    allowed_from: frozenset[str]
    to_state: str | None


@dataclass(frozen=True)
class TransitionResult:
    stage: str
    action: str
    actor: str
    occurred_at: Any
    previous_state: str
    next_state: str
    reason: str
    changed: bool


def plan_transition(
    *,
    current_state: str,
    spec: TransitionSpec,
    actor: str,
    occurred_at: Any,
    already_applied: bool = False,
    reason: str | None = None,
) -> TransitionResult:
    """Plan an idempotent transition without mutating domain state.

    The caller owns authorization, branch/routing policy, persistence, audit
    storage, and side effects.

    ``already_applied=True`` means durable consumer state proves this logical
    action was already completed. A no-op is returned even if the document has
    since advanced beyond the original target state.
    """
    if not actor:
        raise ValueError("Transition actor is required")

    normalized_reason = str(reason or "")

    if already_applied:
        return TransitionResult(
            stage=spec.stage,
            action=spec.action,
            actor=actor,
            occurred_at=occurred_at,
            previous_state=current_state,
            next_state=current_state,
            reason=normalized_reason,
            changed=False,
        )

    if current_state not in spec.allowed_from:
        allowed = ", ".join(sorted(spec.allowed_from))
        raise InvalidTransition(
            f"{spec.action} is not allowed from {current_state!r}; expected one of: {allowed}"
        )

    if spec.to_state is None:
        raise ValueError("A new transition requires a destination state")

    return TransitionResult(
        stage=spec.stage,
        action=spec.action,
        actor=actor,
        occurred_at=occurred_at,
        previous_state=current_state,
        next_state=spec.to_state,
        reason=normalized_reason,
        changed=True,
    )


def audit_payload(result: TransitionResult) -> dict[str, Any] | None:
    """Return a conventional audit-row payload for a changed transition."""
    if not result.changed:
        return None
    return {
        "stage": result.stage,
        "action": result.action,
        "actor": result.actor,
        "occurred_at": result.occurred_at,
        "from_status": result.previous_state,
        "to_status": result.next_state,
        "reason": result.reason,
    }
