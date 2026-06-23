# create-skill

Collaborative skill creation for Claude Code. Works through 11 structured questions with you and builds a `SKILL.md` from your answers — covering invocation, workflow shape, failure modes, file layout, and more.

Built on Anthropic's official [`skill-creator`](https://github.com/anthropics/skills), adapted for skills with longer workflows, branching elements, and iterative refinement.

## Usage

```bash
# Interactive — start from a rough idea
/create-skill

# Pre-seeded — describe the skill upfront
/create-skill <skill name or idea>

# With full control — fill in the worksheet first, then invoke
# Edit: templates/skill-request-longform.md
/create-skill
```

## Templates

| File | Purpose |
|------|---------|
| [`templates/skill-request-longform.md`](./templates/skill-request-longform.md) | 11-section planning worksheet — fill in what you know, leave the rest blank |
| [`templates/skill-request.md`](./templates/skill-request.md) | Short-form version for simpler skills |
| [`templates/skill-header.md`](./templates/skill-header.md) | Author header added to every new `SKILL.md` |

## Personalizing the Header

Every skill created by this workflow starts with an author header. The default is Minda's:

```markdown
*[Minda Myers](https://mindamyers.com) · [𝕏](https://x.com/MindaMyers) · [GitHub](https://github.com/Minda) · [skills repo](https://github.com/Minda/skills)*
```

**If you're using this skill to build your own collection, replace it with yours.**
Edit [`templates/skill-header.md`](./templates/skill-header.md) and swap in your own name, website, X handle, GitHub username, and repo URL. All new skills will pick up your header automatically.

## Reference Files

| File | Loaded when |
|------|------------|
| `references/skill-structure.md` | Questions about frontmatter or directory layout |
| `references/best-practices.md` | Writing style, testing, anti-patterns |
| `references/examples.md` | Concrete examples of complete skills |
| `references/advanced-skill-patterns.md` | Branching, bundled scripts, progressive disclosure |
