from decimal import Decimal

from na_approvals.engine import resolve
from na_approvals.types import Decision, RuleResult

DEFAULT_FINANCE_THRESHOLD = Decimal("500")


def money(value) -> Decimal:
    return Decimal(str(value or 0)).quantize(Decimal("0.01"))


def line_total(quantity, unit_price) -> Decimal:
    return (money(quantity) * money(unit_price)).quantize(Decimal("0.01"))


def request_total(items) -> Decimal:
    total = Decimal("0.00")
    for item in items:
        quantity = getattr(item, "quantity", 0)
        unit_price = getattr(item, "unit_price", 0)
        total += line_total(quantity, unit_price)
    return total.quantize(Decimal("0.01"))


def finance_approval_rule(total_amount, threshold=DEFAULT_FINANCE_THRESHOLD) -> RuleResult:
    total = money(total_amount)
    threshold = money(threshold)

    if total >= threshold:
        return RuleResult(
            rule="finance_threshold",
            decision=Decision.REQUIRE_APPROVAL,
            priority=50,
            reason=f"Purchase request total {total} is at or above finance threshold {threshold}",
        )

    return RuleResult(
        rule="finance_threshold",
        decision=Decision.ALLOW,
        priority=50,
        reason=f"Purchase request total {total} is below finance threshold {threshold}",
    )


def requires_finance_approval(total_amount, threshold=DEFAULT_FINANCE_THRESHOLD) -> bool:
    resolution = resolve([finance_approval_rule(total_amount, threshold)])
    return bool(resolution and resolution.decision == Decision.REQUIRE_APPROVAL)
