# Remaining Proof Gates

Only two proof gates remain before the bootstrap is considered complete.

## Gate 1 — Real Frappe lifecycle

### Preferred: GitHub Actions

The repository contains:

```text
.github/workflows/frappe-integration.yml
```

Push the repository to GitHub with Actions enabled, then either change a relevant
capability file or manually run:

**Actions → Frappe integration → Run workflow**

Pass condition:

```text
appointment-lifecycle  ✓
```

The workflow creates a real Frappe version-15 Bench, MariaDB, Redis services,
a fresh site, installs the reference apps, enables tests, and executes the
`acme_rules` lifecycle suite.

### Alternative: existing Bench

From a Frappe Bench root:

```bash
CAPABILITY_BASE=/absolute/path/to/composable_capability_base \
SITE=test.localhost \
bash "$CAPABILITY_BASE/tools/run_frappe_reference_tests.sh"
```

Pass condition: `bench --site "$SITE" run-tests --app acme_rules` completes green.

After a confirmed green run, record the date/environment in
`docs/FRAPPE_TEST_STATUS.md` and check the two real-Frappe items in
`docs/DEFINITION_OF_DONE.md`.

## Gate 2 — Genuinely fresh coding agent

Use the separately packaged untouched fresh-agent sandbox and evaluator.

Give the fresh agent only the task contained in `ACCEPTANCE_PROMPT.txt`.
Do not give it the evaluator, answer key, this conversation, or an old agent thread.

Pass condition:

```text
ACCEPTANCE PASSED
```

plus human review confirming the implementation is minimal, understandable, and
really reuses the shared capability base rather than gaming the evaluator.

## Completion

When Gate 1 and Gate 2 are both green, mark the bootstrap complete. At that point,
do not keep adding framework machinery merely because it is possible. Start using
the system on real projects and let actual reuse pressure determine the next
capabilities and abstractions.
