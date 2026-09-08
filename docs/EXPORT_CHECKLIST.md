# Export and Handoff Checklist

Use this checklist before treating an exported ZIP or repository snapshot as a current handoff.

## Navigation and authority

- [ ] `README.md` describes the repository's local role and routes global navigation through `BrianMills2718/vision/wiki/index.md`.
- [ ] `docs/README.md` classifies current, operational, experimental, and historical local documentation.
- [ ] `AGENTS.md` contains the current coding-agent sourcing/reuse rules.
- [ ] `docs/ARCHITECTURE_CHARTER.md` and `docs/DECISIONS.md` reflect current local architecture decisions.
- [ ] `docs/PROOF_LEDGER_EXTENDED.md` reflects the current completed/pending proof claims.
- [ ] Historical proof/session documents are clearly labeled and do not present old pending work as current status.

## Machine-readable state

- [ ] Capability manifests and `capability_registry.yml` are synchronized by the repository validators.
- [ ] Shared public interfaces, dependencies, versions, and evidence metadata are current.
- [ ] Every real project has a manifest and `LEARNINGS.md` reuse/sourcing assessment.
- [ ] `reuse_candidates.yml` contains any unpromoted reuse observations that should survive the handoff.

Do not repair disagreement by copying one status into README prose. Resolve the machine-readable inconsistency or record it explicitly as known debt.

## Implementation and tests

- [ ] Project-specific code remains under the relevant project/client directory.
- [ ] No new shared implementation duplicates an adequate native/platform, ecosystem, external, standards-based, or existing internal capability without a documented reason.
- [ ] Local repository checks pass with `python tools/check_bootstrap.py`.
- [ ] If the handoff changes Frappe lifecycle/runtime behavior, the applicable real-site regression suite has been run and the result recorded in the proof ledger/status documentation.
- [ ] External/retryable side effects have appropriate durable idempotency/reliability tests.

The original bootstrap Frappe and fresh-agent acceptance gates have already passed; they do **not** need to be rerun for every export. New research proofs should be run only when the claim under test requires them.

## Export

- [ ] `CHANGELOG.md` records material repository changes where appropriate.
- [ ] `python tools/export_zip.py` has been run after the final changes when a ZIP handoff is required.
- [ ] The exported artifact is treated as a snapshot of the authoritative repository state, not a competing long-lived source of truth.
