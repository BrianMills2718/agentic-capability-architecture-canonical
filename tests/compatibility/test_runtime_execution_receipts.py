from datetime import datetime, timezone
from pathlib import Path
import sys
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "capabilities/approvals/frappe_app/na_approvals"))
sys.path.insert(0, str(ROOT / "capabilities/core/frappe_app/na_core"))
sys.path.insert(0, str(ROOT / "capabilities/notifications/frappe_app/na_notifications"))

from na_approvals.engine import resolve
from na_approvals.types import Decision, RuleResult
from na_core.transitions import TransitionSpec, plan_transition
from na_notifications.email import send_email


def test_provider_bound_slice_executes_and_emits_traceable_receipts(monkeypatch):
    sent = []
    monkeypatch.setitem(sys.modules, "frappe", SimpleNamespace(sendmail=lambda **kw: sent.append(kw) or "mail:1"))

    provenance = {
        "req:appointment-policy-resolution": {"source_clause": "clause:appointment_approval"},
        "req:appointment-approval-transition": {"source_clause": "clause:appointment_approval", "role_binding": "role-binding:appointment-manager"},
        "req:appointment-reminder-notification": {"source_clause": "clause:appointment_reminder"},
    }
    receipts = []

    decision = resolve([RuleResult(
        rule="rule:long_appointment_requires_approval",
        decision=Decision.REQUIRE_APPROVAL,
        priority=100,
        reason="duration exceeds 90 minutes",
    )])
    assert decision is not None and decision.decision is Decision.REQUIRE_APPROVAL
    receipts.append({"requirement_id":"req:appointment-policy-resolution","semantic_action":"policy.resolve","selected_implementation":"na_approvals.engine.resolve","status":"succeeded","outputs":{"decision":decision.decision.value},"provenance":provenance["req:appointment-policy-resolution"]})

    transition = plan_transition(
        current_state="pending_approval",
        spec=TransitionSpec(stage="approval", action="manager_approve", allowed_from=frozenset({"pending_approval"}), to_state="confirmed"),
        actor="manager@example.com",
        occurred_at=datetime(2026, 9, 7, tzinfo=timezone.utc),
    )
    assert transition.changed and transition.next_state == "confirmed"
    receipts.append({"requirement_id":"req:appointment-approval-transition","semantic_action":"state.transition","selected_implementation":"na_core.transitions.plan_transition","status":"succeeded","outputs":{"transition_result":transition.next_state},"provenance":provenance["req:appointment-approval-transition"]})

    delivery = send_email(recipients=["customer@example.com"], subject="Appointment reminder", message="Your confirmed appointment is tomorrow.")
    assert delivery == "mail:1"
    assert sent == [{"recipients":["customer@example.com"],"subject":"Appointment reminder","message":"Your confirmed appointment is tomorrow.","sender":None}]
    receipts.append({"requirement_id":"req:appointment-reminder-notification","semantic_action":"notification.send","selected_implementation":"na_notifications.email.send_email","status":"succeeded","outputs":{"delivery_ref":delivery},"provenance":provenance["req:appointment-reminder-notification"]})

    assert [r["semantic_action"] for r in receipts] == ["policy.resolve", "state.transition", "notification.send"]
    assert all(r["provenance"]["source_clause"].startswith("clause:") for r in receipts)
