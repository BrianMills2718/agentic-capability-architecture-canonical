# Reuse assessment

The reminder trigger is a plausible reuse candidate: client extensions can own
reminder policy while calling the shared notification transport. It remains local
for now because this is the first demonstrated scheduling-reminder consumer and
the reminder window and recipient policy are project-specific.
