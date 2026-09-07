from na_core.transitions import InvalidTransition, TransitionSpec, audit_payload, plan_transition


def test_transition_changes_state_and_emits_audit_payload():
    spec = TransitionSpec(
        stage="Work",
        action="Start",
        allowed_from=frozenset({"Assigned"}),
        to_state="In Progress",
    )
    result = plan_transition(
        current_state="Assigned",
        spec=spec,
        actor="worker@example.com",
        occurred_at="2026-09-06T12:00:00",
    )
    assert result.changed is True
    assert result.next_state == "In Progress"
    assert audit_payload(result)["from_status"] == "Assigned"


def test_already_applied_is_noop_even_after_later_progress():
    spec = TransitionSpec(
        stage="Approval",
        action="Approve",
        allowed_from=frozenset({"Pending"}),
        to_state="Approved",
    )
    result = plan_transition(
        current_state="Fulfilled",
        spec=spec,
        actor="approver@example.com",
        occurred_at="2026-09-06T12:00:00",
        already_applied=True,
    )
    assert result.changed is False
    assert result.next_state == "Fulfilled"
    assert audit_payload(result) is None


def test_invalid_source_state_fails():
    spec = TransitionSpec(
        stage="Work",
        action="Start",
        allowed_from=frozenset({"Assigned"}),
        to_state="In Progress",
    )
    try:
        plan_transition(
            current_state="Closed",
            spec=spec,
            actor="worker@example.com",
            occurred_at="2026-09-06T12:00:00",
        )
    except InvalidTransition:
        pass
    else:
        raise AssertionError("invalid transition should fail")
