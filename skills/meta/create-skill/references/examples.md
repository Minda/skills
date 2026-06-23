# Skill Examples

Real-world examples of effective Claude Code skills from the compound engineering plugin and best practices.

## Example 1: Simple Reference Skill

**Use case:** Provide style guide for writing code in a specific framework

### dhh-rails-style/SKILL.md

```yaml
---
name: dhh-rails-style
description: Rails development conventions following DHH's style guide. Use when writing Rails code, making architectural decisions, or reviewing Rails applications.
---
```

```markdown
# DHH Rails Style Guide

Write Rails applications following David Heinemeier Hansson's architectural principles and conventions.

## Core Principles

### Omakase Philosophy
Rails is "omakase" - accept the chef's choice of defaults and conventions.

### Convention Over Configuration
- Follow Rails conventions without extensive configuration
- Use standard directory structure
- Embrace Rails magic over explicit wiring

### Majestic Monolith
- Prefer monolithic architecture over microservices
- Keep related code together
- Split only when necessary (rarely)

## Code Style

### Models
- Fat models, skinny controllers
- Business logic belongs in models
- Use concerns for shared behavior

### Controllers
- One action per concern
- Avoid complex conditional logic
- Delegate to models

### Views
- Use partials liberally
- Keep templates simple
- Prefer helper methods over view logic

## File Organization

Follow Rails conventions:
- `app/models/` - Domain models
- `app/controllers/` - HTTP interface
- `app/views/` - Templates