# Scheduling

Status: `candidate`

Scheduling contains both experimental/broader scope labels and one verified executable availability boundary. Agents must distinguish them.

## Verified executable availability export

- `availability.query` → `na_scheduling.availability.is_available`
- supporting public types/helpers: `na_scheduling.availability.TimeWindow` and `na_scheduling.availability.find_conflicts`

This boundary is pure Python and framework-neutral. It answers whether a proposed half-open time window conflicts with existing windows, with optional exclusion of the current record during rescheduling.

## Broader capability scope

The manifest also carries booking-oriented scope labels:

- `appointment.create`
- `appointment.cancel`
- `appointment.reschedule`

Those labels are **not verified executable semantic exports**. Do not infer callable appointment actions from them. Add an export only when a real stable public boundary exists and passes the catalog/source checks.

This distinction was tightened after a framework-neutral ATS/booking experiment independently needed availability checking: the reusable implementation already existed, but an agent correctly rejected it because no honest executable boundary had been published.
