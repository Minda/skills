#!/usr/bin/env python3
"""
Audit a baked Mermaid SVG for Figma-import survival of:
  - per-band fill and stroke colors (custom hexes provided as args)
  - bold title tspans (one per node with **bold** in its backtick markdown label)
  - italic description tspans (one or more per node with *italic* lines)
  - no surviving <foreignObject> with <p> payload (empty ones are OK)

Usage:
  python3 audit-styled-bake.py <baked.svg> \\
    --fill "#FEF3C7,#FCE7F3,#DBEAFE,#EDE9FE,#D1FAE5" \\
    --stroke "#92400E,#9D174D,#1E3A8A,#5B21B6,#065F46" \\
    --bold-min 1 --italic-min 1

Exits 0 if every check passes, 1 if any check fails.
"""
import argparse
import re
import sys


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("svg", help="Path to the baked .svg")
    ap.add_argument("--fill", default="", help="Comma-separated fill hexes expected to appear at least once")
    ap.add_argument("--stroke", default="", help="Comma-separated stroke hexes expected to appear at least once")
    ap.add_argument("--bold-min", type=int, default=0, help="Minimum count of font-weight=bold tspans")
    ap.add_argument("--italic-min", type=int, default=0, help="Minimum count of font-style=italic tspans")
    args = ap.parse_args()

    with open(args.svg) as f:
        svg = f.read()

    fills = [h.strip() for h in args.fill.split(",") if h.strip()]
    strokes = [h.strip() for h in args.stroke.split(",") if h.strip()]
    fails: list[str] = []

    foreign_with_p = 0
    for fo in re.findall(r"<foreignObject[^>]*>(.*?)</foreignObject>", svg, re.S):
        if "<p" in fo:
            foreign_with_p += 1
    if foreign_with_p:
        fails.append(f"{foreign_with_p} <foreignObject> with <p> payload remain — pass 6 did not convert them")

    for hx in fills:
        n = len(re.findall(rf'fill="{re.escape(hx)}"', svg, re.IGNORECASE))
        if n == 0:
            fails.append(f"fill={hx} missing (expected at least 1)")
        else:
            print(f"  fill={hx}: {n} OK")
    for hx in strokes:
        n = len(re.findall(rf'stroke="{re.escape(hx)}"', svg, re.IGNORECASE))
        if n == 0:
            fails.append(f"stroke={hx} missing (expected at least 1)")
        else:
            print(f"  stroke={hx}: {n} OK")

    bold = len(re.findall(r'<tspan[^>]*font-weight="bold"', svg))
    italic = len(re.findall(r'<tspan[^>]*font-style="italic"', svg))
    print(f"  bold tspans:   {bold}  (min {args.bold_min})")
    print(f"  italic tspans: {italic}  (min {args.italic_min})")
    if bold < args.bold_min:
        fails.append(f"bold tspans {bold} < required {args.bold_min}")
    if italic < args.italic_min:
        fails.append(f"italic tspans {italic} < required {args.italic_min}")

    if fails:
        print("\nFAIL:")
        for msg in fails:
            print(f"  - {msg}")
        return 1
    print("\nPASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
