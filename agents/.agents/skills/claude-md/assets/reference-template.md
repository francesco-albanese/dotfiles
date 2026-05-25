# Reference Template

Use this as a structural guide when generating CLAUDE.md files. Replace placeholders with actual project info. Remove sections that don't apply. Target <60 lines.

---

# Project Overview

{1-2 sentence description of what the project does and WHY it exists}

## Package Manager

- {language} {version} with `{package_manager}`

## Tech Stack

- {framework/library} for {purpose}
- {service/tool} for {purpose}
- [{Link text}]({relative_path}) — {brief description}

## Commands

- `{test_command}` — run tests
- `{lint_command}` — lint/format
- `{build_command}` — build
- `{run_command}` — run locally

## Git Hooks

- {Hook tool and how to run it, e.g., "Use `prek run --all-files` before committing"}

## Structure

- `{src_dir}/` — source code
- `{test_dir}/` — tests
- `{config_dir}/` — configuration

## Conventions

- {Key convention 1, e.g., "snake_case for file names"}
- {Key convention 2, e.g., "Each module has its own test file"}

## Rules

Task-specific guidance lives in `.claude/rules/`:
- [{Rule name}](.claude/rules/{file}.md) — {when to read it}
