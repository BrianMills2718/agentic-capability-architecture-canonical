class ApprovalRuleError(Exception):
    """Base exception for deterministic approval resolution errors."""


class ApprovalRuleConflict(ApprovalRuleError):
    """Raised when two active rules explicitly declare incompatibility."""


class EqualPriorityDisagreement(ApprovalRuleError):
    """Raised when equally authoritative rules produce different decisions."""


class AppointmentBlocked(ApprovalRuleError):
    """Raised by framework adapters when a resolved BLOCK must stop an operation."""
