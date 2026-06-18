#!/usr/bin/env python3
"""
Package and validate a Claude Code skill for distribution.

Usage:
    python package_skill.py <skill-path> [--output <output-dir>]

Example:
    python package_skill.py .claude/skills/my-skill
    python package_skill.py .claude/skills/my-skill --output dist/
"""

import argparse
import sys
import re
import zipfile
from pathlib import Path
from typing import List, Tuple, Optional


class SkillValidator:
    """Validates skill structure and content."""

    REQUIRED_FRONTMATTER = ['name', 'description']
    MAX_NAME_LENGTH = 64
    MAX_DESCRIPTION_LENGTH = 1024
    MAX_SKILL_SIZE = 500  # lines

    def __init__(self, skill_path: Path):
        self.skill_path = skill_path
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def validate(self) -> bool:
        """Run all validations. Returns True if valid."""
        self.errors = []
        self.warnings = []

        # Check basic structure
        if not self.skill_path.exists():
            self.errors.append(f"Skill path does not exist: {self.skill_path}")
            return False

        if not self.skill_path.is_dir():
            self.errors.append(f"Skill path is not a directory: {self.skill_path}")
            return False

        # Check for SKILL.md
        skill_file = self.skill_path / "SKILL.md"
        if not skill_file.exists():
            self.errors.append("SKILL.md not found")
            return False

        # Validate SKILL.md content
        self._validate_skill_md(skill_file)

        # Validate directory structure
        self._validate_structure()

        # Check file sizes