#!/bin/bash
# block-cat-sensitive.sh — Block Bash commands that read sensitive files

INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

PROTECTED_PATTERNS=(".env" ".git/")
READ_CMDS="cat|head|tail|less|more"

if echo "$COMMAND" | grep -qE "^($READ_CMDS)\b"; then
  for pattern in "${PROTECTED_PATTERNS[@]}"; do
    if echo "$COMMAND" | grep -qE "(^|\s|/)[^ ]*${pattern}"; then
      echo "Blocked: command reads sensitive file matching '$pattern'" >&2
      exit 2
    fi
  done
fi

exit 0
