# Skill Structure - Complete Specification

This document provides a complete specification of Claude Code skill components and structure.

## Directory Structure

```
skill-name/
├── SKILL.md              # Required: Main skill instructions
├── README.md             # Optional: Human-readable documentation
├── scripts/              # Optional: Executable scripts
│   ├── helper.py
│   └── process.sh
├── references/           # Optional: Detailed documentation
│   ├── api-docs.md
│   └── patterns.md
└── examples/             # Optional: Usage examples
    ├── basic.md
    └── advanced.md
```

## SKILL.md Structure

### Frontmatter (Required)

The frontmatter is a YAML block at the top of SKILL.md, delimited by `---`:

```yaml
---
name: skill-name
description: What it does AND when to use it
allowed-tools: [Read, Write, Bash]
disable-model-invocation: false
user-invocable: true
model: sonnet
context: fork
agent: Explore
argument-hint: "<arg> [options]"
---
```

### Frontmatter Fields

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| `name` | ✓ | string | Skill identifier, becomes `/slash-command` |
| `description` | ✓ | string | What skill does AND when to use it (max 1024 chars) |
| `allowed-tools` | | array | Tools Claude can use without asking for approval |
| `disable-model-invocation` | | boolean | `true` = manual only, `false` = can auto-invoke (default: false) |
| `user-invocable` | | boolean | `false` = hidden from menu (default: true) |
| `model` | | string | Specific model to use (sonnet, opus, haiku) |
| `context` | | string | `fork` = run in isolated subagent |
| `agent` | | string | Specialized subagent type (Explore, Plan, etc.) |
| `argument-hint` | | string | CLI hint shown in help menu |

### Body Structure (Markdown)

The body follows standard markdown conventions:

```markdown