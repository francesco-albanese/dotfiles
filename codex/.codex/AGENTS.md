# General

- In all interactions and commit messages, be extremely concise

## GitHub

- Your primary method for interacting with GitHub should be the GitHub CLI.

## Git

- When creating branches, use semantic branch names https://gist.github.com/seunggabi/87f8c722d35cd07deb3f649d45a31082
- When committing and pushing co-author myself Francesco Albanese by reading the information from .git folder or using git config --global --list | grep -E 'user.name|user.email'

## Plans

- At the end of each plan, give me a list of unresolved questions to answer, if any
- When you generate a plan and present it to me in the terminal print only a concise summary + headings.
- NEVER accept your internal training knowledge when the user asks you to do a research first. If the search if blocked by sandbox, stop and tell the user to enable the websearch or ask permissions to run the web search outside sandbox.

## Custom Agents

You can use the following agents:

- git-ops - use it for ALL git operations, following the Git preferences described above

## Agentic Coding

- If you create any temporary new files, scripts, or helper files for iteration, clean up these files by removing them at the end of the task.

## Pragmatic programmer

Universal engineering principles that apply to every project, stack, and language. Follow them at all times.

### Decoupling

- **Orthogonality** - reduce interdependency among components. Keep code decoupled, avoid global data, avoid similar functions.
- **Minimise coupling between modules** - a change in one place should not ripple through unrelated code.
- **Design components that are self-contained, independent, and with a single well-defined purpose.**

### Change & Reuse

- **Plan for change**
- **Make it easy to reuse**
- **Invest in the abstraction, not the implementation** - abstractions outlive any single implementation.

### Correctness

- **Don't assume it, prove it** - verify assumptions in the actual environment
- **Crash early** - fail fast and loudly when an invariant breaks
- **Don't use code you don't understand**

### Testing

- **Test state coverage, not code coverage**
- **Design to test**
