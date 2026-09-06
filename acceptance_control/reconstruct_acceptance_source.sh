#!/usr/bin/env bash
set -euo pipefail

DEST="${1:?usage: reconstruct_acceptance_source.sh DEST}"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
rm -rf "$DEST"
mkdir -p "$DEST"

cat \
  "$ROOT/repair.part00.00" "$ROOT/repair.part00.01" "$ROOT/repair.part00.02" "$ROOT/repair.part00.03" \
  "$ROOT/payload.b64.part01" \
  "$ROOT/repair.part02.00" "$ROOT/repair.part02.01" "$ROOT/repair.part02.02" "$ROOT/repair.part02.03" \
  "$ROOT/payload.b64.part03" "$ROOT/payload.b64.part04" "$ROOT/payload.b64.part05" "$ROOT/payload.b64.part06" \
  > "$RUNNER_TEMP/capability-base.b64"

base64 -d "$RUNNER_TEMP/capability-base.b64" > "$RUNNER_TEMP/capability-base.tar.gz"
echo "900357df7be11d9aada844a1f43bb04b3a25b8e162d460c759417b3ac1157f64  $RUNNER_TEMP/capability-base.tar.gz" | sha256sum -c -
tar -xzf "$RUNNER_TEMP/capability-base.tar.gz" -C "$DEST"

# Apply the Frappe module-package corrections proved by the real lifecycle run.
install -D "$ROOT/proof_overlay/module_init.py" "$DEST/capabilities/approvals/frappe_app/na_approvals/na_approvals/na_approvals/__init__.py"
install -D "$ROOT/proof_overlay/module_init.py" "$DEST/capabilities/notifications/frappe_app/na_notifications/na_notifications/na_notifications/__init__.py"
install -D "$ROOT/proof_overlay/module_init.py" "$DEST/clients/acme_reference/custom/frappe_app/acme_rules/acme_rules/acme_rules/__init__.py"
