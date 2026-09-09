import math

import pytest

from na_approvals.binding import (
    ActionIntent,
    ApprovalBinding,
    ApprovalBindingMismatch,
    InvalidActionIntent,
    bind_approval,
    digest_action_intent,
    verify_approval,
)


def intent(**changes):
    values = {
        "operation_key": "workflow-17:create-task",
        "action": "CREATE_TASK",
        "target": "crm/company-42",
        "payload": {"title": "Call Acme", "tags": ["qualified", "inbound"]},
    }
    values.update(changes)
    return ActionIntent(**values)


def test_binding_verifies_the_exact_approved_action():
    approved = bind_approval(intent(), approval_id="approval-9", approver="brian")

    assert verify_approval(approved, intent()) is approved


@pytest.mark.parametrize(
    "changed",
    [
        {"operation_key": "workflow-17:create-task:other"},
        {"action": "SEND_EMAIL"},
        {"target": "crm/company-99"},
        {"payload": {"title": "Call a different company"}},
    ],
)
def test_changed_execution_cannot_reuse_stale_approval(changed):
    approved = bind_approval(intent(), approval_id="approval-9", approver="brian")

    with pytest.raises(ApprovalBindingMismatch, match="does not match"):
        verify_approval(approved, intent(**changed))


def test_object_key_order_does_not_change_intent_identity():
    left = intent(payload={"title": "Call Acme", "meta": {"b": 2, "a": 1}})
    right = intent(payload={"meta": {"a": 1, "b": 2}, "title": "Call Acme"})

    assert digest_action_intent(left) == digest_action_intent(right)


def test_mutating_payload_after_approval_fails_closed():
    approved_intent = intent()
    approved = bind_approval(
        approved_intent, approval_id="approval-9", approver="brian"
    )
    approved_intent.payload["title"] = "Changed after approval"

    with pytest.raises(ApprovalBindingMismatch, match="does not match"):
        verify_approval(approved, approved_intent)


@pytest.mark.parametrize(
    "payload",
    [
        {"value": math.nan},
        {"value": math.inf},
        {1: "non-string key"},
        {"value": ("tuple",)},
    ],
)
def test_noncanonical_payloads_are_rejected(payload):
    with pytest.raises(InvalidActionIntent):
        intent(payload=payload)


def test_binding_fields_cannot_be_empty_or_forged_with_malformed_digest():
    with pytest.raises(InvalidActionIntent, match="approval_id"):
        bind_approval(intent(), approval_id=" ", approver="brian")
    with pytest.raises(InvalidActionIntent, match="intent_digest"):
        ApprovalBinding("approval-9", "brian", "not-a-digest")
