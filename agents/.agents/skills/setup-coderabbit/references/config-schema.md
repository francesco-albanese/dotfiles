# CodeRabbit `.coderabbit.yaml` schema

Cached from https://docs.coderabbit.ai/reference/configuration on 2026-05-21.
Fetch the live page first; fall back to this if offline.

## Top level

| Key | Type | Default |
|-----|------|---------|
| `language` | enum (ISO) | `"en-US"` |
| `tone_instructions` | string ≤250 | `""` |
| `early_access` | bool | `false` |
| `enable_free_tier` | bool | `true` |

## `reviews`

| Key | Type | Default |
|-----|------|---------|
| `profile` | enum: `chill`, `assertive` | `chill` |
| `request_changes_workflow` | bool | `false` |
| `high_level_summary` | bool | `true` |
| `high_level_summary_instructions` | string | `""` |
| `high_level_summary_placeholder` | string | `"@coderabbitai summary"` |
| `high_level_summary_in_walkthrough` | bool | `false` |
| `auto_title_placeholder` | string | `"@coderabbitai"` |
| `auto_title_instructions` | string | `""` |
| `review_status` | bool | `true` |
| `review_details` | bool | `false` |
| `commit_status` | bool | `true` |
| `fail_commit_status` | bool | `false` |
| `collapse_walkthrough` | bool | `true` |
| `changed_files_summary` | bool | `true` |
| `sequence_diagrams` | bool | `true` |
| `estimate_code_review_effort` | bool | `true` |
| `assess_linked_issues` | bool | `true` |
| `related_issues` | bool | `true` |
| `related_prs` | bool | `true` |
| `suggested_labels` | bool | `true` |
| `auto_apply_labels` | bool | `false` |
| `suggested_reviewers` | bool | `true` |
| `auto_assign_reviewers` | bool | `false` |
| `in_progress_fortune` | bool | `true` |
| `poem` | bool | `true` |
| `enable_prompt_for_ai_agents` | bool | `true` |
| `abort_on_close` | bool | `true` |
| `disable_cache` | bool | `false` |

### `reviews.path_filters`
Array of glob strings. Includes/excludes (prefix `!`) files from review.

### `reviews.path_instructions`
Array of `{ path: glob, instructions: string ≤20000 }`.

### `reviews.labeling_instructions`
Array of `{ label: string, instructions: string ≤3000 }`.

### `reviews.auto_review`
| Key | Type | Default |
|-----|------|---------|
| `enabled` | bool | `true` |
| `description_keyword` | string | `""` |
| `auto_incremental_review` | bool | `true` |
| `auto_pause_after_reviewed_commits` | int ≥0 | `5` |
| `ignore_title_keywords` | string[] | `[]` |
| `labels` | string[] | `[]` |
| `drafts` | bool | `false` |
| `base_branches` | string[] | `[]` |
| `ignore_usernames` | string[] | `[]` |

### `reviews.slop_detection`
| Key | Type | Default |
|-----|------|---------|
| `enabled` | bool | `true` |
| `label` | string | applied label name |

### `reviews.finishing_touches`
- `docstrings.enabled` bool, default `true`
- `unit_tests.enabled` bool, default `true`
- `simplify.enabled` bool, default `false`
- `custom[]` (max 5): `{ enabled, name, instructions }`

### `reviews.pre_merge_checks`
- `override_requested_reviewers_only` bool, default `false`
- `docstrings`: `{ mode: off|warning|error (default warning), threshold: 0–100 (default 80) }`
- `title`: `{ mode, requirements: string }`
- `description`: `{ mode }`
- `issue_assessment`: `{ mode }`
- `custom_checks[]`: `{ mode, name ≤50, instructions ≤10000 }`

## `reviews.tools`

Each entry is `{ enabled: bool }` unless noted. All default `true` unless noted.

`shellcheck`, `ruff`, `markdownlint`, `biome`, `hadolint`, `flake8`, `rubocop`, `buf`, `regal`, `actionlint`, `clippy`, `trivy`, `oxc`, `eslint`, `pylint`, `brakeman`, `phpmd`, `phpcs`, `yamllint`, `gitleaks`, `trufflehog`, `checkov`, `tflint`, `fortitudeLint`, `dotenvLint`, `htmlhint`, `stylelint`, `checkmake`, `osvScanner`, `blinter`, `smartyLint`, `emberTemplateLint`, `psscriptanalyzer`, `clang`, `cppcheck`, `opengrep`, `circleci`, `luacheck`, `prismaLint`.

`presidio` defaults `false`.

With extra keys:
- `ast-grep`: `rule_dirs[]`, `util_dirs[]`, `essential_rules` bool, `packages[]`
- `github-checks`: `enabled`, `timeout_ms` (0–900000, default 90000)
- `languagetool`: `enabled`, `enabled_rules[]`, `disabled_rules[]`, `enabled_categories[]`, `disabled_categories[]`, `enabled_only` bool, `level: default|picky`
- `phpstan`: `enabled`, `level: default|0..9|max`
- `swiftlint`, `golangci-lint`, `detekt`, `pmd`, `semgrep`, `sqlfluff`, `shopifyThemeCheck`: `enabled`, `config_file`

## `chat`

| Key | Type | Default |
|-----|------|---------|
| `art` | bool | `true` |
| `allow_non_org_members` | bool | `true` |
| `auto_reply` | bool | `true` |
| `integrations.jira.usage` | enum: `auto|enabled|disabled` | `auto` |
| `integrations.linear.usage` | enum: `auto|enabled|disabled` | `auto` |

## `knowledge_base`

- `opt_out` bool, default `false`
- `web_search.enabled` bool, default `true`
- `code_guidelines`: `{ enabled, filePatterns[] }`
- `learnings.scope`: `local|global|auto` (default `auto`)
- `issues.scope`: `local|global|auto`
- `jira`: `{ usage, project_keys[] }`
- `linear`: `{ usage, team_keys[] }`
- `pull_requests.scope`: `local|global|auto`
- `mcp`: `{ usage, disabled_servers[] }`
- `linked_repositories[]`: `{ repository: "owner/repo", instructions ≤2000 }`

## `code_generation`

- `docstrings`: `{ language, path_instructions[]: { path, instructions ≤20000 } }`
- `unit_tests`: `{ path_instructions[]: { path, instructions ≤20000 } }`

## `issue_enrichment`

- `auto_enrich.enabled` bool, default `false`
- `planning`: `{ enabled, auto_planning: { enabled, labels[] } }`
- `labeling`: `{ labeling_instructions[]: { label, instructions ≤3000 }, auto_apply_labels }`
