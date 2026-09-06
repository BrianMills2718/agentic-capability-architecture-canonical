import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "snapshot" / "vendor" / "na_core"))
sys.path.insert(
    0, str(Path(__file__).parents[1] / "snapshot" / "vendor" / "na_notifications")
)

import pytest

from shipment_exception.workflow import acknowledge, resolve


def notification_recorder(notifications):
    def notify(**kwargs):
        notifications.append(kwargs)

    return notify


def test_acknowledge_changes_state_and_notifies():
    notifications = []

    result = acknowledge(
        current_state="Open",
        actor="operator@example.test",
        occurred_at="2026-09-06T18:00:00Z",
        already_applied=False,
        notify=notification_recorder(notifications),
    )

    assert result.changed is True
    assert result.next_state == "Acknowledged"
    assert notifications == [
        {
            "recipients": "ops@example.test",
            "subject": "Shipment exception acknowledged",
            "message": (
                "Shipment exception acknowledged by operator@example.test at "
                "2026-09-06T18:00:00Z."
            ),
        }
    ]


def test_acknowledge_replay_is_noop_even_after_state_advanced():
    notifications = []

    result = acknowledge(
        current_state="Resolved",
        actor="operator@example.test",
        occurred_at="2026-09-06T18:00:00Z",
        already_applied=True,
        notify=notification_recorder(notifications),
    )

    assert result.changed is False
    assert result.previous_state == "Resolved"
    assert result.next_state == "Resolved"
    assert notifications == []


def test_resolve_requires_resolution_and_notifies():
    notifications = []

    result = resolve(
        current_state="Acknowledged",
        actor="operator@example.test",
        occurred_at="2026-09-06T18:00:00Z",
        resolution="Replacement shipment dispatched",
        already_applied=False,
        notify=notification_recorder(notifications),
    )

    assert result.changed is True
    assert result.next_state == "Resolved"
    assert notifications[0]["recipients"] == "ops@example.test"


def test_resolve_replay_is_noop_without_duplicate_notification():
    notifications = []

    result = resolve(
        current_state="Resolved",
        actor="operator@example.test",
        occurred_at="2026-09-06T18:00:00Z",
        resolution="Replacement shipment dispatched",
        already_applied=True,
        notify=notification_recorder(notifications),
    )

    assert result.changed is False
    assert notifications == []


@pytest.mark.parametrize("actor", ["", "   "])
def test_actions_require_actor(actor):
    with pytest.raises(ValueError, match="actor"):
        acknowledge(
            current_state="Open",
            actor=actor,
            occurred_at="now",
            already_applied=False,
            notify=lambda **kwargs: None,
        )


def test_resolve_requires_non_empty_resolution():
    with pytest.raises(ValueError, match="Resolution text"):
        resolve(
            current_state="Acknowledged",
            actor="operator@example.test",
            occurred_at="now",
            resolution=" ",
            already_applied=False,
            notify=lambda **kwargs: None,
        )
