#!/usr/bin/env python3
"""
bake-fills.py — convert Mermaid-generated SVG inline `style="fill:X !important;..."`
attributes into direct SVG presentation attributes (`fill="X"`, `stroke="Y"`).

Use this when piping a Mermaid `.mmd` diagram into Figma. Figma's SVG importer
strips embedded <style> blocks and inline style attributes, which makes
per-node `style NodeID fill:…` colors collapse to Mermaid's default lavender.
Direct presentation attributes survive the import.

Usage:
    mmdc -i diagram.mmd -o diagram.svg
    python3 bake-fills.py diagram.svg            # writes diagram.baked.svg
    python3 bake-fills.py diagram.svg out.svg    # explicit output path

Then drag the baked SVG into Figma — not via the Mermaid in Figma plugin, just
the native canvas SVG import.
"""
import re
import sys
from pathlib import Path

ELEMENT = r'<(rect|path|ellipse|polygon|circle)([^>]*style="[^"]*fill:[^"]*"[^>]*)/>'
BAKE_PROPS = ('fill', 'stroke', 'stroke-width')

def rewrite(m: re.Match) -> str:
    tag, attrs = m.group(1), m.group(2)
    style_m = re.search(r'style="([^"]*)"', attrs)
    if not style_m:
        return m.group(0)
    props = {}
    for part in style_m.group(1).split(';'):
        part = part.strip()
        if ':' not in part:
            continue
        k, v = part.split(':', 1)
        v = v.strip().replace('!important', '').strip()
        props[k.strip()] = v
    new_attrs = re.sub(r'\sstyle="[^"]*"', '', attrs)
    # Strip any existing direct presentation attributes we're about to set, so we
    # don't produce duplicates (mmdc sometimes emits fill="…" AND style="fill:…")
    for k in BAKE_PROPS:
        if k in props:
            new_attrs = re.sub(rf'\s{re.escape(k)}="[^"]*"', '', new_attrs)
    new_attrs = new_attrs.strip()
    baked = ' '.join(f'{k}="{props[k]}"' for k in BAKE_PROPS if k in props)
    return f'<{tag} {new_attrs} {baked}/>'

def has_attr(attrs: str, name: str) -> bool:
    return bool(re.search(rf'\s{re.escape(name)}=', ' ' + attrs))


