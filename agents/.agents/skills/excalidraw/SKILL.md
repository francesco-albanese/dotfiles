---
name: excalidraw
description: Map a codebase by fanning out 5 parallel Explore sub-agents (topology, entry-points, call-graph, data-flow, integrations), then emit 4–5 detailed Excalidraw diagrams to docs/diagrams/. Use when the user asks to map the codebase and produce a diagram, explore the codebase and map its logic to a diagram, or visualize how the core modules and core logic are wired together.
---

# /excalidraw

Produces 4–5 `.excalidraw` files under `<repo-root>/docs/diagrams/` that describe how the current codebase is structured: module topology, entry points, cross-module call graph, data flow, and external integrations.

Read [REFERENCE.md](REFERENCE.md) before generating skeleton inputs — it contains the role-to-color palette, the skeleton schema, layout patterns per diagram type, and two exemplars distilled from Francesco's existing diagrams.

## Pipeline

### 1. Pre-flight

Resolve the project root: `git rev-parse --show-toplevel 2>/dev/null || pwd`. All output paths are relative to this. Auto-create `<root>/docs/diagrams/`.

Verify `node` is available: `command -v node`. If missing, stop with: `Install Node.js first.` The renderer has zero npm dependencies — no install step required.

### 2. Plan preamble

Print a single message to the user before fanning out:

> Mapping `<repo-name>`. Five Explore agents in parallel:
> 1. **Map** — repo topology, top-level modules, configured paths
> 2. **Entry-points** — HTTP routes, CLI commands, cron, event handlers, public exports
> 3. **Call-graph** — cross-module function call chains
> 4. **Data-flow** — types/schemas, persistence boundaries, mutations
> 5. **Integrations** — external systems, env vars, third-party APIs
>
> Output: 4–5 `.excalidraw` files under `docs/diagrams/`.

### 3. Fan out 5 Explore sub-agents in parallel

Send all five `Agent` calls in a single message with `subagent_type: "Explore"`. Each prompt must:

