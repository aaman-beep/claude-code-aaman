# Data Sources Per Field

Quick-reference table mapping each brief field to its source priority order. Use this to avoid guessing where to look when filling a field.

For full source definitions and weights, see `source-hierarchy.md`.

> **Check Evergreen first for every row below.** It is Tier 0 (see `source-hierarchy.md`) and usually
> already holds these fields, mined and confidence-scored: pains/lingo/objections/beliefs/dream via
> `GET /api/clients/{slug}` + `POST /api/search`; this-week objections via `GET /api/clients/{slug}/replies`;
> reply behaviour via the deals/contacts reply threads. The transcript/Master-Sheet/web columns fill
> whatever Evergreen lacks — and new findings get saved back.

---

## The mapping

| Field | Primary source (Tier 1) | Secondary (Tier 2) | Fallback (Tier 3) |
|---|---|---|---|
| **1. Buyer** | Transcripts (role mentions) | Master Sheet Tab 3 + onboarding form | LinkedIn job listings for the persona |
| **2. Top 3-5 pains** | Transcripts (extract per `transcript-analysis.md`) | Master Sheet Tab 2 "Pain Points" + Tab 3 "Pain Points in their words" | Reddit/X for {persona} {industry} pain language |
| **3. Their language (verbatim)** | Transcripts (verbatim quotes from buyer) | Onboarding form free-text quotes | G2/Capterra reviews + Reddit verbatim quotes |
| **4a. Industry mistaken beliefs** | Transcripts (beliefs about market) | Master Sheet Tab 2 "Mistaken Beliefs" | Industry forums + LinkedIn |
| **4b. Service hidden objections** | Transcripts (mid-call objections) | Past SMS reply patterns | Reddit threads about cold outreach to {persona} |
| **5. Dream outcome** | Transcripts (buyer's stated dream) | Master Sheet Tab 2 "Dream Outcome" (seed, replaced by Tier 1) | LinkedIn posts by {persona} |
| **6. Sophistication level** | Transcripts (how they speak about tactics) | Master Sheet Tab 2 "Current Solution" + Tab 3 | — |
| **7. Reply behaviour** | Prior campaign log (replies) | Master Sheet (if filled) | — |

---

## Reading rule

For each field, you read sources in order: Tier 1 first, Tier 2 second, Tier 3 only as gap-fill.

If Tier 1 has rich material for a field, you may not even need Tier 2 or 3. Don't pull from lower tiers just because they exist — pull because Tier 1 was thin.

## Dream outcome (Field 5) — special rule

Per v3 plan: Master Sheet Tab 2 "Dream Outcome" is the SEED. When transcripts surface the buyer's actual phrasing of success, that REPLACES the Master Sheet version. Master Sheet stays as fallback only.

This is the one field where Tier 1 doesn't just outrank Tier 2 — it overrides it.

## Field 7 — special note

If no prior campaign log exists for this segment (first campaign), Field 7 gets GAP-marked with: "no campaign history yet for this segment — first send will inform future briefs."

This is expected for new clients and new segments. Don't try to fabricate reply behaviour data.

## Cross-field reading

Some sources fill multiple fields. When you read a transcript, look for all six things at once (per `transcript-analysis.md`):

- Why they took the call → Field 2 + Field 7
- Mid-call reactions → Field 2 + Field 3
- Mid-call objections → Field 4b
- Verbatim language → Field 3
- Dream-outcome statements → Field 5
- Industry beliefs they express → Field 4a

One transcript pass should feed 4-6 fields, not just one.

## Cross-field reading for Master Sheet

When you read Master Sheet Tab 2 row, look for:
- Pain Points → Field 2
- Dream Outcome → Field 5 (seed)
- Current Solution → Field 6 + Field 2
- Mistaken Beliefs → Field 4a
- Dream ICP → Field 1 (context)
- Recognizable Logos → Field 1 (context)

When you read Master Sheet Tab 3 row:
- Job Title → Field 1
- Primary Responsibilities → Field 1
- Pain Points in their words → Field 2 (+ Field 3 if any are verbatim)
- Current Solution → Field 6
- What They Care About → Field 5 (corroboration)
- Decision Authority → Field 1
