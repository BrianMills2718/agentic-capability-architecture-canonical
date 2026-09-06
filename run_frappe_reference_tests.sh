#!/usr/bin/env bash
set -euo pipefail

# Run this from inside a real Frappe Bench.
# Usage:
#   CAPABILITY_BASE=/path/to/composable_capability_base \
#   SITE=test.localhost \
#   bash /path/to/composable_capability_base/tools/run_frappe_reference_tests.sh

: "${CAPABILITY_BASE:?Set CAPABILITY_BASE to the composable_capability_base directory}"
: "${SITE:?Set SITE to the Frappe test site name}"

BENCH_ROOT="$(pwd)"

if [[ ! -d "$BENCH_ROOT/apps" || ! -x "$BENCH_ROOT/env/bin/pip" ]]; then
  echo "Run this script from the root of a Frappe Bench." >&2
  exit 2
fi

for app in na_scheduling na_approvals acme_rules; do
  rm -rf "$BENCH_ROOT/apps/$app"
done

ln -s "$CAPABILITY_BASE/capabilities/scheduling/frappe_app/na_scheduling" "$BENCH_ROOT/apps/na_scheduling"
ln -s "$CAPABILITY_BASE/capabilities/approvals/frappe_app/na_approvals" "$BENCH_ROOT/apps/na_approvals"
ln -s "$CAPABILITY_BASE/clients/acme_reference/custom/frappe_app/acme_rules" "$BENCH_ROOT/apps/acme_rules"

"$BENCH_ROOT/env/bin/pip" install -e "$BENCH_ROOT/apps/na_scheduling" -e "$BENCH_ROOT/apps/na_approvals" -e "$BENCH_ROOT/apps/acme_rules"

apps_file="$BENCH_ROOT/sites/apps.txt"
touch "$apps_file"

# Bench can create apps.txt without a trailing newline. Normalize it before
# appending, otherwise `frappe` + `na_scheduling` becomes `frappena_scheduling`.
apps_tmp="$(mktemp)"
awk 'NF { print }' "$apps_file" > "$apps_tmp"
mv "$apps_tmp" "$apps_file"

for app in na_scheduling na_approvals acme_rules; do
  grep -qxF "$app" "$apps_file" || printf '%s\n' "$app" >> "$apps_file"
done

# install-app is idempotent only at the human workflow level, so check list-apps first.
installed="$(bench --site "$SITE" list-apps)"
for app in na_scheduling na_approvals acme_rules; do
  if ! grep -qxF "$app" <<<"$installed"; then
    bench --site "$SITE" install-app "$app"
  fi
done

bench --site "$SITE" set-config allow_tests true
bench --site "$SITE" run-tests --app acme_rules
