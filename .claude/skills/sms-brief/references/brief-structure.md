# Brief Structure

> Each field's "Source priority" below starts with **Evergreen (Tier 0)** — pull mined pains, lingo,
> objections, beliefs, dream, and reply behaviour from `GET /api/clients/{slug}` + `POST /api/search`
> + `GET /api/clients/{slug}/replies` before Master Sheet / transcripts / web. See `source-hierarchy.md`.

The output document has 8 fields. Field 4 splits into 4a and 4b — they are different things and must not be conflated.

Length is whatever the buyer evidence supports. Half a page or three pages — both are fine if backed by real sources. What's not fine: padding with generic statements to make it look longer, or skipping fields because you didn't find evidence (use GAP markers instead).

## The framing — composite, not individual

Every claim in this brief describes the COMPOSITE / IDEAL buyer for this client's segment. A claim is a PATTERN observed across multiple sources, NOT a single prospect's specific data point.

- The CLAIM (what the brief states) sits at the pattern level.
- The CITATIONS (what supports the claim) point to the specific instances that prove the pattern.

Single-prospect data is evidence, not the headline. See `quality-bar-and-qa.md` Test 1b for the rule.

Every claim gets inline source citations. Format: `[source: <filename or master sheet location or URL>]`. When multiple sources support a pattern, list them all.

---

## Field 1 — Buyer

**What goes here:** Single paragraph (3-5 sentences) describing the buyer with enough specificity that an outsider could picture them.

**Required components:**
- Role (job title, or range of titles)
- Industry / sub-industry
- Company scale (employees, ARR/revenue band)
- Decision authority (final say / influencer / champion)
- Typical reports-to relationship
- Typical career background

**Source priority:** Master Sheet Tab 3 (persona row) → onboarding form free-text → transcript references to the buyer's role.

