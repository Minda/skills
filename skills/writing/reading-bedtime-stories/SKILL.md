---
name: reading-bedtime-stories
description: Generate a roughly 20-minute bedtime story on any topic, formatted for text-to-speech playback (Speechify, Eleven Reader, Apple/Android system TTS). Threads substantive content with a structural wind-down so the listener can both learn and drift toward sleep. Use when user says "bedtime story", "tell me a story about", "wind-down story", "read me to sleep", or wants a sleep-friendly narrated piece on a chosen topic.
allowed-tools: [Read, Write, Bash, Glob, Grep]
argument-hint: "<topic — e.g. octopus cognition, the history of harbors>"
---

*[Minda Myers](https://mindamyers.com) · [𝕏](https://x.com/MindaMyers) · [GitHub](https://github.com/Minda) · [skills repo](https://github.com/Minda/skills)*

# /reading-bedtime-stories

Generate a single ≈20-minute bedtime story on any topic, written to be read aloud by a text-to-speech engine. Designed to thread two goals that pull against each other: deliver something genuinely interesting AND help the listener drift toward sleep.

The skill resolves that tension structurally — substantive content lives in Acts I and II, the closing third dissolves into sensory imagery and repetition so the analytical mind can release.

## When to use

- User says "bedtime story about X", "read me to sleep about X", "wind-down story on X"
- User wants a Speechify-ready or TTS-ready file
- User has a topic but wants the pacing and wind-down structure handled

## When NOT to use

- User wants a children's story with characters and plot → different shape, write a narrative fiction piece instead
- User wants a short three-to-five-minute drift → use this skill but set word target to ~700 and skip Act II
- User wants pure ambient text with no content → this skill always carries substance; use something simpler

## Invocation

- **With topic**: `/reading-bedtime-stories octopus cognition` → confirm the angle in one sentence, then write
- **Without topic**: ask "What topic? I'll write you a ≈20-minute story you can play in Speechify or any TTS app."

## Workflow

1. **Confirm the topic and angle in one sentence.**
   Example: *"Got it — a 20-minute drift through octopus cognition, leaning toward the strangeness of distributed intelligence. Sound right, or adjust?"*
   Invite redirect. Don't proceed if the angle is unclear.

2. **Pick the Act II shape — thread or cluster.**
   - **Thread shape** (default): one mystery deepened across two or three connected insights, with one or two recurring metaphors that get reused and softened. Best for: octopus cognition, the multiverse, the ship of Theseus, anything where the listener should follow a single arc.
   - **Cluster shape**: three to five small topic groups, four to six facts each, with gentle bridges between them ("from there, it is only natural to think about…"). Best for: "small wonders of physics," "a walk through the night sky," "facts about deep-sea life" — taxonomic topics the listener can drift in and out of without losing the thread.
   - Default to thread. Switch to cluster only when the topic is naturally a list.
   - See `references/youtube-bedtime-narrator-patterns.md` for the full comparison and quote bank.

3. **Plan the arc internally.** Three acts, decelerating:
   - **Act I — Welcome** (≈25%, ~750 words): settles the listener, names the topic, opens one real question, gives one concrete anchoring image. Includes one physical-relaxation cue ("you can let your shoulders rest") and at least one "tonight" anchor.
   - **Act II — Substance** (≈40%, ~1,200–1,400 words): real content in the chosen shape (thread or cluster). Two or three genuine insights (thread) or three to five small clusters (cluster). Sentences begin to lengthen and slow. Insert one "breathing beat" — a short permission phrase like "you can let that sit for a moment" — around the midpoint.
   - **Act III — Drift** (≈35%, ~950–1,050 words): no new claims. Return to earlier images and soften them. Repetition. Sensory channels (sound, weight, temperature, slow motion). End with a **cosmic-to-personal** move when the topic permits: zoom back from the broad scale of Act II to the listener's actual room, body, breath, tonight. Soft landing.

4. **Write the full text** following the TTS rules below. Target: **2,900–3,500 words** (≈ 18–22 minutes at 150–170 wpm).

5. **Save to** `downloads/bedtime-stories/YYYY-MM-DD-<topic-slug>.txt`. Plain text. No markdown. Title on line one, blank line, then the body.

6. **Run the validator** (catches TTS hazards and confirms word count):
   ```bash
   python3 .claude/skills/reading-bedtime-stories/scripts/validate_tts.py <path>
   ```
   Fix anything it flags, then re-run until clean.

7. **Report the path** with an `open` command so the user can grab it for Speechify:
   ```
   Saved. About twenty minutes at default Speechify speed.
   open downloads/bedtime-stories/2026-06-20-octopus-cognition.txt
   ```

## TTS-safe writing rules (non-negotiable)

TTS engines read formatting literally. Any markup becomes an audible glitch. These are the most common failure modes — enforce them.

| Avoid | Use instead |
|-------|-------------|
| `—` em-dash | `. ` period, or `, ` comma |
| `()` parentheses | weave the aside into the sentence |
| Markdown headings, bullets, `#`, `*`, `_` | flowing prose only |
| Abbreviations: e.g., i.e., U.S., 19th c., Dr., Mt. | spell them out: for example, that is, the United States, the nineteenth century, Doctor, Mount |
| Numerals under one hundred | spell out: forty thousand, three, seventeen |
| URLs, code, file paths | omit entirely |
| Quotation marks for emphasis | trust the prose |
| Cliffhangers, "tomorrow we will…", "but first…" | finish gently, no opening at the end |
| Questions at the end | the last sentence should not invite further thought |

## Pacing and arc (always followed)

### Act I — Welcome (~25%, ~750 words)

- **First sentence**: low-arousal, second-person, slow.
  Examples:
  - *"Tonight we are going to spend a while with the octopus."*
  - *"You can let your eyes close. I will tell you a story about harbors, and you do not need to follow every part of it."*
- Establish the topic and one real question the story will turn around.
- One small concrete image to anchor attention — a single octopus arm reaching across a coral ledge; a single rope tied to a single piling in a quiet harbor at dusk.
- **One physical-relaxation cue** within the first three paragraphs. *"You can let your shoulders rest."* *"There is no need to hold the body upright tonight."* This addresses the body, not just the attention.
- **Anchor the word "tonight"** at least once in Act I, and let it return in Act III. It tethers cosmic or abstract material to *this evening, this room*.

### Act II — Substance (~40%, ~1,200–1,400 words)

- This is where the *value* lives. Real facts, real ideas, the surprising structure of the topic.
- Sentences still complete and varied, but begin to lengthen slightly.
- **Use the shape chosen in step 2.**
  - **Thread**: two or three genuine insights woven together with connective prose. One or two recurring metaphors that get reused and softened. No lists.
  - **Cluster**: three to five small topic groups, four to six facts each. Bridge between groups with gentle phrases — *"from there, it is only natural to think about…"*, *"there is a related thing worth knowing."* Still no lists. The clusters are paragraphs, not bullet points.
- **Insert one "breathing beat"** near the midpoint — a short permission phrase that releases the listener from tracking. *"You can let that sit for a moment."* *"There is no hurry to remember it."* These are the prose equivalent of a held rest in music.
- **Reframe difficulty as wonder.** Never say "this is hard to understand." Say "this is strange," "this is beautiful," "this is surprising." Lower comprehension anxiety so the listener stays in curiosity.
- Quote thinkers or name people sparingly, without honorifics or titles that disrupt prosody (say "Peter Godfrey-Smith" not "Dr. Peter Godfrey-Smith, philosopher of biology").
- End Act II by returning to the anchoring image from Act I, now lit by what the listener has learned.

### Act III — Drift (~35%, ~950–1,050 words)

- **Stop introducing new claims.** Return to images already established and let them soften.
- **Use repetition.** Same sentence shapes. Same words. The mind should stop tracking new information.
- **Sensory channels**: sound, weight, temperature, slow movement. Avoid sharp visual detail toward the end.
- **Cosmic-to-personal move** (recommended when the topic ranged wide): in the second-to-last beat, zoom back from the large scale of Act II to the listener's actual room, body, breath, tonight. The same atoms, the same evening, this room. This reconciles scale and intimacy and is the most reliable settling move from long-form bedtime narration.
- **Final paragraph**: short. Grounded. No question, no opening, no "tomorrow." The last sentence should land like a hand resting on a table.
  Endings that work:
  - *"And that is enough for tonight."*
  - *"You can let it rest there now."*
  - *"The story rests."*
- **Do not** end with YouTube-outro habits — no "thanks for sticking with me," no "congratulations, you made it," no "where in the world are you listening from." These break the spell. The story should close inside itself.

## Topic adaptation

Different topics need slightly different tones in Act II. Match the substance to the shape. See `references/topic-flavors.md` for fuller guidance and example openings. Quick map:

- **Natural history / science** (octopuses, mycelium, ocean currents, geology) — wonder, scale, *"and then it turns out…"*
- **History** (the Hanseatic League, ancient libraries, the postal system) — long time horizons, slow change, texture of past daily life
- **Biography** — stay in the *quiet middle* of the person's life. Avoid drama, illness, conflict
- **Philosophy / ideas** — concrete examples before abstraction; one idea explored well beats three sketched
- **Place** (a city at night, a quiet harbor, a forest) — pure sensory throughout; Act II can be partly imagery

### Topics to steer away from at bedtime

Unless the user explicitly insists, gently offer an adjacent topic instead of:
- Violence, war, atrocity
- Serious illness or death (Stoic meditations on mortality are an exception — they tend to settle, not activate)
- Active political or social conflict
- Horror, suspense, thriller framing
- Anything with sharp negative emotional charge

If unsure, ask: *"That topic can run hot — want me to angle it toward the quieter parts, or pick something adjacent?"*

## Quality bar

- The story would be interesting if read at noon, **and** it slows the reader down by the end.
- A reader could miss the entire third act and lose nothing important.
- No sentence requires re-reading to understand.
- Read the last paragraph silently. If it sounds like a question or an opening, rewrite it.

## File output

```
downloads/bedtime-stories/2026-06-20-octopus-cognition.txt
```

- Plain text, UTF-8.
- Line 1: the title, in plain text, capitalized as a normal sentence (no markdown `#`).
- Line 2: blank.
- Lines 3+: the story body, prose only, no markup.
- No frontmatter, no metadata, no footer.

Before writing, ensure the directory exists:
```bash
mkdir -p downloads/bedtime-stories
```

## After writing — verify

Run the validator:
```bash
python3 .claude/skills/reading-bedtime-stories/scripts/validate_tts.py downloads/bedtime-stories/<file>.txt
```

It reports:
- Word count and whether it falls in the 2,900–3,500 band
- Any TTS hazards found (em-dashes, parens, markdown, abbreviations, URLs)
- Line numbers for fixes

Fix everything it flags. Re-run until it exits clean.

Also do a human pass:
- Read the last three sentences. They should feel like *settling*, not *opening*.
- Read the first sentence. It should be slow and second-person.
- Skim the middle. There should be at least two real claims worth knowing.

## Reference files

| File | Load when |
|------|-----------|
| `references/topic-flavors.md` | Choosing tone and shape for a specific topic genre |
| `references/example-openings.md` | Need example first sentences, transitions, breathing beats, or closings |
| `references/youtube-bedtime-narrator-patterns.md` | Choosing between thread and cluster Act II shape, or wanting a deeper quote bank from long-form bedtime narration |

## Examples

### Example 1 — Topic given

**User**: `/reading-bedtime-stories octopus cognition`

**Skill**:
1. *"A twenty-minute drift through octopus cognition, leaning toward the strangeness of distributed intelligence. Sound right?"*
2. User confirms.
3. Writes ~3,200 words, three acts, no markup.
4. Saves to `downloads/bedtime-stories/2026-06-20-octopus-cognition.txt`.
5. Runs validator. Two em-dashes flagged. Fixes. Re-runs. Clean.
6. Reports:
   > Saved. About twenty minutes at default Speechify speed.
   > `open downloads/bedtime-stories/2026-06-20-octopus-cognition.txt`

### Example 2 — No topic

**User**: `/reading-bedtime-stories`

**Skill**: *"What topic? I'll write you a roughly twenty-minute story you can play in Speechify or any TTS app. Anything from natural history to philosophy to a slow walk through a place — your pick."*

### Example 3 — Heavy topic

**User**: `/reading-bedtime-stories the Battle of Stalingrad`

**Skill**: *"That one runs hot for bedtime. Want me to angle it toward the quieter parts — the long winter, the river, daily life around the city before — or pick something adjacent like the geography of the Volga basin?"*
