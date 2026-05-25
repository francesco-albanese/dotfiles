#!/bin/bash
# auto-format.sh — Auto-format Python and TypeScript/JS files after edit

INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

if [[ -z "$FILE_PATH" ]] || [[ ! -f "$FILE_PATH" ]]; then
  exit 0
fi

EXT="${FILE_PATH##*.}"

case "$EXT" in
  py)
    ruff format "$FILE_PATH" 2>/dev/null
    pyright "$FILE_PATH" 2>/dev/null || true
    ;;
  ts|tsx|js|jsx)
    pnpx @biomejs/biome format --write "$FILE_PATH" 2>/dev/null
    ;;
esac

exit 0
