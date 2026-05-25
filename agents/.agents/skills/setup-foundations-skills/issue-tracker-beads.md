# Issue tracker: beads

Issues and PRDs for this repo live in a local [beads](https://github.com/steveyegge/beads) database (`.beads/*.db`). Use the `bd` CLI for all operations.

## Conventions

- **Create an issue**: `bd create "title" -d "description"`. Use `--body-file -` with a heredoc for multi-line descriptions, or `-f <file.md>` to batch-create from markdown.
- **Read an issue**: `bd show <id>` for details; add `--long` for extended metadata, and `bd comments <id>` to view the comment thread.
- **List issues**: `bd list --label <name>` (filter by label) or `bd list --all` (include closed). Use `bd ready` for unblocked, ready-to-work issues. Add `--json` / `--format` for scripted output.
- **Comment on an issue**: `bd comment <id> "..."` (use `--file` or `--stdin` for multi-line).
- **Apply / remove labels**: `bd label add <id> "..."` / `bd label remove <id> "..."`.
- **Close**: `bd close <id> --reason "..."`.

Beads operates on the local `.beads/*.db` — `bd` auto-discovers it when run inside the repo. Run `bd init` once if the database does not yet exist.

## When a skill says "publish to the issue tracker"

Create a beads issue with `bd create`.

## When a skill says "fetch the relevant ticket"

Run `bd show <id>` (add `bd comments <id>` if the skill needs the discussion thread).
