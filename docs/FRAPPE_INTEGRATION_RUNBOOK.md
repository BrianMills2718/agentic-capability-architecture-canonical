# Frappe Integration Runbook

> **Status: current local regression runbook.** This documents how to execute the repository's Frappe-facing regression suite from a real Bench. The executable source of truth for the app/site matrix is `tools/run_frappe_reference_tests.sh`; keep this page descriptive and avoid duplicating that matrix in prose.

The repository does not bundle Frappe itself. Capability and project Frappe apps are structured so the regression script can link/install them into a Bench environment and run each project on an isolated site.

## Current regression entry point

Run from the root of a real Frappe Bench with the capability repository available separately.

Set:

```bash
CAPABILITY_BASE=/absolute/path/to/agentic-capability-architecture-canonical
SITE_ACME=acme_test
SITE_INTAKE=intake_test
SITE_PROCUREMENT=procurement_test
SITE_ACCESS=access_test
SITE_MAINTENANCE=maintenance_test
SITE_SERVICE_DESK=service_desk_test
SITE_RESOURCE_RESERVATION=resource_reservation_test
```

Create those seven test sites in the Bench first, then run:

```bash
bash "$CAPABILITY_BASE/tools/run_frappe_reference_tests.sh"
```

The script is intentionally authoritative for:

- which shared/project apps are linked into the Bench;
- editable package installation;
- Bench `apps.txt` registration;
- per-site capability composition;
- guards against unrelated project extensions leaking across sites;
- enabling tests on each site;
- the app test commands executed for each composition.

If the script adds/removes a project composition, update this runbook only where its invocation contract changes; do not hand-copy the full installation matrix here.

## Why integration tests are separate

Pure capability kernels such as deterministic resolution and state-transition planning should remain testable without a Frappe site. Real-Bench tests verify the framework-specific contract that pure tests cannot establish:

- app installation/dependency wiring;
- DocType and hook lifecycle behavior;
- site/database isolation;
- persistence;
- permissions/runtime adapters;
- scheduler/framework integration where exercised;
- compatibility of known project compositions.

## Evidence discipline

The historical baseline proof is recorded in [`FRAPPE_TEST_STATUS.md`](FRAPPE_TEST_STATUS.md) and [`FRAPPE_CI_PROOF.md`](FRAPPE_CI_PROOF.md). It should not be interpreted as evergreen evidence for later revisions.

When a material Frappe-facing change is made, run the applicable current suite and add/update proof evidence rather than changing a historical result.

## CI note

The checked-in `.github/workflows/frappe-integration.yml` is a separate automation surface and must remain synchronized with the environment variables/sites required by `tools/run_frappe_reference_tests.sh`. If those two disagree, treat it as a CI configuration defect; the runbook must not imply the workflow is current merely because the file exists.
