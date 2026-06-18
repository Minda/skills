---
name: lowkey-viz
description: Bootstrap-style TUI components for data exploration. Generate Markdown visualizations that reveal patterns, outliers, edges, and enable abstract understanding of any dataset.
slash_commands:
  - command: lowkey-viz
    description: Analyze a dataset and generate discovery visualizations (patterns, surprises, edges)
  - command: lowkey-viz component
    description: Get a specific component (distribution, timeline, correlation, outlier-detector, etc.)
  - command: lowkey-viz reference
    description: Browse all available pattern components
---

*[Minda Myers](https://mindamyers.com) · [GitHub](https://github.com/Minda) · [skills repo](https://github.com/Minda/skills)*

# Lowkey Viz

**Bootstrap for data exploration.** Generate Markdown visualizations that surface patterns, surprises, and edges in any dataset.

## What It Does

Takes raw data and generates **a series of text-based visualizations** designed to help you understand at a glance:

- **Patterns** — Trends, distributions, clustering, repeating structures
- **Surprises** — Outliers, anomalies, unexpected values, breaks in pattern
- **Edges** — Boundaries, extremes (min/max), thresholds, limits
- **Abstract understanding** — High-level shape of the data without deep analysis

All outputs are **plain Markdown** with Unicode characters—low token cost, no dependencies.

## Quick Start

```
/lowkey-viz [your data]
→ Returns .md file with multiple visualizations

Example inputs:
  "12, 14, 15, 15, 16, 18, 19, 52"
  "Jan: 100 users, Feb: 120, Mar: 135, Apr: 130, May: 145"
  "response times: 23ms, 24ms, 25ms, 26ms, 1200ms, 25ms"
  [list of names] "sort by frequency and show diversity"

/lowkey-viz component distribution
→ Just the distribution component

/lowkey-viz reference
→ Browse all available pattern types
```

## Philosophy: Bootstrap for Data

**Bootstrap (HTML/CSS/JS):**
- Provides reusable components (buttons, cards, grids)
- You choose which to use and combine
- Flexible, not opinionated about full layouts
- Designed for rapid iteration

**Lowkey-viz (Text data):**
- Provides reusable visualizations (sparkline, outlier-markers, distribution, timeline, heatmap, etc.)
- You grab what's useful for YOUR data
- Flexible patterns, not pre-built dashboards
- Designed for rapid exploration

## Component Library

### 1. Distribution & Shape

**Sparkline** — Compact 1-line trend
```
Data: 12, 14, 15, 15, 16, 18, 19, 52
Sparkline: ▁▂▂▂▃▄▄█
```

**Histogram** — Frequency distribution in bands
```
       1 │ █
       5 │ █████
      10 │ ██████████
      15 │ ███████
       1 │ █  ← outlier
```

**Density markers** — Show packed vs sparse regions
```
20-30:   ████████████████████  (dense)
30-40:   ████                  (sparse)
40-50:   ██████                (medium)
```

**Percentile bands** — Understand spread
```
p10    p25    p50    p75    p90
┤├──────┤├──────┤├──────┤├─→
10     25     50     75    90
       ↑ median
       middle 50% of data
```

### 2. Outliers & Anomalies

**Outlier markers** — Flag unusual values
```
Data: 12, 14, 15, 15, 16, 18, 19, 52
      12  14  15  15  16  18  19 ⚠️52 ← surprise!
               ↑ typical range
```

**Deviation from expected** — Show what breaks pattern
```
Month    Value   Expected  Deviation
Jan      100     ────      ────
Feb      120     100+10%   ✓ on track
Mar      135     120+10%   ↑ +12.5% (faster growth)
Apr      130     135+10%   ↓ -3.7% (slowdown)
```

**Cliff detection** — Find sudden changes
```
Timeline: 25, 25, 26, 24, 25, 26, 1200, 25, 24
                              ↑ cliff (50x jump)
               stable         unstable
```

### 3. Correlation & Relationship

**Two-variable scatter** — Show relationship (text style)
```
Y high   ·  ·           ← no clear pattern
         ·  ·  ·
         ·     ·
Y mid    ·  ·  ·
         ·  ·  ·
Y low    ·  ·  ·        ← weak positive slope
         ·  ·     ·
         X low   X high
```

**Pairing matrix** — Which categories appear together
```
            A   B   C   D
        ───────────────────
    A  │  —  ●●  ●   ●●●
    B  │  ●●  —  ◇   ●●
    C  │  ●   ◇   —   ○
    D  │ ●●●  ●●  ○   —

● strong | ◇ medium | ○ weak | — none
```

### 4. Time Series & Sequences

**Mini timeline** — Show pattern over time
```
2024 ─────────────────────────────────→ 2026
Jan │ 100
Feb │ 120  ↑ growing
Mar │ 135  ↑
Apr │ 130  ↓ plateaus
May │ 145  ↑ resumes
```

**Event markers** — Overlay events on timeline
```
Value  │     ╱╲
       │    ╱  ╲      ╱─
       │ ╱─╲    ╲────╱
       │╱    ╲
Time   ├──────┼──────┼──
     Event   Event  Event
       ↑ causes visible changes?
```

**Cycle detection** — Find repeating patterns
```
Mon Tue Wed Thu Fri Sat Sun
 50  52  51  50  49  70  71  ← weekday vs weekend
 51  50  52  51  48  72  69
 49  51  50  51  50  71  70
      ↑ consistent weekday pattern?
```

### 5. Composition & Categories

**Pie-as-text** — Show proportions
```
Category A  ████████████████████░  78%
Category B  ████░                  15%
Category C  ██░                    7%
            ↑ Total 100%
```

**Stacked bar** — Part-to-whole relationships
```
Product  │ Small  │ Medium │ Large
────────────────────────────────────
Widget A │ ████   │ ███    │ ██
Widget B │ ██     │ █████  │ ████
Widget C │ █████  │ ██     │ █

Where does growth come from?
```

**Grouping heatmap** — Density within categories
```
          Sun  Mon  Tue  Wed  Thu  Fri  Sat
Morning   ░░░  ███  ███  ███  ███  ███  ░░░  (weekday peak)
Midday    ▓▓▓  ░░░  ░░░  ░░░  ░░░  ░░░  ▓▓▓  (weekend peak)
Evening   ░░░  ▓▓▓  ▓▓▓  ▓▓▓  ▓▓▓  ▓▓▓  ░░░  (weekday peak)
```

### 6. Diversity & Uniqueness

**Diversity index** — Variety in data
```
Data: A, A, A, B, B, C
Diversity: ░░░░░░░ (low)
All same type? No. Dominated by one? Yes.

Data: A, B, C, D, E, F (all different)
Diversity: ████████ (high)
Even distribution? Yes.
```

**Frequency distribution** — Rank by occurrence
```
apple      ████████████████ 45%
banana     ███████░          20%
cherry     █████░            14%
date       ████░             11%
elderberry ██░               10%

Balanced? No. Top item dominates.
```

**Concentration measure** — How clustered?
```
Sample of 100 items:
                      Count of Category
Concentration Low  ▁▂▃▄▅▆▇█ many categories
Concentration Med  ▃▃▅▅▇▇  few categories
Concentration High █████   one/two dominate
```

### 7. Completeness & Gaps

**Missing data visualization** — Show coverage
```
Field      Complete
Name       ███████████████████  100%
Email      ██████████░░░░░░░░░  50%
Phone      ███░░░░░░░░░░░░░░░░  15%
Address    ░░░░░░░░░░░░░░░░░░░  0%

Coverage by importance? Address unused?
```

**Gap detection** — Find holes
```
Dates: Jan 1, Jan 3, Jan 4, Jan 7, Jan 8, Jan 9
            ↑ gap     ↑ gap     ↑ gap
       2 days    3 days   0 days
Expected: daily, but irregular
```

## Component Reference

| Component | Use When | Shows |
|-----------|----------|-------|
| Sparkline | Quick pattern | Trend shape |
| Histogram | Understand shape | Frequency distribution |
| Percentile | Context | Spread & center |
| Outlier | Spot anomalies | Unusual values |
| Scatter | Find relationships | Correlation |
| Timeline | Track changes | Temporal pattern |
| Pie-as-text | Show parts | Proportions |
| Heatmap | Understand density | Concentration |
| Diversity | Assess variety | Uniqueness |
| Gaps | Check completeness | Missing data |

## Input Formats

### Numeric data
```
Numbers: 12, 14, 15, 15, 16, 18, 19, 52
Timeseries: Jan: 100, Feb: 120, Mar: 135
Matrix: [[1,2,3], [4,5,6]]
```

### Categorical data
```
Names: Alice, Bob, Charlie, Alice, Dave, Bob, Bob
Categories: red, blue, red, green, blue, red
Text: "what patterns do you see in this"
```

### Mixed/complex
```
Paired: (age, income), (24, 50k), (35, 80k), (45, 75k)
Events: "March: 3 sales, April: 5 sales, May: 2 sales"
Ranges: "responses from 10ms to 5000ms"
```

## Output: Always Markdown

- **Pure text** — Unicode + spaces only
- **No SVG, HTML, React** — Token efficient
- **Self-contained** — No external renders
- **Scannable** — Works in terminals, email, docs
- **Explorable** — Multiple views of same data

## Workflow

```
1. You provide data (any format)
   ↓
2. Lowkey-viz generates insights
   ├─ What's the distribution?
   ├─ Are there outliers?
   ├─ What's the range?
   ├─ Is it balanced?
   └─ What surprised you?
   ↓
3. You get .md file with visualizations
   ├─ Sparkline (shape at a glance)
   ├─ Outlier markers (surprises)
   ├─ Distribution (understand spread)
   ├─ Edge values (extremes)
   └─ Interpretation (what does this mean?)
   ↓
4. You scan in <1 minute, understand your data
```

## Example: Numbers With Outlier

**Input:**
```
Response times: 23, 24, 25, 26, 25, 24, 1200, 25, 26
```

**Output:**

```
Response Times Analysis
═══════════════════════════════════════════════

Sparkline (pattern shape)
▁▂▂▂▂▂█▂▂

Outlier detection
23  24  25  26  25  24  ⚠️1200  25  26
                        ↑ 50x higher than others

Distribution (without outlier)
23-26ms: ████████████████████████  9 responses
1200ms:  ░                        1 response (extreme)
         ↑ typical range          ↑ anomaly

Stats
Normal range:  23-26 ms
Outlier:       1200 ms (unusual spike)
Surprise:      One request took 50x longer
Pattern:       Otherwise very consistent

Interpretation
Mostly fast & consistent. One timeout/slow response.
Need to investigate what happened at that point.
```

## Workflow: All Data Types

**Numbers:** Sparkline → Histogram → Outliers → Percentiles  
**Time series:** Mini timeline → Cycles → Trend → Cliff detection  
**Categories:** Frequency → Diversity → Concentration  
**Two vars:** Scatter → Correlation strength → Pairing  
**Temporal + categories:** Heatmap → Cycles + categories → Events  

## When to Use

✓ Exploring unfamiliar dataset  
✓ Spotting patterns before analysis  
✓ Communicating data shape to others  
✓ Finding anomalies quickly  
✓ Understanding extremes (min/max/edges)  
✓ Low-token pattern discovery  

✗ Precise statistical analysis (use stats tools instead)  
✗ Large datasets (tables >1000 rows—sample first)  
✗ Animated/interactive (use HTML/React instead)  

## Philosophy Notes

**Bootstrap analogy works because:**
- Bootstrap doesn't tell you HTML structure; you do
- Bootstrap provides reusable styled components
- You mix and match what's useful
- Same here: I provide visualization components
- You decide which reveal patterns in YOUR data
- No pre-built dashboard assumptions

**Low-token by design:**
- Markdown is ~0.3 tokens/char
- HTML is ~0.4+ tokens/char  
- SVG is even heavier
- Text-based: 1000-char viz = ~300 tokens
- vs. HTML equivalent = ~500+ tokens

**Data exploration, not reporting:**
- Goal: understanding shape, not beautiful output
- Multiple angles on same data
- Quick iteration, not polish
- Surprises matter more than accuracy
- Help you ask better questions

---

## Related Skills

- **dashboard-viz** — Pre-built dashboard layouts (for when you know what you're building)
- **notebook** — Statistical analysis (when you need precision)
- **tui-viz-library** — Reference of all text-based characters
