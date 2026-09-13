# Source Hierarchy

This is the rule for what sources you read, in what order, and how you weight them when items conflict or compete for ranking.

## The four tiers

### Tier 0 — Evergreen (the shared knowledge base — check before all tiers)
Scaletopia's live research provider already holds mined evidence for most clients: **pains, lingo,
objections, beliefs, dream outcomes** (per client, confidence-scored, traced to the source call),
the **niche brain**, tiered **case studies**, **winner/loser copies with real results**, and client
**materials** (voice/positioning). Pull it FIRST — it is curated across every call and campaign we've
run, so it often answers a field before you open a single transcript.

- **Reach it:** `https://knowledgebase-production-f52e.up.railway.app`, header
  `Authorization: Bearer $EVERGREEN_API_KEY`; discover endpoints via `GET /api/docs`. Driven by the
  `evergreen-research` skill (`GET /api/clients/{slug}`, `POST /api/search {type:"pains"|...}`,
  `GET /api/clients/{slug}/replies`, `POST /api/clusters`).
- **Weight:** treat confirmed Evergreen items as Tier-1-grade (they are mined from the same live
  calls); `needs_more`-confidence items rank with Tier 2. Transcripts below are still ground truth
  for anything Evergreen lacks — and any NEW pain you mine should be saved back into Evergreen.

### Tier 1 — Live data (weight 3)
The buyer's actual words, captured live.

- Sales call transcripts (Fathom exports)
- Sales call transcripts (manual GDocs pasted in)
- Discovery / win-interview recordings transcribed via Riverside or similar
- Demo recordings where the buyer raised objections or asked questions

**Why weight 3:** This is the buyer telling you in their own words what they think. There is no higher-fidelity source.

**Where they live:** Inside the client folder, in a `transcripts/` subfolder. Files are usually `.docx`, `.txt`, or `.pdf`. Filenames typically include the prospect's name + date.

**What to extract:** Pains, language quotes, objections, dream outcomes, recurring themes. See `transcript-analysis.md` for how.

### Tier 2 — Structured client input (weight 2)
Filled by the client at onboarding. Variable quality — some clients fill it deeply, others give shallow one-liners.

- Master Sheet Tab 2 (Account Targeting — one row per industry)
- Master Sheet Tab 3 (Persona Targeting — one row per job title)
- Onboarding form (free-text answers)

**Why weight 2:** It's the client's curated view of their buyer, but it's filtered through their own bias and effort level. Two clients with identical buyers can fill the same Master Sheet very differently.

**Where they live:** GDrive client folder. Master Sheet is an xlsx file (5 tabs). Onboarding form is usually a GDoc.

**What to extract:**
- Tab 2: industry pain points, dream outcome, current solution, mistaken beliefs (→ Field 4a), dream ICP, recognizable logos
- Tab 3: persona responsibilities, persona pain points in their words, decision authority, what they care about
- Onboarding form: anything free-text that fills brief fields

**The risk:** If the client filled Tab 2 lazily for one industry but deeply for another, the AI will inherit that gap. The cross-source scoring (`score_pain_points.py`) is how we catch this — single-source-Tier-2 items get flagged as unverified.

### Tier 3 — Inferred market data (weight 1)
What the buyer's peers say publicly. Used to FILL GAPS in Tier 1 and Tier 2.

- Reddit threads (relevant subreddits per persona)
- X / Twitter discussions
- G2 reviews (for the buyer's existing tools / competitor tools)
- Capterra reviews
- Industry forums

**Why weight 1:** It's real language from real buyers, but it's not from THIS client's actual prospects. There's a generalization risk.

**Where they live:** The web. Pulled via `scripts/fetch_web_research.py` using query templates from `references/web-search-prompts.md`.

**What to extract:** Hidden service objections (cold-outreach reactions), verbatim language patterns, industry-belief patterns, dream-outcome statements.

**Rule:** Tier 3 items appearing alone — without corroboration from Tier 1 or Tier 2 — get flagged as `[unverified — Tier 3 only]`. They can be surfaced, but the strategist needs to know what they're looking at.

### Tier 4 — References (no weight, context only)
Read-only context. Used to inform the brief but not directly cited in fields about the buyer.

- Scored & Tiered case studies xlsx (the client's own wins, tiered S/A/B/C/D)
- Client website
- Client marketing material
- Prior briefs for this client (for continuity, NOT for buyer facts)

**Why no weight:** These describe the CLIENT, not the buyer. The brief is about the buyer.

**Where it lives:** Client folder.

## Scoring formula

For pain points, language quotes, and service hidden objections (Field 4b), each candidate item is scored as:

```
score = sum over all source appearances of (tier_weight)

where tier_weight is:
  Tier 1: 3
  Tier 2: 2
  Tier 3: 1
```

**Example — a pain point that appears in:**
- 2 transcripts → 2 × 3 = 6
- Master Sheet Tab 2 → 1 × 2 = 2
- 4 Reddit threads → 4 × 1 = 4
- **Total: 12 → HIGH confidence, surface as top pain**

**Example — a pain point that appears only in:**
- Master Sheet Tab 2 → 1 × 2 = 2
- **Total: 2 → LOW confidence, surface but tag as [unverified]**

**Example — a pain point that appears only in:**
- 1 Reddit thread → 1 × 1 = 1
- **Total: 1 → very LOW confidence, drop unless Tier 1 corroborates later**

## Fallback chain (when a source tier is empty)

The skill runs anyway and explicitly flags what's degraded. Per user spec — option B from Plan v3.

- **No Tier 1 (no transcripts):** Brief is filled from Tier 2 + Tier 3. Field 3 (Their Language) and Field 5 (Dream Outcome) will be the weakest — flag them and add the note "would be stronger with [N] sales transcripts."
- **No Tier 2 (no Master Sheet rows for this segment):** The client may have given the segment as freeform — ask them to fill the Master Sheet row, OR proceed with Tier 1 + Tier 3 only and flag heavily.
- **No Tier 3 (web research disabled or empty):** Brief is filled from Tier 1 + Tier 2 only. Field 4b (Service Hidden Objections) will be the weakest if no transcripts either.

## The rule of two

For pain points, language quotes, and service objections — items appearing in only ONE Tier 2 or Tier 3 source (and never in Tier 1) must be flagged as `[unverified — needs corroboration]`. Tier 1 items can stand alone.

This is your defense against the "AI takes the Master Sheet literally" failure mode.

## What the skill does NOT do

- It does not invent sources. If a file isn't there, the skill says it isn't there. It never fabricates.
- It does not invent quotes. If "Their language" needs verbatim quotes and there are none, the field gets a GAP marker.
- It does not silently fall back. If a tier is empty, the strategist sees the gap in the brief's source inventory appendix.
