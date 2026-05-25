#!/bin/bash
# block-npm-npx.sh — Block npx/npm commands, suggest pnpx/pnpm

INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

BLOCKED=("npx" "npm")

for pattern in "${BLOCKED[@]}"; do
  # Block if command starts with npx/npm, optionally preceded by env vars (FOO=bar)
  # Avoids false positives when npm/npx appear in commit messages or comments
  if echo "$COMMAND" | grep -qE "^([[:space:]]*[A-Za-z_][A-Za-z0-9_]*=[^[:space:]]*[[:space:]]+)*[[:space:]]*(${pattern})([[:space:]]|$)"; then
    echo "Blocked: use pnpx/pnpm instead of npx/npm" >&2
    exit 2
  fi
done

exit 0
