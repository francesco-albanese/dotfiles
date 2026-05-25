---
name: pragmatic-programmer-check
description: Audit a code change against the Pragmatic Programmer principles (orthogonality, coupling, testability, crash-early, prove-don't-assume, abstraction-over-implementation). Use when user wants to check code against pragmatic-programmer rules, or as part of a quality gate review.
---

# Pragmatic Programmer Check

Audit the current change against the universal engineering rules in [../../rules/general/pragmatic-programmer.md](../../rules/general/pragmatic-programmer.md). Produce a concise report

## 1. Gather the diff

Run `git diff main...HEAD` (fallback `master...HEAD`, then `HEAD~5...HEAD`). If the user passed a path or PR number as `$ARGUMENTS`, scope to that instead.

## 2. Score each principle

For every principle below, decide **PASS / WARN / FAIL** and cite `file:line` evidence when WARN/FAIL.

| # | Principle | What to look for |
|---|-----------|------------------|
| 1 | Orthogonality | Cross-module reach-ins, shared mutable globals, near-duplicate functions |
| 2 | Minimise coupling | New imports across layer boundaries, modules that know too much about each other |
| 3 | Self-contained components | Single responsibility per unit; no god-files, no grab-bag utils |
| 4 | Plan for change | Magic numbers, hard-coded config, decisions that will be painful to reverse |
| 5 | Make it easy to reuse | Code that is copy-paste-ready vs locked to one call site |
| 6 | Invest in the abstraction | Leaky abstractions, abstractions that expose implementation details |
| 7 | Don't assume it, prove it | Untested assumptions, missing integration check, "should work" comments |
| 8 | Crash early | Silent catches, fallback defaults that hide bugs, swallowed errors |
| 9 | Don't use code you don't understand | Copy-pasted snippets, unexplained magic, unfamiliar libraries pulled in without rationale |
| 10 | Test state coverage, not code coverage | Tests that hit lines without asserting meaningful state transitions |
| 11 | Design to test | Hard-to-test code: hidden dependencies, time/IO not injected, untestable side effects |

## 3. Report

Output exactly this structure — nothing else:

```
# Pragmatic Programmer Check

## Summary
<one line: overall verdict + count of FAIL / WARN>

## Findings
<for each WARN/FAIL>
- [SEVERITY] <principle> — <file:line> — <one sentence: what's wrong + suggested fix>

## Passes
<one line listing principle numbers that passed cleanly>
```

If everything passes, say so in one line and stop. Do not pad.
