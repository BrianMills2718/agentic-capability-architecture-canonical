from procurement_requests.notifications import notify_requester, notify_role
from procurement_requests.permissions import (
    FINANCE_ROLE,
    MANAGER_ROLE,
    OFFICER_ROLE,
    require_not_requester,
    require_request_owner_or_system_manager,
    require_role,
)
from procurement_requests.policy import requires_finance_approval
from na_approvals.transitions import (
    InvalidApprovalTransition,
    TransitionSpec,
    audit_payload,
    plan_transition,
)


def get_finance_threshold():
    import frappe

    configured = frappe.db.get_single_value("Procurement Settings", "finance_threshold")
    return configured or 500


def _now():
    from frappe.utils import now_datetime

    return now_datetime()


def _actor(actor=None):
    import frappe

    return actor or frappe.session.user


def _has_event(request, *, stage, action):
    return any(
        row.stage == stage and row.action == action
        for row in (getattr(request, "approval_events", None) or [])
    )


def _append_event(request, *, stage, action, actor, from_status, to_status, reason=None):
    request.append(
        "approval_events",
        {
            "stage": stage,
            "action": action,
            "actor": actor,
            "occurred_at": _now(),
            "from_status": from_status,
            "to_status": to_status,
            "reason": reason or "",
        },
    )


def _plan_approval(
    request,
    *,
    stage,
    action,
    expected_status,
    next_status,
    actor,
    already_applied=False,
    reason=None,
    invalid_message,
):
    import frappe

    try:
        return plan_transition(
            current_state=request.status,
            spec=TransitionSpec(
                stage=stage,
                action=action,
                allowed_from=frozenset({expected_status}),
                to_state=next_status,
            ),
            actor=actor,
            occurred_at=_now(),
            already_applied=already_applied,
            reason=reason,
        )
    except InvalidApprovalTransition:
        frappe.throw(invalid_message)


def _append_approval_transition(request, transition):
    payload = audit_payload(transition)
    if payload is not None:
        request.append("approval_events", payload)


def _save(request):
    request.save(ignore_permissions=True)
    return request.status


def submit_request(request, *, actor=None):
    actor = _actor(actor)

    if request.status != "Draft":
        if request.submitted_at:
            return request.status
        import frappe
        frappe.throw("Only a draft purchase request can be submitted")

    require_request_owner_or_system_manager(request, actor)

    if not request.items:
        import frappe
        frappe.throw("At least one purchase request item is required")

    previous = request.status
    request.status = "Pending Manager Approval"
    request.current_approval_stage = "Manager"
    request.submitted_at = _now()
    _append_event(
        request,
        stage="Submission",
        action="Submit",
        actor=actor,
        from_status=previous,
        to_status=request.status,
    )
    _save(request)

    notify_role(
        MANAGER_ROLE,
        subject=f"Purchase request {request.name} needs manager approval",
        message=f"{request.requester} submitted purchase request {request.name} for {request.total_amount}.",
    )
    return request.status


def approve_manager(request, *, actor=None):
    actor = _actor(actor)
    already_applied = _has_event(request, stage="Manager", action="Approve")

    if already_applied:
        transition = _plan_approval(
            request,
            stage="Manager",
            action="Approve",
            expected_status="Pending Manager Approval",
            next_status=None,
            actor=actor,
            already_applied=True,
            invalid_message="Purchase request is not pending manager approval",
        )
        return transition.next_state

    require_role(actor, MANAGER_ROLE)
    require_not_requester(request, actor)

    finance_required = requires_finance_approval(
        request.total_amount,
        get_finance_threshold(),
    )
    next_status = (
        "Pending Finance Approval"
        if finance_required
        else "Ready to Purchase"
    )
    transition = _plan_approval(
        request,
        stage="Manager",
        action="Approve",
        expected_status="Pending Manager Approval",
        next_status=next_status,
        actor=actor,
        invalid_message="Purchase request is not pending manager approval",
    )

    request.status = transition.next_state
    if finance_required:
        request.current_approval_stage = "Finance"
    else:
        request.current_approval_stage = ""
        request.approved_at = transition.occurred_at

    _append_approval_transition(request, transition)
    _save(request)

    if finance_required:
        notify_role(
            FINANCE_ROLE,
            subject=f"Purchase request {request.name} needs finance approval",
            message=f"Manager approved {request.name}; finance review is required for {request.total_amount}.",
        )
    else:
        notify_requester(
            request,
            subject=f"Purchase request {request.name} approved",
            message="Your purchase request is approved and ready for procurement.",
        )
        notify_role(
            OFFICER_ROLE,
            subject=f"Purchase request {request.name} ready to purchase",
            message=f"Purchase request {request.name} is fully approved.",
        )

    return request.status


def reject_manager(request, *, reason, actor=None):
    return _reject(
        request,
        expected_status="Pending Manager Approval",
        stage="Manager",
        role=MANAGER_ROLE,
        reason=reason,
        actor=actor,
    )


