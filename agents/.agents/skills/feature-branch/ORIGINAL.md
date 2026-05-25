---
description: Create new feature branch using git-ops agent
---

Use the git-ops subagent (Task tool with subagent_type='git-ops') to:
1. Check current branch status (ensure clean working tree or stash changes)
2. Fetch latest from remote
3. Create new feature branch from main with semantic naming (feat/, fix/, chore/, etc.)
4. Push branch to remote with upstream tracking

Branch name should follow semantic conventions. If I provide a description, derive the branch name. If not, ask me what the feature is about.
