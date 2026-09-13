# Transcript Analysis

Sales call transcripts are Tier 1 — the highest-weight source. They contain unfiltered buyer language, which is what makes Layer A copy land or fail.

> Check **Evergreen (Tier 0)** first: the pains/lingo/objections from these calls may already be mined
> (`GET /api/clients/{slug}`, `POST /api/search {"type":"pains"|"calls"}`, traced to `source_call`). Analyze
> raw transcripts for what it lacks — and save new findings back (`POST /api/agents/transcript`) so it compounds.

This Blueprint defines what to extract from a raw transcript and how to tag each extraction so it can be cited later.

## What you're looking for

A sales transcript is dense with signal but most of it is noise (small talk, scheduling, audio glitches). You're hunting for six things:

### 1. Why the prospect agreed to the call
Almost every discovery call has a moment in the first 5-10 minutes where the prospect explains why they took the meeting. This is gold — it tells you what trigger pulled them in.

**What to capture:** A verbatim or near-verbatim version of their answer.

**Why it matters:** This is direct evidence of the buyer's current pain or current curiosity. Field 2 (Top pains) and Field 7 (Reply behaviour — what works in outbound) lean on this.

**Common patterns:**
- "We tried [thing] and it didn't work, so I was open to hearing your angle"
- "Your message about [specific topic] caught my eye because we've been struggling with [thing]"
- "I get pitched a lot but yours mentioned [X] which is something we're actively working on"

### 2. What they found interesting (live reaction patterns)
Listen for moments where the prospect leans in — verbal cues like "oh that's interesting", "wait — say that again", "that's exactly what we need", "huh, I hadn't thought about that."

**What to capture:** The thing that triggered the reaction (the specific claim, mechanism, or outcome the sender mentioned), plus the prospect's exact reaction.

**Why it matters:** This is direct evidence of what resonates with this buyer. If 5 transcripts all show the prospect lighting up at "we got them ranked for non-branded long-tail keywords", that mechanism belongs in Layer C drafts.

### 3. Mid-call objections (Field 4b material)
Every discovery call surfaces 2-5 objections the buyer hasn't said out loud before. These are GOLD for Field 4b (service hidden objections).

**What to capture:** The objection in their words. Note the moment it was raised (after what claim from the sender).

**Common patterns:**
- "But how is that different from what [competitor] does?"
- "We tried that before with [previous agency] — what makes you think it'll be different?"
- "How quickly would we see results — because I need to show ROI by [date]"
- "I've been burned by agencies before, what's the catch?"
- "Your guarantee — is that real or just marketing?"

**Why it matters:** These are the exact objections that stop replies on cold SMS. If your draft doesn't preemptively address them, it dies.

### 4. Common questions across multiple transcripts (recurring themes)
When you have 5+ transcripts for one client+segment, look for questions or concerns that come up REPEATEDLY across multiple prospects.

**What to capture:** The question, how many transcripts it appears in, the exact phrasing variations.

**Why it matters:** Recurring questions across prospects = the dominant pattern of confusion or interest in that segment. This is what the brief's Field 2 (Top pains) is supposed to surface.

**Example:**
- 5 of 7 DTC supplement transcripts contain a version of: "How is what you do different from just running more Meta ads?"
- That's a recurring theme. Field 2 should reflect "buyer assumes Meta ads is the default solution" and Field 4b should reflect "all agencies sound the same — what makes you specifically different?"

### 5. Verbatim language patterns (Field 3 material)
Listen for the buyer's actual vocabulary — the words and phrases they use for their work, their problems, their goals.

**What to capture:** Direct quotes (with citation: transcript filename + rough timestamp or surrounding quote). Look for:
- How they describe their job ("I run paid", "I own demand gen", "I'm head of growth")
- How they describe the problem ("CaC is creeping up", "we're stuck", "performance has plateaued")
- How they describe success ("hitting our number", "blended CAC under X", "scaling without burning budget")
- Industry jargon they use casually (which marks them as an insider)
- Words that mark you as an outsider if YOU use them (corporate-speak the buyer never uses)

**Rule:** EVERY verbatim quote in Field 3 must come with a citation. Paraphrased = not verbatim = drop the quotes.

### 6. Dream outcome statements (Field 5 material)
Listen for moments where the prospect describes the future they want.

**Common patterns:**
- "What I really need is..."
- "If we could just..."
- "My boss is on me about [outcome]"
- "If I could show [X result] by [date], I'd look like a hero"

**What to capture:** Their exact framing of success.

