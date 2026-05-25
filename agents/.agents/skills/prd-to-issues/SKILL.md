---
name: prd-to-issues
description: Break a PRD into independently-grabbable GitHub issues or beads child tasks using tracer-bullet vertical slices. Use when user wants to convert a PRD to issues, create implementation tickets, or break down a PRD into work items.
---

# PRD to Issues

Break a PRD into independently-grabbable work items using vertical slices (tracer bullets). Supports either GitHub issues or beads child tasks under a parent epic.

## Process

### 0. Ask the user which tracker to use

Use AskUserQuestion with two options: **GitHub issues** (default) or **beads (`bd`)**. If the user already hands you a reference (e.g. `#42` or `<prefix>-1`), infer from that.

### 1. Locate the PRD

- **GitHub**: ask for the PRD issue number (or URL). If not in context, fetch with `gh issue view <number>` (with comments).
- **Beads**: ask for the PRD epic ID. If not provided, auto-find with `bd list --type epic --status open` — use the single match or ask if ambiguous. Fetch with `bd show <epic-id>`.

### 2. Explore the codebase (optional)

If you have not already explored the codebase, do so to understand the current state of the code.

### 3. Draft vertical slices

Break the PRD into **tracer bullet** issues. Each issue is a thin vertical slice that cuts through ALL integration layers end-to-end, NOT a horizontal slice of one layer.

Slices may be **HITL** or **AFK**. HITL slices require human interaction (architectural decision, design review). AFK slices can be implemented and merged without human interaction. Prefer AFK over HITL where possible.

<vertical-slice-rules>
- Each slice delivers a narrow but COMPLETE path through every layer (schema, API, UI, tests)
- A completed slice is demoable or verifiable on its own
- Prefer many thin slices over few thick ones
</vertical-slice-rules>

### 4. Quiz the user

Present the proposed breakdown as a numbered list. For each slice, show:

- **Title**: short descriptive name
- **Type**: HITL / AFK
- **Blocked by**: which other slices (if any) must complete first
- **User stories covered**: which user stories from the PRD this addresses

Ask the user:

- Does the granularity feel right? (too coarse / too fine)
- Are the dependency relationships correct?
- Should any slices be merged or split further?
- Are the correct slices marked as HITL and AFK?

Iterate until the user approves the breakdown.

### 5. Create the work items

Create in dependency order (blockers first) so real IDs can be referenced in the "Blocked by" field.

#### GitHub backend

For each approved slice, create a GitHub issue using `gh issue create`. Use the issue body template below.

After creating each issue, ensure labels exist and apply them:

- Create labels if missing: `gh label create "status:blocked" --repo "owner/repo" --color "fbca04" --description "Blocked by dependency"` (note: `--color` takes hex without the `#`).
- Apply label and milestone: `gh issue edit <issue-number> --repo "owner/repo" --milestone "<milestone-title>" --add-label "<label1>,<label2>"`.

Ask the user which milestone to assign, or create one if needed.

<issue-template>
## Parent PRD

#<prd-issue-number>

## What to build

A concise description of this vertical slice. Describe the end-to-end behavior, not layer-by-layer implementation. Reference specific sections of the parent PRD rather than duplicating content.

## Acceptance criteria

- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Blocked by

- Blocked by #<issue-number> (if any)

Or "None - can start immediately" if no blockers.

## User stories addressed

Reference by number from the parent PRD:

- User story 3
- User story 7

</issue-template>

Do NOT close or modify the parent PRD issue.

#### Beads backend

For each approved slice, create a child task under the epic. Slugify any milestone name (lowercase, spaces → `-`) if scoping is used.

```bash
bd create "<slice title>" \
  --type task \
  --parent "<epic-id>" \
  --description "<What-to-build markdown, including 'User stories addressed' and optional 'Parent PRD' reference>" \
  --acceptance "$(cat <<'AC'
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3
AC
)" \
  --deps blocks:<blocker-id-1>,blocks:<blocker-id-2> \
  --label hitl \
  --label milestone:<slug>    # only if scoping
```

Swap `--label hitl` for `--label afk` on AFK slices. Omit `--deps` for unblocked slices. Omit the milestone label when the user isn't scoping.

Do NOT pre-create labels — beads creates them lazily on first use.
Do NOT modify or close the parent epic.

### 6. Progress log setup

#### GitHub backend

Create `in-progress`, `done`, and `progress-log` labels if missing, then create a Progress Log issue:

```bash
gh label create "in-progress" --repo "owner/repo" --color "fbca04" --description "Work currently underway"
gh label create "done" --repo "owner/repo" --color "0e8a16" --description "Work completed"
gh label create "progress-log" --repo "owner/repo" --color "c5def5" --description "Progress log for autonomous coding loop"

gh issue create --repo "owner/repo" --title "[Progress Log] <PRD title>" --label "progress-log" --milestone "<milestone>" --body "$(cat <<'EOF'

## Parent PRD

# <prd-issue-number>

## Codebase Patterns

(Add patterns discovered during implementation)

## Key Files

(List important files for context)
EOF
)"
```

#### Beads backend

No setup required. The progress log lives directly on the epic:

- **Iteration summaries** → `bd comment <epic-id>` (timestamped stream, analogous to `gh issue comment`)
- **Codebase Patterns** (evergreen) → `bd note <epic-id>` (appended to the epic's notes field, shown in `bd show`)

Both streams are seeded on the first Ralph iteration — nothing to create up front.
