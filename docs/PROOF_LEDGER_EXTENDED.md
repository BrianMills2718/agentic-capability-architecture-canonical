# Proof Ledger

This file records proof identifiers referenced during development. GitHub Actions run IDs are retained so claims can be checked against the original proof repositories where access remains available.

## Bootstrap and agent behavior

- `34001408766` — baseline real Frappe lifecycle proof; 6 tests OK.
- `34010580867` — genuinely fresh coding-agent acceptance hidden evaluator; acceptance passed.

## Real project proofs

- `34012529168` — Client Intake + Booking staff approval lifecycle; ACME regression 6/6, Client Intake 4/4.
- `34015479165` — Internal Procurement on isolated site; Procurement 5/5 while prior suites remained green.
- `34017058788` — IT Access Control; third materially different approval-action use.
- `34020413484` — Facility Maintenance five-site proof; Maintenance 4/4.
- Later Service Desk proof added a sixth isolated composition and prospective primitive-model pressure.
- `34046554727` — Shared Resource Reservation seven-site proof; non-appointment scheduling domain added while prior suites remained green.

## Cross-repository portability

- `34047230770` — independent consumer repository resolved portable capabilities, verified package hashes, installed dependency closure, and passed 7/7 consumer tests.

## Evidence interpretation

Passing tests prove bounded implementation claims, not universal architectural correctness.

The strongest recurring evidence so far is:

- state-transition planning generalized across multiple domains;
- Notifications remained small while serving multiple distinct domains;
- client-specific Frappe apps can remain isolated on separate sites/databases;
- capability portability can work outside the source monorepo;
- prospective modeling can reveal abstraction ownership mistakes before implementation;
- Resource Reservation showed that a capability interface such as `availability.query` need not automatically become a primitive.

## Pending proof

The fresh-agent registry-discovery challenge under `proof/fresh_agent_registry_discovery/` still needs a genuinely separate coding agent run.

That test should establish whether an agent can discover, select, reject, and compose portable capabilities without receiving the source monorepo or this conversation.
