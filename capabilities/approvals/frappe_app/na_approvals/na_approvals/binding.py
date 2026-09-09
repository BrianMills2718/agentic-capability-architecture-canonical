"""Bind an approval record to one exact executable action intent.

This module does not authenticate an approver or persist consent.  It gives the
trusted approval boundary a deterministic receipt that fails closed when later
execution changes the operation identity, action, target, or payload.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import hmac
import json
import math
import re
from typing import Any


_DIGEST = re.compile(r"^[0-9a-f]{64}$")
_SCHEMA = "approval.action-intent/v1"


class InvalidActionIntent(ValueError):
    """Raised when an action intent cannot be represented canonically."""


class ApprovalBindingMismatch(ValueError):
    """Raised when approval was granted for a different action intent."""


def _required_text(value: str, field: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise InvalidActionIntent(f"{field} must be a non-empty string")


def _validate_json(value: Any, path: str = "payload") -> None:
    if value is None or type(value) in {str, bool, int}:  # noqa: E721 - exact JSON types
        return
    if type(value) is float:  # noqa: E721 - reject numeric subclasses
        if not math.isfinite(value):
            raise InvalidActionIntent(f"{path} contains a non-finite number")
        return
    if type(value) is list:  # noqa: E721 - tuples are not JSON arrays
        for index, item in enumerate(value):
            _validate_json(item, f"{path}[{index}]")
        return
    if type(value) is dict:  # noqa: E721 - keep the canonical surface narrow
        for key, item in value.items():
            if not isinstance(key, str):
                raise InvalidActionIntent(f"{path} contains a non-string object key")
            _validate_json(item, f"{path}.{key}")
        return
    raise InvalidActionIntent(f"{path} contains unsupported type {type(value).__name__}")


@dataclass(frozen=True)
class ActionIntent:
    """The complete consequential action a trusted human may approve."""

    operation_key: str
    action: str
    target: str
    payload: dict[str, Any]

    def __post_init__(self) -> None:
        _required_text(self.operation_key, "operation_key")
        _required_text(self.action, "action")
        _required_text(self.target, "target")
        if type(self.payload) is not dict:  # noqa: E721
            raise InvalidActionIntent("payload must be a JSON object")
        _validate_json(self.payload)


@dataclass(frozen=True)
class ApprovalBinding:
    """A caller-persisted record binding an approval event to an intent digest."""

    approval_id: str
    approver: str
    intent_digest: str

    def __post_init__(self) -> None:
        _required_text(self.approval_id, "approval_id")
        _required_text(self.approver, "approver")
        if not isinstance(self.intent_digest, str) or not _DIGEST.fullmatch(
            self.intent_digest
        ):
            raise InvalidActionIntent("intent_digest must be a lowercase SHA-256 digest")


def digest_action_intent(intent: ActionIntent) -> str:
    """Return the stable SHA-256 identity of one exact action intent."""

    if not isinstance(intent, ActionIntent):
        raise InvalidActionIntent("intent must be an ActionIntent")
    _validate_json(intent.payload)
    envelope = {
        "schema": _SCHEMA,
        "operation_key": intent.operation_key,
        "action": intent.action,
        "target": intent.target,
        "payload": intent.payload,
    }
    encoded = json.dumps(
        envelope,
        allow_nan=False,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def bind_approval(
    intent: ActionIntent, *, approval_id: str, approver: str
) -> ApprovalBinding:
    """Create a receipt after a trusted boundary records human approval."""

    _required_text(approval_id, "approval_id")
    _required_text(approver, "approver")
    return ApprovalBinding(
        approval_id=approval_id,
        approver=approver,
        intent_digest=digest_action_intent(intent),
    )


def verify_approval(binding: ApprovalBinding, intent: ActionIntent) -> ApprovalBinding:
    """Return the binding only when it covers the exact action to be executed."""

    if not isinstance(binding, ApprovalBinding):
        raise ApprovalBindingMismatch("approval binding is missing or invalid")
    actual = digest_action_intent(intent)
    if not hmac.compare_digest(binding.intent_digest, actual):
        raise ApprovalBindingMismatch(
            "approved action does not match the action presented for execution"
        )
    return binding
