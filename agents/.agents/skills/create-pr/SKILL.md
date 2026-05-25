---
name: create-pr
description: Create a pull request using the migrated git-ops workflow.
---

# create-pr

Use this skill when the user asks to create a pull request for the current branch.

Use the Codex `git-ops` subagent, if available, to:

1. Check current branch status and whether changes are pushed.
2. Create a pull request with a concise title and description following the user's conventions.
3. Return the pull request URL.

If a pull request already exists, return the existing URL. Do not merge the PR. If subagent tooling is unavailable, follow the same workflow directly while honoring the `git-ops` agent rules in `~/.codex/agents/git-ops.toml`.

The original Claude slash command is preserved unchanged in `ORIGINAL.md`.
