# Reuse assessment

The >90-minute approval threshold and hourly reminder policy remain local to
Beta because they are project-specific choices. The reusable lesson is that a
client extension can compose the shared approval resolver, notification
transport, and scheduler trigger without changing existing capability behavior.
If a second materially different project needs durable reminder delivery, record
that as a candidate for a shared scheduling/notification interface rather than
copying this extension.
