# Reuse assessment

The duration-based approval rule is still local to ACME because only one materially different consumer has demonstrated it. The reusable lesson is the extension pattern itself: project rules should return shared approval decisions and delegate final resolution to `na_approvals` instead of mutating Scheduling internals. If a second project needs the same threshold behavior, review it as a candidate configurable approval rule rather than copying ACME code.
