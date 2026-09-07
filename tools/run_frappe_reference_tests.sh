#!/usr/bin/env bash
set -euo pipefail

# Run from the root of a real Frappe Bench after creating separate test sites.
# Required environment:
#   CAPABILITY_BASE=/path/to/composable_capability_base
#   SITE_ACME=acme_test
#   SITE_INTAKE=intake_test
#   SITE_PROCUREMENT=procurement_test
#   SITE_ACCESS=access_test
#   SITE_MAINTENANCE=maintenance_test
#   SITE_SERVICE_DESK=service_desk_test
#   SITE_RESOURCE_RESERVATION=resource_reservation_test

: "${CAPABILITY_BASE:?Set CAPABILITY_BASE to the composable_capability_base directory}"
: "${SITE_ACME:?Set SITE_ACME to the ACME Frappe test site name}"
: "${SITE_INTAKE:?Set SITE_INTAKE to the client-intake Frappe test site name}"
: "${SITE_PROCUREMENT:?Set SITE_PROCUREMENT to the internal-procurement Frappe test site name}"
: "${SITE_ACCESS:?Set SITE_ACCESS to the IT-access Frappe test site name}"
: "${SITE_MAINTENANCE:?Set SITE_MAINTENANCE to the facility-maintenance Frappe test site name}"
: "${SITE_SERVICE_DESK:?Set SITE_SERVICE_DESK to the service-desk Frappe test site name}"
: "${SITE_RESOURCE_RESERVATION:?Set SITE_RESOURCE_RESERVATION to the resource-reservation Frappe test site name}"

BENCH_ROOT="$(pwd)"
source "$CAPABILITY_BASE/tools/lib/bench_apps_registry.sh"

if [[ ! -d "$BENCH_ROOT/apps" || ! -x "$BENCH_ROOT/env/bin/pip" ]]; then
  echo "Run this script from the root of a Frappe Bench." >&2
  exit 2
fi

for app in na_core na_scheduling na_approvals na_notifications acme_rules intake_booking procurement_requests access_requests maintenance_requests service_desk_requests resource_reservations; do
  rm -rf "$BENCH_ROOT/apps/$app"
done

ln -s "$CAPABILITY_BASE/capabilities/core/frappe_app/na_core" "$BENCH_ROOT/apps/na_core"
ln -s "$CAPABILITY_BASE/capabilities/scheduling/frappe_app/na_scheduling" "$BENCH_ROOT/apps/na_scheduling"
ln -s "$CAPABILITY_BASE/capabilities/approvals/frappe_app/na_approvals" "$BENCH_ROOT/apps/na_approvals"
ln -s "$CAPABILITY_BASE/capabilities/notifications/frappe_app/na_notifications" "$BENCH_ROOT/apps/na_notifications"
ln -s "$CAPABILITY_BASE/clients/acme_reference/custom/frappe_app/acme_rules" "$BENCH_ROOT/apps/acme_rules"
ln -s "$CAPABILITY_BASE/clients/client_intake_booking/custom/frappe_app/intake_booking" "$BENCH_ROOT/apps/intake_booking"
ln -s "$CAPABILITY_BASE/clients/internal_procurement/custom/frappe_app/procurement_requests" "$BENCH_ROOT/apps/procurement_requests"
ln -s "$CAPABILITY_BASE/clients/it_access_control/custom/frappe_app/access_requests" "$BENCH_ROOT/apps/access_requests"
ln -s "$CAPABILITY_BASE/clients/facility_maintenance/custom/frappe_app/maintenance_requests" "$BENCH_ROOT/apps/maintenance_requests"
ln -s "$CAPABILITY_BASE/clients/service_desk/custom/frappe_app/service_desk_requests" "$BENCH_ROOT/apps/service_desk_requests"
ln -s "$CAPABILITY_BASE/clients/resource_reservation/custom/frappe_app/resource_reservations" "$BENCH_ROOT/apps/resource_reservations"

"$BENCH_ROOT/env/bin/pip" install \
  -e "$BENCH_ROOT/apps/na_core" \
  -e "$BENCH_ROOT/apps/na_scheduling" \
  -e "$BENCH_ROOT/apps/na_approvals" \
  -e "$BENCH_ROOT/apps/na_notifications" \
  -e "$BENCH_ROOT/apps/acme_rules" \
  -e "$BENCH_ROOT/apps/intake_booking" \
  -e "$BENCH_ROOT/apps/procurement_requests" \
  -e "$BENCH_ROOT/apps/access_requests" \
  -e "$BENCH_ROOT/apps/maintenance_requests" \
  -e "$BENCH_ROOT/apps/service_desk_requests" \
  -e "$BENCH_ROOT/apps/resource_reservations"

# apps.txt is a Bench-level import registry, not a per-site installation list.
# Keep each name on its own line even if Bench left the existing file without
# a trailing newline.
for app in na_core na_scheduling na_approvals na_notifications acme_rules intake_booking procurement_requests access_requests maintenance_requests service_desk_requests resource_reservations; do
  ensure_bench_apps_entry "$BENCH_ROOT/sites/apps.txt" "$app"
done

install_if_missing() {
  local site="$1"
  local app="$2"
  if ! bench --site "$site" list-apps | grep -qxF "$app"; then
    bench --site "$site" install-app "$app"
  fi
}

# ACME site: only shared dependencies + ACME's local extension.
for app in na_core na_scheduling na_approvals acme_rules; do
  install_if_missing "$SITE_ACME" "$app"
done

# Intake site: only the capabilities and local extension used by this project.
for app in na_core na_scheduling na_approvals na_notifications intake_booking; do
  install_if_missing "$SITE_INTAKE" "$app"
