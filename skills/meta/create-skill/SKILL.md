---
name: create-skill
description: Collaborative skill-creation workflow. Guides you through building a new Claude Code skill by working through a structured worksheet — invocation, workflow shape, failure modes, file structure, and more. Use when you want to create a new skill or understand how to structure one.
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep]
argument-hint: "<skill idea or name — or leave blank to start from scratch>"
---

*[Minda Myers](https://mindamyers.com) · [𝕏](https://x.com/MindaMyers) · [GitHub](https://github.com/Minda) · [skills repo](https://github.com/Minda/skills)*

# /create-skill

Collaborative skill creation. Works through 11 structured questions with you — invocation, workflow shape, failure modes, file layout — and builds the SKILL.md from your answers.

> Built on Anthropic's official [`skill-creator`](https://github.com/anthropics/skills) skill, adapted for skills with **longer workflows, branching elements, and iterative refinement cycles** — the kind where a single linear pass isn't enough to get it right.

## Invocation

**With argument** (skill name or rough idea): start the worksheet, pre-filling what you already know from the argument.

**Without argument**: ask for a brief description of the skill idea first, then begin Part 1.

**Want more control over the flow?** Fill in [`templates/skill-request-longform.md`](./templates/skill-request-longform.md) before invoking — any sections you complete will be used directly; blank sections will be filled in collaboratively. The template covers all 11 sections and is safe to leave partially filled.

**Header template:** Every new `SKILL.md` created by this skill includes the author header from [`templates/skill-header.md`](./templates/skill-header.md). Replace the values in that file with your own name, website, X handle, and repo before creating skills — or update them in each file after.

## Collaboration Style

- **Quote the user verbatim** wherever possible — even imperfect phrasing — then suggest an expanded version of what you perceive to be their intent
- **Flag uncertainty** rather than guessing: "I'm reaching here — is this right?"
- **Go one or two sections at a time** — never dump the whole worksheet at once
- **Invite correction at every step** — the user may have context you don't

---

## Part 1 — Understanding the Skill (Sections 1–8)

Work through these interactively. Ask, listen, quote back, expand, confirm.

### Section 1 — Overview

Ask: *"What will this skill do? A sentence or two is enough to start."*

From their answer, extract:
- A 2–3 sentence description
- 3–5 trigger keywords

### Section 2 — Invocation

Ask:
- What's the slash command name?
- What would a user say conversationally to trigger it?
- Should any situation or file type trigger it automatically?
- Manual-only (`/slash-command`) or auto-invoke when context matches?

**Naming guidance:** use gerund form (`processing-pdfs`, `analyzing-spreadsheets`). Avoid `helper`, `utils`, `tools`, `anthropic-*`, `claude-*`.

### Section 3 — Arguments

Ask: *"Does this skill take arguments? What are they?"*

| Pattern | Use when |
|---------|----------|
| `$ARGUMENTS` | Freeform input after the slash command |
| `$0`, `$1` | Positional arguments |
| `argument-hint` | Short hint shown in the skill picker UI |

If the skill should preview and ask for input when invoked bare, note that in Section 4.

### Section 4 — Workflow Shape

Ask: *"Is this one linear path, or does the skill handle different types of requests?"*

Have them describe up to 4 routes, then the steps for each:

| User wants to... | Workflow |
|-----------------|---------|
| ___ | → ___ |

> Real skills almost always branch. Without explicit routing, Claude either follows the wrong workflow or guesses — unreliably.

If invoked bare (no argument), should it preview what it does and ask for input before proceeding? Yes / No.

> **Dialog vs. conversational ask:** If the skill needs to pick between a small set of named routes (e.g., "create new / update existing / audit"), `AskUserQuestion` renders a clean multiple-choice dialog and blocks until the user selects. If the input is freeform or hard to enumerate, ask in plain text instead. Skills that route on a small, stable option set are good candidates for `AskUserQuestion` — note this in the workflow table above.

### Section 5 — Known Failure Modes

Ask: *"What does Claude reliably get wrong at this task without guidance?"*

Prompt with examples: wrong file format, wrong naming convention, wrong output structure, wrong tone.

| What Claude does wrong | What it should do instead |
|------------------------|--------------------------|
| ___ | ___ |

> These are often the most valuable part of a skill. Be specific — "uses unicode bullets" is better than "formats badly."

### Section 6 — Guidelines

Ask:
- What should Claude always do?
- What should it never do?
- When should it stop and ask rather than proceed?

| Always | Never |
|--------|-------|
| ___ | ___ |

### Section 7 — Error Handling

Ask:
- What are the bad or ambiguous inputs?
- What should Claude say for each?
- Should it verify output and fix in a loop?

**Output verification prompts:**
- What are the most common ways the output can be subtly wrong?
- Should Claude run any scripts or linters to check?
- Should it fix-and-verify in a loop until a clean pass?

### Section 8 — Quality Standards

Ask: *"What does 'excellent' look like for this output, beyond just being correct?"*

Then ask about creative latitude:
- **Low** — follow exact specifications, consistency is critical, deviation is a bug
- **Medium** — preferred patterns exist, some adaptation to context is fine
- **High** — multiple approaches are valid, use judgment and be creative

---

## Part 2 — Planning the Skill Contents (Sections 9–10)

### Section 9 — Environmental Adaptation

Ask: *"Does this skill's behavior change depending on what tools or integrations are available?"*

| If available... | Then... |
|-----------------|---------|
| ___ | ___ |
| Nothing / unclear | Ask the user: "___ " |

Also ask: should the output format adapt to context (e.g., terminal vs. file vs. Notion)?

> Skills that detect integrations (Slack, Drive, Notion) and adapt gracefully outperform those that assume the best case.

### Section 10 — File Structure

Ask: *"What information does Claude need every time vs. only sometimes?"*

**Always needed** → goes in `SKILL.md` (keep under ~500 lines)

**Needed only for sub-tasks** → goes in `references/` files, loaded on demand

Also ask:
- Are there deterministic operations that should be pre-written scripts (rather than code Claude improvises)?
- Are there templates, fonts, images, or other assets to bundle?

Suggest the resulting structure:

```
skill-name/
├── SKILL.md
├── references/
├── scripts/
└── assets/
```

> SKILL.md stays lean. Move detailed docs, API references, and large examples to `references/`. Pre-write scripts for anything deterministic.

---

## Part 3 — The Skill in Action (Section 11)

### Section 11 — Example Interaction

Ask for a complete end-to-end example:

> **User:** "___"
> **Claude should:**
> 1. ___
> 2. ___
> 3. Verify: ___
> 4. Return: ___

---

## Building the Skill

Once Parts 1–3 are complete:

1. **Check the catalog** — ensure no duplicate exists:
   ```bash
   cat skills/meta/create-skill/skills-catalog.json | jq '.skills[] | select(.name | contains("keyword"))'
   ```

2. **Scaffold the directory:**
   ```bash
   python skills/meta/create-skill/scripts/init_skill.py <skill-name> --path .claude/skills
   ```

3. **Write `SKILL.md`** using the worksheet answers. Quote the user's words verbatim where they gave specific phrasing.

4. **Create reference files** for anything needed only sometimes (from Section 10).

5. **Check line count — split if over 500:**
   ```bash
   wc -l .claude/skills/<skill-name>/SKILL.md
   ```
   If the result exceeds 500 lines, move each discrete workflow section into its own file under `references/` and replace the section body in `SKILL.md` with a single load instruction:
   ```markdown
   > See [`references/<workflow-name>.md`](./references/<workflow-name>.md)
   ```
   Repeat until `SKILL.md` is under 500 lines.

6. **Offer to package** for distribution (optional):
   ```bash
   python skills/meta/create-skill/scripts/package_skill.py .claude/skills/<skill-name>
   ```

---

## Technical Reference

### Frontmatter

Loaded at every agent boot — keep minimal.

```yaml
---
name: skill-name                    # Lowercase, hyphens, max 64 chars
description: What it does AND when to use it. Include trigger keywords.
allowed-tools: [Read, Write, Bash]
disable-model-invocation: false     # true = manual /slash-command only
argument-hint: "<hint shown in skill picker>"
---
```

### How Skills Load

| Component | When | Token budget |
|-----------|------|-------------|
| Frontmatter | Every boot | ~100 |
| Body | On activation | <5,000 |
| Reference files | On demand | As needed |

### Available Tools

| Tool | Needs permission prompt |
|------|------------------------|
| `Read`, `Glob`, `Grep`, `Task`, `TodoWrite` | No |
| `Write`, `Edit`, `Bash`, `WebFetch`, `WebSearch` | Yes |
| `AskUserQuestion` | No — built-in dialog, no `allowed-tools` entry needed |

**`AskUserQuestion` capabilities and limits:**
- Renders a structured multiple-choice dialog; 1–4 questions per call, 2–4 options each
- Single-select (default) or multi-select per question
- Each option accepts an optional `description` (fine print) and `preview` (markdown rendered side-by-side — useful for comparing code snippets or layouts)
- A free-text "Other" option is always appended automatically — the only way to capture arbitrary text
- Blocks until the user answers — Claude does not continue until a selection is made
- Does **not** support open-ended text input (for that, ask in conversational text instead)

Use `AskUserQuestion` when a skill needs a structured, bounded choice from the user. Prefer conversational text when the answer space is open-ended or unpredictable.

Pattern matching: `Bash(git *)`, `Read(./secrets/**)`

### Body Template

```markdown
# Skill Name

Brief overview.

## When to Use
- Condition A

## When Not to Use
- Condition X

## Instructions

Core guidance and step-by-step procedures.

## Examples

Concise input/output pairs.
```

### Anti-Patterns

- XML tags in body — use markdown
- Vague description — "A helpful skill" → "Expert guide for X"
- Scripts that punt to Claude — if deterministic, do it in the script
- Loading files >10MB into context — use scripts
- SKILL.md over ~500 lines — move content to `references/`
- Skipping the catalog — read `skills-catalog.json` before creating anything new
- Asking freeform questions when choices are well-defined — if a skill needs the user to pick from a bounded set of routes or options, design it to call `AskUserQuestion` rather than asking in plain text; the dialog UI is clearer and guarantees a valid selection

---

## Reference Files

| File | Load when |
|------|-----------|
| `references/skill-structure.md` | Questions about frontmatter fields or directory layout |
| `references/best-practices.md` | Questions about writing style, testing, anti-patterns |
| `references/examples.md` | Need concrete examples of complete skills |
| `references/advanced-skill-patterns.md` | Progressive disclosure, bundled scripts, workflow routing |

## Install

`npx skills add Minda/skills` — then select **skill-create-workflow** when prompted.
