# Approvals

Status: `candidate`

Reusable approval boundaries with two deliberately separate meanings:

- deterministic resolution of competing business-rule results;
- binding a trusted human approval event to the exact consequential action that
  may later execute or retry.

Verified semantic actions:

- `approval.resolve` → `na_approvals.engine.resolve`
- `approval.action.bind` → `na_approvals.binding.bind_approval`
- `approval.action.verify` → `na_approvals.binding.verify_approval`

For action approval, construct an `ActionIntent` containing the stable operation
key, action, target, and complete JSON payload. Call `bind_approval` only after a
trusted application boundary records human consent, persist the returned
`ApprovalBinding`, and call `verify_approval` immediately before every initial or
retried execution. Any changed field fails closed.

This capability does not prove who clicked approve, provide authentication or
authorization, store the receipt, or execute the action. Those remain the
application/runtime's responsibility.

Do not expand this capability speculatively. Add real interfaces, configuration, and tests when a real project needs them.
