# Skill Best Practices

Advanced patterns and practices for creating effective Claude Code skills.

## Writing Effective Descriptions

The description field is **critical** for automatic invocation. Claude uses it to decide when to invoke the skill.

### Anatomy of a Good Description

A good description has three components:

1. **What it does** - The capability
2. **When to use it** - The trigger context
3. **Specific keywords** - Terms users will say

#### Example: Bad Description

```yaml
description: A helpful skill for working with git
```

Problems:
- Too vague ("helpful")
- No trigger keywords
- Doesn't specify what git operations

#### Example: Good Description

```yaml
description: Expert guide for managing git worktrees. Use this when users want to create, switch, or manage parallel git working trees for feature development and experimentation.
```

Why it works:
- Specific capability: "managing git worktrees"
- Clear triggers: "create, switch, or manage"
- Keywords: "worktrees", "parallel", "feature development"

### Description Patterns

**Task-oriented:**
```yaml
description: Generate comprehensive commit messages based on git diff. Use when users want to commit changes and need help writing descriptive commit messages.
```

**Reference-oriented:**
```yaml
description: Rails development conventions and DHH style guide. Use when writing Rails code, making architectural decisions, or following Rails best practices.
```

**Tool-oriented:**
```yaml
description: Process and analyze spreadsheet data using pandas. Use when users need to read, transform, or analyze Excel/CSV files.
```

## Prompting Best Practices

### Be Direct and Imperative

❌ **Avoid:**