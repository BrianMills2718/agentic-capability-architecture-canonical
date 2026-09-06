# Automated Frappe Lifecycle Proof

## Purpose

The remaining framework-level proof is automated in:

```text
.github/workflows/frappe-integration.yml
```

It creates a real Frappe **version-15** Bench with MariaDB and Redis, creates a
fresh site, installs the reference apps, and runs the `acme_rules` integration
tests against a real `Appointment` document lifecycle.

## What the workflow proves

The integration suite verifies that:

- the `Appointment.validate` lifecycle invokes the ACME `doc_events` hook;
- `ALLOW` permits validation without adding an approval requirement;
- `REQUIRE_APPROVAL` writes the approval fields;
- `BLOCK` raises a Frappe validation error;
- a stricter shared approval requirement is not weakened by project-specific `ALLOW`;
- approval fields persist through a real `insert()`;
- `BLOCK` prevents the Appointment from being inserted.

## CI environment

The workflow intentionally follows the same basic setup pattern used by current
Frappe application CI:

- Ubuntu GitHub Actions runner;
- Frappe `version-15`;
- Python 3.11;
- Node 20;
- MariaDB 10.6;
- separate Redis cache and queue services;
- `bench init --skip-redis-config-generation --skip-assets`;
- a fresh test site;
- `allow_tests` enabled before `bench run-tests`.

The capability apps do not currently require frontend assets, so the workflow
skips asset building and focuses on the server/document lifecycle.

## Run it on GitHub

Put the capability base in a GitHub repository and enable Actions. The workflow
runs automatically when relevant capability/reference files change and can also
be started manually with **Actions → Frappe integration → Run workflow**.

A green `appointment-lifecycle` job closes the real-Frappe integration gate in
`DEFINITION_OF_DONE.md`.

## Local equivalent

If you already have a Frappe Bench, the same test suite can be run from the
Bench root:

```bash
CAPABILITY_BASE=/absolute/path/to/composable_capability_base \
SITE=test.localhost \
bash "$CAPABILITY_BASE/tools/run_frappe_reference_tests.sh"
```

The local runner and CI runner intentionally converge on the same script so the
proof does not depend on two separate installation procedures.
