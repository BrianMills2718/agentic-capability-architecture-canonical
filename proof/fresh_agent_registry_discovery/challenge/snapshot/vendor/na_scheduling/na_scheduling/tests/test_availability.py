from datetime import datetime

from na_scheduling.availability import TimeWindow, find_conflicts, is_available, overlaps


def at(hour, minute=0):
    return datetime(2026, 9, 7, hour, minute)


def test_half_open_windows_allow_back_to_back_reservations():
    first = TimeWindow(start=at(10), duration_minutes=60, key="a")
    second = TimeWindow(start=at(11), duration_minutes=60, key="b")
    assert overlaps(first, second) is False
    assert is_available(second, [first]) is True


def test_overlapping_windows_conflict():
    existing = TimeWindow(start=at(10), duration_minutes=60, key="a")
    proposed = TimeWindow(start=at(10, 30), duration_minutes=60, key="b")
    assert overlaps(existing, proposed) is True
    assert [w.key for w in find_conflicts(proposed, [existing])] == ["a"]


def test_excluding_current_window_supports_reschedule():
    current = TimeWindow(start=at(10), duration_minutes=60, key="self")
    other = TimeWindow(start=at(13), duration_minutes=60, key="other")
    proposed = TimeWindow(start=at(11), duration_minutes=60, key="self")
    assert is_available(proposed, [current, other], exclude_key="self") is True


def test_non_positive_duration_is_rejected():
    try:
        TimeWindow(start=at(10), duration_minutes=0)
    except ValueError as exc:
        assert "greater than zero" in str(exc)
    else:
        raise AssertionError("zero-duration window should fail")
