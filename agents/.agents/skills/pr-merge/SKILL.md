---
name: pr-merge
description: Create or reuse a pull request and merge it using the migrated git-ops workflow.
---

# pr-merge

Use this skill when the user asks to create or merge a pull request.

Use the Codex `git-ops` subagent, if available, to:

1. Check current branch status and ensure changes are pushed.
2. Create a pull request, or use the existing pull request if one already exists.
3. Wait for required checks to pass when checks are present.
4. Merge the pull request using GitHub CLI.
5. Delete the remote branch after merge when appropriate.

Treat merge operations as complex git operations: present the exact merge command and get explicit confirmation before running it. If subagent tooling is unavailable, follow the same workflow directly while honoring the `git-ops` agent rules in `~/.codex/agents/git-ops.toml`.

The original Claude slash command is preserved unchanged in `ORIGINAL.md`.
