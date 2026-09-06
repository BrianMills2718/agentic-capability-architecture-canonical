from types import SimpleNamespace

import pytest

from na_approvals.engine import apply_resolution, resolve
from na_approvals.exceptions import ApprovalRuleConflict, EqualPriorityDisagreement
from na_approvals.types import Decision, RuleResult


def rule(name, decision, priority, reason=None, conflicts_with=()):
    return RuleResult(
        rule=name,
        decision=decision,
        priority=priority,
        reason=reason or name,
        conflicts_with=frozenset(conflicts_with),
    )


def test_allow_beats_lower_priority_require():
    resolution = resolve([
        rule("long", Decision.REQUIRE_APPROVAL, 50),
        rule("vip", Decision.ALLOW, 60),
    ])
    assert resolution.decision == Decision.ALLOW
    assert resolution.winning_rules == ("vip",)


def test_require_beats_lower_priority_allow():
    resolution = resolve([
        rule("vip", Decision.ALLOW, 60),
        rule("high_value", Decision.REQUIRE_APPROVAL, 90),
    ])
    assert resolution.decision == Decision.REQUIRE_APPROVAL
    assert resolution.priority == 90


def test_block_wins_even_with_lower_numeric_priority():
    resolution = resolve([
        rule("vip", Decision.ALLOW, 100),
        rule("compliance", Decision.BLOCK, 20),
    ])
    assert resolution.decision == Decision.BLOCK


def test_equal_priority_same_decision_is_deterministic():
    a = resolve([
        rule("z_rule", Decision.REQUIRE_APPROVAL, 80),
        rule("a_rule", Decision.REQUIRE_APPROVAL, 80),
    ])
    b = resolve([
        rule("a_rule", Decision.REQUIRE_APPROVAL, 80),
        rule("z_rule", Decision.REQUIRE_APPROVAL, 80),
    ])
    assert a == b
    assert a.winning_rules == ("a_rule", "z_rule")


def test_equal_priority_disagreement_fails():
    with pytest.raises(EqualPriorityDisagreement):
        resolve([
            rule("allow", Decision.ALLOW, 80),
            rule("require", Decision.REQUIRE_APPROVAL, 80),
        ])


def test_explicit_conflict_fails_before_priority_can_hide_it():
    with pytest.raises(ApprovalRuleConflict):
        resolve([
            rule("vip", Decision.ALLOW, 10, conflicts_with=("compliance",)),
            rule("compliance", Decision.BLOCK, 100),
        ])


def test_no_rules_returns_none():
    assert resolve([]) is None


def test_require_is_applied():
    doc = SimpleNamespace(approval_required=0, approval_reason="")
    resolution = resolve([
        rule("long", Decision.REQUIRE_APPROVAL, 50, "Long appointment")
    ])
    apply_resolution(doc, resolution)
    assert doc.approval_required == 1
    assert doc.approval_reason == "Long appointment"


def test_allow_does_not_remove_existing_shared_requirement():
    doc = SimpleNamespace(
        approval_required=1,
        approval_reason="Shared policy",
    )
    resolution = resolve([rule("vip", Decision.ALLOW, 100)])
    apply_resolution(doc, resolution)
    assert doc.approval_required == 1
    assert doc.approval_reason == "Shared policy"
