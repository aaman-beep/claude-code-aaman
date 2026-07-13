---
name: mechanism-wordsmith
description: Wordsmith a literal agency mechanism into 5–7 cold-SMS-ready reframings using patterns extracted from Scaletopia's winning SMS templates database. Use when a strategist has the brief (pains, dreams, language) and a chosen case study with a known literal mechanism, but needs to turn "what the agency actually did" into a sticky, jargon-free, pain-dissolving line that fits inside an SMS template's {{unique_mechanism}} slot. Triggers on phrases like "wordsmith this mechanism", "make this mechanism sticky", "reframe [tactic] for SMS", "mechanism variants for [case study]", "unique mechanism for [client]", "give me SMS-able mechanisms", "I have the case study, need the mechanism line". Do NOT use to invent mechanisms from scratch — the literal mechanism must already be known from the case study, master sheet, or sales call. Do NOT use for full SMS copy drafting — this skill produces only the mechanism string; SMS assembly happens downstream.
---

# Mechanism Wordsmith

## What this skill does

Takes a **literal mechanism** (one or two sentences describing what the agency actually did — the tactic, the channel, the process, the tool) and returns **5–7 SMS-ready reframings**, each anchored to a verified pattern from Scaletopia's winning SMS templates database.

The strategist does not have to invent the reframing structure. The structure is borrowed from a proven winning SMS. The strategist's own creativity is freed up for the final pick.

## Why this skill exists

When Scaletopia strategists sit down to write the `{{unique_mechanism}}` portion of an SMS, the bottleneck is not creativity. The bottleneck is:

1. Re-reading the case study to extract what the agency actually did
2. Stripping jargon ("Cost Cap per SKU", "contribution margin", "blended ROAS")
3. Matching the mechanism to a pain in the brief
4. Inventing a sticky framing — usually from scratch, every time

Step 4 burns hours and produces inconsistent quality because there is no library of mechanism patterns to draw from. This skill IS that library. It pre-encodes the 8 mechanism reframing patterns that appear in the 13 proven winning SMS examples, and applies them to any literal mechanism the strategist hands in.

## Inputs

**REQUIRED:**
- **Literal mechanism** — 1–2 sentences describing what the agency actually did. Examples:
  - "Used 1,000 unpaid micro-influencer videos as paid creative on meta, combined with Cost Cap campaigns per SKU"
  - "Trained meta CPA bidding to optimize on first-time customers, not site visitors or form fills"
  - "Wrapped agency creative output with a flywheel of 150 ad concepts per month sourced from real users"
- **Case study client name** — for tagging output (e.g., "Supergut", "Black Girl Vitamins")
- **Case study outcome** — the headline number (e.g., "$100k paused meta spend → $1m/mo NCR in 3 months")

**STRONGLY RECOMMENDED:**
- **Pain hierarchy from the Layer A brief** — top 3 pains the SMS must dissolve. Without this, the skill can only optimize for stickiness and jargon, not pain-dissolution.

**OPTIONAL:**
- **Industry / segment** (e.g., "DTC Health & Wellness") — sharpens which patterns apply
- **Persona** (e.g., "Founder/CEO" vs "Marketing Leader") — affects which framings land
- **Already-tried variants the strategist wants to avoid repeating**

## Output

A ranked menu of 5–7 mechanism variants. For each variant:

- **The variant text** — exactly as it would slot into `{{unique_mechanism}}` in the SMS template
- **Pattern tag** — which of the 8 patterns from the library it uses (e.g., "Pattern 3: Constraint Negation")
- **Pain dissolved** — which brief pain it answers (if pain hierarchy was provided)
- **Quality flags** — jargon-free (Y/N), under 25 words (Y/N), has sticky anchor (Y/N), borrows from a winning example (Y/N)
- **Score** — 0–4, sum of the quality flags
- **One-line rationale** — why this pattern fits this mechanism

The menu is sorted by score, then by pattern leverage for the target pain.

The strategist picks the final one (or two — Email 1 and Email 3 can use different patterns for the same case study).

## Workflow

### Step 0 — Confirm inputs

If the literal mechanism is vague, missing, or contains pure jargon ("we used Cost Cap" with no explanation), stop and ask the strategist to clarify. Do not invent the mechanism. If the case study has no clear mechanism in the Master Sheet or transcripts, that case study is not ready for SMS — kick it back.

### Step 1 — Load the pattern library

Read `references/mechanism-patterns.md`. The 8 patterns are:

1. Contrarian Refresh
2. Hidden Misattribution Fix
3. Constraint Negation
4. Trigger / Moment Frame
5. Position Engineering
6. Visual Theft / Inversion
7. Named Methodology Abstraction
8. Plain-English Tactic

