---
name: skill-creator-mm
description: Expert guide for creating and writing Claude Code skills. Use this when the user wants to create a new skill or learn about skill structure and best practices.
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep]
---

# Skill Creator MM

A comprehensive guide for creating effective Claude Code skills that extend Claude's capabilities with specialized knowledge, workflows, and tool integrations.

## Quick Start

Creating a skill involves six steps:

1. **Check existing skills** — Review 126+ indexed skills before creating new ones
2. **Understand the use case** — Clarify what the skill does and when it triggers
3. **Identify bundled resources** — Scripts, references, examples
4. **Initialize the skill** — Use `init_skill.py` or create manually
5. **Write the SKILL.md** — Clear instructions using best practices
6. **Package the skill** — Validate and bundle for distribution (optional)

**After creation:** Use `/skill-optimization` to test, refine, and optimize your skill.

## When to Use

- Creating a new skill from scratch
- Learning skill structure and best practices
- Understanding skill conventions and patterns
- Setting up initial skill structure

## When Not to Use

- An existing skill already covers the need (check catalog first)
- Task is too simple—just use a prompt directly
- Need persistent services—use an MCP server instead
- Building a full application—skills are focused components

## What's Included in a Skill?

There are only **two requirements**:
1. **Frontmatter** with `name` and `description`
2. **Body** containing instructions

Everything else is optional.

### How Skills Load

| Component | When Loaded | Budget |
|-----------|-------------|--------|
| **Frontmatter** | Every agent boot | ~100 tokens |
| **Body** | On activation | <5,000 tokens |
| **Supporting files** | On-demand | As needed |

This is why frontmatter must be minimal but body can be detailed.
name: skill-creator-mm
description: Expert guide for creating and writing Claude Code skills. Use this when the user wants to create a new skill or learn about skill structure and best practices.
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep]
---

# Skill Creator MM

A comprehensive guide for creating effective Claude Code skills that extend Claude's capabilities with specialized knowledge, workflows, and tool integrations.

Renamed from skill-creator to skill-creator-mm (MM initials).

