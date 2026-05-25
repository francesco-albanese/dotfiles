---
description: Run code-quality-verifier agent to audit implementation quality against spec or commit history
---

Run a quality gate audit on the current branch's changes.

## 1. Find the Spec

If `$ARGUMENTS` is provided and non-empty, use it as the path to the spec file. Read it.

Otherwise, search for specs:
- Glob `~/.claude/plans/*.md` for active plans

If multiple specs found, ask me which one to use (AskUserQuestion). If none found, skip — commit history becomes the source of truth (no spec mode).

## 2. Gather Git Diff

Run `git diff main...HEAD` to capture all changes on this branch. If that fails (no `main` branch), fall back to `git diff master...HEAD`. If both fail, use `git diff HEAD~5...HEAD` as last resort.

Also run `git log --oneline main...HEAD` (same fallback logic) to understand commit history.

**When no spec is available (no spec mode):** also run `git log --no-merges main...HEAD` (same fallback logic) to capture full commit messages as context for auditing against commit intent.

## 3. Launch Quality Audit

Use the Task tool with `subagent_type: "code-quality-verifier"` passing:
- The git diff summary (truncate if extremely large, focus on file list + key changes)
- The current project working directory path
- Instruction to produce the standard verification summary with severity levels

**When spec exists:** also pass the full spec content.

**When no spec (no spec mode):** pass the full commit history as context. Instruct the agent to audit against commit intent — verify that the code changes match what the commits describe, and flag any discrepancies.

## 4. Pragmatic Programmer Check

After the verifier agent returns, run `/pragmatic-programmer-check` on the same diff and include its findings in the final report under a dedicated "Pragmatic Programmer" section. Treat any FAIL from that check as a blocking issue in the quality gate.

## 5. Report Findings

Present the agent's findings directly in the terminal. Do not write any output files. Include the full verification summary with:
- Spec Compliance status (omit if no spec — replace with Commit Intent Alignment)
- Security assessment
- Test quality assessment
- Architecture alignment
- Pragmatic Programmer check results (from step 4)
- All issues with severity levels and file:line references
- Required actions
