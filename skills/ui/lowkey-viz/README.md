# Lowkey Viz

**Bootstrap-style TUI components for data exploration.**

## What's Here

```
lowkey-viz/
├── SKILL.md              # Main skill documentation
├── README.md             # You are here
├── components/           # Individual pattern components
│   ├── sparkline.md
│   ├── histogram.md
│   ├── outlier-detector.md
│   ├── distribution.md
│   ├── timeline.md
│   ├── heatmap.md
│   └── ...
├── examples/             # How to use on real data
│   ├── example-numbers.md
│   ├── example-timeseries.md
│   ├── example-categories.md
│   └── example-paired-data.md
├── reference/            # Pattern library & guidelines
│   ├── all-components.md
│   ├── when-to-use.md
│   └── philosophy.md
```

## Quick Concept

Think **Bootstrap for data exploration:**

| Bootstrap | Lowkey Viz |
|-----------|-----------|
| Provides button, card, grid components | Provides sparkline, outlier, distribution components |
| You choose which to use | You choose which visualization reveals patterns |
| Mix & match for your layout | Mix & match for your data |
| Not a framework, a toolkit | Not a dashboard, a pattern library |

## Usage

```
Input any data:
  "12, 14, 15, 15, 16, 18, 19, 52"
  "Jan: 100, Feb: 120, Mar: 135"
  List of names or categories
  
Output: Multiple Markdown visualizations showing:
  • Patterns (sparkline, distribution)
  • Surprises (outliers, anomalies)
  • Edges (min, max, extremes)
  • Abstract understanding (what's the shape?)
  
All in one .md file, ready to read immediately.
```

## Core Idea

Not "here's how to build a dashboard"  
But "here's how to understand any dataset at a glance"

- **Fast:** Scan in <1 minute
- **Low-token:** Plain Markdown, no SVG/HTML/React
- **Pattern-focused:** Reveals surprising things
- **Exploration-first:** Before deep analysis

## Components Available

**Shape & Distribution:**
- Sparkline — 1-line trend
- Histogram — Frequency bands  
- Percentile — Spread & center
- Density — Packed vs sparse

**Anomalies:**
- Outlier markers — Flag surprises
- Cliff detection — Sudden changes
- Deviation — What breaks pattern

**Relationships:**
- Scatter (text) — Correlation
- Pairing matrix — Which go together

**Time:**
- Timeline — Changes over time
- Cycle detection — Repeating patterns
- Event overlay — Causes visible changes

**Composition:**
- Pie-as-text — Proportions
- Stacked bar — Part-to-whole
- Heatmap — Density by category

**Diversity:**
- Frequency rank — Most common
- Diversity index — Variety level
- Concentration — How clustered

**Completeness:**
- Coverage — Missing data
- Gaps — Holes in sequence

## Philosophy

**Data exploration ≠ beautiful dashboards**

Lowkey-viz helps you ask better questions:
- "What's unusual about this data?"
- "What's the typical range?"
- "Is this pattern real or noise?"
- "What surprised me?"

Then you decide what to do next.

---

For full docs, see `SKILL.md` in this folder.
