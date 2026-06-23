# exobrain-skills

My personal agent skills for planning, writing, research, visual output, and skill creation.

## Reference

Skills split on one axis — who can invoke them. **User-invoked** skills are reachable only when you type them (e.g. `/gtd`). **Model-invoked** skills can be reached by the agent automatically when the task fits.

### Executive Function

Planning, prioritization, and session context management.

**User-invoked**

- **[gtd](./skills/executive-function/gtd/SKILL.md)** — Weekly and daily planning with tradeoff visualization and Notion integration.

### Writing

Text creation and transformation.

**User-invoked**

- **[de-ai](./skills/writing/de-ai/SKILL.md)** — Transform AI-generated text to sound more human by removing telltale patterns and adding authentic voice.
- **[nerdsnipe](./skills/writing/nerdsnipe/SKILL.md)** — Make any problem irresistibly engaging to curious minds by surfacing intellectual offense and low-hanging fruit.
- **[bedtime-story](./skills/writing/bedtime-story/SKILL.md)** — Generate a ≈20-minute bedtime story on any topic, TTS-ready (Speechify, Eleven Reader), threading real substance with a structural wind-down.

### Research

Content acquisition and enrichment.

**User-invoked**

- **[download-url](./skills/research/download-url/SKILL.md)** — Download web articles to PDF and Markdown. Supports single articles or entire documentation sites.
- **[youtube-fetching-transcripts](./skills/research/youtube-fetching-transcripts/SKILL.md)** — Fetch YouTube video transcripts as timestamped JSON and clean Markdown, with content-based file naming.

### UI

Visual output: ASCII diagrams and data visualizations.

**User-invoked**

- **[lowkey-viz](./skills/ui/lowkey-viz/SKILL.md)** — Bootstrap-style TUI components for data exploration. Generates Markdown visualizations that surface patterns, outliers, and edges in any dataset.
- **[creating-ascii-drawings](./skills/ui/creating-ascii-drawings/SKILL.md)** — Create visual ASCII diagrams to capture complex conceptual relationships.
- **[mermaid](./skills/ui/mermaid/SKILL.md)** — Create and edit Mermaid diagram files (.mmd) that render correctly in Figma via plugin or native SVG export.

### Meta

Skills for building and maintaining skills.

**User-invoked**

- **[create-skill](./skills/meta/create-skill/SKILL.md)** — Expert guide for creating and writing Claude Code skills. Covers structure, best practices, bundled resources, and packaging.
- **[hypercontext](./skills/meta/hypercontext/SKILL.md)** — Render session state as a spatial ASCII map: threads, activity heat, files, tools, and context runway. Created by [Danielle Fong](https://daniellefong.com/).
