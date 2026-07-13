#!/usr/bin/env bash
set -euo pipefail

if [[ -n "${DB_SECRET_ARN:-}" ]]; then
  # Assign-then-eval (not eval "$(...)" directly) so a nonzero exit from
  # resolve_secrets.py trips `set -e` instead of being silently swallowed.
  secrets="$(python3 resolve_secrets.py)"
  eval "$secrets"
fi

exec "$@"
