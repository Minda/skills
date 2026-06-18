# Example: Growth Metrics (Time Series)

**Input data:** Monthly user growth  
**Data:** Jan: 100, Feb: 120, Mar: 135, Apr: 130, May: 145, Jun: 155  
**Duration:** 6 months  
**Pattern:** Mostly growing, one plateau  

---

## Growth Metrics Analysis

### 1. Mini Timeline (Changes Over Time)

```
Jan │ 100
Feb │ 120  ↑ +20 (+20%)
Mar │ 135  ↑ +15 (+12%)
Apr │ 130  ↓ -5  (-4%) ← pause
May │ 145  ↑ +15 (+12%)
Jun │ 155  ↑ +10 (+7%)

Trend: Mostly growing. One month plateau.
```

### 2. Sparkline (Pattern Shape)

```
Pattern: ▁▂▃▃▄▅

Tells you:
• Steady growth overall
• One pause/dip in middle
• Then resume
• Trajectory still up

Not a straight line—has variation.
```

### 3. Growth Rate Analysis

```
Month   Value  Growth  Rate
────────────────────────────
Jan     100    —       —
Feb     120    +20     +20%
Mar     135    +15     +12%
Apr     130    -5      -4%   ⚠️ unexpected pause
May     145    +15     +12%
Jun     155    +10     +7%

Expected trend (if continuing Feb):
Feb: +20%, Mar: +20%, Apr: +20%... ✗
Reality: March slows to +12%, April dips

Question: What happened in April?
```

### 4. Cumulative Growth

```
Total growth Jan→Jun: 100→155 = +55 users (+55%)

Month-by-month contribution:
Feb: 20 new users  ████████████
Mar: 15 new users  ██████████
Apr: -5 lost users ██← churn?
May: 15 new users  ██████████
Jun: 10 new users  ███████

Observation:
April is the anomaly. All other months add users.
```

### 5. Slope Detection (Acceleration)

```
Jan→Mar: Steep growth (20→15 per month)
        ╱
      ╱
    ╱
   ╱
   
Mar→Apr: Flat/negative (loses users)
  ──  ← plateau, then cliff

Apr→Jun: Modest recovery (15→10 per month)
         ╱
       ╱
     ╱

Interpretation:
Growth is slowing over time, even excluding April dip.
Feb was strongest month. Now around 10/month.
```

### 6. What's Normal?

```
Jan-Mar trend: +17.5 avg per month (steep)
May-Jun trend: +12.5 avg per month (moderate)
Apr:           -5 (anomaly)

If trend continues at Jun rate (+10/mo):
Jul: ~165 ✓ (continues)

If reverting to Feb rate (+20/mo):
Jul: ~175 ✗ (return to growth? unlikely)
```

---

## Components Used

| Component | Purpose | Finding |
|-----------|---------|---------|
| Timeline | Changes over time | Steady growth with April dip |
| Sparkline | Shape | Up-pause-up pattern |
| Growth rate | Trend direction | Slowing over time |
| Slope detection | Acceleration | Was steep, now moderate |

---

## Interpretation

**One-sentence summary:**  
"Growing 10–20 users/month, but April had unexpected drop and growth is moderating."

**Follow-up questions:**
1. What happened in April? (Bug? Marketing pause? Churn event?)
2. Why is growth slowing (Feb: +20%, Jun: +7%)?
3. Is 10 users/month acceptable for your goals?
4. How many users do you need before expanding?
5. Can you predict Jun→Jul trend?

**Next actions:**
- **Investigate April:** Was it churn, refund, or marketing pause?
- **Understand slowdown:** Is it natural (diminishing return) or problematic (saturation)?
- **Forecast:** If trend continues, when do you hit 300 users? 500?
- **Set goals:** Is 155 users enough? Or scale more needed?

---

## How Lowkey-Viz Helped

**Without it**, you might observe:
- "We grew from 100 to 155" ← True but vague
- "June is better than January" ← True but obvious
- "Growth is stable" ← Wrong! April is anomaly

**With it**, instantly:
- Shape shows April is unusual (every other month positive)
- Rate shows growth is slowing (20% → 7%)
- Timeline shows momentum stalled then resumed
- Outlier is isolated for investigation

**Result:** You see the April event is the story, not the overall growth. You ask better follow-up questions faster.

---

## Real-World Application

This same pattern would work for:
- **Signup funnel:** Daily signups → spot day with drop-off
- **API calls:** Daily volume → spot when usage pattern changes
- **Support tickets:** Weekly volume → see if backlog growing/shrinking
- **Any metric tracked over time:** Spot anomalies and trend shifts

The components stay the same; only the data changes.
