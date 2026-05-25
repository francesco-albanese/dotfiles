---
name: quality-gate
description: Run a quality gate audit using code-quality-verifier and pragmatic-programmer-check.
---

# quality-gate

Use this skill when the user asks to audit the current branch against a spec, PRD, task list, or commit history. Treat the user text after `$quality-gate` as an optional spec path.

If a spec path is provided, read it. Otherwise search `~/.claude/plans/*.md` for active plans. If multiple specs are found, ask the user which one to use. If none is available, use commit history as the source of intent.

Gather branch context:

1. Run `git diff main...HEAD`; fall back to `git diff master...HEAD`, then `git diff HEAD~5...HEAD`.
2. Run `git log --oneline main...HEAD`; use the same fallback order.
3. In no-spec mode, also run `git log --no-merges` with the same fallback order.

Use the Codex `code-quality-verifier` subagent, if available, and pass the spec or commit intent, the diff summary, and the current working directory. Ask for the standard verification summary with severity levels. If subagent tooling is unavailable, perform the same audit directly while honoring `~/.codex/agents/code-quality-verifier.toml`.

After the verifier returns, run `$pragmatic-programmer-check` on the same diff and include its findings under a `Pragmatic Programmer` section. Treat any FAIL from that check as blocking.

Do not write output files. Present the full quality gate report in the response.

The original Claude slash command is preserved unchanged in `ORIGINAL.md`.