def main(argv: list[str]) -> int:
    if len(argv) < 2 or len(argv) > 3:
        print(__doc__, file=sys.stderr)
        return 2
    src = Path(argv[1])
    dst = Path(argv[2]) if len(argv) == 3 else src.with_suffix('.baked.svg')
    s = src.read_text()

    # Pass 1: convert inline style="fill:..." into direct presentation attributes
    s = re.sub(ELEMENT, rewrite, s)

    # Pass 2: <text> elements with no fill → Mermaid default #333. Figma's SVG
    # importer strips the embedded <style> block where this normally lives, so
    # every label (node, edge, cluster) goes invisible without this.
    def text_fix(m: re.Match) -> str:
        attrs = m.group(1)
        if has_attr(attrs, 'fill'):
            return m.group(0)
        return f'<text {attrs.strip()} fill="#333">'
    s = re.sub(r'<text\s+([^>]*?)>', text_fix, s)

    # Pass 2b: edge / cluster labels with multi-line content come out of Mermaid
    # as N sibling <tspan class="text-outer-tspan row"> elements, each with its
    # own absolute `y` attribute. Figma's SVG importer only honors the `y` of
    # the first sibling, so subsequent lines collapse onto line 1 ("No\nfallback"
    # → "Nofallback"). Rewrite the structure to one tspan per line with `dy`
    # offsets, matching pass 6's pattern for node labels.
    outer_tspan_re = re.compile(
        r'<tspan\b[^>]*\bclass="text-outer-tspan row"[^>]*>(.*?)</tspan>', re.S,
    )
    def text_multiline_fix(m: re.Match) -> str:
        text_open, body = m.group(1), m.group(2)
        outers = outer_tspan_re.findall(body)
        if len(outers) < 2:
            return m.group(0)
        lines = []
        for outer in outers:
            inner = re.sub(r'<[^>]+>', '', outer)
            inner = (inner.replace('&amp;', '&')
                          .replace('&lt;', '<')
                          .replace('&gt;', '>')
                          .replace('&quot;', '"'))
            lines.append(inner.replace('&', '&amp;')
                              .replace('<', '&lt;')
                              .replace('>', '&gt;'))
        # Centre vertically around the existing text y. Use x="0" since the
        # parent text element already carries text-anchor="middle" and the
        # text element sits inside a translated <g>.
        n = len(lines)
        first_dy = -(n - 1) * 0.6
        new_inner = (
            f'<tspan x="0" dy="{first_dy:.2f}em">{lines[0]}</tspan>' +
            ''.join(f'<tspan x="0" dy="1.2em">{ln}</tspan>' for ln in lines[1:])
        )
        return f'{text_open}{new_inner}</text>'
    # Match a <text>…</text> only when it contains two or more outer tspans.
    s = re.sub(
        r'(<text\b[^>]*>)((?:(?!</text>).)*?<tspan\b[^>]*?class="text-outer-tspan row".*?<tspan\b[^>]*?class="text-outer-tspan row".*?)</text>',
        text_multiline_fix, s, flags=re.S,
    )

    # Pass 3: <rect> directly inside <g class="cluster"> gets the cluster fill.
    def cluster_rect_fix(m: re.Match) -> str:
        prefix, rect_attrs = m.group(1), m.group(2)
        if has_attr(rect_attrs, 'fill'):
            return m.group(0)
        return f'{prefix}<rect {rect_attrs.strip()} fill="#ffffde" stroke="#aaaa33" stroke-width="1"/>'
    s = re.sub(
        r'(<g\b[^>]*\bclass="cluster"[^>]*>\s*)<rect\s+([^>]+?)/>',
        cluster_rect_fix, s,
    )

    # Pass 4: edge lines — flowchart-link / edgePath / relationshipLine.
    # Give them a stroke and explicit fill:none so they show as lines.
    def edge_path_fix(m: re.Match) -> str:
        attrs = m.group(1)
        if has_attr(attrs, 'stroke') and has_attr(attrs, 'fill'):
            return m.group(0)
        extras = []
        if not has_attr(attrs, 'stroke'):
            extras.append('stroke="#333"')
        if not has_attr(attrs, 'fill'):
            extras.append('fill="none"')
        return f'<path {attrs.strip()} {" ".join(extras)}/>'
    s = re.sub(
        r'<path\s+([^>]*\bclass="[^"]*(?:flowchart-link|edgePath|relationshipLine)[^"]*"[^>]*?)/>',
        edge_path_fix, s,
    )

    # Pass 5: arrow-marker shapes — Mermaid emits .arrowMarkerPath on <path>,
    # <circle>, AND <polygon> depending on the marker style. Give them a solid
    # fill so the arrowheads render as filled triangles/circles.
    def marker_shape_fix(m: re.Match) -> str:
        tag, attrs = m.group(1), m.group(2)
        if has_attr(attrs, 'fill'):
            return m.group(0)
        return f'<{tag} {attrs.strip()} fill="#333"/>'
    s = re.sub(
        r'<(path|circle|polygon)\s+([^>]*\bclass="[^"]*arrowMarkerPath[^"]*"[^>]*?)/>',
        marker_shape_fix, s,
    )

    # Pass 5b: sequence diagram labelBox polygons (loop/alt header tabs).
    # Mermaid emits <polygon class="labelBox"/> with no inline style; default
    # SVG fill is black so without intervention they become solid black blocks.
    def labelbox_fix(m: re.Match) -> str:
        attrs = m.group(1)
        if has_attr(attrs, 'fill'):
            return m.group(0)
        return f'<polygon {attrs.strip()} fill="#ECECFF" stroke="#9370DB" stroke-width="1"/>'
    s = re.sub(
        r'<polygon\s+([^>]*\bclass="labelBox"[^>]*?)/>',
        labelbox_fix, s,
    )

    # Pass 5c: shapes inside <marker> defs that don't carry .arrowMarkerPath
    # (ER cardinality markers, sequence custom arrowheads). Default SVG fill is
    # black and stroke is none, so an unfilled open path (no closing `z`)
    # renders as nothing. We heuristically classify: a `d` ending in `z`/`Z` is
    # a filled shape (give it fill=#333 if missing); otherwise it's a stroked
    # line set (give it stroke=#333 fill=none).
    def marker_inner_fix(m: re.Match) -> str:
        marker_open, body, marker_close = m.group(1), m.group(2), m.group(3)
        def shape_fix(sm: re.Match) -> str:
            tag, attrs = sm.group(1), sm.group(2)
            if has_attr(attrs, 'fill') or has_attr(attrs, 'stroke'):
                # If circle has fill but no stroke, still give it a stroke so
                # the cardinality circle outline shows.
                if tag == 'circle' and has_attr(attrs, 'fill') and not has_attr(attrs, 'stroke'):
                    return f'<{tag} {attrs.strip()} stroke="#333"/>'
                return sm.group(0)
            d_m = re.search(r'd="([^"]+)"', attrs)
            is_closed_path = (tag == 'path' and d_m and re.search(r'[zZ]\s*$', d_m.group(1).strip()))
            if tag == 'polygon' or is_closed_path:
                return f'<{tag} {attrs.strip()} fill="#333"/>'
            return f'<{tag} {attrs.strip()} fill="none" stroke="#333"/>'
        new_body = re.sub(
            r'<(path|circle|polygon|ellipse)\s+([^>]*?)/>',
            shape_fix, body,
        )
        return marker_open + new_body + marker_close
    s = re.sub(
        r'(<marker[^>]*>)(.*?)(</marker>)',
        marker_inner_fix, s, flags=re.S,
    )

    # Pass 6: <foreignObject>...<p>...</p>...</foreignObject> → native <text><tspan>.
    # Mermaid v11 still emits foreignObject for *node* labels even with
    # htmlLabels:false, and Figma's native SVG importer silently drops them. We
    # convert each foreignObject into an SVG <text> with one <tspan> per <br/>-
    # separated line, centered inside the original foreignObject box.
    foreign_re = re.compile(
        r'<foreignObject\s+([^>]*)>(.*?)</foreignObject>', re.S,
    )
    def foreign_fix(m: re.Match) -> str:
        attrs_str, inner = m.group(1), m.group(2)
        w_m = re.search(r'width="([^"]+)"', attrs_str)
        h_m = re.search(r'height="([^"]+)"', attrs_str)
        if not (w_m and h_m):
            return m.group(0)
        try:
            W, H = float(w_m.group(1)), float(h_m.group(1))
        except ValueError:
            return m.group(0)
        p_m = re.search(r'<p\b[^>]*>(.*?)</p>', inner, re.S)
        if not p_m:
            return m.group(0)
        # Walk the <p>…</p> content character by character so <strong>/<em>
        # state persists across <br/>-separated lines (Mermaid emits the bold
        # title as <strong>X</strong><br/> and the italic description as
        # <em>line1<br/>line2</em> — italics span breaks, bold typically
        # doesn't, but the parser handles both either way).
        html = p_m.group(1)
        styled_lines = []  # list of (text, bold, italic)
        buf = []
        buf_bold = buf_italic = False  # state captured when text first appears
        text_started = False
        bold = italic = False
        i = 0
        while i < len(html):
            if html[i] == '<':
                gt = html.find('>', i)
                if gt == -1:
                    i += 1
                    continue
                tag = html[i+1:gt].strip().lower().rstrip('/').strip()
                if tag in ('strong', 'b'):
                    bold = True
                elif tag in ('/strong', '/b'):
                    bold = False
                elif tag in ('em', 'i'):
                    italic = True
                elif tag in ('/em', '/i'):
                    italic = False
                elif tag.startswith('br'):
                    styled_lines.append(
                        (''.join(buf).strip(), buf_bold, buf_italic)
                    )
                    buf = []
                    text_started = False
                # other tags are ignored — fall through
                i = gt + 1
            else:
                if not text_started and not html[i].isspace():
                    # Snapshot styles at the first real character — the closing
                    # tag for that style hasn't fired yet, so this captures the
                    # styling that applied while the chunk was accumulated.
                    buf_bold = bold
                    buf_italic = italic
                    text_started = True
                buf.append(html[i])
                i += 1
        if buf:
            styled_lines.append(
                (''.join(buf).strip(), buf_bold, buf_italic)
            )
        # Decode entities so the visible glyphs are right, then re-encode
        # for SVG output.
        def decode_then_encode(t: str) -> str:
            t = (t.replace('&amp;', '&')
                  .replace('&lt;', '<')
                  .replace('&gt;', '>')
                  .replace('&quot;', '"'))
            return (t.replace('&', '&amp;')
                     .replace('<', '&lt;')
                     .replace('>', '&gt;'))
        styled_lines = [
            (decode_then_encode(t), b, it)
            for (t, b, it) in styled_lines if t
        ]
        if not styled_lines:
            return m.group(0)
        cx, cy = W / 2, H / 2
        n = len(styled_lines)
        # Vertical centering: dominant-baseline isn't reliable across importers,
        # so compute dy on the first tspan to push the block above center by
        # (n-1)/2 lines. Line height ≈ 1.2em.
        first_dy = -(n - 1) * 0.6
        def style_attrs(bold: bool, italic: bool) -> str:
            parts = []
            if bold:
                parts.append('font-weight="bold"')
            if italic:
                parts.append('font-style="italic"')
            return (' ' + ' '.join(parts)) if parts else ''
        head_text, head_bold, head_italic = styled_lines[0]
        tspans = [
            f'<tspan x="{cx:.4f}" dy="{first_dy:.2f}em"'
            f'{style_attrs(head_bold, head_italic)}>{head_text}</tspan>'
        ] + [
            f'<tspan x="{cx:.4f}" dy="1.2em"'
            f'{style_attrs(b, it)}>{t}</tspan>'
            for (t, b, it) in styled_lines[1:]
        ]
        return (
            f'<text x="{cx:.4f}" y="{cy:.4f}" text-anchor="middle" '
            f'dominant-baseline="middle" fill="#111" '
            f'font-family="trebuchet ms, verdana, arial, sans-serif" '
            f'font-size="14">{"".join(tspans)}</text>'
        )
    s = foreign_re.sub(foreign_fix, s)

    # Pass 7: <rect class="background"> elements (behind edge labels) have no
    # styling in the SVG itself — they rely on CSS rules Figma strips, and end
    # up as solid black blocks. Make them invisible.
    def bg_rect_fix(m: re.Match) -> str:
        attrs = m.group(1)
        attrs = re.sub(r'\sfill="[^"]*"', '', attrs)
        attrs = re.sub(r'\sstroke="[^"]*"', '', attrs)
        return f'<rect {attrs.strip()} fill="none" stroke="none"/>'
    s = re.sub(
        r'<rect\s+([^>]*\bclass="background"[^>]*?)/>',
        bg_rect_fix, s,
    )

    dst.write_text(s)
    baked_count = len(re.findall(r'fill="#[A-Fa-f0-9]{3,8}"', s))
    text_count = len(re.findall(r'<text\s+[^>]*fill="#333"', s))
    print(f'Wrote {dst} ({baked_count} direct fill="…" attributes, {text_count} text fills)')
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
