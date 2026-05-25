---
name: check-coderabbit-comments
description: Triage CodeRabbit comments on a GitHub PR or GitLab MR — fetch them, drop nitpicks, group surviving items by severity with pre-populated fixes, apply the ones the user approves, then auto-reply and resolve the threads. Use when the user wants to check, review, triage, address, or apply CodeRabbit comments / suggestions / feedback on a PR or MR.
---

# Check CodeRabbit Comments

## Workflow

1. **Locate the PR/MR.** Use the number/URL the user gave, else infer from the current branch (`gh pr view --json number,url` or `glab mr view -F json`).

2. **Fetch CodeRabbit threads (open only).**
   - GitHub — `gh api graphql` on `pullRequest.reviewThreads(first:100){ id isResolved comments(first:20){ nodes{ author{login} body path line } } }`. Keep threads where the first comment's `author.login == "coderabbitai"` and `isResolved == false`. Also pull issue-level comments via `gh pr view --json comments` for CodeRabbit's summary blocks.
   - GitLab — `glab api projects/:id/merge_requests/:iid/discussions`. Keep where `notes[0].author.username == "coderabbit-ai"` and `resolved == false`.

3. **Triage.** Read the file around each anchor. **Drop silently:** anything anchored to a `*.md` / `*.mdx` file, anything CodeRabbit tags `nitpick`, `nit`, `style`, `Prettier`, formatting-only, duplicates, suggestions that conflict with surrounding code, or items already fixed in a later commit. Bucket the rest:
   - 🔴 **Critical** — security, auth, data loss, broken behaviour.
   - 🟠 **Important** — bugs, perf, missing error paths, contract/API changes.
   - 🟡 **Minor** — refactors with real benefit, dead code, naming that hurts readability.

4. **Present.** One block per item, grouped by severity. No CodeRabbit quotes longer than one line, no prose between items:

   ```
   🔴 1. src/api/users.ts:42 — missing auth check on PATCH
        Fix: wrap handler with requireAuth(...)
        ```diff
        - export const PATCH = async (req) => {
        + export const PATCH = requireAuth(async (req) => {
        ```
   ```

5. **Ask:** *"Apply all / pick numbers / skip all?"* Apply approved fixes with Edit.

6. **Reply + resolve.** For each addressed thread:
   - GitHub — post `@coderabbitai resolve` as a reply on the thread, then call the `resolveReviewThread` GraphQL mutation with the thread `id`.
   - GitLab — post a reply on the discussion, then `PUT projects/:id/merge_requests/:iid/discussions/:did?resolved=true`.

   For skipped items, post one short reply with the reason and leave the thread unresolved.
