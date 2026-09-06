# Frappe Integration Runbook

The local repository does not bundle Frappe itself. The Frappe-facing folders are
structured as apps so they can be copied or linked into a Bench environment.

## Apps

- `capabilities/scheduling/frappe_app/na_scheduling`
- `capabilities/approvals/frappe_app/na_approvals`
- `clients/acme_reference/custom/frappe_app/acme_rules`

## Intended Bench flow

From a Frappe Bench, make these apps available under `apps/` (for example using
Git repositories, editable installs, or development symlinks), then install them
on the test site in dependency order:

```bash
bench --site <test-site> install-app na_scheduling
bench --site <test-site> install-app na_approvals
bench --site <test-site> install-app acme_rules
```

Then run the integration suite:

```bash
bench --site <test-site> run-tests --app acme_rules
```

The `acme_rules` app declares `required_apps = ["na_scheduling", "na_approvals"]`.

## Why integration tests are separate

The pure resolver deliberately has no Frappe dependency. This gives fast tests
for composition semantics while the Frappe tests verify the actual framework
hook/document lifecycle separately.
