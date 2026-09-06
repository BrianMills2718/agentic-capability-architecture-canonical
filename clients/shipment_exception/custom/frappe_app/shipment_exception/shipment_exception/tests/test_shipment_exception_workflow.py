from types import SimpleNamespace

from na_approvals.types import Decision

from shipment_exception.workflow import (
    apply_shipment_exception,
    evaluate_shipment_exception,
    notify_exception_team,
)


def test_delayed_shipment_requires_approval():
    shipment = SimpleNamespace(
        shipment_id="S-2001",
        exception_type="late",
        delay_hours=36,
        risk_level="normal",
        approval_required=0,
        approval_reason="",
    )

    resolution = evaluate_shipment_exception(shipment)

    assert resolution is not None
    assert resolution.decision == Decision.REQUIRE_APPROVAL
    assert resolution.priority == 60

    apply_shipment_exception(shipment)
    assert shipment.approval_required == 1
    assert "requires manager approval" in shipment.approval_reason


def test_blocked_shipment_blocks_release():
    shipment = SimpleNamespace(
        shipment_id="S-2002",
        exception_type="damaged",
        delay_hours=0,
        risk_level="normal",
        blocked=True,
        approval_required=0,
        approval_reason="",
    )

    resolution = evaluate_shipment_exception(shipment)

    assert resolution is not None
    assert resolution.decision == Decision.BLOCK
    try:
        apply_shipment_exception(shipment)
        assert False, "blocked shipment should raise a validation error"
    except ValueError:
        pass


def test_notification_sent_after_approval_is_required():
    shipment = SimpleNamespace(
        shipment_id="S-2003",
        exception_type="missing",
        delay_hours=0,
        risk_level="high",
        approval_required=1,
        approval_reason="Shipment exception requires manager approval before release.",
    )
    calls = []

    def fake_send_email(**kwargs):
        calls.append(kwargs)

    sent = notify_exception_team(shipment, send_email=fake_send_email)

    assert sent is True
    assert calls[0]["recipients"] == ["ops@example.com"]
    assert "requires review" in calls[0]["subject"]
