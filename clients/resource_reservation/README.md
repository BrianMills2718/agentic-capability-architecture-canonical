# Shared Resource Reservation

Project 6 and the first deliberately non-appointment pressure test for the Scheduling
capability.

The project reserves project-local resources (rooms, equipment, or vehicles) while reusing
shared Scheduling behavior only where the abstraction is genuinely domain-neutral.

The project must not turn the shared `Appointment` DocType into a fake universal resource
reservation record.
