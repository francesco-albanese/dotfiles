---
description: Create PR and merge it using GitHub CLI via git-ops agent
---

Use the git-ops subagent (Task tool with subagent_type='git-ops') to:
1. Check current branch status and ensure changes are pushed
2. Create a PR with proper title/description following my conventions
3. Wait for PR checks to pass (if any)
4. Merge the PR using GitHub CLI (gh pr merge)
5. Clean up by deleting the remote branch after merge

If PR already exists, use existing PR. Handle any issues that arise.
