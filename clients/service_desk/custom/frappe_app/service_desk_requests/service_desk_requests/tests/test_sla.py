from datetime import datetime, timedelta
from types import SimpleNamespace
from service_desk_requests.sla import calculate_due_at, hours_for_priority

def test_defaults():
    assert [hours_for_priority(p) for p in ["Urgent","High","Normal","Low"]] == [2,8,24,72]

def test_override():
    s=SimpleNamespace(urgent_hours=1, high_hours=4, normal_hours=12, low_hours=48)
    start=datetime(2026,9,6,12)
    assert calculate_due_at(start,"High",s)==start+timedelta(hours=4)
