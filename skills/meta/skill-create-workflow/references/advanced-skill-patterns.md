# Advanced Skill Patterns

This guide covers six advanced patterns that distinguish polished, production-quality skills from basic ones. Each pattern includes the problem it solves, questions to ask when designing, and a full example using a hypothetical **"data-report-builder"** skill.

---

## 1. Progressive Disclosure / File Structure

**The problem:** Skills aren't flat documents. Loading everything into context every time wastes tokens and confuses Claude. Real skills keep the main SKILL.md lean and push detailed reference material into separate files that only get loaded when relevant.

**What to ask the person requesting the skill:**

> What information does Claude need *every single time* this skill runs vs. only in certain situations?

### Example — Directory structure

```
data-report-builder/
├── SKILL.md                    ← Always loaded. Core workflow, routing logic, ~200 lines max.
├── references/
│   ├── chart-guide.md          ← Loaded only when the report needs charts
│   ├── financial-formatting.md ← Loaded only for financial reports
│   ├── narrative-style.md      ← Loaded only when report includes written analysis
│   └── table-patterns.md       ← Loaded only when complex tables are involved
├── scripts/
│   ├── render_chart.py         ← Called to produce chart PNGs from data
│   └── validate_report.py      ← Called at the end to check the output
└── assets/
    ├── report-template.docx    ← Starting point for DOCX reports
    └── fonts/                  ← Bundled fonts for PDF output
```

### Example — What goes in SKILL.md (always loaded)

```markdown
# Data Report Builder

## Workflow
1. Identify report type (financial, operational, executive summary)
2. Load the appropriate reference:
   - Financial reports → read `references/financial-formatting.md`
   - Reports with charts → read `references/chart-guide.md`
   - Reports with narrative sections → read `references/narrative-style.md`
3. Process data and build report
4. Run validation

## Quick Reference
| Report type        | Reference to load            | Output format |
|--------------------|------------------------------|---------------|
| Financial          | financial-formatting.md      | XLSX + PDF    |
| Executive summary  | narrative-style.md           | DOCX          |
| Operational        | table-patterns.md            | PDF           |
```

### Example — What goes in a reference file (loaded on demand)

```markdown
# references/financial-formatting.md

## Number Formatting