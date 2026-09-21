# Audit addendum — independent-composition pilot (2026-09-21)

Plan: [ACA-PLAN-002](../../plans/2026-09-21-evidence-repair-cross-repo-reuse.md), stage A0 (evidence repair).
Audited baseline: canonical `main` at `0cfa0ef` (merge of PR #62), on branch `a0-evidence-repair-20260921`.
Audited scope: ACA-PLAN-001 P3/P5/P6 artifacts in this directory, their tests under `tests/unit/`, ADR-017, and the proof/navigation documents that cite them.

This addendum does **not** rewrite the pilot's history. `RESULTS.md`, `SECOND_CONSUMER.md`, `P6_DECISION.md`, and `PROTOCOL.md` remain what was written on 2026-09-19/20, with dated qualification notes added at the points listed in §5. Where a historical statement and this addendum disagree, use this addendum for *current* status and the historical file for *what was claimed and when*.

## 0. How each statement below was established

| Tag | Meaning |
| --- | --- |
| **[R]** | Read in the code/tests at the audited baseline. |
| **[C]** | Counted or searched (`wc`, `grep`, `find`, `sha256sum`) in the audited tree. |
| **[G]** | Read from git history. |
| **[X]** | Executed in A0 and the output was observed. See §6 for exactly which executions occurred. |
| **[S]** | Carried from ACA-PLAN-002 or the historical documents; **not** re-verified by A0. |

Reading code and seeing it "look right" is weaker than running it; tags are used so the two are not confused.

## 1. Verified facts

| # | Fact | Tag |
| --- | --- | --- |
| F1 | Frozen artifacts are byte-identical before and after A0's edits (sha256 taken at the audited baseline, re-taken after all A0 edits, and `git diff --stat` on `fixtures/` and `n8n/` empty). Full digests are in §6. | [C] |
| F2 | Static `def test_` counts: `test_p3_independent_composition.py` 25, `test_p3_twitterapi_io_collection.py` 6, `test_p3_live_pipeline.py` 10 (total **41**), `test_engineering_signal_digest.py` 22. | [C] |
| F3 | No pilot module or test references `approval.action.bind` / `approval.action.verify` or any `capabilities/approvals` code. The exports exist in `capabilities/approvals/capability.yml`, but the pilot never composes them. | [C] |
| F4 | `approval_gated_handoff` compares the decision string to `"shortlist"`. The handoff record carries only `candidate_id`, a derived `handoff_id`, and a status. Nothing binds the decision to an action, target, or payload. | [R] |
| F5 | `IdempotentLocalSink` is a per-instance in-memory `dict`. `compose_run` builds a new sink on every call. Nothing is persisted. A second record with the same `handoff_id` but different content is reported as a duplicate and the difference is discarded. | [R] |
| F6 | `semantic_reject` returns a rejection iff a pattern's `field` key is present in the data **and** the pattern has a truthy `risk`. The value and the pattern's `maps_to` are never read. A renamed field is not detected. | [R] |
| F7 | The `assertions` block in `compose_run` (`production_crm_write`, `outbound_message_sent`, `score_alone_authorizes_handoff`) is three literal `False` constants, not measurements. | [R] |
| F8 | In `engineering_signal_digest.adapt_candidates_to_signals` (pre-A0), `candidate.get(k, "").strip()` returns `None` for a key that is present with value `None`, so `.strip()` raised `AttributeError`, not `AdapterError`. A0 changes this to `AdapterError` (module edit + regression tests). | [R] pre-change behavior; the new behavior is asserted by tests (see §6 for whether they were executed) |
| F9 | No test in `test_engineering_signal_digest.py` imports `twitterapi_io_collection` or calls the real `search_candidates`. Every test injects `search_fn` or literal candidate lists. The CLI `main()` imports the boundary lazily from the script's own directory. | [C] |
| F10 | `search_candidates` silently `continue`s past non-object entries in the provider's `tweets` list. A consumer cannot observe that malformed items were dropped. | [R] |
| F11 | `engineering_signal_digest.py` was 149 lines at the baseline (before A0's edit), `test_engineering_signal_digest.py` 444, `SECOND_CONSUMER.md` 301. The `adapt_candidates_to_signals` function spans 43 lines (47–89). | [C] |
| F12 | Frozen `CASES.json` uses `review_threshold` 0.7 and `live_pipeline.py` defaults to 0.7 (function and CLI). The recorded live runs used 0.5 and then 0.65 as explicit overrides. No live run at 0.7 is recorded. | [R] [C] |
| F13 | `RESULTS.md` says the scorer's maximum is "~0.95" but the same file records a candidate scored 1.0. The code caps at 1.0 and the signal weights sum to 1.55. | [R] |
| F14 | The "Evidence JSON" block in `RESULTS.md` contains `score_range_observed` and `score_range_bounded`. `live_pipeline.py` emits neither key. The block is therefore an abridged/edited transcription, not a verbatim tool receipt. | [R] |
| F15 | A0 found no retained log, receipt, or captured output for the 2026-09-19 pipeline runs or 2026-09-20 digest run under `docs/experiments/independent-composition/`; those canonical experiment artifacts therefore retain prose only. A0 did not exhaustively search external machine/chat logs, so it does not claim the output never existed elsewhere. | [C] |
| F16 | `n8n/validate_fixture_baseline.py` checks required top-level keys, the exact node-name list, and invariants of `CASES.json`. It does not parse or execute the Code nodes. No retained record shows the workflow JSON was imported into an n8n instance. | [R] |
| F17 | Neither `search_candidates` nor `twitterapi_io_collection` is referenced by any capability manifest, the registry, or a client project. It is not a registered capability. | [C] |
| F18 | Commit `072565d` (the pinned revision cited by the P5 report) exists; the digest consumer was added later in `17bcdf8` in the same repository and directory. Nothing in code enforces that pin; the consumer resolves the boundary via its own directory. | [G] [R] |

## 2. Historical claims, and their current standing

"Standing" is one of: **Supported** (as scoped), **Qualified**, **Overstated**, **Unsupported**, **Stale**.

| Claim (source) | Standing | Reason |
| --- | --- | --- |
| P3 baseline: 5 frozen cases pass (`RESULTS.md`, `P6_DECISION.md`) | **Qualified** | The runners check fixture-derived expectations. Scoring in `normal-composition` reads `scoring_fixture`, not a scorer. The structural case checks output *keys* only; the semantic case passes on any rejection (F6). Reasonable as a fixture regression, weak as behavioral proof. |
| 41 tests (P6, PROTOCOL) vs 31 tests (`RESULTS.md`) | **Stale** (31) / **Supported** (41, F2) | 31 predates the live-pipeline tests. 41 = 25 + 6 + 10. |
| "Approval binding is programmatic" (`RESULTS.md`); "Safety (Approval): Programmatic binding (existing AES `approval.action` pattern)" (`P6_DECISION.md`) | **Unsupported** | The pilot uses a string gate (F4), not ADR-014 binding (F3). The claim that an existing AES pattern was used is false for this code. |
| "Idempotent side effects are real (tracked state)" (`RESULTS.md`); "Safety (Idempotency): Durable state tracking (existing pattern)" (`P6_DECISION.md`) | **Unsupported** | State is process-local and per-instance (F5). It does not survive a new process or a new `compose_run`. `P6_DECISION.md` elsewhere says "in-memory", so the document disagrees with itself. |
| Safety assertions ✓ (`RESULTS.md` live run) | **Overstated** | Hard-coded constants (F7). The live run also did not attempt any effect; absence of an effect is not evidence that a guard works. |
| Semantic rejection "enforced" (`RESULTS.md`) | **Qualified** | Field-presence trigger only (F6). |
| Second consumer "meets all six conformance checks"; "tests verify all six" (`SECOND_CONSUMER.md`); "All six conformance checks passed" (`P6_DECISION.md`) | **Unsupported** | No test invokes the real boundary (F9) or checks a pinned version. There is no example artifact for check 5 beyond the consumer's own fixtures, and the semantic-mismatch and side-effect checks are trivially satisfied by a read-only boundary. Checks 1–6 were never mapped to concrete assertions. |
| Adapter "raises `AdapterError` if any required field is missing, null, or whitespace-only" (`SECOND_CONSUMER.md`) | **Overstated** at the time; **now true** | Explicit `None` raised `AttributeError` (F8). Fixed and regression-tested in A0. |
| "Resilient to null/missing author object (raises `ProviderAccessError`)" (`SECOND_CONSUMER.md`) | **Supported** for a missing/non-object `author`; **Qualified** otherwise | `normalize_tweet` does reject a non-dict author. Non-object *tweets* are silently skipped (F10). |
| Live second-consumer run: "observability", 20 items, 14 authors (`SECOND_CONSUMER.md`) | **Qualified** | A one-off CLI run recorded in prose, with no retained machine receipt (F15). It is a real observation by the operator but not reproducible from the repository. The report's line "deduplication tested by boundary returning duplicates" refers to unit tests on injected lists, not to duplicates observed live. |
| "`engineering_signal_digest.py`, 135 lines" (`SECOND_CONSUMER.md`) | **Stale**; correct is 149 (F11) | The same file's table already says 149. |
| Two "materially different consumers" and "eligible for `proven` review" (`SECOND_CONSUMER.md`, `P6_DECISION.md`) | **Overstated** | Both consumers, the boundary, and the fixtures share one repository, one directory, one language, and one provider. The second consumer's brief names the boundary; no discovery or rejection was exercised. The only behavior both consumers use is one read-only call plus field access. AGENTS.md requires the *generalized* behavior to be exercised by materially different projects; a single GET wrapper exercises no distinctive invariant. |
| "Pinned at `072565d`" (`SECOND_CONSUMER.md`) | **Qualified** | The commit exists (F18) but no dependency pin is used. Same-directory import is not version pinning. |
| "n8n was evaluated; Python was sufficient and simpler" (`P6_DECISION.md`) | **Overstated** | A static fixture was built and structurally validated (F16). Live n8n orchestration was not completed and n8n was not evaluated as a product. The reported "overhead" was not measured. `PROTOCOL.md` already says the pivot is not evidence against n8n; P6 should be read that way. |
| "Importable n8n fixture workflow" (`RESULTS.md`) | **Unsupported** | Import into n8n was not retained/verified (F16). Say "structurally validated fixture". |
| Threshold "repair" 0.5 → 0.65 (`RESULTS.md`) | **Qualified** | The frozen threshold was 0.7 (F12); the repair moved to a third value, tuned on the same 20 live results it was judged against, with no human judgment of the resulting queue. Configuration-only is accurate; "successful" is not established. |
| "Evidence JSON" as the live receipt (`RESULTS.md`) | **Overstated** | Not verbatim (F14). |
| "Not yet claimed: … second-consumer reuse has occurred" (`RESULTS.md`) | **Stale** | The P5 second consumer ran on 2026-09-20. |
| "Next genuine gate: explicit human review decision" (`RESULTS.md`); P6 "P0–P6 complete" (ACA-PLAN-001 header) | **Qualified** | P6 completed a *decision*. The product slice (human review, real handoff, LLM scoring, live n8n) was never completed. |
| ADR-017 "two materially different consumers … using ordinary Python functions … proved sufficient" | **Qualified** | See §3 and the ADR-017 dated amendment. |
| "No ACA machinery required in the observed runs" (ADR-017, P6) | **Supported for the exercised path** | Also true that nothing effectful, cross-repo, or economic was exercised. |

## 3. Current qualifications — what may now be said

**May be said, as scoped:**

- A small read-only Python wrapper (`search_candidates`) was called by two different downstream modules in the same repository, and the second (a digest) needed no change to the wrapper. That is real, cheap, ordinary reuse.
- The pilot needed no registry, semantic layer, workflow engine, or connector platform *for that read-only, same-repo, same-language path*.
- Ordinary interfaces, documentation, and tests remain the default posture (ADR-007, ADR-013, ADR-017 as amended).
- A recorded live collection from TwitterAPI.io succeeded twice on 2026-09-19 and once through the digest on 2026-09-20, per prose records, with no external effects reported.

**May not be said on this evidence:**

- That approval binding (ADR-014) or durable idempotency was composed, tested, or shown sufficient. Neither was exercised (F3, F4, F5). The local-sink test is a process-local fixture.
- That the semantic-mismatch check is a semantic compatibility checker (F6).
- That all six profile checks were run against the boundary, or that a version pin was used (F9, F18).
- That the boundary generalizes across repositories, languages, or effectful actions, or that delivery is cheaper with it. No control arm, cost, time, or package/version-drift measurement exists.
- That discovery/selection worked. The consumer was told the boundary.
- That `search_candidates` is `proven` or even a mature `candidate`. It is currently an `observed` reuse result (see `reuse_candidates.yml`), because the later caller exercised only a trivial read-only subset in the same repository/domain family.
- That n8n is unsuitable or was evaluated.
- That the Twitter Prospector product was completed (no human review event, LLM scorer, or real handoff).

## 4. Remaining unknowns

1. Whether the pre-existing Product N `TwitterApiIoClient` (recorded in ACA-PLAN-002 §2 [S]) can be consumed from another repository, and at what publication cost. Not examined by A0.
2. Delivery economics: time, tokens, dollars, and human intervention for a control versus a reuse arm. Never measured; unknown is not zero.
3. Whether a fresh worker discovers and correctly selects or rejects the boundary without being told.
4. Behavior under provider or boundary version change (no packaging or version-drift evidence).
5. Exact-action approval binding and durable idempotency under retry, restart, and concurrency. That is ACA-PLAN-002 stage A5, deferred.
6. Whether the digest and the pipeline would still pass with a real (not injected) boundary call under the tests. The only such evidence is the un-retained CLI run.
7. Original raw output of the 2026-09-19/20 live runs. Not recoverable from this repository; do not reconstruct.
8. Whether builders A/B/C were independent in the sense of PROTOCOL. The repository has one P5 session ID and commit identities, not builder independence records.

## 5. Changes made in A0

- This addendum (new).
- ADR-017: dated amendment; ADR-011/013/014/015 retained unchanged.
- `P6_DECISION.md`, `RESULTS.md`, `SECOND_CONSUMER.md`, `PROTOCOL.md`: dated qualification notes and inline corrections of stale counts; original text preserved.
- ACA-PLAN-001 header: historical/bounded status, pointer to ACA-PLAN-002.
- `docs/README.md`, `docs/NEXT_PROOF.md`, `docs/PROOF_LEDGER_EXTENDED.md`: navigation/status reconciled.
- `reuse_candidates.yml`: `search_candidates` wrapper recorded as an `observed` reuse observation with limitations. Not registered, not promoted.
- `engineering_signal_digest.py`: explicit `None`/non-string required fields raise `AdapterError`.
- `tests/unit/test_a0_independent_composition_limits.py` (new): regression for the above and characterization tests for F5, F6, F10, and the payload-unbound approval gate. These pin limitations; they are not production-safety tests.

Not changed: `fixtures/CASES.json`, `fixtures/EVALUATION.json`, `n8n/*`, all other Python modules, and existing tests.

## 6. Verification performed in A0

The editing worker session could execute only read-only shell commands, so it correctly reported its own Python/test/commit checks as unavailable. After that session completed, the coordinator reconnected through the authorized Remote MCP path and ran the required verification against the same working tree. The table below is the final A0 verification record; the worker's earlier inability to run commands remains part of the session history, not the final project status.

| Check | Result |
| --- | --- |
| Frozen-artifact sha256, before and after A0 edits | **PASS; unchanged.** `fixtures/CASES.json` `3643f3a93f2c59406c31b13dd05588444bdae2e054e58f23192870c3b7dfd7b6`; `fixtures/EVALUATION.json` `aba3d75231383ef4e047b700e73363becbcc0e25093ba7c9e11ef80a293cddf3`; `n8n/twitter-prospector-fixture-baseline.json` `170e4d40e3fde00a1def222c44a790f44a0b7c0baab7ae35f7ec6bbbc51ebf2e`; `n8n/validate_fixture_baseline.py` `cb769b276e449a425e41b9b168a41d611ace3967c3347d899a89341ff58d7b43`. |
| Focused A0/P3/P5 tests | **PASS: 83 tests.** Collected counts: A0 limits 20, P3 composition 25, provider adapter 6, live pipeline 10, Engineering Signal Digest 22. |
| Frozen n8n validator | **PASS:** `fixture workflow structure and frozen evaluator invariants: PASS`. This remains a static fixture check, not live n8n execution. |
| `git diff --check` | **PASS.** |
| Full completion gate | **PASS** using `/tmp/aca-bootstrap-venv/bin/python tools/check_bootstrap.py`: documentation/schema/registry/catalog/project/package checks passed; 11 Frappe packages built; repository pytest result **175 passed, 35 skipped**; `LOCAL BOOTSTRAP CHECKS PASSED`. |
| Isolated interpreter | `/tmp/aca-bootstrap-venv/bin/python` (Python 3.12 environment created with system site packages and `wheel`). |
| A0 effort/cost | Active editing/review time and subscription usage were not systematically metered in A0. No experiment-specific live provider call was made during A0. Cash/model cost is therefore **unobserved**, not zero; ACA-PLAN-002 requires prospective measurement for the scored comparison. |
| Commits | Code/characterization-test checkpoint: `37ee6b0` (`test: make independent-composition limits explicit`). Evidence/navigation amendments are committed separately in the same A0 PR so code characterization and claim repair remain reviewable independently. |

F2's static counts were independently confirmed by pytest collection for the focused suites. F8's repaired explicit-`None` behavior is covered by the new A0 regression suite, which passed. The characterization tests also passed and should be read as executable documentation of limitations, not as claims of production effect safety.
