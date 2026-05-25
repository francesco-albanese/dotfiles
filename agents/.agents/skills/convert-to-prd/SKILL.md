---
name: convert-to-prd
description: Convert a markdown plan into structured prd.json items with testable acceptance criteria.
---

# convert-to-prd

Use this skill when the user asks to convert a markdown plan or requirements document into PRD JSON. Treat the user text after `$convert-to-prd` as the input path or source description.

Read the referenced markdown file and write `prd.json` in the current working directory. Each item must include:

- `category`: one of `functional`, `ui`, `integration`, `performance`, `security`
- `description`: a clear requirement statement
- `steps`: specific, testable verification steps
- `passes`: `false`

If `prd.json` does not exist, create it. If it exists and all items have `passes: true`, replace it. If any existing item has `passes: false`, append the new items without duplicating obvious matches.

The original Claude slash command is preserved unchanged in `ORIGINAL.md`.
