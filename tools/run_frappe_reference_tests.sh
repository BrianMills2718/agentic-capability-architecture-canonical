#!/usr/bin/env bash
set -euo pipefail
: "${CAPABILITY_BASE:?Set CAPABILITY_BASE to the composable_capability_base directory}"
: "${SITE_ACME:?Set SITE_ACME to the ACME Frappe test site name}"
: "${SITE_INTAKE:?Set SITE_INTAKE to the client-intake Frappe test site name}"
BENCH_ROOT="$(pwd)"
for app in na_scheduling na_approvals na_notifications acme_rules intake_booking; do rm -rf "$BENCH_ROOT/apps/$app"; done
ln -s "$CAPABILITY_BASE/capabilities/scheduling/frappe_app/na_scheduling" "$BENCH_ROOT/apps/na_scheduling"
ln -s "$CAPABILITY_BASE/capabilities/approvals/frappe_app/na_approvals" "$BENCH_ROOT/apps/na_approvals"
ln -s "$CAPABILITY_BASE/capabilities/notifications/frappe_app/na_notifications" "$BENCH_ROOT/apps/na_notifications"
ln -s "$CAPABILITY_BASE/clients/acme_reference/custom/frappe_app/acme_rules" "$BENCH_ROOT/apps/acme_rules"
ln -s "$CAPABILITY_BASE/clients/client_intake_booking/custom/frappe_app/intake_booking" "$BENCH_ROOT/apps/intake_booking"
"$BENCH_ROOT/env/bin/pip" install -e "$BENCH_ROOT/apps/na_scheduling" -e "$BENCH_ROOT/apps/na_approvals" -e "$BENCH_ROOT/apps/na_notifications" -e "$BENCH_ROOT/apps/acme_rules" -e "$BENCH_ROOT/apps/intake_booking"
for app in na_scheduling na_approvals na_notifications acme_rules intake_booking; do grep -qxF "$app" "$BENCH_ROOT/sites/apps.txt" || echo "$app" >> "$BENCH_ROOT/sites/apps.txt"; done
install_if_missing() { local site="$1"; local app="$2"; if ! bench --site "$site" list-apps | grep -qxF "$app"; then bench --site "$site" install-app "$app"; fi; }
for app in na_scheduling na_approvals acme_rules; do install_if_missing "$SITE_ACME" "$app"; done
for app in na_scheduling na_approvals na_notifications intake_booking; do install_if_missing "$SITE_INTAKE" "$app"; done
if bench --site "$SITE_ACME" list-apps | grep -qxF intake_booking; then echo "intake_booking must not be installed on the ACME site" >&2; exit 3; fi
if bench --site "$SITE_INTAKE" list-apps | grep -qxF acme_rules; then echo "acme_rules must not be installed on the intake site" >&2; exit 3; fi
bench --site "$SITE_ACME" set-config allow_tests true
bench --site "$SITE_INTAKE" set-config allow_tests true
bench --site "$SITE_ACME" run-tests --app acme_rules
bench --site "$SITE_INTAKE" run-tests --app intake_booking
