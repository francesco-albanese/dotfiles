---
description: Convert markdown plan to structured PRD JSON with testable acceptance criteria
---

Convert the feature requirements from the provided markdown file into structured PRD items.

## Input
Read the markdown file at: $ARGUMENTS

## Output Requirements
Each requirement/feature should become a PRD item with:
- **category**: One of `functional`, `ui`, `integration`, `performance`, `security`
- **description**: Clear statement of what the feature/requirement does
- **steps**: Array of specific, testable verification steps (be specific about acceptance criteria)
- **passes**: Always set to `false` initially

## Output Format
```json
[
  {
    "category": "functional",
    "description": "Feature description here",
    "steps": [
      "Navigate to X",
      "Perform action Y",
      "Verify outcome Z"
    ],
    "passes": false
  }
]
```

## File Handling
Write output to `prd.json` in the current working directory:
1. If `prd.json` doesn't exist: create it with the new items
2. If `prd.json` exists and ALL items have `passes: true`: overwrite entirely with new items
3. If `prd.json` exists with ANY `passes: false`: merge by appending new items to existing array

## Guidelines
- Parse each markdown section/feature as a separate PRD item
- Make verification steps specific and actionable (not vague)
- Include UI navigation steps where applicable
- Think like a QA engineer writing test cases
- Avoid duplicate items when merging
