## 2026-09-05 — Acceptance harness rehearsal

- Ran a disposable end-to-end rehearsal from the exact fresh-agent sandbox.
- Rehearsal Beta composition passed the external evaluator.
- Verified the pristine sandbox fails before implementation, providing a negative control.
- Recorded that this validates the harness only; independent fresh-agent proof remains open.
- Definition of Done now distinguishes authored Frappe tests from executed Frappe lifecycle proof.

## 2026-09-05 — Fresh-agent acceptance package

- Added a canonical fresh-agent prompt file.
- Acceptance sandbox now initializes a clean Git baseline and includes only the normal
  repository context plus the task prompt.
- Added byte-for-byte shared-runtime baselines for Scheduling, Approvals, and Notifications.
- Strengthened the evaluator to require actual shared approval/notification usage and
  visible reminder behavior.
- Added a copy-paste acceptance runbook for Codex CLI and other coding agents.

# Changelog

## 2026-09-05 — Reference implementation bootstrap

- Established the shared/config/custom architecture.
- Added agent operating rules and capability lifecycle guidance.
- Added reusable `approvals` capability with deterministic rule resolution.
- Added reusable Frappe `na_scheduling` app skeleton with an `Appointment` DocType.
- Added reusable Frappe `na_approvals` app skeleton.
- Added `acme_reference` as the first composed project.
- Added `acme_rules` as a project-specific Frappe extension without modifying Scheduling.
- Added pure tests for ALLOW, REQUIRE_APPROVAL, BLOCK, conflicts, ties, and monotonic ALLOW behavior.
- Added compatibility tests protecting registry use and preventing ACME leakage into Scheduling.
- Added Frappe integration tests for real `Appointment.validate` and `insert()` lifecycle behavior.
- Added a project-manifest validator and a bootstrap acceptance-test specification.

### Verified in the current environment

- Root pure/compatibility test suite passes.
- ACME project manifest validates against the capability registry.

### Not yet verified here

- Frappe integration tests require a real Bench/test site; Frappe is not installed in this runtime.
- Fresh-agent acceptance test has not yet been executed independently.

## 2026-09-05 — Acceptance harness and Notifications

- Added a minimal reusable `na_notifications` Frappe app with a stable email transport interface.
- Added pure tests for recipient normalization.
- Added a fresh-agent acceptance sandbox generator that hides the answer key.
- Added a structural acceptance evaluator and protected ACME baseline hashes.
- Formalized automated + human acceptance as the final fresh-agent proof.
- Made Frappe package checks auto-discover new capability/client apps instead of using a hard-coded list.
- Acceptance evaluation now explicitly executes beta-specific tests as well as the full bootstrap check.
- Acceptance evaluator distinguishes legitimate consumer/evidence metadata from forbidden project-specific shared runtime behavior.

## 2026-09-05 — Machine-readable reuse discipline

- Added JSON Schemas for the registry, capability manifests, project manifests, and reuse-candidate log.
- Added schema validation to the bootstrap check.
- Added evidence thresholds for `proven` and `core` capability promotion.
- Added `reuse_candidates.yml` plus a helper for recording reuse observations without premature abstraction.
- Added a project scaffolder that composes registered capabilities into a clean client/project layer.
- Registry validation now checks that registry entries and per-capability manifests remain synchronized.

## 2026-09-05 — Portable real-Frappe proof gate

- Added `.github/workflows/frappe-integration.yml` using a real Frappe version-15 Bench with MariaDB and Redis services.
- Updated the local Frappe runner to enable `allow_tests` before executing the integration suite.
- Added compatibility tests that protect the CI/runtime proof contract.
- Added `docs/FRAPPE_CI_PROOF.md` and `docs/NEXT_PROOF.md`.
- Reconciled `DEFINITION_OF_DONE.md` with demonstrated evidence instead of leaving completed items unchecked.
- Local evidence at this point: 17 tests pass, all schemas/registry/evidence checks pass, Python compiles, and all 4 Frappe app packages build.
