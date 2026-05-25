# Excalidraw Skill Reference

How to feed `scripts/render.js` to produce diagrams that look like Francesco's existing ones.

## CLI

```
node ~/.claude/skills/excalidraw/scripts/render.js --skeleton <input.json> --out <output.excalidraw>
```

Zero npm dependencies. Just Node.

## Skeleton input format

```jsonc
[
  {
    "type": "rectangle",
    "id": "auth",                    // referenced by arrows; auto-generated if omitted
    "x": 50, "y": 100,
    "width": 200, "height": 90,
    "role": "core",                  // → fills backgroundColor from palette
    "label": { "text": "AuthService\n(token verify)", "fontSize": 18 }
  },
  {
    "type": "rectangle",
    "id": "api",
    "x": 350, "y": 100, "width": 200, "height": 90,
    "role": "entry-point",
    "label": { "text": "POST /login" }
  },
  {
    "type": "arrow",
    "start": { "id": "api" },
    "end":   { "id": "auth" },
    "label": { "text": "verifies\ntoken" }
  }
]
```

Notes:
- Arrows that reference shape ids skip all coord math — `render.js` computes points + populates `startBinding` / `endBinding` / `boundElements`.
- Multi-line labels use `\n`.
- For `text` elements (free-floating titles), pass `width`/`height` explicitly or let `render.js` measure them.
- For grouping, set `groupIds: ["layer-presentation"]` on every member rectangle and add a wrapping `{type:"rectangle", role:"group", groupIds:["layer-presentation"], label:{text:"Presentation"}}` outline behind them.
- Supported types: `rectangle`, `ellipse`, `diamond`, `text`, `arrow`, `line`.

## Visual style baked into render.js

- `roughness: 1`, `fontFamily: 1` (Virgil), `strokeWidth: 2`, `strokeColor: "#1e1e1e"`
- `fillStyle`: `solid` when a `backgroundColor` or `role` is set, otherwise `hachure`
- Rectangles get `roundness: { type: 3 }`; arrows/lines `{ type: 2 }`

## Role-to-color palette

When you write a skeleton element with a `role` field, `render.js` fills in the matching `backgroundColor` automatically. Override per-element with an explicit `backgroundColor` if needed.

| Role | Color | Use for |
|---|---|---|
| `entry-point` | `#a5d8ff` | HTTP routes, CLI commands, cron, event handlers, public library exports |
| `core` / `business` | `#b2f2bb` | Domain logic modules, services |
| `data` / `persistence` | `#ffc9c9` | Repositories, DAOs, schemas, DB clients |
| `infra` / `config` | `#fab005` | DI wiring, startup, env loaders, feature flags |
| `external` / `integration` | `#ced4da` | Third-party APIs, message queues, S3, Redis |
| `cross-cutting` | `#7950f288` | Auth, logging, metrics, error handling |
| `group` | `transparent` | Grouping containers (just an outline) |

## Layout patterns per diagram type

Default sizes: rectangle `200×90`, ellipse `180×80`, gap_x `80`, gap_y `120`.

### `system-map.excalidraw` — layered

Rows by role, top to bottom:

```
row 0 (y=  60):  entry-points          ← role: "entry-point"
row 1 (y= 240):  core / business       ← role: "core"
row 2 (y= 420):  data / persistence    ← role: "data"
row 3 (y= 600):  infra / config        ← role: "infra"
right column:    cross-cutting band    ← role: "cross-cutting"  (x= row_width + 100)
```

Wrap each row in a transparent `role: "group"` rectangle with a row title. Edges flow downward by default. If a node has `score > 4` (high centrality), upsize to `260×110`.

### `entry-points.excalidraw` — two columns

Left column (x=60): triggers (HTTP/CLI/event), `role: "entry-point"`. Right column (x=520): the module each one dispatches into. One arrow per row. Add a free-floating `text` title at the top: "Entry points → Core modules".

### `call-graph.excalidraw` — module clusters

For each top-level module from the Map agent, emit a `role: "group"` rectangle (size based on member count, ~`(members × 220)+40` wide × `~140` tall) at a position computed by ranking modules in topological order along x. Place member rectangles inside (`role` per member). Use the same `groupIds: ["mod-<name>"]` on every member. Edges only between modules — drop intra-module edges.

### `data-flow.excalidraw` — types and the modules that touch them

Types are `type: "ellipse"`, `role: "data"`, `180×80`, top row. Modules are rectangles, `role` per module, second row. Edge labels are exactly `reads`, `writes`, or `transforms`. Free-floating title at top.

