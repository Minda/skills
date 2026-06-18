# CLAUDE.md

Skills are organized into bucket folders under `skills/`:

- `executive-function/` — planning, prioritization, and session context management
- `writing/` — text creation and transformation
- `research/` — content acquisition and enrichment
- `ui/` — visual output: ASCII diagrams and data visualizations
- `meta/` — skills for building and maintaining skills

Every skill in a bucket must have a reference in the top-level `README.md` and an entry in `.claude-plugin/plugin.json`.

Each bucket folder has a `README.md` that lists every skill with a one-line description, linked to its `SKILL.md`. Bucket `README.md`s and the top-level `README.md` group entries into **User-invoked** and **Model-invoked**.

Every `SKILL.md` is either user-invoked (reachable only by the human typing a slash command) or model-invoked (model- or user-reachable via trigger phrases in the description).