done


# Procurement site: shared approvals/notifications + procurement's local extension.
for app in na_core na_approvals na_notifications procurement_requests; do
  install_if_missing "$SITE_PROCUREMENT" "$app"
done

# Access-control site: approvals + notifications + access-specific extension.
for app in na_core na_approvals na_notifications access_requests; do
  install_if_missing "$SITE_ACCESS" "$app"
done


# Maintenance site: Notifications + maintenance-specific extension only.
for app in na_core na_notifications maintenance_requests; do
  install_if_missing "$SITE_MAINTENANCE" "$app"
done


# Service Desk site: core + Notifications + project extension only.
for app in na_core na_notifications service_desk_requests; do
  install_if_missing "$SITE_SERVICE_DESK" "$app"
done


# Resource Reservation site: Core + Scheduling + Notifications + local extension.
for app in na_core na_scheduling na_notifications resource_reservations; do
  install_if_missing "$SITE_RESOURCE_RESERVATION" "$app"
done

# Guard against accidental cross-client extension installation.
if bench --site "$SITE_ACME" list-apps | grep -qxF intake_booking; then
  echo "intake_booking must not be installed on the ACME site" >&2
  exit 3
fi
if bench --site "$SITE_INTAKE" list-apps | grep -qxF acme_rules; then
  echo "acme_rules must not be installed on the intake site" >&2
  exit 3
fi
if bench --site "$SITE_ACME" list-apps | grep -qxF procurement_requests; then
  echo "procurement_requests must not be installed on the ACME site" >&2
  exit 3
fi
if bench --site "$SITE_INTAKE" list-apps | grep -qxF procurement_requests; then
  echo "procurement_requests must not be installed on the intake site" >&2
  exit 3
fi
if bench --site "$SITE_PROCUREMENT" list-apps | grep -Eq '^(acme_rules|intake_booking)$'; then
  echo "unrelated client extension must not be installed on the procurement site" >&2
  exit 3
fi

if bench --site "$SITE_PROCUREMENT" list-apps | grep -qxF na_scheduling; then
  echo "na_scheduling must not be installed on the procurement site" >&2
  exit 3
fi

if bench --site "$SITE_ACME" list-apps | grep -qxF access_requests; then
  echo "access_requests must not be installed on the ACME site" >&2
  exit 3
fi
if bench --site "$SITE_INTAKE" list-apps | grep -qxF access_requests; then
  echo "access_requests must not be installed on the intake site" >&2
  exit 3
fi
if bench --site "$SITE_PROCUREMENT" list-apps | grep -qxF access_requests; then
  echo "access_requests must not be installed on the procurement site" >&2
  exit 3
fi
if bench --site "$SITE_ACCESS" list-apps | grep -Eq '^(acme_rules|intake_booking|procurement_requests)$'; then
  echo "unrelated client extension must not be installed on the access site" >&2
  exit 3
fi
if bench --site "$SITE_ACCESS" list-apps | grep -qxF na_scheduling; then
  echo "na_scheduling must not be installed on the access site" >&2
  exit 3
fi


if bench --site "$SITE_MAINTENANCE" list-apps | grep -Eq '^(acme_rules|intake_booking|procurement_requests|access_requests)$'; then
  echo "unrelated client extension must not be installed on the maintenance site" >&2
  exit 3
fi
if bench --site "$SITE_MAINTENANCE" list-apps | grep -Eq '^(na_scheduling|na_approvals)$'; then
  echo "approvals and scheduling must not be installed on the maintenance site" >&2
  exit 3
fi


if bench --site "$SITE_SERVICE_DESK" list-apps | grep -Eq '^(acme_rules|intake_booking|procurement_requests|access_requests|maintenance_requests)$'; then
  echo "unrelated client extension must not be installed on the service desk site" >&2
  exit 3
fi
if bench --site "$SITE_SERVICE_DESK" list-apps | grep -Eq '^(na_scheduling|na_approvals)$'; then
  echo "approvals and scheduling must not be installed on the service desk site" >&2
  exit 3
fi


if bench --site "$SITE_RESOURCE_RESERVATION" list-apps | grep -Eq '^(acme_rules|intake_booking|procurement_requests|access_requests|maintenance_requests|service_desk_requests)$'; then
  echo "unrelated client extension must not be installed on the resource reservation site" >&2
  exit 3
fi
if bench --site "$SITE_RESOURCE_RESERVATION" list-apps | grep -qxF na_approvals; then
  echo "approvals must not be installed on the resource reservation site" >&2
  exit 3
fi

bench --site "$SITE_ACME" set-config allow_tests true
bench --site "$SITE_INTAKE" set-config allow_tests true
bench --site "$SITE_PROCUREMENT" set-config allow_tests true
bench --site "$SITE_ACCESS" set-config allow_tests true
bench --site "$SITE_MAINTENANCE" set-config allow_tests true
bench --site "$SITE_SERVICE_DESK" set-config allow_tests true
bench --site "$SITE_RESOURCE_RESERVATION" set-config allow_tests true

bench --site "$SITE_ACME" run-tests --app acme_rules
bench --site "$SITE_INTAKE" run-tests --app intake_booking
bench --site "$SITE_PROCUREMENT" run-tests --app procurement_requests
bench --site "$SITE_ACCESS" run-tests --app access_requests
bench --site "$SITE_MAINTENANCE" run-tests --app maintenance_requests
bench --site "$SITE_SERVICE_DESK" run-tests --app service_desk_requests
bench --site "$SITE_RESOURCE_RESERVATION" run-tests --app resource_reservations
