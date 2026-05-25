---
name: feature-branch
description: Create a new feature branch using the migrated git-ops workflow.
---

# feature-branch

Use this skill when the user asks to create a new feature branch. Treat the user text after `$feature-branch` as the branch purpose.

Use the Codex `git-ops` subagent, if available, to:

1. Check current branch status.
2. Ensure the working tree is clean or decide with the user whether to stash changes.
3. Fetch the latest remote state.
4. Create a semantic branch from `main` using an appropriate prefix such as `feature/`, `fix/`, `chore/`, `docs/`, or `test/`.
5. Push the branch with upstream tracking.

If no branch purpose is provided, ask what the feature is about. If subagent tooling is unavailable, follow the same workflow directly while honoring the `git-ops` agent rules in `~/.codex/agents/git-ops.toml`.

The original Claude slash command is preserved unchanged in `ORIGINAL.md`.
