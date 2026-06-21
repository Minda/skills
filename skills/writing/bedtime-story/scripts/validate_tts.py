#!/usr/bin/env python3
"""
Validate a bedtime story file for TTS readability and word count.

Usage:
    python3 validate_tts.py <story.txt>

Exits 0 if clean, 1 if hazards found, 2 on usage error.
"""

import re
import sys
from pathlib import Path

WORD_TARGET_LOW = 2900
WORD_TARGET_HIGH = 3500

HAZARDS = [
    ("em-dash", r"—"),
    ("en-dash mid-word", r"(?<=\w)–(?=\w)"),
    ("parenthesis", r"[()]"),
    ("square bracket", r"[\[\]]"),
    ("markdown heading", r"(?m)^#+\s"),
    ("markdown bullet", r"(?m)^\s*[-*+]\s"),
    ("asterisk emphasis", r"\*\S"),
    ("underscore emphasis", r"(?:^|\s)_\S"),
    ("code fence", r"```"),
    ("inline code", r"`[^`]+`"),
    ("URL", r"https?://\S+"),
    ("abbreviation e.g.", r"\be\.g\."),
    ("abbreviation i.e.", r"\bi\.e\."),
    ("abbreviation U.S.", r"\bU\.S\."),
    ("abbreviation etc.", r"\betc\."),
    ("abbreviation Dr.", r"\bDr\."),
    ("abbreviation Mt.", r"\bMt\."),
    ("abbreviation St.", r"\bSt\."),
    ("century abbreviation", r"\b\d+th c\."),
    ("ampersand", r"&"),
    ("slash between words", r"(?<=\w)/(?=\w)"),
]


def find_hits(text):
    lines = text.splitlines()
    hits = []
    for label, pattern in HAZARDS:
        for m in re.finditer(pattern, text):
            line_no = text.count("\n", 0, m.start()) + 1
            snippet = lines[line_no - 1].strip()
            if len(snippet) > 80:
                col = m.start() - sum(len(l) + 1 for l in lines[: line_no - 1])
                start = max(0, col - 30)
                snippet = "…" + snippet[start : start + 70] + "…"
            hits.append((line_no, label, snippet))
    return hits


def check_ending(text):
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    if not paragraphs:
        return None
    last = paragraphs[-1]
    if last.endswith("?"):
        return "Last paragraph ends with a question. Bedtime endings should not invite further thought."
    opening_phrases = ["tomorrow", "next time", "but first", "soon we will", "and then we will"]
    if any(phrase in last.lower() for phrase in opening_phrases):
        return f"Last paragraph contains an opening phrase. Endings should close, not open. Found near: \"{last[-100:]}\""
    return None


def main():
    if len(sys.argv) != 2:
        print("Usage: validate_tts.py <story.txt>", file=sys.stderr)
        return 2

    path = Path(sys.argv[1])
    if not path.exists():
        print(f"File not found: {path}", file=sys.stderr)
        return 2

    text = path.read_text()
    word_count = len(text.split())
    hits = find_hits(text)
    ending_issue = check_ending(text)

    print(f"File: {path}")
    print(f"Word count: {word_count}  (target band: {WORD_TARGET_LOW}–{WORD_TARGET_HIGH})")
    if word_count < WORD_TARGET_LOW:
        print(f"  → too short by {WORD_TARGET_LOW - word_count} words (~{(WORD_TARGET_LOW - word_count) // 150} min)")
    elif word_count > WORD_TARGET_HIGH:
        print(f"  → too long by {word_count - WORD_TARGET_HIGH} words")
    else:
        print(f"  → in band")

    print(f"\nTTS hazards: {len(hits)}")
    for line_no, label, snippet in hits[:30]:
        print(f"  line {line_no:>4}  {label:<25}  {snippet}")
    if len(hits) > 30:
        print(f"  … {len(hits) - 30} more (run again after fixing)")

    if ending_issue:
        print(f"\nEnding check: {ending_issue}")

    in_band = WORD_TARGET_LOW <= word_count <= WORD_TARGET_HIGH
    clean = not hits and not ending_issue and in_band
    print(f"\n{'PASS' if clean else 'FAIL — fix the items above'}")
    return 0 if clean else 1


if __name__ == "__main__":
    sys.exit(main())
