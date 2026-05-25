---
name: commit-push-pr
description: Commit, push, and create a pull request using the migrated git-ops workflow.
---

# commit-push-pr

Use this skill when the user asks to commit changes, push them, and open a pull request.

Use the Codex `git-ops` subagent, if available, to:

1. Check git status.
2. Stage all relevant changes.
3. Create a commit with a concise message following the user's conventions.
4. Push to the remote.
5. Create a pull request with a concise title and description.

If there is nothing to commit, skip to PR creation if the branch has unpushed or already-pushed commits suitable for a PR. If subagent tooling is unavailable, follow the same workflow directly while honoring the `git-ops` agent rules in `~/.codex/agents/git-ops.toml`.

The original Claude slash command is preserved unchanged in `ORIGINAL.md`.
