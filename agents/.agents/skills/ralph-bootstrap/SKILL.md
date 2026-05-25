---
name: ralph-bootstrap
description: 'This skill should be used when the user asks to: "initialise Ralph", "bootstrap Ralph", "set up Ralph Wiggum", "add Ralph to project", "create Ralph directory" or wants to set up autonomous coding loops with Ralph.'
---

# Ralph Bootstrap

Initialise the Ralph Wiggum autonomous coding loop in the current project.

## 1. Ask the user which tracker Ralph should drive

Use AskUserQuestion with two options: **GitHub issues** (default) or **beads (`bd`)**. The choice picks the prompt template that gets baked into the project.

## 2. Prerequisites

- `gh` CLI installed and authenticated (GitHub backend)
- `bd` CLI installed and an initialised `.beads/` database (beads backend)
- Task issues already created via `/prd-to-issues`

## 3. Run the bootstrap script

Pass the chosen backend as the first argument:

```bash
# GitHub
~/.agents/skills/ralph-bootstrap/scripts/bootstrap.sh github

# beads
~/.agents/skills/ralph-bootstrap/scripts/bootstrap.sh beads
```

This creates `scripts/ralph/prompt.md` containing the tracker-specific instructions (with a `<!-- tracker: github -->` or `<!-- tracker: beads -->` marker on the first line so the ralph scripts can detect the backend), plus `scripts/ralph/notify.env.example` for WhatsApp notifications.

## Files Created

```
scripts/ralph/
├── prompt.md            # Instructions for Claude (tracker-specific)
└── notify.env.example   # WhatsApp notify template (copy to notify.env to enable AFK pings)
```

## Usage After Bootstrap

```bash
# HITL mode - single iteration
ralph-once

# AFK mode - 10 iterations (default)
afk-ralph 25
```

## Workflow

1. `/write-a-prd` — create PRD as GitHub issue or beads epic
2. `/prd-to-issues` — break PRD into task issues / child beads (progress log on GitHub, stream on epic in beads)
3. `/ralph-bootstrap` — copy the matching prompt template into the project
4. `ralph-once` or `afk-ralph` — run autonomous coding loops
