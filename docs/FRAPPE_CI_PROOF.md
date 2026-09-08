# Automated Frappe Lifecycle Proof

> **Status: baseline proof record.** The original real-Frappe lifecycle gate has passed; GitHub Actions run `34001408766` completed the baseline proof with 6 tests OK. Current proof status is indexed in [`PROOF_LEDGER_EXTENDED.md`](PROOF_LEDGER_EXTENDED.md), and the recorded environment/result is summarized in [`FRAPPE_TEST_STATUS.md`](FRAPPE_TEST_STATUS.md).

## Purpose

The repository contains a Frappe integration workflow at:

```text
.github/workflows/frappe-integration.yml
```

The original baseline form created a real Frappe **version-15** Bench with MariaDB and Redis, created a fresh site, installed the reference apps, and ran the `acme_rules` integration tests against a real `Appointment` document lifecycle.

The repository's regression surface has since expanded beyond that original three-app/single-site proof. Use [`FRAPPE_INTEGRATION_RUNBOOK.md`](FRAPPE_INTEGRATION_RUNBOOK.md) and `tools/run_frappe_reference_tests.sh` for the current local multi-site regression contract rather than inferring it from this historical proof narrative.

## What the baseline workflow proved

The integration suite verified that:

- the `Appointment.validate` lifecycle invokes the ACME `doc_events` hook;
- `ALLOW` permits validation without adding an approval requirement;
- `REQUIRE_APPROVAL` writes the approval fields;
- `BLOCK` raises a Frappe validation error;
- a stricter shared approval requirement is not weakened by project-specific `ALLOW`;
- approval fields persist through a real `insert()`;
- `BLOCK` prevents the Appointment from being inserted.

## Baseline CI environment

The successful proof used:

- Ubuntu GitHub Actions runner;
- Frappe `version-15`;
- Python 3.11;
- Node 20;
- MariaDB 10.6;
- separate Redis cache and queue services;
- `bench init --skip-redis-config-generation --skip-assets`;
- a fresh test site;
- `allow_tests` enabled before `bench run-tests`.

The capability apps did not require frontend assets for this proof, so the workflow skipped asset building and focused on the server/document lifecycle.

## Current interpretation

A green baseline lifecycle proof closes the claim that the reference hook/persistence path worked in a real Frappe environment at the recorded revision. It does not prove that every later project or every future revision is green.

When current Frappe-facing code changes, run the applicable current regression suite and record new evidence rather than treating the historical run ID as evergreen certification.

## Local regression entry point

The current repository script is:

```text
tools/run_frappe_reference_tests.sh
```

It defines the authoritative current app/site regression matrix for local Bench execution. See [`FRAPPE_INTEGRATION_RUNBOOK.md`](FRAPPE_INTEGRATION_RUNBOOK.md) for invocation and scope.
