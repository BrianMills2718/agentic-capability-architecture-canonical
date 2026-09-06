#!/usr/bin/env bash
set -euo pipefail
: "${CAPABILITY_BASE:?Set CAPABILITY_BASE to the composable_capability_base directory}"
: "${SITE:?Set SITE to the Frappe test site name}"
BENCH_ROOT="$(pwd)"
for app in na_scheduling na_approvals na_notifications acme_rules intake_booking; do rm -rf "$BENCH_ROOT/apps/$app"; done
ln -s "$CAPABILITY_BASE/capabilities/scheduling/frappe_app/na_scheduling" "$BENCH_ROOT/apps/na_scheduling"
ln -s "$CAPABILITY_BASE/capabilities/approvals/frappe_app/na_approvals" "$BENCH_ROOT/apps/na_approvals"
ln -s "$CAPABILITY_BASE/capabilities/notifications/frappe_app/na_notifications" "$BENCH_ROOT/apps/na_notifications"
ln -s "$CAPABILITY_BASE/clients/acme_reference/custom/frappe_app/acme_rules" "$BENCH_ROOT/apps/acme_rules"
ln -s "$CAPABILITY_BASE/clients/client_intake_booking/custom/frappe_app/intake_booking" "$BENCH_ROOT/apps/intake_booking"
"$BENCH_ROOT/env/bin/pip" install -e "$BENCH_ROOT/apps/na_scheduling" -e "$BENCH_ROOT/apps/na_approvals" -e "$BENCH_ROOT/apps/na_notifications" -e "$BENCH_ROOT/apps/acme_rules" -e "$BENCH_ROOT/apps/intake_booking"
for app in na_scheduling na_approvals na_notifications acme_rules intake_booking; do grep -qxF "$app" "$BENCH_ROOT/sites/apps.txt" || echo "$app" >> "$BENCH_ROOT/sites/apps.txt"; done
installed="$(bench --site "$SITE" list-apps)"
for app in na_scheduling na_approvals na_notifications acme_rules intake_booking; do if ! grep -qxF "$app" <<<"$installed"; then bench --site "$SITE" install-app "$app"; fi; done
bench --site "$SITE" set-config allow_tests true
bench --site "$SITE" run-tests --app acme_rules
bench --site "$SITE" run-tests --app intake_booking
