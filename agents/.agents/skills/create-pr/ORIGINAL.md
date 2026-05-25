---
description: Create PR using git-ops agent (Claude reviews on GitHub)
---

Use git-ops subagent (Task tool with subagent_type='git-ops') to:
1. Check current branch status, ensure changes pushed
2. Create PR with proper title/description following conventions
3. Return PR URL

If PR already exists, return existing PR URL. Don't merge - Claude will review on GitHub.
