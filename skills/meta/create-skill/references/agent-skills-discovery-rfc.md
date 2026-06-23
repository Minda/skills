# Agent Skills Discovery RFC Reference

## Overview

The Cloudflare Agent Skills Discovery RFC (https://github.com/cloudflare/agent-skills-discovery-rfc) proposes a standardized mechanism for discovering AI agent skills using the `.well-known` URI path pattern, following RFC 8615.

This creates a universal discovery endpoint that allows agents to automatically find and retrieve skills without prior configuration or manual searching.

## Key Concepts

### The Problem Being Solved

Currently, finding agent skills requires manual searching through:
- GitHub repositories
- Vendor documentation
- Social media
- User configuration files

There's no standard way to answer: "What skills does example.com publish?"

### The Solution: Predictable Discovery

Organizations can publish skills at a standardized location:
```
https://example.com/.well-known/skills/
```

This provides a single discovery endpoint for agents and tools to automatically find available skills.

## Technical Specification

### URI Structure

```
/.well-known/skills/
├── index.json                    # Required: Skills inventory
├── {skill-name}/                 # Individual skill directory
│   ├── SKILL.md                  # Required: Skill definition
│   ├── scripts/                  # Optional: Supporting scripts
│   ├── references/               # Optional: Documentation
│   └── assets/                   # Optional: Other resources
```

### Skill Naming Requirements

- **Length**: 1-64 characters
- **Characters**: Lowercase alphanumeric and hyphens only
- **Format**: No leading/trailing or consecutive hyphens
- **Examples**: `processing-pdfs`, `git-workflow`, `data-analysis`

### Index Format

The `index.json` file must contain:

```json
{
  "skills": [
    {
      "name": "processing-pdfs",
      "description": "Extract and manipulate PDF content including text extraction, page splitting, and metadata analysis",