def approve_finance(request, *, actor=None):
    actor = _actor(actor)
    already_applied = _has_event(request, stage="Finance", action="Approve")

    if already_applied:
        transition = _plan_approval(
            request,
            stage="Finance",
            action="Approve",
            expected_status="Pending Finance Approval",
            next_status=None,
            actor=actor,
            already_applied=True,
            invalid_message="Purchase request is not pending finance approval",
        )
        return transition.next_state

    require_role(actor, FINANCE_ROLE)
    require_not_requester(request, actor)

    transition = _plan_approval(
        request,
        stage="Finance",
        action="Approve",
        expected_status="Pending Finance Approval",
        next_status="Ready to Purchase",
        actor=actor,
        invalid_message="Purchase request is not pending finance approval",
    )

    request.status = transition.next_state
    request.current_approval_stage = ""
    request.approved_at = transition.occurred_at
    _append_approval_transition(request, transition)
    _save(request)

    notify_requester(
        request,
        subject=f"Purchase request {request.name} approved",
        message="Your purchase request is fully approved and ready for procurement.",
    )
    notify_role(
        OFFICER_ROLE,
        subject=f"Purchase request {request.name} ready to purchase",
        message=f"Purchase request {request.name} is fully approved.",
    )
    return request.status


def reject_finance(request, *, reason, actor=None):
    return _reject(
        request,
        expected_status="Pending Finance Approval",
        stage="Finance",
        role=FINANCE_ROLE,
        reason=reason,
        actor=actor,
    )


def _reject(request, *, expected_status, stage, role, reason, actor=None):
    import frappe

    actor = _actor(actor)
    already_applied = _has_event(request, stage=stage, action="Reject")
    if already_applied:
        transition = _plan_approval(
            request,
            stage=stage,
            action="Reject",
            expected_status=expected_status,
            next_status=None,
            actor=actor,
            already_applied=True,
            reason=reason,
            invalid_message=f"Purchase request is not pending {stage.lower()} approval",
        )
        return transition.next_state

    require_role(actor, role)
    require_not_requester(request, actor)

    if not str(reason or "").strip():
        frappe.throw("Rejection reason is required")

    transition = _plan_approval(
        request,
        stage=stage,
        action="Reject",
        expected_status=expected_status,
        next_status="Rejected",
        actor=actor,
        reason=str(reason).strip(),
        invalid_message=f"Purchase request is not pending {stage.lower()} approval",
    )

    request.status = transition.next_state
    request.current_approval_stage = ""
    request.rejected_at = transition.occurred_at
    request.rejection_reason = transition.reason
    _append_approval_transition(request, transition)
    _save(request)

    notify_requester(
        request,
        subject=f"Purchase request {request.name} rejected",
        message=f"Your purchase request was rejected at the {stage.lower()} stage: {request.rejection_reason}",
    )
    return request.status


def mark_purchased(request, *, actor=None):
    actor = _actor(actor)
    if request.purchased_at and request.status in {"Purchased", "Received", "Closed"}:
        return request.status

    require_role(actor, OFFICER_ROLE)
    if request.status != "Ready to Purchase":
        import frappe
        frappe.throw("Only an approved request can be marked purchased")

    previous = request.status
    request.status = "Purchased"
    request.purchased_at = _now()
    _append_event(
        request,
        stage="Procurement",
        action="Mark Purchased",
        actor=actor,
        from_status=previous,
        to_status=request.status,
    )
    _save(request)
    notify_requester(
        request,
        subject=f"Purchase request {request.name} purchased",
        message="Your approved purchase request has been marked purchased.",
    )
    return request.status


def mark_received(request, *, actor=None):
    actor = _actor(actor)
    if request.received_at and request.status in {"Received", "Closed"}:
        return request.status

    require_role(actor, OFFICER_ROLE)
    if request.status != "Purchased":
        import frappe
        frappe.throw("Only a purchased request can be marked received")

    previous = request.status
    request.status = "Received"
    request.received_at = _now()
    _append_event(
        request,
        stage="Procurement",
        action="Mark Received",
        actor=actor,
        from_status=previous,
        to_status=request.status,
    )
    _save(request)
    notify_requester(
        request,
        subject=f"Purchase request {request.name} received",
        message="Your purchase request has been marked received.",
    )
    return request.status


def close_request(request, *, actor=None):
    actor = _actor(actor)
    if request.status == "Closed" and request.closed_at:
        return request.status

    require_role(actor, OFFICER_ROLE)
    if request.status != "Received":
        import frappe
        frappe.throw("Only a received request can be closed")

    previous = request.status
    request.status = "Closed"
    request.closed_at = _now()
    _append_event(
        request,
        stage="Procurement",
        action="Close",
        actor=actor,
        from_status=previous,
        to_status=request.status,
    )
    return _save(request)
