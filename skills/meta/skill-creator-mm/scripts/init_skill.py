#!/usr/bin/env python3
"""
Initialize a new Claude Code skill with standard structure.

Usage:
    python init_skill.py <skill-name> [--path <output-dir>]

Example:
    python init_skill.py analyzing-logs --path .claude/skills
"""

import argparse
import sys
from pathlib import Path


SKILL_TEMPLATE = """---
name: {name}
description: {description}
allowed-tools: []
---

# {title}

Brief overview of what this skill does.

## Quick Start

Immediate actionable guidance for using this skill.

## Instructions

Core guidance Claude follows when using this skill:

1. **First step** - What to do first
2. **Second step** - What to do next
3. **Third step** - Final actions

## Examples

### Example 1: Common Use Case

**Input:**
```
User request example
```

**Output:**
```
Expected result
```

## Guidelines

**Do:**
- Clear actionable items
- Specific instructions
- Concrete examples

**Don't:**