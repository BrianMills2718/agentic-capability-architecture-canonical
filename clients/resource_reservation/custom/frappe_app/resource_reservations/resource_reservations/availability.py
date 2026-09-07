from dataclasses import dataclass

from na_scheduling.availability import TimeWindow, find_conflicts


@dataclass(frozen=True)
class AvailabilityResult:
    free: bool
    conflicts: tuple[str, ...]


def _window_from_row(row):
    return TimeWindow(
        start=row.start_time,
        duration_minutes=int(row.duration_minutes),
        key=row.name,
    )


def query_availability(
    *,
    resource,
    start_time,
    duration_minutes,
    exclude_reservation=None,
):
    import frappe
    from frappe.utils import get_datetime

    if not frappe.db.exists("Reservable Resource", resource):
        frappe.throw("Reservable Resource does not exist")
    if not bool(frappe.db.get_value("Reservable Resource", resource, "active")):
        frappe.throw("Reservable Resource is inactive")

    rows = frappe.get_all(
        "Resource Reservation",
        filters={"resource": resource, "status": "Reserved"},
        fields=["name", "start_time", "duration_minutes"],
    )
    proposed = TimeWindow(
        start=get_datetime(start_time),
        duration_minutes=int(duration_minutes),
        key=exclude_reservation,
    )
    conflicts = find_conflicts(
        proposed,
        [_window_from_row(row) for row in rows],
        exclude_key=exclude_reservation,
    )
    names = tuple(window.key for window in conflicts if window.key)
    return AvailabilityResult(free=not names, conflicts=names)
