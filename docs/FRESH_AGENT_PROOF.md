# Fresh-Agent Acceptance Proof

## Iteration 1 — FAIL (useful bootstrap evidence)

A clean acceptance sandbox was materialized into the disposable private GitHub repository `BrianMills2718/test` and the exact acceptance issue was assigned to GitHub Copilot's cloud coding agent. This was a separate coding-agent session with no access to the evaluator or this conversation.

- Issue: `#1` — `Fresh-agent acceptance: beta_reference`
- PR: `#2` — Copilot-created draft PR
- Frozen submission head for the first score: `34037d622518642bbb0ecb2f30cfa27d588b1947`
- Copilot's own checks: 19 tests passed; secret scan and CodeQL reported 0 alerts.

The external evaluator rejected the submission because it did **not record a reuse assessment / learning note**. Human review also identified that the implementation provided an email reminder adapter but did not wire an actual scheduled trigger.

No corrective hint was sent to the coding agent before scoring. Therefore this is a valid failure of the bootstrap's self-guidance, not a corrected run.

### Improvements made after iteration 1

1. Every completed project must now contain `clients/<project>/LEARNINGS.md` with either a reuse candidate/lesson or an explicit `No promotion candidate yet` assessment.
2. `tools/new_project.py` scaffolds that file.
3. `tools/validate_project.py` fails when the reuse assessment is missing/incomplete.
4. Agent/workflow instructions now state that scheduled requirements need a real trigger path; a callable transport/helper is not sufficient.
5. The external evaluator now requires visible automatic reminder triggering plus trigger/wiring tests.

A second genuinely fresh agent run is required after these changes.
## Iteration 2 — FAIL (test harness resilience gap)

A new clean GitHub Copilot cloud-agent session was launched from the strengthened base with the same plain task and no iteration-1 feedback.

- Issue: `#3`
- PR: `#4`
- Frozen submission head: `2cdc764c059e3714738a38608605ee7d4bd7beea`

Iteration 2 corrected both previous failures: it wrote `LEARNINGS.md` and registered a real Frappe `scheduler_events` cron trigger for reminders. The external evaluator then found a new integration failure: the agent created `tests/unit/test_beta_reference.py` and `tests/compatibility/test_beta_reference.py`, and pytest's default import mode treated them as the same top-level module during full-suite collection.

This exposed a repository test-harness weakness as well as a process weakness: the agent ran targeted validation but did not run the exact full `python tools/check_bootstrap.py` completion gate.

### Improvements made after iteration 2

1. `pytest.ini` now uses `--import-mode=importlib`, allowing modular test directories to safely reuse test basenames.
2. A compatibility regression test protects that setting.
3. Agent instructions now state that the exact full `python tools/check_bootstrap.py` command is mandatory before completion; targeted substitutes do not count.

A third genuinely fresh run is required.
## Iteration 3 — FAIL (nested app test discovery / clean import gap)

A third clean Copilot cloud-agent session ran from the importlib-mode baseline and followed the strengthened instructions, including its own repository bootstrap checks.

- Issue: `#5`
- PR: `#6`
- Frozen submission head: `9c3e61467e0c8129f1575d9fd7242e67cf2bc0cb`

The submission included a reuse assessment and an hourly Frappe scheduler trigger. The external clean evaluator still rejected it: its focused Beta app test could not import `na_notifications`. The agent's own repository-wide check had reported green because `check_bootstrap.py` only ran top-level test roots and did not automatically execute tests nested inside newly added Frappe apps. Its development shell could therefore mask missing import wiring.

Human inspection also showed the new Frappe app omitted the module-package marker implied by `modules.txt`, a layout defect that a wheel build alone does not detect.

### Improvements made after iteration 3

1. `check_bootstrap.py` now discovers every Frappe app dynamically.
2. It constructs a clean `PYTHONPATH` from those app roots instead of depending on the developer shell.
3. It discovers and runs nested `tests/` directories inside all Frappe apps in addition to top-level tests.
4. `check_frappe_packages.py` now validates every `modules.txt` entry has its expected Python module package marker before building.
5. The external evaluator uses the same clean dynamic import environment for focused tests.

A fourth genuinely fresh run is required.
## Iteration 4 — AUTOMATED PASS / HUMAN REVIEW FAIL (side-effect idempotency gap)

A fourth clean Copilot cloud-agent session ran from the nested-test/package-layout-hardened baseline.

- Issue: `#7`
- PR: `#8`
- Frozen submission head: `1e78cb78042d6a24d14f29261835d404eef11b77`
- External evaluator: `ACCEPTANCE PASSED`
- Clean local result with the submission applied: `26 passed, 1 skipped`

The submission correctly composed `core`, `scheduling`, `approvals`, and `notifications`; kept the >90-minute approval policy local; wrote `LEARNINGS.md`; registered a real Frappe scheduler; used the shared approval resolver and email transport; preserved shared runtime; and passed the automated acceptance evaluator.

Human review rejected it because the hourly reminder job queried all appointments in a 24-hour look-ahead window and sent an email on every run. The same appointment could therefore receive repeated reminders for many consecutive scheduler runs. A scheduler window is not a durable delivery guarantee.

### Improvements made after iteration 4

1. Agent instructions now require scheduled/retryable user-visible or external side effects to be idempotent.
2. The rule explicitly requires durable state/idempotency keys rather than relying on scheduler timing or query windows.
3. Project workflow now requires a repeat-execution test: run the same job twice for the same logical event and assert the side effect happens once.
4. The acceptance evaluator now checks for visible durable reminder deduplication and a duplicate-delivery/idempotency regression test.

A fifth genuinely fresh run is required.

