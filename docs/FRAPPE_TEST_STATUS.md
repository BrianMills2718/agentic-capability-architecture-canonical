# Frappe Test Status

## Current status

The Frappe integration suite is **authored and CI-packaged, but has not yet produced a green external Bench run in this workspace**.

This execution environment does not provide the MariaDB/Redis/Docker services needed to run a real Frappe Bench lifecycle directly.

## Automated proof path

The repository now contains `.github/workflows/frappe-integration.yml`, which creates a real Frappe version-15 test Bench with MariaDB and Redis and invokes the same `tools/run_frappe_reference_tests.sh` used for local Bench testing.

See `docs/FRAPPE_CI_PROOF.md`.

## What a green run proves

- `Appointment.validate` invokes the `acme_rules` `doc_events` hook.
- ALLOW leaves the Appointment valid.
- REQUIRE_APPROVAL sets approval fields.
- BLOCK raises a Frappe validation error.
- REQUIRE_APPROVAL fields persist on insert.
- BLOCK prevents insert.
- project-specific ALLOW does not clear a stricter shared requirement.

## Local Bench command

From the root of an existing Frappe Bench:

```bash
CAPABILITY_BASE=/absolute/path/to/composable_capability_base \
SITE=test.localhost \
bash "$CAPABILITY_BASE/tools/run_frappe_reference_tests.sh"
```

A confirmed green CI or local Bench run closes the remaining Frappe integration proof gate.
