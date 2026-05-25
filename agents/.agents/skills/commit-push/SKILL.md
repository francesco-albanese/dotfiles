---
name: commit-push
description: Commit and push changes using the migrated git-ops workflow.
---

# commit-push

Use this skill when the user asks to commit and push the current work.

Use the Codex `git-ops` subagent, if available, to:

1. Check git status.
2. Stage all relevant changes.
3. Create a commit with a concise message following the user's conventions.
4. Push to the remote.

If there is nothing to commit, say so. If subagent tooling is unavailable, follow the same workflow directly while honoring the `git-ops` agent rules in `~/.codex/agents/git-ops.toml`.

The original Claude slash command is preserved unchanged in `ORIGINAL.md`.
