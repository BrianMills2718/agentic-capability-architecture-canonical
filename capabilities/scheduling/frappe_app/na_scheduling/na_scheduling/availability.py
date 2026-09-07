from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Iterable


def validate_duration_minutes(value: int) -> int:
    duration = int(value)
    if duration <= 0:
        raise ValueError("duration_minutes must be greater than zero")
    return duration


@dataclass(frozen=True)
class TimeWindow:
    start: datetime
    duration_minutes: int
    key: str | None = None

    def __post_init__(self):
        validate_duration_minutes(self.duration_minutes)

    @property
    def end(self) -> datetime:
        return self.start + timedelta(minutes=self.duration_minutes)


def overlaps(left: TimeWindow, right: TimeWindow) -> bool:
    """Return True when half-open windows [start, end) intersect."""
    return left.start < right.end and right.start < left.end


def find_conflicts(
    proposed: TimeWindow,
    existing: Iterable[TimeWindow],
    *,
    exclude_key: str | None = None,
) -> list[TimeWindow]:
    conflicts = []
    for window in existing:
        if exclude_key is not None and window.key == exclude_key:
            continue
        if overlaps(proposed, window):
            conflicts.append(window)
    return conflicts


def is_available(
    proposed: TimeWindow,
    existing: Iterable[TimeWindow],
    *,
    exclude_key: str | None = None,
) -> bool:
    return not find_conflicts(proposed, existing, exclude_key=exclude_key)