**Example structure (don't copy verbatim — use as shape reference):**
> Director of Marketing at DTC supplement brands, $5M–$50M ARR. Reports to Founder/CEO. Owns the marketing P&L, including paid acquisition, organic, and creative production. Typically came up through performance marketing at a previous DTC brand or agency. Decision-maker on marketing tooling and agency relationships; final spend authority for budgets under $50K/month. [source: Master Sheet Tab 3, "DTC VP of Marketing" row]

---

## Field 2 — Top 3-5 pains (ranked)

**What goes here:** Bulleted list of the 3-5 highest-confidence pain PATTERNS — observable across multiple sources for this segment.

**Format per pain (pattern level):**
- The pain PATTERN in 1 sentence describing what's TRUE for buyers in this segment (not for any one prospect)
- Sub-bullet: cross-source evidence summary (e.g., "5 of 7 transcripts; Master Sheet Tab 2; 12 Reddit threads")
- Sub-bullet: 2-3 supporting verbatim quotes from different sources, each with citation, that prove the pattern
- Sub-bullet: score from `score_pain_points.py` + verification status

**Quality requirements:**
- Each pain must be a PATTERN, not a single-prospect data point. If only 1 transcript supports it (no other sources), it's not yet a pattern — handle per the rule in `transcript-analysis.md` Pass 2.
- Each pain must appear in ≥2 sources OR be Tier 1 with multiple transcript appearances.
- Single-source-Tier-2-or-3 pains: include them but tag as `[unverified — needs corroboration]`
- No "CaC is high" generic statements (Test 1a). No "Brand X had a specific Q3 issue" data dumps (Test 1b). The headline pain is the pattern; the data points are the citations beneath it.

**Worked example (right level):**
> **Pain #1: 30-60% CAC inflation across DTC health & wellness post-iOS attribution loss + creative restrictions on supplement claims**
> - Evidence: 5/7 sales transcripts mention this in similar terms; Master Sheet Tab 2 row "DTC Health" lists rising CAC as top pain; 12 Reddit threads in r/ecommerce and r/supplements echo
> - Supporting quotes:
>   - "Our blended CAC is up 47% YoY and Meta keeps rejecting our creative" [transcript-003.docx, ~22:15]
>   - "CAC creeping up — used to break even at $40, now we need $65 just to keep ROAS at 2" [transcript-005.docx, ~14:20]
>   - "iOS killed our retargeting and the creative restrictions are killing our new prospecting" [Master Sheet Tab 2, "DTC Health" row]
> - Score: 14 (verified — Tier 1 + Tier 2 + Tier 3 corroboration)

---

## Field 3 — Their language

**What goes here:** 10-20 verbatim quotes from sources, organized into:
- **How they describe the problem** (5-8 quotes)
- **How they describe success / what they want** (3-5 quotes)
- **Words they use for the work** (industry-specific vocabulary)
- **Words / phrases that mark you as an outsider — AVOID** (3-5 phrases)

**Hard rules:**
- Every quote must be VERBATIM. If you paraphrased, drop the quotation marks.
- Every quote must have a citation (transcript + timestamp/quote, G2 review URL, Reddit thread URL)
- If you can't find 5+ verbatim quotes for a sub-section, GAP-mark it with: "needs more sales transcripts" or "needs G2/review research"

This is the highest-leverage field. SMS copy lives or dies on whether it sounds like the buyer's voice or like an agency pitch.

---

## Field 4a — Industry mistaken beliefs

**What goes here:** What this buyer wrongly believes about their own industry or market.

**Examples:**
- "SEO is dying because everyone uses LLMs now"
- "I can measure each channel independently to gauge effectiveness"
- "PPC is safer than SEO because it's easier to measure"
- "Buying leads is faster than building demand"

**Source priority:** Master Sheet Tab 2 "Mistaken Beliefs" column → transcripts (when buyer expresses a belief about their market) → industry forums.

**Format:** Bulleted list. Each belief gets a citation. Each belief gets a one-line note on WHY it's wrong (the real picture).

---

## Field 4b — Service hidden objections

**What goes here:** What the buyer is thinking when they receive your kind of cold outreach. What stops them from replying.

**Examples:**
- "Another agency promising the moon, like the last three"
- "All agencies say the same thing — performance + brand + measurable"
- "If it sounds too good to be true, it is"
- "They're going to disappear after onboarding like the last one"

**Source priority:** Sales transcripts (look for mid-call objections the prospect raised before they bought) → past SMS reply patterns (negative replies) → Reddit threads about cold outreach to this persona type.

**Format:** Bulleted list. Each objection gets a citation. Each objection gets a one-line note on WHAT mechanism in the SMS would dissolve it (this is the bridge to Layer C).

**This is different from 4a.** 4a is about their world; 4b is about your offer. Don't conflate.

---

## Field 5 — Dream outcome

**What goes here:** What this buyer wants — in their words, not in agency-speak.

**Format:** 2-4 bullets, each a verbatim or near-verbatim restatement of a stated dream outcome from a real source. Each cited.

**Source priority (per user spec):** Master Sheet Tab 2 "Dream Outcome" column as **seed**. Then when sales transcripts exist, surface the buyer's actual phrasing of success and **replace** the Master Sheet phrasing. Master Sheet stays as fallback only.

**Quality requirement:** If the only source is Master Sheet and you wouldn't be surprised to read the same wording in 5 other clients' Master Sheets, flag for follow-up: "needs transcript corroboration."

---

## Field 6 — Sophistication level

**What goes here:** Low / Mid / High, with a one-line justification grounded in evidence.

**How to assess:**
- **Low:** They're surprised by basic best practices. They describe their stack vaguely. They use generic industry language. They have an in-house junior team or first-time agency.
- **Mid:** They know what works. They've worked with an agency before. They describe their stack in specific tools. They distinguish between tactics.
- **High:** They speak the agency's language back at them. They reference specific frameworks (PMF, blended CAC, attribution windows). They've been through 2-3 agency cycles. They critique tactics, not endorse them.

**Source priority:** Transcripts (best signal) → Master Sheet Tab 2 "Current Solution" + Tab 3 → onboarding form.

**Format:** `Sophistication: [Low/Mid/High]. Evidence: [one-line]. [source citation]`

---

## Field 7 — Reply behaviour

**What goes here:** What's gotten this buyer (or buyers in this segment) to reply to outbound vs. what hasn't.

**Format:**
- Replies favorably to: [bullets] [source: prior campaign log + transcripts]
- Ignores / negative-replies to: [bullets] [source: prior campaign log]
- Reply lag / channel preference: [if known]

**Source priority:** Prior campaign log (best signal — actual replies) → Master Sheet Tab 2 "Mistaken Beliefs" / Tab 3 → transcript references to past outreach experiences.

**If no prior campaign data:** GAP-mark with "no campaign history yet for this segment — first send will inform future iterations."

---

## Appendix — Source Inventory

Append a summary at the bottom showing what the skill found vs. what was missing:

```
SOURCE INVENTORY
✓ Master Sheet Tab 2 — DTC Supplements row
✓ Master Sheet Tab 3 — VP of Marketing DTC row
✓ Onboarding form
✓ Sales transcripts: 7 found (in client folder /transcripts/)
✓ Scored & Tiered case studies xlsx
✗ Prior SMS campaign log (no campaigns shipped yet for this segment)
✗ G2 reviews (not pulled — client not on G2)

QA PASS SUMMARY
12 claims passed all 4 QA tests
2 claims flagged as unverified (single-source-Tier-3)
1 field GAP-marked (Field 7 — no campaign history)
```

This appendix matters. It tells the strategist exactly what they're working with.

---

## What's NOT in the brief

These are explicitly NOT in the brief — they belong to other layers:

- Outcome variants — that's Layer B (sms-synthesis)
- Mechanisms — that's Layer B (sms-synthesis)
- Psychological lever pick — that's Layer C (sms-draft)
- Template references — that's Layer C (sms-draft)
- Draft SMS copy — that's Layer C (sms-draft)

The brief is buyer evidence only. Keep it that way.
