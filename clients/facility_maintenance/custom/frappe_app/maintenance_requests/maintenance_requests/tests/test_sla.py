from datetime import datetime, timedelta
from types import SimpleNamespace

from maintenance_requests.sla import calculate_due_at, hours_for_priority

def test_default_sla_hours():
    assert hours_for_priority("Urgent") == 4
    assert hours_for_priority("High") == 24
    assert hours_for_priority("Normal") == 72
    assert hours_for_priority("Low") == 120

def test_settings_override_and_due_calculation():
    settings = SimpleNamespace(urgent_hours=2, high_hours=12, normal_hours=48, low_hours=96)
    start = datetime(2026, 9, 6, 12, 0, 0)
    assert calculate_due_at(start, "High", settings) == start + timedelta(hours=12)
