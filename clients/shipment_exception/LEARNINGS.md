# Reuse assessment

The shipment exception workflow remains local because the business trigger and escalation policy are project-specific. It successfully reuses the shared approval and notification capabilities, but the shipping domain logic should stay in the client extension until a second materially different workflow demonstrates the same pattern. The reusable lesson is the composition model itself: keep the shared rule engine and email adapter stable while the client decides which shipments require review and who receives the notice.
