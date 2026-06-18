# Example: Feature Usage (Categories)

**Input data:** Which features users actually use  
**Data:** Feature counts from 100 active users  
**Pattern:** Highly unbalanced—few features account for most usage  

---

## Feature Usage Analysis

### 1. Frequency Distribution

```
Feature           Count  Proportion
────────────────────────────────────
Search            ████████████████  45  (45%)
Export            ████████          20  (20%)
Filter            █████             12  (12%)
Share             ████              10  (10%)
Duplicate         ██                 8   (8%)
Archive           ░                  3   (3%)
Settings          ░                  2   (2%)

Observation:
Top 3 features = 77% of usage
Bottom 4 features = 23% of usage

Heavily skewed. Not balanced.
```

### 2. Concentration Index

```
If users loved all features equally: ▁▁▁▁▁▁▁ (flat)
If all users use one feature:        ████████ (peak)

Reality (your data):                 ▆▃▂▂▁░░ (skewed)
                                     ↑ dominated by top 2
```

### 3. Diversity Measure

```
"How many different features does a typical user use?"

Coverage by % of users:
Just Search:        5%  (only use 1 feature)
Search + 1 more:   30%  (use 2 features)
Search + 2 more:   40%  (use 3 features)
Search + 3+ more:  25%  (power users)

Interpretation:
Most users are minimal (1–2 features).
Power users are minority.
Search is essential. Others are optional.
```

### 4. Feature Tiers

```
Tier 1 (essential):  Search (45%)
                     └─ If you remove: lose 45% engagement

Tier 2 (important):  Export (20%), Filter (12%)
                     └─ Combined 32% of usage

Tier 3 (nice-to-have): Share (10%), Duplicate (8%)
                     └─ Combined 18% of usage

Tier 4 (rarely used): Archive (3%), Settings (2%)
                     └─ Combined 5% of usage

Maintenance burden vs. usage ratio:
  Archive & Settings: 2 features, 5% usage
  Export & Filter:    2 features, 32% usage ← better ROI
```

### 5. Pareto Analysis (80/20 Rule)

```
How many features needed to hit 80% usage?

Top 1 (Search):           45%  (need more)
Top 2 (Search + Export):  65%  (getting close)
Top 3 (+ Filter):         77%  (almost there)
Top 4 (+ Share):          87%  ← Hit 80%

Finding:
Just 4 out of 7 features give 87% of value.

If you only built 4 features, you'd get ~85% of value
without 3 lower-tier features.
```

### 6. Outlier Features (Surprisingly Popular/Unpopular)

```
Expected vs. Actual:

Share:         Expected 15%, Actual 10% ⚠️ underperforming
               (Has potential—maybe UX barrier?)

Archive:       Expected 8%, Actual 3% ⚠️ nobody uses
               (Is it discoverable? Is it needed?)

Search:        Expected 20%, Actual 45% ⭐ overperforming
               (Your killer feature. Protect it.)
```

---

## Components Used

| Component | Purpose | Finding |
|-----------|---------|---------|
| Frequency rank | Order by usage | Search dominates |
| Concentration | Balance check | Heavily skewed |
| Diversity | Variety measure | Most users minimal |
| Pareto | Core features | Top 4 of 7 give 87% |
| Outlier | Surprises | Archive unused, Share underperforms |

---

## Interpretation

**One-sentence summary:**  
"Search is your killer feature (45%). Three features rarely used (8% combined)."

**Follow-up questions:**
1. Why is Search so dominant? (Is it the entry point? Best feature?)
2. Why are Archive and Settings barely used? (Hidden? Not needed?)
3. Is Share underperforming due to UX or lack of use case?
4. Should you kill rarely-used features, or improve them?
5. Can you improve Export to rival Search's popularity?

**Next actions:**
- **Protect Search:** Make sure it's rock-solid. It's your moat.
- **Investigate underperformers:** Is Archive's low use intentional (users don't need) or fixable (UX issue)?
- **Consider consolidation:** If Archive + Settings = 5% usage, maybe merge them and simplify.
- **Invest in Tier 2:** Export and Filter are solid. Can you make them better to increase share?
- **Test Share:** Experiment with UX. If you could hit 15%, that's +5 percentage points.

---

## How Lowkey-Viz Helped

**Without it**, you might think:
- "All features get used" ← Wrong! 40% of value is Search
- "Features are balanced" ← Wrong! Skewed heavily
- "Archive is important because it exists" ← Not backed by data
- "I should improve everything equally" ← Wrong strategy

**With it**, instantly:
- Skew is visible (not flat distribution)
- Pareto insight: 4 features = 87% of value
- Outliers identified: Archive/Settings are ghosts
- Search is flagged as critical (protect it!)

**Result:** You prioritize ruthlessly. You know what matters to users. You can make build decisions based on actual usage.

---

## Real-World Application

This same pattern would work for:
- **User permissions:** Which capabilities do people actually grant?
- **Config options:** Which settings do users actually change?
- **Menu items:** Which actions do users click?
- **API endpoints:** Which are actually called?
- **Product features:** Which do users enable?

The components stay the same; only the data changes.

---

## Extension: Feature Combinations

```
Users who use Search:           100% (everyone)
Users who use Search + Export:   44% (strong pairing)
Users who use Search + Filter:   27% (also popular)
Users who use all 3:             18% (minimal overlap)

Implication:
Export and Filter are independent use cases.
Not everyone needs both.
Reflects different user workflows.
```

This is why simplistic UI (export one button) works—
not all users need both options visible.
