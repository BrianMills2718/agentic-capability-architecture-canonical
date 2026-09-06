#!/usr/bin/env bash

# Ensure one Frappe app name appears as a complete line in sites/apps.txt.
# Frappe/Bench-created files are not guaranteed to end with a trailing newline,
# so append one first when necessary. Without this guard, app names can be
# concatenated (for example: `frappena_scheduling`).
ensure_bench_apps_entry() {
  local file="$1"
  local app="$2"
  local last_byte=""

  mkdir -p "$(dirname "$file")"
  touch "$file"

  if [[ -s "$file" ]]; then
    last_byte="$(tail -c 1 "$file" | od -An -t x1 | tr -d '[:space:]')"
    if [[ "$last_byte" != "0a" ]]; then
      printf '\n' >> "$file"
    fi
  fi

  if ! grep -qxF "$app" "$file"; then
    printf '%s\n' "$app" >> "$file"
  fi
}
