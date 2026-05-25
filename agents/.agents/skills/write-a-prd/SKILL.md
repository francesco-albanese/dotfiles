---
name: write-a-prd
description: Create a PRD through user interview, codebase exploration, and module design, then submit it as a GitHub issue or a beads epic. Use when user wants to write a PRD, create a product requirements document, or plan a new feature.
---

This skill will be invoked when the user wants to create a PRD. You may skip steps if you don't consider them necessary.

## 0. Ask the user which tracker to use

Use AskUserQuestion with two options: **GitHub issues** (default) or **beads (`bd`)**. Record the choice — the submission step in section 6 branches on it.

If **beads** is chosen and `.beads/` does not exist in the current working directory, run:

```bash
bd init --prefix "$(basename "$PWD")"
```

This uses the default (non-stealth) mode so `.beads/` is tracked with the repo.

## 1. Gather the problem

Ask the user for a long, detailed description of the problem they want to solve and any potential ideas for solutions.

## 2. Explore the repo

Verify their assertions and understand the current state of the codebase.

## 3. Interview relentlessly

Interview the user about every aspect of this plan until you reach a shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one.

## 4. Sketch modules

Sketch out the major modules you will need to build or modify to complete the implementation. Actively look for opportunities to extract deep modules that can be tested in isolation.

A deep module (as opposed to a shallow module) is one which encapsulates a lot of functionality in a simple, testable interface which rarely changes.

Check with the user that these modules match their expectations. Check with the user which modules they want tests written for.

## 5. Draft the PRD

Use the template below.

<prd-template>

## Problem Statement

The problem that the user is facing, from the user's perspective.

## Solution

The solution to the problem, from the user's perspective.

## User Stories

A LONG, numbered list of user stories. Each user story should be in the format of:

1. As an <actor>, I want a <feature>, so that <benefit>

<user-story-example>
1. As a mobile bank customer, I want to see balance on my accounts, so that I can make better informed decisions about my spending
</user-story-example>

This list of user stories should be extremely extensive and cover all aspects of the feature.

## Implementation Decisions

A list of implementation decisions that were made. This can include:

- The modules that will be built/modified
- The interfaces of those modules that will be modified
- Technical clarifications from the developer
- Architectural decisions
- Schema changes
- API contracts
- Specific interactions

Do NOT include specific file paths or code snippets. They may end up being outdated very quickly.

## Testing Decisions

A list of testing decisions that were made. Include:

- A description of what makes a good test (only test external behavior, not implementation details)
- Which modules will be tested
- Prior art for the tests (i.e. similar types of tests in the codebase)

## Out of Scope

A description of the things that are out of scope for this PRD.

## Further Notes

Any further notes about the feature.

</prd-template>

## 6. Submit the PRD

### GitHub backend

Create the PRD as a GitHub issue with `gh issue create`. Use the full PRD markdown as the body.

### Beads backend

Write the full PRD markdown to a tempfile and create it as an open epic:

```bash
TMP=$(mktemp)
cat > "$TMP" <<'PRD'
<full PRD markdown from step 5>
PRD

bd create "<PRD title>" \
  --type epic \
  --body-file "$TMP" \
  --priority 2
```

Capture the resulting epic ID (e.g. `<prefix>-1`) and report it to the user — they'll pass it to `/prd-to-issues` next.