### `integrations.excalidraw` — perimeter map

Central app group on the left (transparent `role: "group"` rectangle wrapping all internal modules that touch externals). External systems as a column on the right, `role: "external"`. One arrow per external link, labeled with the protocol/operation (`HTTPS`, `gRPC`, `S3 PutObject`, `pub/sub`, etc.).

## Centrality cap

Each diagram is capped at ~30 rectangles. Compute `score = in_degree + out_degree` per node. Keep the top-N; group the rest into a single transparent "+ K supporting modules" rectangle off to the side, with `groupIds: ["tail"]`.

## Exemplars distilled from Francesco's existing diagrams

### Exemplar A — high-level architecture

Pattern from `tomoro-ai/docs/high-level-architecture.excalidraw`: layered, translucent-bg perimeter group, dark anchor headers, rectangles ~200×90 for modules.

```jsonc
[
  { "type": "rectangle", "id": "edge",  "x":  20, "y":  20, "width": 700, "height": 110, "role": "group",
    "label": { "text": "Edge",  "fontSize": 22 } },
  { "type": "rectangle", "id": "cdn",   "x":  60, "y":  60, "width": 200, "height": 60, "role": "entry-point",
    "label": { "text": "CloudFront" } },
  { "type": "rectangle", "id": "wafr",  "x": 290, "y":  60, "width": 200, "height": 60, "role": "cross-cutting",
    "label": { "text": "WAF\nrules" } },
  { "type": "rectangle", "id": "logs",  "x": 520, "y":  60, "width": 180, "height": 60, "role": "data",
    "label": { "text": "Access logs" } },

  { "type": "rectangle", "id": "app",   "x":  20, "y": 180, "width": 700, "height": 200, "role": "group",
    "label": { "text": "Application", "fontSize": 22 } },
  { "type": "rectangle", "id": "api",   "x":  60, "y": 230, "width": 200, "height": 90, "role": "core",
    "label": { "text": "API\nrouter" } },
  { "type": "rectangle", "id": "use",   "x": 290, "y": 230, "width": 200, "height": 90, "role": "core",
    "label": { "text": "Use cases" } },
  { "type": "rectangle", "id": "repo",  "x": 520, "y": 230, "width": 180, "height": 90, "role": "data",
    "label": { "text": "Repo (PG)" } },

  { "type": "arrow", "start": { "id": "cdn" }, "end": { "id": "api" } },
  { "type": "arrow", "start": { "id": "api" }, "end": { "id": "use" } },
  { "type": "arrow", "start": { "id": "use" }, "end": { "id": "repo" }, "label": { "text": "writes" } }
]
```

### Exemplar B — flow with annotations

Pattern from `aws-api-gateway-mtls/diagrams/lambdas-business-logic.excalidraw`: bullet-list multi-line text inside boxes, occasional emoji.

```jsonc
[
  { "type": "rectangle", "id": "ca",
    "x":  60, "y":  60, "width": 280, "height": 160, "role": "infra",
    "label": { "text": "Root CA\n— create private key\n— self-sign cert\n— valid 10 years" } },
  { "type": "rectangle", "id": "ica",
    "x": 420, "y":  60, "width": 280, "height": 160, "role": "infra",
    "label": { "text": "Intermediate CA\n— generate CSR\n— signed by Root CA\n— valid 5 years" } },
  { "type": "rectangle", "id": "client",
    "x": 240, "y": 280, "width": 280, "height": 160, "role": "external",
    "label": { "text": "🔐 Client cert\n— generated CSR\n— signed by Intermediate" } },

  { "type": "arrow", "start": { "id": "ca" },     "end": { "id": "ica" },    "label": { "text": "signs" } },
  { "type": "arrow", "start": { "id": "ica" },    "end": { "id": "client" }, "label": { "text": "issues" } }
]
```

## Common gotchas

- **Don't put text *inside* a rectangle as a separate `text` element with the same coords.** Use the rectangle's `label` field — the converter handles bound-text positioning and adds the bidirectional `boundElements` ↔ `containerId` link automatically.
- **Arrow ids in `start`/`end` must match shape ids in the same input file.** Unresolved ids are silently dropped and the arrow falls back to absolute coords.
- **`groupIds` must be identical across all members of a group.** A typo creates a phantom group.
- **Why no Mermaid path?** The upstream `mermaid-to-excalidraw` library depends on `mermaid`, which calls SVG `getBBox` to compute layout. `getBBox` is not implemented by jsdom — only by real browser engines (puppeteer/playwright). Skipped to keep this skill dependency-free.
