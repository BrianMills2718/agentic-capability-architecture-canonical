from types import SimpleNamespace

from na_approvals.types import Decision
from procurement_requests.policy import (
    finance_approval_rule,
    line_total,
    request_total,
    requires_finance_approval,
)


def test_server_money_calculations_are_deterministic():
    items = [
        SimpleNamespace(quantity=2, unit_price="125.50"),
        SimpleNamespace(quantity=3, unit_price="10"),
    ]

    assert line_total(2, "125.50") == 251
    assert request_total(items) == 281


def test_finance_threshold_uses_shared_approval_decision_vocabulary():
    below = finance_approval_rule(499.99, 500)
    at_threshold = finance_approval_rule(500, 500)

    assert below.decision == Decision.ALLOW
    assert at_threshold.decision == Decision.REQUIRE_APPROVAL
    assert not requires_finance_approval(499.99, 500)
    assert requires_finance_approval(500, 500)
