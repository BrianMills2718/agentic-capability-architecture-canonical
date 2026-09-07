"""Backward-compatible approval namespace for the neutral core transition primitive."""

from na_core.transitions import (
    InvalidTransition,
    TransitionResult,
    TransitionSpec,
    audit_payload,
    plan_transition,
)

# Historical compatibility name used by existing project code/tests.
InvalidApprovalTransition = InvalidTransition

__all__ = [
    "InvalidApprovalTransition",
    "InvalidTransition",
    "TransitionResult",
    "TransitionSpec",
    "audit_payload",
    "plan_transition",
]
