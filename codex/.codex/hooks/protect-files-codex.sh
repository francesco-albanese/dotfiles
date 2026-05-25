#!/bin/bash
# protect-files-codex.sh - Codex wrapper for edit/apply_patch protected paths.

INPUT=$(cat)
FILE_PATH=$(printf '%s' "$INPUT" | jq -r '.tool_input.file_path // empty')
COMMAND=$(printf '%s' "$INPUT" | jq -r '.tool_input.command // empty')

PROTECTED_PATTERNS=(".env" "package-lock.json" "pnpm-lock.yaml" "uv.lock" ".git/")

for pattern in "${PROTECTED_PATTERNS[@]}"; do
  if [[ -n "$FILE_PATH" && "$FILE_PATH" == *"$pattern"* ]]; then
    echo "Blocked: $FILE_PATH matches protected pattern '$pattern'" >&2
    exit 2
  fi

  if [[ -n "$COMMAND" && "$COMMAND" == *"$pattern"* ]]; then
    echo "Blocked: patch command references protected pattern '$pattern'" >&2
    exit 2
  fi
done

exit 0
