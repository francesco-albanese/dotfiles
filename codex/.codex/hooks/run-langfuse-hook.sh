#!/bin/bash

if [[ -x "$HOME/.codex/hooks/.venv-langfuse/bin/python" ]]; then
  exec "$HOME/.codex/hooks/.venv-langfuse/bin/python" "$HOME/.codex/hooks/langfuse_hook.py"
fi

exec python3 "$HOME/.codex/hooks/langfuse_hook.py"
