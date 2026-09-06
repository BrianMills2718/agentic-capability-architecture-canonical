from collections.abc import Iterable

from na_approvals.exceptions import ApprovalRuleConflict, EqualPriorityDisagreement
from na_approvals.types import Decision, Resolution, RuleResult


def resolve(results: Iterable[RuleResult]) -> Resolution | None:
    """Resolve approval rule results deterministically.

    Semantics:
    1. Explicit conflicts fail.
    2. Any BLOCK result wins; the highest-priority BLOCK is the primary winner.
    3. Otherwise the highest priority wins.
    4. Equal-priority rules must agree on decision.
    5. Rule-name ordering makes output deterministic when priorities tie.
    """
    ordered = sorted(results, key=lambda result: (-result.priority, result.rule))
    if not ordered:
        return None

    _check_explicit_conflicts(ordered)

    blocks = [r for r in ordered if r.decision == Decision.BLOCK]
    if blocks:
        top_priority = blocks[0].priority
        top = [r for r in blocks if r.priority == top_priority]
        return Resolution(
            decision=Decision.BLOCK,
            priority=top_priority,
            winning_rules=tuple(r.rule for r in top),
            reasons=tuple(r.reason for r in top),
        )

    highest_priority = ordered[0].priority
    highest = [r for r in ordered if r.priority == highest_priority]
    decisions = {r.decision for r in highest}

    if len(decisions) > 1:
        details = ", ".join(f"{r.rule}={r.decision.value}" for r in highest)
        raise EqualPriorityDisagreement(
            f"Equal-priority approval rules disagree: {details}"
        )

    return Resolution(
        decision=highest[0].decision,
        priority=highest_priority,
        winning_rules=tuple(r.rule for r in highest),
        reasons=tuple(r.reason for r in highest),
    )


def _check_explicit_conflicts(results: list[RuleResult]) -> None:
    active = {result.rule for result in results}
    conflicts: set[tuple[str, str]] = set()

    for result in results:
        for other in result.conflicts_with:
            if other in active:
                conflicts.add(tuple(sorted((result.rule, other))))

    if conflicts:
        details = ", ".join(f"{a} <-> {b}" for a, b in sorted(conflicts))
        raise ApprovalRuleConflict(f"Explicit approval rule conflict: {details}")


def apply_resolution(document, resolution: Resolution | None) -> None:
    """Apply a non-BLOCK decision to a document-like object.

    BLOCK is intentionally left to the framework adapter because the core engine
    has no dependency on Frappe. ALLOW is monotonic: it never clears an already
    required approval set by a shared/core policy.
    """
    if resolution is None:
        return

    if resolution.decision == Decision.BLOCK:
        raise ValueError("BLOCK must be enforced by the framework adapter")

    if resolution.decision == Decision.REQUIRE_APPROVAL:
        document.approval_required = 1
        document.approval_reason = "; ".join(resolution.reasons)
        return

    if resolution.decision == Decision.ALLOW:
        if not getattr(document, "approval_required", False):
            document.approval_required = 0
