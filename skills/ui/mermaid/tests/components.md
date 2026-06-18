# Mermaid for Figma — Component Library

Copy/paste reference for authoring `.mmd` files that survive the
`mmdc → bake-fills.py → drag into Figma` pipeline at full fidelity.

Every snippet below is taken from a working test diagram in this directory.
For a single file that exercises **every flowchart construct in one place**,
see [`shapes-test.mmd`](shapes-test.mmd). For sequence and ER variants, see
[`sequence-test.mmd`](sequence-test.mmd) and [`er-test.mmd`](er-test.mmd).

---

## 1. File header (always include)

```
---
title: Your Diagram Title Here
---
%% Describes what this diagram shows. One to three lines.
%%{init: {"flowchart": {"htmlLabels": false}}}%%
graph TB
```

- `---` block must be the very first content in the file.
- The `%%{init}%%` directive applies only to `graph` / `flowchart`.
  Leave it off for `sequenceDiagram` and `erDiagram`.

---

## 2. Node shapes

All shapes use the same labelling pattern: open bracket(s), `"text"`, close
bracket(s). For multi-line labels, put a **literal newline** inside the quotes
and indent the continuation **4 spaces past the start of the opening line**.

| Intent | Syntax | Renders as |
|---|---|---|
| Rectangle (default) | `Node["Plain rectangle"]` | square-cornered box |
| Rounded rectangle | `Node("Rounded box")` | rounded corners |
| Stadium / pill | `Node(["Stadium shape"])` | full-rounded ends — good for start/end nodes |
| Subroutine | `Node[["Subroutine"]]` | double-walled rectangle |
| Cylinder | `Node[("Cylinder")]` | database shape |
| Circle | `Node(("Circle"))` | full circle |
| Double circle | `Node((("Double circle")))` | concentric circles — good for terminal states |
| Asymmetric | `Node>"Asymmetric"]` | flag shape, one side angled |
| Diamond | `Node{"Decision"}` | diamond — good for decisions/branches |
| Hexagon | `Node{{"Hexagon"}}` | six-sided — preparation/process |
| Parallelogram | `Node[/"Parallelogram"/]` | slanted box — input/output |
| Parallelogram (reverse) | `Node[\"Reverse"\]` | slanted the other way |
| Trapezoid | `Node[/"Trapezoid"\]` | wider top |
| Trapezoid (reverse) | `Node[\"Reverse"/]` | wider bottom |

### Multi-line labels

```
%% Two lines — opening line is "Managed UI"
SPA["Managed UI
    (React + Amplify)"]

%% Three lines
Disc["Discovery Lambdas
    (Scheduler · Search · Update)
    runs daily"]
```

Continuation lines are indented **4 spaces past the start of the opening line**.
The closing `"]` aligns with the last continuation line's last character. Up
to 4 lines confirmed working in the bake; 5+ lines may need a vertical-centering
tweak in `bake-fills.py` pass 6.

### HTML entities

Use `&amp;`, `&lt;`, `&gt;` (or just literal `<` `>`). All survive the bake.

```
Node["Compares A &amp; B against C &lt; D"]
```

---

## 3. Edges and edge labels

```
%% Simple arrow
A --> B

%% Arrow with label
A -->|"Step 1"| B

%% Multi-line edge label — use \n, NOT a literal newline
A -->|"GraphQL\n+ WebSocket"| B

%% Dashed line, thick line, dotted
A -.-> B
A ==> B
A -.->|"Dashed with label"| B
```

Edge labels go through native `<text><tspan>` in mmdc's output (no
foreignObject), so they require no bake-time conversion. The label
background blob behind them gets neutralized to invisible by bake pass 7.

---

## 4. Subgraphs (clusters)

```
subgraph UI["UI"]
    User(["End User"])
    SPA["Managed UI
        (React + Amplify)"]
end

%% Multi-line subgraph titles use \n, not literal newlines
subgraph LF["Lambda Functions\n(18 total)"]
    ...
end
```

Nested subgraphs are supported (verified to one level of nesting; deeper
nesting is plausible but unverified):

```
subgraph Outer["Outer cluster"]
    subgraph Inner["Inner cluster"]
        A["Item"]
    end
end
```

---

## 5. Styling (Figma-compatible)

