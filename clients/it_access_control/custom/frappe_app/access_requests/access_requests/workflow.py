from access_requests.notifications import notify_requester_and_target, notify_role
from access_requests.permissions import (
    MANAGER_ROLE,
    PROVISIONER_ROLE,
    SECURITY_ROLE,
    require_not_requester_or_target,
    require_not_target,
    require_request_owner_or_system_manager,
    require_role,
)
from access_requests.policy import requires_security_approval
from na_approvals.transitions import (
    InvalidApprovalTransition,
    TransitionSpec,
    audit_payload,
    plan_transition,
)


def _now():
    from frappe.utils import now_datetime

    return now_datetime()


def _actor(actor=None):
    import frappe

    return actor or frappe.session.user


def get_security_levels():
    import frappe

    configured = frappe.db.get_single_value("Access Control Settings", "security_approval_levels")
    return configured or "Sensitive\nPrivileged"


def _has_event(request, *, stage, action):
    return any(
        row.stage == stage and row.action == action
        for row in (getattr(request, "approval_events", None) or [])
    )


def _event_actor(request, *, stage, action):
    for row in reversed(getattr(request, "approval_events", None) or []):
        if row.stage == stage and row.action == action:
            return row.actor
    return None


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
        frappe.throw("Only a draft access request can be submitted")

    require_request_owner_or_system_manager(request, actor)

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
        subject=f"Access request {request.name} needs manager approval",
        message=f"{request.requester} requested {request.access_level} access to {request.system_name} for {request.target_user}.",
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
            invalid_message="Access request is not pending manager approval",
        )
        return transition.next_state

    require_role(actor, MANAGER_ROLE)
    require_not_requester_or_target(request, actor)

    security_required = requires_security_approval(
        request.access_level,
        get_security_levels(),
    )
    next_status = (
        "Pending Security Approval"
        if security_required
        else "Ready to Provision"
    )
    transition = _plan_approval(
        request,
        stage="Manager",
        action="Approve",
        expected_status="Pending Manager Approval",
        next_status=next_status,
        actor=actor,
        invalid_message="Access request is not pending manager approval",
    )

    request.status = transition.next_state
    if security_required:
        request.current_approval_stage = "Security"
    else:
        request.current_approval_stage = ""
        request.approved_at = transition.occurred_at

    _append_approval_transition(request, transition)
    _save(request)

    if security_required:
        notify_role(
            SECURITY_ROLE,
            subject=f"Access request {request.name} needs security approval",
            message=f"{request.access_level} access to {request.system_name} needs security review.",
        )
    else:
        notify_role(
            PROVISIONER_ROLE,
            subject=f"Access request {request.name} is ready to provision",
            message=f"Approved access for {request.target_user} is ready to provision.",
        )
        notify_requester_and_target(
            request,
            subject=f"Access request {request.name} approved",
            message="Your access request has been approved and is ready to provision.",
        )

    return request.status


def approve_security(request, *, actor=None):
    actor = _actor(actor)
    already_applied = _has_event(request, stage="Security", action="Approve")

    if already_applied:
        transition = _plan_approval(
            request,
            stage="Security",
            action="Approve",
            expected_status="Pending Security Approval",
            next_status=None,
            actor=actor,
            already_applied=True,
            invalid_message="Access request is not pending security approval",
        )
        return transition.next_state

    require_role(actor, SECURITY_ROLE)
    require_not_requester_or_target(request, actor)

    manager_actor = _event_actor(request, stage="Manager", action="Approve")
    if manager_actor and manager_actor == actor:
        import frappe
        frappe.throw("Security approval must be performed by a different actor")

    transition = _plan_approval(
        request,
        stage="Security",
        action="Approve",
        expected_status="Pending Security Approval",
        next_status="Ready to Provision",
        actor=actor,
        invalid_message="Access request is not pending security approval",
    )

    request.status = transition.next_state
    request.current_approval_stage = ""
    request.approved_at = transition.occurred_at
    _append_approval_transition(request, transition)
    _save(request)

    notify_role(
        PROVISIONER_ROLE,
        subject=f"Access request {request.name} is ready to provision",
        message=f"Approved access for {request.target_user} is ready to provision.",
    )
    notify_requester_and_target(
        request,
        subject=f"Access request {request.name} approved",
        message="Your access request has been approved and is ready to provision.",
    )
    return request.status


def _reject(request, *, stage, required_role, actor=None, reason):
    import frappe

    actor = _actor(actor)
    already_applied = _has_event(request, stage=stage, action="Reject")
    if already_applied:
        transition = _plan_approval(
            request,
            stage=stage,
            action="Reject",
            expected_status=f"Pending {stage} Approval",
            next_status=None,
            actor=actor,
            already_applied=True,
            reason=reason,
            invalid_message=f"Access request is not pending {stage.lower()} approval",
        )
        return transition.next_state

    require_role(actor, required_role)
    require_not_requester_or_target(request, actor)

    if not (reason or "").strip():
        frappe.throw("Rejection reason is required")

    transition = _plan_approval(
        request,
        stage=stage,
        action="Reject",
        expected_status=f"Pending {stage} Approval",
        next_status="Rejected",
        actor=actor,
        reason=reason.strip(),
        invalid_message=f"Access request is not pending {stage.lower()} approval",
    )

    request.status = transition.next_state
    request.current_approval_stage = ""
    request.rejected_at = transition.occurred_at
    request.rejection_reason = transition.reason
    _append_approval_transition(request, transition)
    _save(request)

    notify_requester_and_target(
        request,
        subject=f"Access request {request.name} rejected",
        message=f"Access request rejected at {stage} stage: {request.rejection_reason}",
    )
    return request.status


def reject_manager(request, *, actor=None, reason):
    return _reject(
        request,
        stage="Manager",
        required_role=MANAGER_ROLE,
        actor=actor,
        reason=reason,
    )


def reject_security(request, *, actor=None, reason):
    return _reject(
        request,
        stage="Security",
        required_role=SECURITY_ROLE,
        actor=actor,
        reason=reason,
    )


def mark_provisioned(request, *, actor=None):
    actor = _actor(actor)

    if request.status == "Provisioned" and request.provisioned_at:
        return request.status

    require_role(actor, PROVISIONER_ROLE)
    require_not_target(request, actor)

    if request.status != "Ready to Provision":
        import frappe
        frappe.throw("Only approved access can be provisioned")

    previous = request.status
    request.status = "Provisioned"
    request.provisioned_at = _now()
    _append_event(
        request,
        stage="Provisioning",
        action="Provision",
        actor=actor,
        from_status=previous,
        to_status=request.status,
    )
    _save(request)

    notify_requester_and_target(
        request,
        subject=f"Access request {request.name} provisioned",
        message=f"{request.access_level} access to {request.system_name} has been provisioned.",
    )
    return request.status


def revoke_access(request, *, actor=None, reason=None):
    actor = _actor(actor)

    if request.status == "Revoked" and request.revoked_at:
        return request.status

    require_role(actor, PROVISIONER_ROLE)
    require_not_target(request, actor)

    if request.status != "Provisioned":
        import frappe
        frappe.throw("Only provisioned access can be revoked")

    previous = request.status
    request.status = "Revoked"
    request.revoked_at = _now()
    _append_event(
        request,
        stage="Provisioning",
        action="Revoke",
        actor=actor,
        from_status=previous,
        to_status=request.status,
        reason=reason,
    )
    _save(request)

    notify_requester_and_target(
        request,
        subject=f"Access request {request.name} revoked",
        message=f"Access to {request.system_name} has been revoked.",
    )
    return request.status
