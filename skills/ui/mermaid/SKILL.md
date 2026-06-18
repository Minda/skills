---
name: mermaid
description: Create or edit Mermaid diagram files (.mmd) that render correctly in Figma — either pasted into the Mermaid in Figma plugin or exported via mmdc and the bake-fills.py post-process for full-fidelity native SVG import. Use when creating architecture diagrams, flow charts, sequence diagrams, ERDs, or any other Mermaid diagram.
argument-hint: "<describe the diagram to create, or path to an existing .mmd file to edit>"
---

*[Minda Myers](https://mindamyers.com) · [GitHub](https://github.com/Minda) · [skills repo](https://github.com/Minda/skills)*

# /mermaid

Create or edit a Mermaid diagram (`.mmd`) that renders correctly in Figma. Two import paths exist; the `.mmd` source patterns below are compatible with both:

- **Plugin path:** paste `.mmd` into the **Mermaid in Figma** plugin with "Use HTML tags" unchecked. Labels and layout survive; specific fill colors are replaced with Mermaid theme defaults.
- **Native SVG path (full fidelity):** render `.mmd → .svg` with `mmdc`, post-process with `bake-fills.py`, drag the baked SVG onto Figma's canvas. Specific fill colors, edge lines, arrowheads, and node labels all survive — validated end-to-end (see test-5 below).

## Component library and test diagrams

The `tests/` directory is the canonical reference for what survives the pipeline:

- **[`tests/components.md`](tests/components.md)** — cheatsheet: every node shape, multi-line labels, subgraphs, styling, edge syntax, sequence/ER constructs. Copy/paste from here when authoring a new diagram.
- **[`tests/shapes-test.mmd`](tests/shapes-test.mmd)** — exercises every flowchart shape in one file (test-6).
- **[`tests/orientation-test-lr.mmd`](tests/orientation-test-lr.mmd)** — `graph LR` reference (test-7).
- **[`tests/sequence-test.mmd`](tests/sequence-test.mmd)** — actors, messages, notes, activations, loops, alt (test-8).
- **[`tests/er-test.mmd`](tests/er-test.mmd)** — entities, attributes, relationship cardinalities (test-9).

Each test file ships with its `mmdc` reference PNG and a `.baked.svg`. **When `bake-fills.py` changes, re-bake all four and re-import to Figma to catch regressions.**

## Usage

```
/mermaid $ARGUMENTS
```

## Every diagram must include

### 1. Frontmatter title block (first thing in the file)
```
---
title: Short descriptive title of the diagram
---
```

### 2. Description comment (immediately after frontmatter)
A `%%` comment explaining what the diagram depicts and the point it is making — one to three lines:
```
%% Describes X. Shows how Y connects to Z. Key point: W is the bottleneck.
```

### 3. Figma compatibility directive (after comments, before diagram type)
```
%%{init: {"flowchart": {"htmlLabels": false}}}%%
```
Use `"flowchart"` for `graph` and `flowchart` diagrams. For sequence diagrams this directive is not needed (they don't use HTML labels).

### Full header template
```
---
title: Your Title Here
---
%% What this diagram shows and the key point it makes.
%%{init: {"flowchart": {"htmlLabels": false}}}%%
graph LR
```

## Figma SVG compatibility rules

These rules were determined by empirical testing with the **Mermaid in Figma** plugin:

| Test | Change | Result |
|---|---|---|
| test-1 | `htmlLabels: false` + `<br/>` → `\n` | ✅ SVG rendered correctly |
| test-2 | `&lt;`/`&gt;` → literal `<`/`>` only | ❌ Failed |
| test-3 | Removed all `classDef`/`style` lines only | ❌ Mermaid parse / blank diagram |
| test-4 | `classDef`+`class` styling vs per-node `style` styling on a graph with subgraphs + cylinder shapes | ❌ `classDef` → black nodes, only second line of multi-line labels visible (via plugin) · ✅ inline `style NodeID …` → readable diagram (via plugin) |
| test-5 | mmdc `.mmd → .svg` → `bake-fills.py` → drag into Figma's **native** SVG canvas import (no plugin), same `simplified-arch-A` diagram | ✅ Full fidelity: every node fill in its specified hex, all node/edge/cluster labels visible, subgraph backgrounds pale-yellow, edges drawn with arrowheads, label background blobs invisible |
| test-6 | bake + native import on `shapes-test.mmd` — every flowchart shape (rect, rounded, stadium, subroutine, cylinder, circle, asymmetric, diamond, hexagon, parallelogram, trapezoid, double-circle), 1/2/3/4-line labels, HTML entities, nested subgraphs | ✅ Structural audit clean: 0 unhandled `<foreignObject>`, every text element has fill, every shape has fill or stroke. Visual confirmation in Figma still pending |
| test-7 | bake + native import on `orientation-test-lr.mmd` — `graph LR` orientation | ✅ Structural audit clean (same as test-6). Note: mmdc rendered the reference PNG as top-to-bottom even though the directive is `LR` — Mermaid may auto-rotate when the chain is long; the bake itself doesn't care about orientation |
| test-8 | bake + native import on `sequence-test.mmd` — actors, sync/async messages, notes, activations, loops, alt blocks | ✅ after extending bake passes 4–5: arrow markers can be `<path>`/`<circle>`/`<polygon>`, and sequence's `<polygon class="labelBox">` (loop/alt tabs) now gets a fill. 3 SVG sprite paths inside `<defs><symbol>` remain unfilled but are unreferenced so don't render |
| test-9 | bake + native import on `er-test.mmd` — entities with PK/FK attributes, three relationship cardinalities, relationship labels | ✅ after extending bake pass 4 to also match `relationshipLine` and adding a marker-inner heuristic (closed `d` path → fill, open path → stroke). Note: ER diagrams use `<foreignObject>` for *every* label (attribute names, types, cardinality labels) — pass 6 converts them all, including `<strong>`/`<em>` formatting from backtick-markdown labels. Foreign objects without a `<p>` payload (empty Mermaid label spans) are left alone since there is nothing to convert |
| test-10 | bake on `component-sys-02-step-functions-agent-discovery-overview.mmd` and the matching component zoom — backtick-markdown labels with `**bold title**` and `*italic description*` spanning multiple `<br/>` | ✅ Structural audit: every band's fill and stroke hex survives as direct attributes; every bold title emits `font-weight="bold"` and every italic description tspan emits `font-style="italic"`; Choice/Skip nodes that have only a bold title (no description) emit one bold tspan with no italic; the audit script in `tests/audit-styled-bake.py` confirms counts match per-node expectations |

**Conclusions:**

- **`<br/>` in node labels** causes Mermaid to emit `<foreignObject>` elements. Figma does not support `<foreignObject>` and silently drops them, breaking the SVG render. Fix: set `htmlLabels: false` via `%%{init}%%` AND replace every `<br/>` with `\n` (in edge labels) or a literal newline (in node labels).
- **`classDef` + `class` styling does not survive the Figma plugin** — at least on graphs that combine subgraphs and band-styling across multiple node groups. Mermaid emits the per-class fills as CSS rules inside an embedded `<style>` block plus inline `style="fill:… !important"` attributes; the Figma plugin appears to ignore both for `classDef`-styled shapes, leaving nodes with no fill so they render as default-black, and the corresponding label-layout pass for those shapes loses the first line of multi-line labels. Fix: use per-node **inline `style NodeID fill:…,stroke:…,…`** directives (the directive named `style`, not `classDef`). These are rendered as inline `style="fill:…"` attributes that the Figma plugin reliably honors.
- **HTML entities** (`&lt;`, `&gt;`, etc.) are safe to use — not the cause of failures.
- **`---` frontmatter** must be the very first content in the file. Placing `%%{init}%%` before it causes a parse error: `Expecting 'NEWLINE', 'SPACE', 'GRAPH', got 'LINK'`.
- **Frontmatter title** (`---` block) requires Mermaid v10+. It was confirmed working in the target Figma plugin.

## How the Figma plugin appears to work (working hypothesis)

This is an inferred model of the **Mermaid in Figma** plugin's pipeline, derived from comparing the SVG that `mmdc` produces from a `.mmd` file against what the plugin shows once imported into Figma. It is a hypothesis, not a spec — treat it as the best current explanation, not ground truth. Update this section when new evidence comes in.

**Pipeline (inferred):**

1. The plugin runs Mermaid.js client-side to convert the pasted `.mmd` source into an SVG string.
2. That SVG arrives with three styling channels in play:
   - an embedded `<style>` block at the top of the SVG (Mermaid's default theme rules plus any rules derived from `classDef`),
   - per-element inline `style="fill:…;stroke:…"` attributes (added by Mermaid when `classDef`-styled and when `style NodeID …` directives are used),
   - direct SVG presentation attributes such as `fill="#ECECFF"` on a small number of shapes.
3. The plugin then passes the SVG through Figma's SVG import path. Figma's SVG renderer **does not support CSS in `<style>` blocks** — those rules are dropped entirely. Inline `style="…"` attributes are partially honored, but the exact subset that survives appears to be limited and is the suspected source of the residual quirks below.
4. The end result is a Figma frame containing one node per Mermaid shape, with whatever fills/strokes survived the import.

**Observed consequences:**

- `<foreignObject>` is completely unsupported by Figma's SVG importer (both plugin and native paths) and is silently dropped. `htmlLabels: false` suppresses foreignObject for **edge labels** and **cluster/subgraph labels**, but Mermaid v11 still emits foreignObject for **node labels** regardless of the directive — verified empirically: a flowchart with `htmlLabels: false` produces 9–12 `<foreignObject>` elements, one per node. The plugin path handles this by translating foreignObject content back to SVG text client-side before the SVG ever reaches Figma. The native-SVG path does not — node labels go missing unless they are converted (see `bake-fills.py` pass 6).
- For shapes whose only color information came from a `<style>` block class rule (the `classDef`/`class` path), the fill is lost on import. Mermaid does *also* emit the same fill as an inline `style="fill:… !important;stroke:… !important"` attribute on the shape, but in practice these multi-property `!important` inline styles do not appear to survive either — possibly because Figma's SVG importer normalises or skips them. The shape ends up with no fill, the `classDef`-specific layout produced extra outline elements that now have no fill either, and the result is the black-rectangle-with-overflowing-text symptom from test-4.
- For shapes whose fill came from a per-node `style NodeID fill:…` directive imported **via the plugin**, the diagram is legible (labels intact, layout correct) but the specific hex colors are replaced with Mermaid's pale-lavender theme default. Imported **via the native bake workflow**, the specific hex colors do survive — because `bake-fills.py` rewrites them as direct `fill="…"` presentation attributes, which Figma's native importer respects (see test-5).

**Practical implications for authoring:**

- Always set `htmlLabels: false`. (Suppresses foreignObject for edge and cluster labels; node-label foreignObject still requires bake pass 6 if going via the native path.)
- Prefer per-node inline `style NodeID …` over `classDef` + `class`. It's required for the plugin path (test-4) and produces the inline `style="…"` attributes that the bake script lifts into direct presentation attributes for the native path.
- If colors are non-load-bearing, the plugin path is the simplest route — just paste, preview, export.
- If exact hex colors matter, use the native bake workflow below — colors, labels, edges, and arrowheads all survive.

## Preserving exact node colors in Figma (bake workflow)

When the diagram's specific hex colors matter (not just legibility), the Mermaid in Figma plugin alone will substitute defaults. Workaround: render the `.mmd` to SVG, post-process the SVG to convert inline `style="fill:X"` into direct `fill="X"` SVG attributes, then drag the post-processed SVG straight onto Figma's canvas (using Figma's *native* SVG import, not the plugin).

```sh
# Render to SVG via mermaid-cli
npx -y @mermaid-js/mermaid-cli -i diagram.mmd -o diagram.svg

# Bake inline styles into direct SVG attributes
python3 .claude/skills/mermaid/bake-fills.py diagram.svg
# → produces diagram.baked.svg

# Drag diagram.baked.svg into Figma (native canvas import)
```

The `bake-fills.py` helper lives alongside this skill and performs seven passes:

1. Lifts `fill`/`stroke`/`stroke-width` out of inline `style="…!important"` attributes on `<rect|path|ellipse|polygon|circle>` and re-attaches them as direct presentation attributes (de-duplicating against any pre-existing direct attributes mmdc also emitted).
2. Adds `fill="#333"` to every `<text>` element that has no fill — restores edge and cluster labels (Mermaid's default text color lives only in the stripped `<style>` block).
3. Adds the Mermaid cluster fill + stroke (`fill="#ffffde" stroke="#aaaa33"`) to the `<rect>` directly inside every `<g class="cluster">` so subgraphs render with their pale-yellow background instead of black.
4. Adds `stroke="#333" fill="none"` to every `.flowchart-link` / `.edgePath` path so edges actually appear as lines.
5. Adds `fill="#333"` to every `.arrowMarkerPath` so arrowheads render at the line ends.
6. Converts every `<foreignObject>` to a native `<text><tspan>` block. Mermaid v11 still emits `<foreignObject>` for **node labels** (not edge/cluster labels) even with `htmlLabels:false`, and Figma's native SVG importer silently drops them — that's why node text goes missing on import. The bake rebuilds a centered SVG text element from the inner `<p>...<br/>...</p>` payload, with one `<tspan>` per line and approximate vertical centering via `dy` offsets. **Bold and italic survive**: `<strong>`/`<b>` blocks emit `font-weight="bold"` on the matching tspan, and `<em>`/`<i>` blocks (which Mermaid spans across `<br/>` for multi-line italic descriptions) emit `font-style="italic"` on every tspan whose text was accumulated while italic was open. This preserves the "bold title + italic description" pattern that the backtick-markdown Rule 4 produces.
7. Neutralizes `<rect class="background">` elements (the rounded blobs Mermaid places behind edge/cluster labels). Their fill normally comes from a CSS `rgba(...)` rule Figma strips, leaving them as solid black blocks. The bake sets `fill="none" stroke="none"` so they vanish.

Plus three additional passes added during testing:

- Pass 2b (multi-line edge / cluster labels): Mermaid emits multi-line labels (`"No\nfallback"`, `subgraph Outer["Outer\n(nested)"]`) as N sibling `<tspan class="text-outer-tspan row">` elements with their own absolute `y` attributes. Figma's SVG importer ignores the `y` on siblings after the first, so all lines collapse onto line 1 ("Nofallback", "Outer(nested)"). Pass 2b rewrites these to a single set of inner tspans with `dy` line offsets — the same structure pass 6 produces for node labels, which Figma honors.
- Pass 5b: `<polygon class="labelBox">` (the loop/alt header tabs in sequence diagrams) get `fill="#ECECFF" stroke="#9370DB"`.
- Pass 5c: walks every `<marker>` definition and applies a heuristic to inner shapes — closed paths (`d` ending in `z`/`Z`) and polygons get `fill="#333"`, open paths get `fill="none" stroke="#333"`, and circles with a fill but no stroke get one added. This handles ER cardinality crow's feet and any custom-arrowhead markers that aren't classed `arrowMarkerPath`.

Why this works: Figma's native SVG renderer respects direct presentation attributes (`fill="…"`, `stroke="…"`) and ignores `<style>` blocks, `style="…"` inline attributes, and `<foreignObject>` entirely. The bake converts the surviving information into the form Figma honors. If any element is found to already have the relevant attribute, it is left alone — so user-specified colors via inline `style NodeID …` (pass 1) take priority over Mermaid's theme defaults (passes 2–7).

### Known caveats still unverified

- **Multi-line label vertical centering for 3+ lines**: the `dy="-(n-1)*0.6em"` approximation looked right for 2-line labels in test-5; with 3- or 4-line labels in `shapes-test.mmd` the centering may visibly drift. Eyeball in Figma; if it's off, adjust `0.6` in pass 6 of `bake-fills.py`.
- **`graph LR` label positioning** in Figma vs the reference PNG.
- **Nested subgraphs at 3+ levels** — `shapes-test.mmd` covers 2 levels; deeper nesting is plausibly fine but unverified.
- **Sequence diagram fonts / actor icons** — if a diagram references `<symbol>` icons (e.g., `participant U as user`), the bake doesn't fill the icon paths; they may render black. Easy fix if encountered.
- **Mermaid theme overrides** (`%%{init: {"theme": "dark"}}%%` etc.) — the bake's hardcoded defaults (`#333`, `#ffffde`, `#ECECFF`) match the `default` theme. Other themes will produce SVG with different CSS that this bake script won't translate.

## Line breaks in labels

### How it works

Mermaid's parser reads a node label as everything between the opening `"` and closing `"` of
`["..."]` — including literal newlines. With `htmlLabels: false`, those newlines (whether literal
or `\n`) are rendered as SVG `<tspan>` line breaks and produce identical output. The source form
is what matters: literal newlines are far easier to read, diff, and edit.

### Required — literal newlines in node labels

Inside `["..."]` and all other node-shape brackets, **use literal newlines**, not `\n`. Indent each
continuation line **4 spaces past the start of the opening line** so the continuation hangs visually
under the label text and the bracket column stays scannable.

```
%% ✅ correct — literal newlines, continuation indented 4 past the opening line
graph TB
    subgraph Sys["System"]
        SPA["Managed UI
            (React + Amplify)"]
        Brain["Bedrock AgentCore
            (Brain)"]
    end
```

```
%% ❌ wrong — \n escape used where a literal newline works. Harder to read and diff.
NodeA["First line\nSecond line"]
```

The 4-space rule applies regardless of containing indent: a node at 8-space indent gets its
continuation at 12; a node at 0 gets its continuation at 4. The opening `"` and the continuation
line's first non-space character don't need to align — the 4-space hang under the label start is
what matters.

### `\n` is only for places literal newlines break parsing

Use `\n` **only** in:
- Edge labels `-->|"..."|` — the `|` delimiter closes before a literal newline.
- Subgraph titles `subgraph id["..."]` — parser support varies by version.
- Anywhere else that empirical testing shows the parser rejects a literal newline.

```
%% ✅ correct — \n in an edge label
A -->|"GraphQL\n+ WebSocket"| B

%% ✅ correct — \n in a subgraph title
subgraph LF["Lambda Functions\n(18 total)"]
```

### Never — `<br/>` in any label

```
%% ❌ always wrong — breaks Figma SVG
NodeA["First line<br/>Second line"]
```

### Where literal newlines work and where they don't

| Location | Use |
|---|---|
| Node labels `["..."]` and all node shapes `(["..."])`, `{{"..."}}`, `[["..."]]`, `>("..."]` | **Literal newline (required)**, indented 4 past the opening line |
| Subgraph titles `subgraph id["..."]` | `\n` — parser varies by version |
| Edge labels `-->|"..."|` | `\n` — `|` closes before the newline |
| Sequence diagram messages `A->>B: text` | No multi-line support; rewrite as two messages |

**Rule of thumb:** literal newlines inside any `[...]` node bracket — required. Anywhere else — `\n`.

## Sequence diagrams

Sequence diagrams (`sequenceDiagram`) do not use HTML labels, so the `%%{init}%%` directive and `\n` rule do not apply. Still include the frontmatter title and `%%` description comment.

```
---
title: Your Sequence Diagram Title
---
%% What this sequence shows.
sequenceDiagram
    ...
```

## ERDs

Same as sequence diagrams — `erDiagram` does not use HTML labels. Include frontmatter and description, omit `%%{init}%%`.

## Style and color

For Figma-target diagrams, **use per-node inline `style` directives** for fills, strokes, and text color. Do **not** use `classDef` + `class` — see test-4 above.

```
%% ✅ correct — per-node inline style; renders in Figma
style User    fill:#FCE7F3,stroke:#9D174D,stroke-width:1px,color:#111
style SPA     fill:#FCE7F3,stroke:#9D174D,stroke-width:1px,color:#111
style Cron    fill:#DBEAFE,stroke:#1E3A8A,stroke-width:1px,color:#111
```

```
%% ❌ wrong for Figma — classDef + class produces black nodes in the Figma plugin
classDef uiBand  fill:#FCE7F3,stroke:#9D174D,stroke-width:1px,color:#111
classDef sysBand fill:#DBEAFE,stroke:#1E3A8A,stroke-width:1px,color:#111
class User,SPA uiBand
class Cron,SFN sysBand
```

If many nodes share the same band, accept the repetition — each node still needs its own `style` line. The verbosity is the cost of survival through the Figma SVG import. A short helper section grouping `style` lines by band keeps the file readable:

```
%% UI band
style User fill:#FCE7F3,stroke:#9D174D,stroke-width:1px,color:#111
style SPA  fill:#FCE7F3,stroke:#9D174D,stroke-width:1px,color:#111

%% System band
style Cron fill:#DBEAFE,stroke:#1E3A8A,stroke-width:1px,color:#111
...
```

## System / architecture diagrams

When the diagram is an architecture or system diagram (component diagrams, platform diagrams, infrastructure flows), apply the following rules in addition to the general rules above. These produce clean, presentation-ready diagrams suitable for stakeholder communication and Figma export.

### Rule 1 — Abstract, functional labels

Node labels describe *what happens at each step*, not implementation details. The diagram itself shows what flows in and out via edge labels.

Ask "what does this block do?" not "what does it call?" Strip API paths, method signatures, SDK calls, and env var names:

```
%% ❌ wrong — implementation detail
IR["bedrock_agentcore.invoke_agent_runtime(
    agentRuntimeArn,
    runtimeSessionId = uuid4(),
    payload = JSON blob
)"]

%% ✅ correct — functional description
IR["Agent Entry Point
    Receives the request and dispatches
    it into the runtime"]
```

### Rule 2 — Collapse equivalent callers into one node

When multiple nodes serve the same architectural role (e.g., two Lambda functions that both invoke the same downstream service), represent them as a single node named by role.

```
%% ❌ wrong — exposes instances
LG["grants-search-v2"]
LE["eu-grants-search-v2"]

%% ✅ correct — names the role
Lambda["Lambda Function
    Invokes AgentCore on behalf of
    user requests or scheduled workflows"]
```

### Rule 3 — No URLs, function calls, or env var names in labels

Every label describes *what* the block does, never *how* it does it. Implementation details rot; functional descriptions stay accurate longer and communicate to non-technical readers.

### Rule 4 — Bold title + italic description

Use backtick markdown strings. Line 1 is `**bold title**`. Subsequent lines are `*italic description*`.

```
NodeId["`**Title**
    *What this block does,
    described functionally*`"]
```

Requires `%%{init: {"flowchart": {"htmlLabels": false}}}%%` — already required by the general rules above.

### Rule 5 — Flow-describing edge labels

Arrow labels name what is *flowing* between nodes, not the action or method name. Use noun or noun phrases (2–4 words).

```
%% ❌ wrong — names the method
AT -->|"invoke_model / stream"| BR

%% ✅ correct — names what flows
AT -->|"Inference request"| BR
```

| Instead of | Use |
|---|---|
| `"invoke_agent_runtime"` | `"Request payload"` |
| `"write via mutation resolvers"` | `"Grant & event records"` |
| `"put_object"` | `"Proposal files"` |
| `"retrieve (HYBRID)"` | `"Search query"` |

## Layout control — TB and LR diagrams

Mermaid uses the Dagre layout engine, which assigns nodes to **ranks** based on edge topology. Understanding how ranks are assigned is the key to controlling whether subgraphs stack or appear side by side.

### How Dagre ranks work

- In `graph TB`, ranks are horizontal rows — nodes at the same rank appear **left to right** on the same row.
- In `graph LR`, ranks are vertical columns — nodes at the same rank appear **stacked top to bottom** in the same column.
- Two nodes land on the same rank when they are the same number of hops from any common source node.

**The core consequence:** sibling subgraphs that both receive arrows from the same parent node end up at the same rank. In `graph TB` that means side by side; in `graph LR` that means stacked vertically.

### Rule L1 — Match `direction` inside subgraphs to the desired internal layout, and keep it consistent

`direction TB` or `direction LR` inside a subgraph controls how that subgraph's own children are arranged, independent of the parent graph direction. Use it consistently across all subgraphs:

| Goal | Outer graph | `direction` inside subgraphs |
|---|---|---|
| Everything flows top to bottom | `graph TB` | `direction TB` everywhere |
| Subgraphs appear in columns, contents stack vertically in each column | `graph LR` | `direction TB` everywhere |

**Gotcha:** mixing `direction LR` inside a subgraph when the outer graph is `graph TB` creates horizontal pressure that pushes that subgraph sideways relative to its siblings. Use `direction TB` uniformly when you want a clean top-to-bottom layout.

### Rule L2 — Move hub nodes outside subgraphs that contain their sources

A hub node receives arrows from many sources (e.g., a shared AI model or database). When a hub lives *inside* a subgraph alongside its sources, Dagre places it at the same rank as those sources and pulls it sideways.

Fix: declare the hub node outside any subgraph. It then becomes a standalone tier between the source subgraph and the outputs.

```
%% ❌ wrong — hub pulled sideways to same rank as its sources
subgraph Guard["Guardrail"]
    AGUS[...]
    AGEU[...]
    Claude[...]   %% shares rank with agents, drifts to the side
end

%% ✅ correct — hub outside its source subgraph, becomes its own tier
subgraph Guard["Guardrail"]
    AGUS[...]
    AGEU[...]
end
Claude[...]       %% sits cleanly between Guard and Outputs
```

### Rule L3 — Use `~~~` invisible links to enforce rank ordering

When two nodes should be at different ranks but Dagre can't infer an ordering from real edges, add an invisible link — it creates a rank dependency without rendering an arrowhead or label:

```
A ~~~ B   %% B is forced to a rank after A; nothing visible is drawn
```

**When to add `~~~` in `graph TB`:**
- Between a node in one sibling subgraph and a node in the next sibling, when both share a common parent source (otherwise they'd land side by side at the same rank)
- Between a hub node and its first downstream node
- General pattern: one `~~~` per tier boundary that isn't already enforced by a real edge

**When to add `~~~` in `graph LR`:**
- Between a hub node and its downstream node (same as TB)
- Between the last node of one tier and the first of the next, when no real edge crosses the boundary
- Do **not** add `~~~` between siblings that should stack vertically — in `graph LR`, same-source siblings stack vertically by default; a `~~~` between them would push them into different horizontal columns instead

### Rule L4 — Never write `%%` comments trailing an edge on the same line

Mermaid's parser expects a newline or EOF after an edge target. A trailing `%%` comment is treated as a node string and causes a parse error:

```
%% ❌ parse error — "Expecting 'SEMI', 'NEWLINE', 'EOF' … got 'NODE_STRING'"
A ~~~ B   %% forces B after A
A -->|"label"| B   %% sends data

%% ✅ correct — comment on its own line above the edge
%% forces B after A
A ~~~ B
```

This applies to all edge types: `-->`, `-.->`, `~~~`, `---`, etc.

### Summary — TB vs LR recipe

**Clean `graph TB` (top-to-bottom flow):**
1. `direction TB` inside every subgraph
2. Hub nodes declared outside the subgraph that contains their sources
3. `~~~` between same-source sibling subgraphs — use one node from each subgraph, one hint per sibling pair
4. `~~~` from hub node to first downstream node if no real edge exists
5. All `%%` comments on their own lines, never trailing an edge

**Clean `graph LR` (left-to-right flow):**
1. `direction TB` inside every subgraph (stacks contents vertically within each column)
2. Hub nodes declared outside the subgraph that contains their sources
3. Do *not* `~~~` between same-source siblings — they already stack vertically in LR for free
4. `~~~` from hub node to first downstream node if no real edge exists
5. All `%%` comments on their own lines, never trailing an edge

## Handling existing files

When the skill is invoked with a path to an existing `.mmd` file, **always read the file first**, then:

1. **Check for missing frontmatter title** — if the file does not start with a `---\ntitle: ...\n---` block, add one derived from the file name and diagram content.
2. **Check for missing description comment** — if there is no `%%` comment immediately after the frontmatter, add one (one to three lines summarising what the diagram shows and the key point it makes).
3. **Check for missing Figma directive** — for `graph`/`flowchart` diagrams, add `%%{init: {"flowchart": {"htmlLabels": false}}}%%` if absent.
4. **Check for `<br/>` in labels** — replace all occurrences in `graph`/`flowchart` diagrams: use literal newlines in node labels `["..."]`, use `\n` in edge labels `-->|"..."|`.
5. **Check for `\n` in node labels** — in `graph`/`flowchart` diagrams, convert every `\n` inside node-shape brackets (`["..."]`, `[("...")]`, `(["..."])`, `{{"..."}}`, etc.) to a literal newline, with the continuation indented 4 spaces past the start of the opening line. Leave `\n` in edge labels `-->|"..."|` and subgraph titles `subgraph id["..."]` alone — those still need it.
6. **Check for `classDef` + `class` styling** — in `graph`/`flowchart` diagrams targeted at Figma, convert every `classDef ClassName fill:…,stroke:…,…` plus `class NodeA,NodeB ClassName` pair into per-node `style NodeA fill:…,stroke:…,…` / `style NodeB fill:…,stroke:…,…` directives, then delete the `classDef` and `class` lines. See "Style and color" above for an example.
7. Apply whatever additional edits the user requested.

Do not add the `%%{init}%%` directive to `sequenceDiagram` or `erDiagram` files — those diagram types do not use HTML labels.

## Output

When creating a new `.mmd` file:
1. Apply the full header template above.
2. Use **literal newlines** inside node labels `["..."]` and all other node-shape brackets, with continuation lines indented 4 spaces past the start of the opening line. Use `\n` only in edge labels `-->|"..."|` and subgraph titles `subgraph id["..."]`. Never use `<br/>`.
3. Save to the appropriate diagrams directory.
4. Confirm the file is renderable by checking for any `<br/>` remaining (there should be none in flowcharts) and any `\n` inside node-shape brackets (should be none — those should be literal newlines).

## Known gotcha — do not write `%%{` inside `%%` comments

Mermaid's tokeniser scans for `%%{` even inside `%%` comment lines. Writing something like:

```
%% Use the %%{init}%% directive to disable htmlLabels.
```

will cause a parse error (`Cannot convert undefined or null to object`). Always describe the directive in plain text instead:

```
%% Use the init directive to disable htmlLabels.
```