- State the project root and the auto-excludes (`.git`, `node_modules`, `dist`, `build`, `.next`, `target`, `venv`, `.venv`, `__pycache__`, lockfiles; honor `.gitignore`).
- Define the agent's slice (one of the five below).
- **Require the response to be a single fenced ```json block** matching this schema:

```json
{
  "nodes": [
    { "id": "kebab-case-id",
      "label": "Display name (multi-line ok with \\n)",
      "role": "entry-point|core|data|infra|external|cross-cutting",
      "evidence_path": "src/foo/bar.ts",
      "evidence_line": 42,
      "notes": "optional one-liner"
    }
  ],
  "edges": [
    { "from": "kebab-case-id",
      "to":   "kebab-case-id",
      "kind": "calls|reads|writes|publishes|subscribes|depends-on|http|invokes",
      "evidence": "src/foo/bar.ts:42 → src/baz/qux.ts:88"
    }
  ],
  "notes": ["Free-text observations the synthesizer should know about."]
}
```

The five agent briefs:

1. **Map agent** — Walk the directory tree. Identify top-level modules (packages, apps, services, layers). Read `package.json` / `pyproject.toml` / `go.mod` / `Cargo.toml` / `tsconfig.json` paths. One node per top-level module; edges = explicit dependencies declared between them.

2. **Entry-points agent** — Find every way execution enters this codebase: HTTP route definitions (Express/FastAPI/Hono/Lambda handlers/etc.), CLI entry points (`bin` in package.json, `if __name__ == "__main__"`, click/typer/cobra commands), cron/scheduled handlers, event/queue subscribers, exported public APIs (for libraries). Edges connect each entry point to the first internal module it dispatches into.

3. **Call-graph agent** — For each module identified by the Map agent, find the most significant cross-module function calls. Skip intra-module calls. Aim for ~30 most-central edges. Use grep for import statements + function call sites.

4. **Data-flow agent** — Identify the core domain types/schemas (TypeScript interfaces, Pydantic models, SQL tables, protobuf messages, etc.). For each, trace where it's created, transformed, and persisted. Nodes are the types and the modules that touch them; edges have `kind: reads|writes|transforms`.

5. **Integrations agent** — Identify external systems the codebase talks to: databases, message queues, third-party HTTP APIs, cloud services (S3/SQS/Lambda/etc.), env-loaded secrets, observability backends. Each external system is a `role: external` node; edges connect from the internal module that touches it.

If any agent returns malformed JSON, re-prompt that single agent with the schema and an example. Do not re-explore.

### 4. Synthesize

Merge the five reports in the main thread:

- Concatenate all `nodes`, dedupe by `id` (later definitions override earlier — Map agent runs first conceptually).
- Concatenate all `edges`, dedupe by `(from, to, kind)`.
- Compute centrality `score = in_degree + out_degree` for each node.
- For each diagram below, select up to **30 nodes** by descending centrality from the relevant subset; collapse the long tail into a single `+ N supporting modules` group rectangle.

### 5. Render diagrams

All diagrams use the skeleton input format (see REFERENCE.md). Write each diagram's skeleton JSON to `~/.claude/skills/excalidraw/scripts/.tmp/<name>.json`, then invoke `render.js`. Output goes to `<repo-root>/docs/diagrams/<name>.excalidraw`.

| Diagram | Source from | Layout pattern |
|---|---|---|
| `system-map.excalidraw` | Map + Call-graph nodes | Layered rows: entry-points (row 0), core (row 1), data (row 2), infra (row 3). Cross-cutting in a translucent purple band on the right. |
| `entry-points.excalidraw` | Entry-points subset | Two columns: triggers on the left, dispatched modules on the right. Arrows left-to-right. |
| `call-graph.excalidraw` | Call-graph nodes + edges | Module-as-cluster: each Map module is a `role: group` rectangle containing its members; edges only between clusters. |
| `data-flow.excalidraw` | Data-flow nodes + edges | Types as ellipses (`type: "ellipse"`), modules as rectangles. Arrows labeled `reads` / `writes` / `transforms`. |
| `integrations.excalidraw` | Integrations + the modules touching them | Central app group on the left, external systems on the right. **Skip if Integrations agent returned 0 nodes.** |

Use the role-to-color palette from REFERENCE.md. Default box size `200×90`, ellipse size `180×80`, horizontal gap `80`, vertical gap `120`.

Run renders in parallel with multiple `Bash` calls in one message:

```bash
node ~/.claude/skills/excalidraw/scripts/render.js --skeleton .tmp/system-map.json     --out <root>/docs/diagrams/system-map.excalidraw
node ~/.claude/skills/excalidraw/scripts/render.js --skeleton .tmp/entry-points.json   --out <root>/docs/diagrams/entry-points.excalidraw
# etc.
```

Clean up `.tmp/` after.

### 6. End-of-run summary + deep-dive offer

Print one tight summary:

> Wrote N diagrams to `docs/diagrams/`:
> - `system-map.excalidraw` — 27 modules, 41 edges
> - `entry-points.excalidraw` — 8 entry points
> - `call-graph.excalidraw` — 30 nodes, 52 edges
> - `data-flow.excalidraw` — 12 types across 9 modules
> - `integrations.excalidraw` — 6 external systems
>
> Drag any onto excalidraw.com to view/edit.
>
> Want a focused diagram for a specific module? Tell me the name and I'll spawn one Explore agent and reuse the merged report.

If the user requests a deep-dive, spawn **one** Explore agent scoped to that module. Reuse the merged JSON in conversation context — do not re-explore the whole repo. Render one new file: `docs/diagrams/<module>-detail.excalidraw`.

## Out of scope

- Auto-commit / PR creation
- Watch mode / regen on save
- Cross-run caching of agent JSON
- Generating a `README.md` alongside the diagrams
- Language-specific agent briefs (agents stay language-agnostic; project files inform them)
- Mermaid input (the renderer is skeleton-only — Mermaid runtime requires a real browser engine for SVG layout)
