from dataclasses import dataclass, field
from enum import Enum


class Decision(str, Enum):
    ALLOW = "ALLOW"
    REQUIRE_APPROVAL = "REQUIRE_APPROVAL"
    BLOCK = "BLOCK"


@dataclass(frozen=True)
class RuleResult:
    rule: str
    decision: Decision
    priority: int
    reason: str
    conflicts_with: frozenset[str] = field(default_factory=frozenset)


@dataclass(frozen=True)
class Resolution:
    decision: Decision
    priority: int
    winning_rules: tuple[str, ...]
    reasons: tuple[str, ...]
