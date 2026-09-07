from na_approvals.engine import resolve
from na_approvals.types import Decision, RuleResult


DEFAULT_SECURITY_LEVELS = frozenset({"Sensitive", "Privileged"})


def parse_security_levels(value):
    if value is None:
        return set(DEFAULT_SECURITY_LEVELS)
    if isinstance(value, (set, frozenset, list, tuple)):
        return {str(item).strip() for item in value if str(item).strip()}
    return {
        part.strip()
        for part in str(value).replace(",", "\n").splitlines()
        if part.strip()
    }


def requires_security_approval(access_level, configured_levels=None):
    levels = parse_security_levels(configured_levels)
    result = RuleResult(
        rule="security_sensitive_access",
        decision=(
            Decision.REQUIRE_APPROVAL
            if access_level in levels
            else Decision.ALLOW
        ),
        priority=50,
        reason=f"{access_level} access security policy",
        conflicts_with=frozenset(),
    )
    resolution = resolve([result])
    return resolution.decision == Decision.REQUIRE_APPROVAL
