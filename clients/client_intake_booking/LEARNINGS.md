# Reuse assessment

The service intake workflow is intentionally local to the booking client. It composes the shared approval and notification capabilities, but the intake form, service-type validation, and approval threshold remain project-specific and only one client has demonstrated this pattern. The reusable lesson is to keep the workflow orchestration shared while leaving the intake-specific rules and email content in the project extension until a second materially different consumer appears.
