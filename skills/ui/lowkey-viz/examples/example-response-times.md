# Example: Response Times (Numbers with Outlier)

**Input data:** API response times in milliseconds  
**Data:** 23, 24, 25, 26, 25, 24, 1200, 25, 26  
**Size:** 9 measurements  
**Pattern:** Mostly consistent, one extreme  

---

## Response Times Analysis

### 1. Sparkline (Pattern Shape)

```
Pattern: ▁▂▂▂▂▂█▂▂

This tells you:
• Left side: Flat (stable values)
• Middle: Flat (stable values)
• Peak: One giant spike
• Right side: Back to flat

Interpretation: Mostly predictable, one anomaly
```

### 2. Outlier Detection

```
23  24  25  26  25  24  ⚠️1200  25  26
                        ↑ 50x higher!

What surprised you?
One request took 50 times longer than typical.
```

### 3. Distribution (Without Outlier)

```
Typical range (23-26ms):
████████████████████████████ 8 responses

Outlier (1200ms):
█ 1 response (extreme)

Observation:
If you remove the outlier, this data is dead boring—
every response is nearly identical.
That outlier is the story here.
```

### 4. Percentile Bands (Spread & Center)

```
              p10   p25   p50   p75   p90
              │     │     │     │     │
Normal range  ├─────┤─────┤─────┤─────┤
              23    24    25    26    26 (ms)
              
Outlier completely outside this range.
```

### 5. What Changed Interpretation

**Median (middle value):** 25 ms  
**Range (typical):** 23–26 ms  
**Outlier:** 1200 ms  

**Questions this raises:**
- What was different that one time?
- Cache miss? Resource contention? Cold start?
- Is it repeatable?
- Does it matter (is 1200ms acceptable)?

### 6. Statistics

```
Metric                Value
────────────────────────────
Count                 9
Median (p50)          25 ms
Typical range         23–26 ms
Min (normal)          23 ms
Max (normal)          26 ms
Outlier               1200 ms

Spread within normal:  3 ms (very tight)
Outlier deviation:     +1175 ms from median
Outlier ratio:         1/9 = 11% of requests slow
```

---

## Components Used

| Component | Purpose | Finding |
|-----------|---------|---------|
| Sparkline | Shape | One spike, otherwise flat |
| Outlier markers | Anomalies | One extreme value |
| Distribution | Frequency | 8 fast, 1 slow |
| Percentile | Spread | Very tight in normal range |

---

## Interpretation

**One-sentence summary:**  
"Almost all requests are 23–26ms. One request took 1200ms."

**Follow-up questions:**
1. What caused the 1200ms spike?
2. Does it happen every run or intermittent?
3. Is 1200ms acceptable for your SLA?
4. Is the 25ms median acceptable?
5. Is the 3ms spread good (consistent) or bad (variable)?

**Next actions:**
- If 1200ms is unacceptable: Debug that case
- If 25ms is too slow: Optimize everything
- If 25ms is fine: Current performance is good, just monitor outliers
- If 3ms spread is too variable: Investigate consistency

---

## How Lowkey-Viz Helped

Without it, you might think:
- "Average is probably 100ms" ← Wrong
- "All requests are similar" ← Mostly true, but misses story
- "This data is boring" ← Until you see the outlier

With it, instantly:
- Shape is visible (flat + spike)
- Outlier is flagged (50x larger)
- Typical behavior isolated (23–26ms cluster)
- Anomaly ratio shown (11% slow)

**Result:** You understand your data in <30 seconds instead of 30 minutes of analysis.
