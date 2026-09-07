from __future__ import annotations

import json

from na_approvals.engine import resolve
from na_approvals.types import Decision, RuleResult
from na_core.transitions import TransitionSpec, plan_transition
from na_notifications.email import send_email

APPROVAL_THRESHOLD_MINUTES = 90
SOURCE_CLAUSE = "clause:appointment_approval"
REMINDER_CLAUSE = "clause:appointment_reminder"
ROLE_BINDING = "role-binding:appointment-manager"


def execute_compiled_appointment(*, appointment_name: str, actor: str, recipient: str) -> dict:
    """Execute the proof-local mapping for the exact compiled 90-minute requirement."""
    import frappe
    from frappe.utils import now_datetime

    appointment = frappe.get_doc("Appointment", appointment_name)
    duration = int(appointment.duration_minutes or 0)
    results = []
    if duration > APPROVAL_THRESHOLD_MINUTES:
        results.append(
            RuleResult(
                rule="rule:long_appointment_requires_approval",
                decision=Decision.REQUIRE_APPROVAL,
                priority=100,
                reason="Appointment duration exceeds 90 minutes.",
            )
        )

    resolution = resolve(results)
    decision = resolution.decision if resolution else Decision.ALLOW
    appointment.db_set("approval_required", int(decision is Decision.REQUIRE_APPROVAL), update_modified=False)
    appointment.db_set("approval_reason", "; ".join(resolution.reasons) if resolution else "", update_modified=False)

    receipts = [{
        "requirement_id": "req:appointment-policy-resolution",
        "semantic_action": "policy.resolve",
        "selected_implementation": "na_approvals.engine.resolve",
        "status": "succeeded",
        "outputs": {"decision": decision.value},
        "provenance": {"source_clause": SOURCE_CLAUSE, "semantic_rule": "rule:long_appointment_requires_approval"},
    }]

    if decision is Decision.REQUIRE_APPROVAL:
        transition = plan_transition(
            current_state=appointment.status,
            spec=TransitionSpec(
                stage="appointment",
                action="manager_approve",
                allowed_from=frozenset({"Pending"}),
                to_state="Confirmed",
            ),
            actor=actor,
            occurred_at=now_datetime(),
            reason=resolution.reasons[0],
        )
        appointment.db_set("status", transition.next_state, update_modified=False)
        receipts.append({
            "requirement_id": "req:appointment-approval-transition",
            "semantic_action": "state.transition",
            "selected_implementation": "na_core.transitions.plan_transition",
            "status": "succeeded",
            "outputs": {"transition_result": transition.next_state},
            "provenance": {"source_clause": SOURCE_CLAUSE, "role_binding": ROLE_BINDING},
        })

    delivery = send_email(
        recipients=[recipient],
        subject="Appointment reminder",
        message="Your confirmed appointment is tomorrow.",
    )
    receipts.append({
        "requirement_id": "req:appointment-reminder-notification",
        "semantic_action": "notification.send",
        "selected_implementation": "na_notifications.email.send_email",
        "status": "succeeded",
        "outputs": {"delivery_ref": str(delivery)},
        "provenance": {"source_clause": REMINDER_CLAUSE},
    })

    comment = frappe.get_doc({
        "doctype": "Comment",
        "comment_type": "Info",
        "reference_doctype": "Appointment",
        "reference_name": appointment.name,
        "content": json.dumps({"schema_version": "1.0", "receipts": receipts}, sort_keys=True),
    })
    comment.insert(ignore_permissions=True)
    frappe.db.commit()
    return {"appointment": appointment.name, "receipt_comment": comment.name, "receipts": receipts}
