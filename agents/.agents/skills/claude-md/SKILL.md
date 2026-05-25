---
name: claude-md
description: Generate or improve CLAUDE.md files following best practices. Use when creating a new CLAUDE.md, auditing or improving an existing one, or setting up Claude Code project instructions.
argument-hint: "[path-to-project]"
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, AskUserQuestion
---

# CLAUDE.md Generator

Generate or improve CLAUDE.md files using the WHY/WHAT/HOW framework with progressive disclosure.

## Step 1 — Detect Scenario

Run these checks:

1. Check if `CLAUDE.md` exists in current working directory
2. Check if project has source files (any of: `package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `Makefile`, `*.tf`, `src/`, `lib/`, `app/`)

Map to scenario:
- **Source files exist + no CLAUDE.md** → Scenario A (explore & generate)
- **No source files + no CLAUDE.md** → Scenario B (new project questionnaire)
- **CLAUDE.md exists** → Scenario C (audit & improve)

## Step 2A — Existing Project, No CLAUDE.md

Explore the codebase systematically. Read these files if they exist:

- `package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod` — stack, deps, scripts
- `Makefile`, `justfile` — available commands
- `README.md` — project purpose
- `.github/workflows/*.yml` — CI/CD
- `tsconfig.json`, `ruff.toml`, `.eslintrc*`, `biome.json` — tooling
- `.pre-commit-config.yaml`, `prek.toml` — git hooks
- `Dockerfile`, `docker-compose.yml` — containerization
- `terraform/`, `*.tf` — infrastructure
- `.env.example` — environment variables

Also run:
- `ls -la` for top-level structure
- `ls src/` or `ls app/` or `ls lib/` for source layout
- Check for `.claude/rules/` directory

From gathered info, draft CLAUDE.md following the template in `assets/reference-template.md`.

**Key rules**:
- Target <60 lines for root CLAUDE.md
- WHY/WHAT/HOW: project purpose → tech stack → how to work with it
- Runnable commands over prose (e.g., `uv run pytest -v` not "run tests using pytest")
- Reference `file:line` instead of embedding code snippets
- Universal rules only — task-specific rules go in `.claude/rules/`
- No linter rules in CLAUDE.md (use hooks or `.claude/rules/linting.md`)

After drafting, use `AskUserQuestion` to show a summary and ask:
- "Anything to add/change before I write?"
- Offer to generate `.claude/rules/` files for task-specific guidance (testing, linting, deployment, etc.)

## Step 2B — New Project Questionnaire

Use `AskUserQuestion` to gather info in batched questions:

**Batch 1**:
- Project purpose (1-2 sentences)
- Primary language/framework

**Batch 2**:
- Package manager
- Test command
- Build/run commands
- Linting/formatting tools

**Batch 3**:
- Key conventions (naming, structure, patterns)
- Deployment target
- Any existing docs/specs to reference

From answers, generate CLAUDE.md following the template.

## Step 2C — Existing CLAUDE.md (Audit & Improve)

Read existing CLAUDE.md. Audit against this checklist:

| Check | Pass criteria |
|-------|--------------|
| Brevity | <60 lines root file |
| Structure | Has WHY (overview) + WHAT (stack) + HOW (commands) |
| Universal only | No task-specific rules in root (should be in `.claude/rules/`) |
| No code snippets | References `file:line` instead of inline code |
| No linter config | Linting handled by hooks or rules files |
| Runnable commands | Commands are copy-pasteable, not prose descriptions |
| Progressive disclosure | Links to `.claude/rules/` for detailed guidance |

Present audit results via `AskUserQuestion`:
- List what's good
- List gaps/violations
- Ask which improvements to apply

When rewriting:
- **Preserve** existing content that follows best practices
- **Reorganize** into WHY/WHAT/HOW sections
- **Extract** task-specific rules to `.claude/rules/` files
- **Replace** code snippets with `file:line` references
- **Add** missing sections (commands, structure, conventions)
- **Trim** to <60 lines, moving excess to rules files

## Step 3 — Write Output

1. Write `CLAUDE.md` to project root
2. If progressive disclosure files needed, create `.claude/rules/` directory and write task-specific files:
   - `testing.md` — how to run tests, test conventions
   - `linting.md` — formatting/linting commands
   - `deployment.md` — deploy process
   - `lambda.md`, `api.md`, etc. — domain-specific rules
3. Add rules references to CLAUDE.md (e.g., `- [Testing rules](.claude/rules/testing.md)`)

## Best Practices Reference

These principles MUST be followed in all generated CLAUDE.md files:

1. **Brevity**: <60 lines root file. If it's longer, extract to `.claude/rules/`
2. **WHY/WHAT/HOW framework**: Project overview → Tech stack → Working commands
3. **Progressive disclosure**: Root file = universal rules. Task-specific = `.claude/rules/`
4. **Runnable commands**: `make test` not "run the test suite using make"
5. **No code snippets**: Use `file:line` references (e.g., "See `src/auth/middleware.ts:42` for auth pattern")
6. **No linter rules**: Use hooks (`prek`, `pre-commit`) or `.claude/rules/linting.md`
7. **Universal rules only**: If a rule only applies when doing X, it belongs in `.claude/rules/x.md`
8. **Reference example**: See `assets/reference-template.md` for ideal structure
