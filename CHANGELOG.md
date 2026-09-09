## 2026-09-09 — Capability selection requires net value

- Made semantic fit necessary but insufficient: selected capabilities must provide a concrete advantage over the smallest equally reliable local implementation after discovery and integration costs.
- Added capability-plan schema version 2 with a required `local_alternative` for every selected provider; frozen version-1 engagement workspaces remain self-contained.
- Added regression coverage proving missing comparison baselines fail validation and semantically fitting but uneconomic capabilities may be rejected in favor of a local gap.
- Recorded ADR-013 so capability count cannot substitute for lower marginal delivery effort or reliability.

## 2026-09-08 — Paid engagement operating MVP

- Added an isolated contractor/client engagement kit generator with a hashed read-only capability snapshot and portable self-validator.
- Added machine-readable engagement, capability-plan, evidence-proposal, and business-metrics contracts.
- Made selection/rejection, explicit composition, residual local gaps, client-work-product isolation, and sanitized evidence closeout part of the paid-work operating loop.
- Closeout emits proposal-only generalized evidence for human review and keeps client task text, client reference, client code, and financial metrics out of canonical evidence intake.
- Added five focused engagement-tool regression tests; the full local bootstrap remains green.

## 2026-09-08 — Final lineage-convergence cleanup

- Recorded `architecture/lineage_inventory.yml` with one active canonical capability-architecture repository and explicit preserved predecessor/proof dispositions.
- Added an always-on lightweight `Bootstrap checks` pull-request workflow so the repository completion gate can be required before merge.
- Protected `main` so pull requests, up-to-date branches, resolved conversations, and the GitHub Actions `bootstrap` check are required; admins are covered and force pushes/deletion are disabled.
- Preserved the seven-site Frappe workflow as the heavier integration proof rather than misconfiguring its push-only job as a required PR check.
- Superseded experimental and prior acceptance PRs were closed without merging transitional architecture back into the clean mainline.
- The genuinely isolated fresh-agent registry-discovery challenge remains the next active experiment under issue #23.

## 2026-09-05/06 — Fresh-agent iteration 4 exposed reminder idempotency gap

- Fresh Copilot acceptance iteration 4 passed the automated evaluator but failed human review.
- The hourly reminder implementation could resend the same appointment email on repeated scheduler runs.
- Added a general contract: scheduled/retryable external side effects must use durable idempotency state/keys.
- Added a regression requirement to execute the same scheduled job twice and prove the side effect occurs once.
- Strengthened the hidden acceptance evaluator to require visible reminder deduplication plus a duplicate-delivery test.

## 2026-09-05/06 — Fresh-agent iteration 3 exposed nested app test discovery gap

- Third independent fresh-agent run included reuse learning and a real scheduler trigger.
- External clean scoring failed because nested Beta app tests could not import `na_notifications`.
- Reworked `check_bootstrap.py` to discover all Frappe app roots, set clean dynamic import paths, and run nested app tests automatically.
- Strengthened `check_frappe_packages.py` to validate Frappe `modules.txt` package markers, not just wheel builds.
- Updated external focused-test scoring to use the same clean app import environment.
- Iteration 3 remains a recorded FAIL; iteration 4 is required.

## 2026-09-05/06 — Fresh-agent iteration 2 exposed modular pytest collision

- Second independent Copilot cloud-agent run fixed the reuse-assessment and scheduled-trigger gaps.
- External full-suite evaluation failed because unit and compatibility tests reused the basename `test_beta_reference.py` under pytest's default import mode.
- Switched the repository to `--import-mode=importlib` for modular test isolation.
- Added a regression test for the test-harness contract.
- Made the exact full `python tools/check_bootstrap.py` command a mandatory completion gate for agents.
- Iteration 2 remains a recorded FAIL; iteration 3 is required.

## 2026-09-05/06 — Fresh-agent iteration 1 exposed two bootstrap gaps

- Launched an independent GitHub Copilot cloud coding-agent session from a clean sandbox.
- Copilot reused shared capabilities and passed its own 19-test validation, but external acceptance failed because no reuse assessment was recorded.
- Human review also found that reminder transport existed without an automatic scheduler/trigger.
- Made `LEARNINGS.md` mandatory for every project and enforced it in `validate_project.py`.
- Strengthened agent rules and project workflow for scheduled/triggered behavior.
- Strengthened acceptance scoring to require reminder trigger/wiring.
- Iteration 1 remains a recorded FAIL; a new fresh-agent run is required.

## 2026-09-05/06 — Real Frappe lifecycle proof passed

- Used the disposable connected GitHub repository `BrianMills2718/test`.
- Ran the proof on branch `chatgpt/frappe-proof-20260905`.
- GitHub Actions run `34001408766` provisioned Frappe version-15, MariaDB, and Redis.
- Installed `na_scheduling`, `na_approvals`, and `acme_rules` into a fresh site.
- Real Frappe lifecycle suite completed successfully: `Ran 6 tests in 0.256s` / `OK`.
- Closed the real-Frappe integration and persistence proof gate.
- Only the genuinely fresh coding-agent acceptance gate remains.

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

## 2026-09-09 — Action-bound human approval

- Added candidate semantic actions `approval.action.bind` and
  `approval.action.verify`.
- Bound approval receipts to the exact operation key, action, target, and
  canonical JSON payload so changed work cannot execute under stale approval.
- Kept authentication, persistence, authorization, and execution outside the
  capability's claim boundary.

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
