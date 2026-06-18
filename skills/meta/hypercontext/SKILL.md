---
name: hypercontext
description: Render session state as spatial ASCII map showing threads, activity heat, files, tools, and context runway. Use when user says "/hypercontext", "/hypercontext compact", "/hypercontext threads", or "/hypercontext heat."
allowed-tools: []
---

*Created by [Danielle Fong](https://daniellefong.com/) · [𝕏](https://x.com/DanielleFong)*
*Packaged by [Minda Myers](https://mindamyers.com) · [𝕏](https://x.com/MindaMyers) · [GitHub](https://github.com/Minda) · [skills repo](https://github.com/Minda/skills)*

# Hypercontext — Spatial Context Awareness
 
**Trigger:** User says `/hypercontext`, `/hypercontext compact`, `/hypercontext threads`, or `/hypercontext heat`

## Purpose

Render session state as a spatial ASCII map showing threads, activity heat, files, tools, and runway. Self-awareness as UX.

## Commands

- `/hypercontext` — full visualization
- `/hypercontext compact` — markdown format for continuation prompts (use at 70%+ context)
- `/hypercontext threads` — thread-specific view
- `/hypercontext heat` — activity heat map

## Output Format

### Full Visualization

```
HyperContext: Session State
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Context: ~45% (90k/200k)
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░░░░░░░░░░

Runway: ~110k tokens
Velocity: ▁▂▃▅▆▇▇█ (accelerating)

Threads:
┌─────────────────┐
│ ✅ Setup Redis  │
└─────────────────┘
        │▼
┌─────────────────┐  ┌──────────────┐
│ ⏳ Auth Flow    │  │ 💡 API Cache │
└─────────────────┘  └──────────────┘

Heat:
  auth.ts          ████
  redis.config.ts  ███░
  app.ts           ██░░
  types.ts         ░░░░

Files:
  ◆ src/auth.ts
  ◆ config/redis.config.ts
  ◇ src/types.ts
  ◇ lib/utils.ts

Tools:
  Edit  ████████ (8)
  Read  ██████ (6)
  Bash  ███ (3)

Systems:
  ✅ Git
  ✅ npm
```

### Compact Mode (for continuation prompts)

```
**Context:** ~45% (90k/200k) | Runway: ~110k | Velocity: ▁▂▃▅▆▇▇█
**Threads:** ✅ Setup Redis → ⏳ Auth Flow ∥ 💡 API Cache
**Hot:** auth.ts, redis.config.ts | **Modified:** auth.ts, redis.config.ts
**Tools:** Edit(8), Read(6), Bash(3) | **Systems:** Git, npm
```

## Implementation Details

### Context Bar

- 35 characters total
- `▓` = used, `░` = remaining
- Budget: 200k tokens
- Estimation formula: `5000 + (turns × 2000) + (files_read × 2000) + (skills × 2000)`
- Round to nearest 5%

### Velocity Sparkline

- 8 characters: `▁▂▃▄▅▆▇█`
- Left = early session, right = recent
- Reflects actual activity patterns (don't fake it)

### Thread Status

- `✅` = completed
- `⏳` = in progress
- `❌` = blocked
- `💡` = idea/planned

**Layout:**
- Dependencies: stack vertically with `│▼`
- Parallel work: side-by-side

**Limit:** Show 3-6 most relevant threads

### Heat Ranking

**Pure recency only** — no importance guessing

- `████` = most recent
- `███░` = recent
- `██░░` = less recent
- `░░░░` = stale

Show 4-6 items, ranked by last access time.

### File Tracking

- `◆` = modified
- `◇` = read-only
- Show last 2-3 path segments
- Sort by most-changed first

### Tools & Systems

**Tools:** Bar-scaled usage counts
**Systems:** Mark `✅` if contacted this session

## The Integrity Rule

**Don't hallucinate.**

Every thread, file, tool count, and system status must reflect what **actually happened** in this session. No assumptions, no fake data, no aspirational threads.

If uncertain about a metric, omit it or mark it as estimated.

## Context Optimization Recommendations

At **~70% context usage**, recommend:
- Switching to compact mode
- Finishing current threads
- Considering a fresh session for new work

## Example Interactions

**User:** `/hypercontext`
→ Show full ASCII visualization

**User:** `/hypercontext compact`
→ Show dense markdown format

**User:** `/hypercontext threads`
→ Focus on thread dependencies and status

**User:** `/hypercontext heat`
→ Show activity heat map with recency ranking

## Install

`npx skills add Minda/skills` — then select **hypercontext** when prompted.
