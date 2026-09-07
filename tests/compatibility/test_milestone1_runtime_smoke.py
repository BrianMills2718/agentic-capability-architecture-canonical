"""Focused runtime smoke for the milestone-1 selected public interfaces."""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import sys
import types

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "capabilities/approvals/frappe_app/na_approvals"))
sys.path.insert(0, str(ROOT / "capabilities/core/frappe_app/na_core"))
sys.path.insert(0, str(ROOT / "capabilities/notifications/frappe_app/na_notifications"))

from na_approvals.engine import resolve
from na_approvals.types import Decision, RuleResult
from na_core.transitions import TransitionSpec, plan_transition
from na_notifications.email import send_email


def test_selected_milestone1_providers_interoperate() -> None:
    resolution = resolve(
        [
            RuleResult(
                rule="rule:long_appointment_requires_approval",
                decision=Decision.REQUIRE_APPROVAL,
                priority=50,
                reason="Appointment duration exceeds 90 minutes.",
            )
        ]
    )
    assert resolution is not None
    assert resolution.decision is Decision.REQUIRE_APPROVAL

    transition = plan_transition(
        current_state="pending_policy_evaluation",
        spec=TransitionSpec(
            stage="appointment",
            action="require_approval",
            allowed_from=frozenset({"pending_policy_evaluation"}),
            to_state="pending_approval",
        ),
        actor="biz:Manager",
        occurred_at=datetime(2026, 9, 7, tzinfo=timezone.utc),
        reason=resolution.reasons[0],
    )
    assert transition.changed is True
    assert transition.next_state == "pending_approval"
    assert transition.actor == "biz:Manager"

    sent = []
    fake_frappe = types.ModuleType("frappe")

    def fake_sendmail(**kwargs):
        sent.append(kwargs)
        return {"queued": True}

    fake_frappe.sendmail = fake_sendmail
    previous = sys.modules.get("frappe")
    sys.modules["frappe"] = fake_frappe
    try:
        result = send_email(
            recipients="customer@example.test",
            subject="Appointment confirmed",
            message="Your appointment is confirmed; reminder timing remains domain-owned.",
        )
    finally:
        if previous is None:
            sys.modules.pop("frappe", None)
        else:
            sys.modules["frappe"] = previous

    assert result == {"queued": True}
    assert sent == [
        {
            "recipients": ["customer@example.test"],
            "subject": "Appointment confirmed",
            "message": "Your appointment is confirmed; reminder timing remains domain-owned.",
            "sender": None,
        }
    ]