**Why it matters per spec:** When a transcript has a dream outcome stated by the buyer, it REPLACES the Master Sheet Tab 2 "Dream Outcome" phrasing (per the v3 plan). Master Sheet is a seed; transcripts are ground truth.

## What to ignore

Most of a transcript is noise. Specifically ignore:

- Small talk and pleasantries
- Logistics (scheduling, tool issues, "can you hear me")
- The salesperson's own pitch language (you're listening for the BUYER's voice, not the seller's)
- Compliments and politeness ("yeah totally", "for sure", "makes sense") — these aren't real signal
- Closing logistics (next steps, calendar invites)

If a section of the transcript doesn't contain BUYER signal, skip it.

## Citation format

Every extraction gets tagged like this:

```
[source: transcript-filename.docx, "<verbatim quote or surrounding context>"]
```

Or if the transcript has timestamps:

```
[source: transcript-filename.docx, ~12:34, "<verbatim quote>"]
```

The point of the citation is so the strategist can verify any claim by going back to the source.

## When you have multiple transcripts — THIS IS THE WHOLE POINT

Reading one transcript gives you data points about one prospect. Reading multiple transcripts and finding COMMONALITY across them gives you the PATTERN — which is what the brief is supposed to surface.

The brief is NOT a summary of any single prospect. It's a composite ICP built from patterns observed across multiple sources.

### Two-pass extraction

**Pass 1 — Per-transcript extraction:**
For each transcript individually, extract per the six things above (pains, language, objections, themes, dream outcomes, beliefs). Tag each extraction with its source citation.

**Pass 2 — Cross-transcript pattern detection (the critical pass):**
Now look across ALL extractions and answer:

- Which pains appear in 3+ transcripts? Those are PATTERN pains — surface them as Field 2.
- Which objections appear in 2+ transcripts? Those are PATTERN objections — surface them in Field 4b.
- Which language phrases or vocabulary patterns repeat across 3+ transcripts? Those are the AUTHENTIC voice of the segment — surface as Field 3.
- Which dream-outcome statements appear in similar form across 2+ transcripts? That's the SHARED dream outcome — surface as Field 5.
- Which beliefs (about their industry) come up repeatedly? Those are Field 4a patterns.

**The output of Pass 2 is what goes in the brief.** Pass 1 extractions are the EVIDENCE that supports the patterns — they become the citations under each claim.

### Single-transcript items

Themes, pains, or objections that appear in ONLY ONE transcript are not yet patterns. Handle them like this:

- If the item also appears in Master Sheet Tab 2 (Tier 2) → it's still a pattern, just weaker. Surface with the `[unverified — only 1 transcript + Master Sheet]` flag.
- If the item appears in NO other source → it's not a pattern. Don't surface it as a Field 2 pain. (It might still be useful context, but it's not the segment's pattern.)

### Why this matters

Without Pass 2, the brief becomes a quote dump from individual prospects. With Pass 2, the brief becomes a characterization of what's TRUE across the segment.

Example of the difference:

❌ Without Pass 2 (per-transcript dump):
> Field 2 Pain #1: "Prospect at Company X said their CAC jumped from $89 to $134 in Q3" [transcript-005.docx, ~14:20]

✓ With Pass 2 (cross-transcript pattern):
> Field 2 Pain #1: "Mid-size DTC health & wellness brands are seeing 30-60% CAC inflation post-iOS attribution changes — a category-wide pressure, not a one-off." 
> Evidence: 5 of 7 transcripts mention CAC inflation in this range; Master Sheet Tab 2 lists "rising CAC" as a top pain; r/ecommerce threads echo the pattern. [sources: transcript-001, 003, 005, 006, 007; Master Sheet Tab 2 row "DTC Health & Wellness"; reddit.com/r/ecommerce/comments/xyz...]

Same underlying data. One reads like a quote dump. The other reads like ICP intelligence. That's the difference Pass 2 makes.

## What if you only have one transcript?

You can still use it — it's Tier 1 weight. But:
- Note in the source inventory: "only 1 transcript — recurring-pattern signal is weak"
- Cross-corroborate aggressively with Tier 2 + Tier 3
- Push for more transcripts to be recorded for future iterations

## What if you have ZERO transcripts?

Tell the strategist explicitly in the source inventory: "no transcripts available. Field 3 (Their Language) will be weak; Field 5 (Dream Outcome) will rely on Master Sheet phrasing only; Field 4b (Hidden Objections) will rely on Tier 3 scraping."

Then run the skill anyway with what you have. Per the v3 source-missing behaviour: degrade and flag, don't refuse.
