# Beliefs vs. Objections — Field 4a vs. 4b

The original flowchart combined "hidden objections" into one field. That's wrong because it's two different things, and conflating them produces sloppy copy.

> Evergreen mines both, separately: `kind=belief` and `kind=objection` per client (`POST /api/search {"type":"pains"}`), plus this-week objections via `GET /api/clients/{slug}/replies`. Pull those first, then use this Blueprint to keep 4a vs 4b clean.

This Blueprint defines the distinction and gives worked examples.

---

## Field 4a — Industry Mistaken Beliefs

**Definition:** What the buyer WRONGLY believes about their own industry, market, or category.

These are not objections to your service. They are misconceptions about how their world works.

### Source priority
- Master Sheet Tab 2 "Mistaken Beliefs" column (this is exactly what the column captures)
- Sales transcripts (when the buyer expresses a belief about their market that you know is wrong)
- Industry forums (Tier 3)

### Examples by client type

**B2B SaaS:**
- "SEO is dying because everyone uses LLMs now"
- "I can measure each channel independently to gauge effectiveness"
- "PPC is safer than SEO because it's easier to measure"

**DTC ecommerce:**
- "Influencer marketing is the only way to break through the noise"
- "Humor doesn't work in our category — too serious"
- "Facebook ads are too expensive to run profitably now"

**Multi-location / franchise:**
- "I need different agencies for different channels"
- "AI is going to replace marketers in the next 2 years anyway"
- "Local SEO is just GMB listings"

**Insurance / financial services:**
- "Nobody can write content for our industry because of compliance"
- "Buying leads is safer than building demand"
- "Brand doesn't matter in our space — only lead cost"

### Format in the brief
```
4a — Industry Mistaken Beliefs:

- "SEO is dying because everyone uses LLMs"
  - Why this is wrong: GEO + traditional SEO together is producing 3-5x more 
    AI-indexed visibility than pure organic for B2B SaaS in 2025.
  - [source: Master Sheet Tab 2, B2B SaaS row; corroborated in transcript-001.docx 
    where prospect said "isn't SEO basically dead in the AI era?"]
```

### Why this matters for Layer C
4a beliefs become the SETUP for the SMS hook. If the buyer believes "SEO is dying," you can lead with "SEO isn't dying — it's bifurcating, and the agencies that figured out GEO are winning." That's a pattern interrupt rooted in their actual worldview.

---

## Field 4b — Service Hidden Objections

**Definition:** What the buyer thinks when they SEE YOUR COLD OUTREACH. The mental wall between reading your SMS and replying to it.

These are objections to your offer, your channel, your pitch — not objections to their industry.

### Source priority
- Sales transcripts (look for mid-call objections — what the prospect raised before they decided to buy from the salesperson)
- Past SMS reply patterns (specifically negative or non-replies — what got ignored, what got "not now" responses)
- Reddit threads about cold outreach to this persona type (Tier 3)

### Examples by buyer type

**B2B SaaS / VP of Marketing:**
- "Another agency promising the moon, like the last three"
- "All agencies say the same thing — they help with brand and performance"
- "Their case study is probably one outlier they got lucky on"
- "They'll disappear after onboarding"
- "I don't have time for another sales call this quarter"

**DTC founder:**
- "Agencies don't understand DTC specifically — they treat us like B2B"
- "They'll burn my budget for 3 months learning the brand"
- "Last agency promised 5x ROAS and delivered 1.2x"
- "Why is a stranger texting me — this feels like a scam"

**Multi-location / franchise:**
- "They don't get how franchises work — they'll try to do generic SEO"
- "I've tried 4 agencies in 2 years, none kept their promises"
- "Their case study is for one location, not 50"

### Format in the brief
```
4b — Service Hidden Objections (what blocks replies):

- "Another agency promising the moon"
  - Mechanism that dissolves it: lead with the SPECIFIC client + SPECIFIC number 
    + SPECIFIC mechanism (not generic claims). Skip the "we help X grow Y" frame.
  - [source: transcript-003.docx, prospect said "I've heard that pitch 10 times this year"]

- "They'll disappear after onboarding"
  - Mechanism that dissolves it: mention the length of an existing client 
    relationship in the SMS (e.g., "we've been the partner behind Awardco for 5 years")
  - [source: Reddit r/marketing thread about agency horror stories]
```

### Why this matters for Layer C
4b objections are the friction points the SMS must preemptively neutralize. Each objection gets a "dissolves it via [mechanism]" annotation so the copywriter knows what tactical move addresses each block.

---

## How to tell them apart (decision rule)

When you find a candidate item, ask:

**"Is this about how the buyer's WORLD works (industry, market, category)?"**
- YES → Field 4a
- NO → continue

**"Is this about how the buyer perceives MY OUTREACH or MY KIND OF SERVICE?"**
- YES → Field 4b

### Edge cases

**"Marketing agencies are all the same"** — This is about agencies (the service category being pitched). It's 4b.

**"AI is going to replace marketing teams"** — This is about their industry/future. It's 4a.

**"I tried 3 agencies and none worked"** — This is past experience with the service category. It's 4b.

**"SEO doesn't work for my industry"** — This is about their industry's relationship to a tactic. It's 4a (a mistaken belief about their world).

**"You're going to charge me $10K/month and disappear"** — This is about my offer specifically. It's 4b.

**"My industry doesn't respond to cold outreach"** — Ambiguous. If they're saying "buyers in my industry generally don't respond" → 4a. If they're saying "I personally don't respond to cold outreach" → 4b. Default to 4b when in doubt.

---

## Why this distinction matters

4a beliefs become the HOOK setup — you challenge a mistaken belief about their world.
4b objections become the FRICTION removal — you preemptively address what blocks their reply.

Conflating them produces copy that addresses neither well. Splitting them gives the copywriter two precise tools.