Each pattern has an applicability test ("when does this fit the mechanism?").

### Step 2 — Run pattern applicability for the input mechanism

For each of the 8 patterns, ask the applicability question (see `mechanism-patterns.md`). Mark each pattern as APPLIES, MAYBE, or DOESN'T FIT.

A pattern APPLIES if there's a clean structural mapping from the literal mechanism to the pattern. A pattern MAYBE applies if the mechanism can be twisted into the pattern but the fit is not natural. A pattern DOESN'T FIT if forcing it produces a sentence that is misleading or empty.

Aim for 4–6 APPLIES + MAYBE patterns. If fewer than 3 patterns apply, the literal mechanism is either too vague (kick back) or too unique to be SMS-able with a proven structure (rare — write a Plain-English Tactic variant and flag).

### Step 3 — Generate one variant per applicable pattern

For each APPLIES pattern, write ONE variant. For each MAYBE pattern, write a variant if it produces something legitimately different from the APPLIES variants. Do not write multiple variants of the same pattern.

Each variant must:
- Slot cleanly into `{{unique_mechanism}}` in any SMS template — no leading conjunction, no trailing punctuation
- Be ≤ 25 words (target: 8–18 words)
- Use the literal mechanism's actual content (no hallucinated tactics)
- If the pattern requires it, borrow a 2–3 word phrase structure from a verified winner (see `mechanism-patterns.md` for which phrases are reusable)

### Step 4 — Run quality filters

Read `references/quality-filters.md`. For each variant, apply the four filters:

- **Jargon test** — would a smart person outside the industry understand it without Googling?
- **Length test** — ≤ 25 words?
- **Sticky anchor test** — has at least one of: specific number, named tactic, contrarian word, "without X" clause, named position?
- **Pain-dissolution test** — if pain hierarchy is provided, does this variant answer at least one named pain? Mark which one.

A variant fails the menu if it fails jargon OR length. (Sticky anchor and pain-dissolution failures just lower the score; they don't disqualify.)

### Step 5 — Score and rank

Read `references/scoring-rubric.md`. Score each variant 0–4 (one point per filter passed). Rank descending. Break ties by pattern leverage for the top pain (see rubric).

### Step 6 — Output the menu

Render the ranked menu in this exact format:

```
=== MECHANISM VARIANTS FOR [Client Name] ===
Outcome anchor: [outcome line]
Literal mechanism: [verbatim input]

Top pain being dissolved: [pain #1 from brief, if provided]

#1 (Score 4/4) — [Pattern Name]
  Variant: "[the variant text]"
  Pain dissolved: [pain name]
  Why this fits: [one line]

#2 (Score 4/4) — [Pattern Name]
  ...

[continue for all variants, ranked]

=== STRATEGIST PICK ===
Reminder: pick 1–2. Email 1 and Email 3 (separate threads) can use different patterns for the same case study. Email 2 stays on the Email 1 thread, so it doesn't repeat the mechanism.
```

### Step 7 — DO NOT write the full SMS

This skill produces only the `{{unique_mechanism}}` string. Full SMS assembly is downstream. If the strategist asks "now write the SMS," redirect — that is a separate skill.

## Hard rules

- Never invent a tactic that isn't in the literal mechanism input. If the input says "1,000 micro-influencers", variants may say 1,000 — they may not say 5,000.
- Never wordsmith jargon into a variant. If the literal mechanism is "Cost Cap campaigns per SKU", the variant must translate that into plain English (e.g., "set a hard ceiling on what we'd pay per sale, per product"). The strategist should be able to defend every word on a sales call.
- Never produce a variant that breaks an SMS template's grammar. Test by mentally inserting it into Template 1: "I took {{client}} from {{X}} to {{Y}} using {{variant}}". If it reads weird, rewrite.
- Never produce more than 7 variants. If more than 7 patterns apply, the strategist picks the top 7 by quality score; do not pad with low-quality variants.
- Never output without quality flags. Every variant ships with all four flags visible so the strategist knows exactly why it scored what it scored.

## When NOT to use this skill

- The strategist has not yet selected a case study (use Layer B selection first)
- The literal mechanism is unknown (go research the case study first)
- The strategist wants the full SMS, not just the mechanism string (separate skill)
- The strategist is writing for a non-cold channel (LinkedIn DM, email, voice — patterns may differ; this library is anchored to cold SMS specifically)

## Quality bar

A v1 run is successful if at least 3 of the 5–7 variants score 4/4 and the strategist picks one within 5 minutes of seeing the menu. If the strategist needs to write a variant themselves because none of the menu fits, that's a signal the pattern library is missing a pattern — log the gap and iterate.
