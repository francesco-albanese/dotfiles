---
name: setup-coderabbit
description: Configure CodeRabbit for a repository by writing .coderabbit.yaml. Explores the codebase to detect tech stacks per folder (backend, frontend, IaC, CI, etc.), then writes per-path review instructions focused on intent, convention adherence, and security — explicitly not nitpicks. Use when the user wants to set up, bootstrap, configure, refresh, or audit CodeRabbit (.coderabbit.yaml / .coderabbit.yml) in a project.
---

# Setup CodeRabbit

## Workflow

1. **Check existing config.** Look for `.coderabbit.yaml` or `.coderabbit.yml` at repo root. If present, read it and ask before overwriting; otherwise show a diff at the end.
2. **Refresh the schema.** Fetch `https://docs.coderabbit.ai/reference/configuration` to pick up new keys. If unreachable, use [config schema](references/config-schema.md).
3. **Map the repo.** Identify the _purpose_ (README, package metadata, top-level docs) and which tech lives in which top-level folder. Note linters/formatters already wired up (eslint, ruff, tflint, etc.) — these inform the `tools` block.
4. **Start from [`assets/coderabbit.yaml.skeleton`](assets/coderabbit.yaml.skeleton).** It already locks in the non-negotiable settings.
5. **Add one `reviews.path_instructions` entry per detected stack.** Use the rules of thumb in [Per-stack focus](#per-stack-focus). Each instruction must say what to flag _and_ what to ignore.
6. **Enable matching `tools`.** Only turn on what the stack uses (e.g. Python→ruff, JS/TS→eslint+biome, Terraform→tflint+checkov, GitHub Actions→actionlint). Always enable `gitleaks`. Never enable `markdownlint` — markdown is excluded via `path_filters` in the skeleton. Leave everything else at defaults.
7. **Validate.** Parse the YAML (`python3 -c 'import yaml; yaml.safe_load(open(".coderabbit.yaml"))'` or equivalent). Show the user the final file.

## Per-stack focus

Use these as the _spine_ of each `path_instructions` entry — one entry per area found in the repo

- **Backend** — intent vs PR description, API/contract changes, error handling, authn/authz boundaries, input validation, secret handling, N+1 / perf footguns, migration safety.
- **Frontend** — intent vs PR description, accessibility regressions, prop/typing changes that break consumers, state-management leaks, secret exposure in client bundles, bundle-size regressions on key routes.
- **Terraform / IaC** — blast radius (IAM, public ingress, deletions), state impact, drift, missing required tags, encryption defaults, provider/version pins.
- **GitHub Actions / CI** — secret handling, untrusted input injected into `run:`, third-party action pinning (SHA, not tag), `permissions:` scope, cache-poisoning risk.
- **Tests / fixtures** — coverage of stated intent rather than implementation, deleted assertions, snapshot churn that hides behavior changes.
- **Docs / config** — flag when behavior changes without doc updates, or vice-versa.

## What to skip

- Don't enable `auto_apply_labels`, `auto_assign_reviewers`, `finishing_touches`, or anything that mutates the PR unless the user asks.
- Don't expand the skeleton with options the user hasn't asked for — defaults are fine.
- Don't add `path_instructions` for stacks that don't exist in the repo.