**Use per-node inline `style` directives.** Do not use `classDef` / `class`
— see test-4 in SKILL.md.

```
%% UI band — pink
style User    fill:#FCE7F3,stroke:#9D174D,stroke-width:1px,color:#111
style SPA     fill:#FCE7F3,stroke:#9D174D,stroke-width:1px,color:#111

%% System band — blue
style AppSync fill:#DBEAFE,stroke:#1E3A8A,stroke-width:1px,color:#111
style Backend fill:#DBEAFE,stroke:#1E3A8A,stroke-width:1px,color:#111

%% Data band — green
style DDB     fill:#D1FAE5,stroke:#065F46,stroke-width:1px,color:#111

%% External band — amber
style ExtAPI  fill:#FEF3C7,stroke:#92400E,stroke-width:1px,color:#111
```

Group `style` lines by visual band with a `%%` band comment. The repetition
is the cost of surviving `classDef`-strip in the Figma plugin path; the bake
script lifts these into direct SVG `fill="…"` attributes for native import.

### Suggested palette (used in `shapes-test.mmd`)

| Band | Fill | Stroke |
|---|---|---|
| UI | `#FCE7F3` | `#9D174D` |
| System | `#DBEAFE` | `#1E3A8A` |
| Data | `#D1FAE5` | `#065F46` |
| External | `#FEF3C7` | `#92400E` |

All four are light pastels so labels stay legible at `color:#111`.

---

## 6. Sequence diagrams

```
---
title: Your Sequence Diagram Title
---
%% What this sequence shows.
sequenceDiagram
    participant U as User
    participant GE as Gemini<br/>Enterprise

    U->>GE: Ask a question
    activate GE
    Note over GE: Process and<br/>plan
    GE-->>U: Response
    deactivate GE
```

Sequence diagrams use `<br/>` inside participant labels and notes — that's
Mermaid syntax, not HTML — and they don't use HTML labels at the SVG level.
Omit the `%%{init}%%` directive (it does nothing for sequence). For other
constructs (loops, alts, opts, parallels), see `sequence-test.mmd`.

---

## 7. ER diagrams

```
---
title: Your ER Diagram Title
---
%% What this entity model shows.
erDiagram
    USER ||--o{ ORDER : "places"
    USER {
        string id PK
        string email
        string name
    }
    ORDER {
        string id PK
        string user_id FK
        decimal total
    }
```

Cardinality syntax (Mermaid standard):

- `||--||` — one to one
- `||--o{` — one to zero-or-many
- `||--|{` — one to one-or-many
- `}o--o{` — zero-or-many to zero-or-many

The bake handles ER cardinality markers (crow's foot symbols) and
relationship lines via passes 4 and 5c. See `er-test.mmd` for a full example.

---

## 8. Build pipeline (full fidelity)

```sh
# Render to SVG via mermaid-cli
mmdc -i diagram.mmd -o diagram.svg

# Bake fills, text, edges, arrowheads, and foreignObject text into direct SVG attribs
python3 .claude/skills/mermaid/bake-fills.py diagram.svg
# → produces diagram.baked.svg

# Drag diagram.baked.svg into Figma's canvas (NOT through the Mermaid in Figma plugin)
```

If colors aren't load-bearing, the simpler workflow is to paste the `.mmd`
source into the Mermaid in Figma plugin with "Use HTML tags" unchecked — but
you'll get lavender defaults for fills, not the colors you wrote.

---

## 9. Validated reference diagrams

- [`shapes-test.mmd`](shapes-test.mmd) — every flowchart shape, nested
  subgraphs, multi-line labels, HTML entities. Use as the canonical
  copy/paste source when authoring a new flowchart.
- [`orientation-test-lr.mmd`](orientation-test-lr.mmd) — minimal `graph LR`
  layout.
- [`sequence-test.mmd`](sequence-test.mmd) — actors, sync/async messages,
  notes, activations, loop, alt.
- [`er-test.mmd`](er-test.mmd) — entities with attributes, three
  relationship cardinalities, relationship labels.

Each has a sibling `.svg` (mmdc output), `.png` (reference render), and
`.baked.svg` (Figma-ready). When the bake script changes, re-run all four
through it and eyeball the resulting baked SVGs in Figma to catch
regressions.
