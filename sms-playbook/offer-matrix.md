# Offer Matrix — the universality router

> ⏸ **ON HOLD (Aaman's call).** This read as over-built / confusing. **Routing for now comes from the
> winners** — match the case study to the closest tagged winner(s) (same offer/niche) and pull
> lever / what-carries / pattern / mechanism-or-omit from there. Pull those winners from **Evergreen**
> (`POST /api/search {"type":"copies","status":"winner"}` + `{"type":"offers"}` by `service`), which is
> the live version of the routing this matrix hand-rolled; `winners.csv` is the local seed. Kept for
> reference, not in the critical path. (If revived, fold in the correction: **ammo / case-strength picks
> the lever, sophistication only flavours tone** — not the other way round.)

> The lookup that makes the system work across ALL clients, not just Kynship. It takes an **offer
> archetype** and tells you which lever to lean on, what carries the text, and — critically — **whether to
> generate a mechanism or omit it.** This is the fix for "it broke on GEO/SEO-to-SaaS (Big Leap)": that
> failure was forcing a unique mechanism onto an offer that doesn't have one.
>
> Read this FIRST, before the wordsmith generates anything.

---

## Step 1 — Identify the offer archetype

| Archetype | Example offers | Example winners |
|---|---|---|
| **DTC paid-creative / seeding** | Meta/TikTok creative, UGC, influencer seeding | W1, W11, W16, W17 (Kynship) |
| **SEO / GEO / organic** | Google ranking, organic, GEO, local SEO | W4, W5, W8, W9, W10, W14 (**Big Leap lives here**) |
| **PR / authority** | PR, founder positioning, media | W2 |
| **Local / home-services / trigger** | restoration, vet, insurance, trades, guarantee offers | W3, W12 |
| **Agency / outbound / lead-gen** | cold outbound, appointment-setting for agencies | W6, W13, W15 |

---

## Step 2 — Route it

| Archetype | Lead lever | What carries | Mechanism? | Live Tier-2 patterns |
|---|---|---|---|---|
| **DTC creative / seeding** | Unique / Curious | mechanism (it's genuinely distinctive) | **GENERATE** | Contrarian, High-level abstraction |
| **SEO / GEO / organic** | Helpful / Curious | **result + specificity** | **OMIT** (the tactic *is* the result) → use Plain-English + "without ads" wrapper | Plain-English (+ wrapper) |
| **PR / authority** | Curious / Helpful | mechanism (the *position*) + authority | **GENERATE (abstract)** | High-level abstraction |
| **Local / trigger** | Timely / Helpful / FOMO | trigger **or** guarantee + result | trigger: GENERATE · guarantee: OMIT | Trigger/Timing, Risk-reversal |
| **Agency / outbound** | FOMO / Curious | **specificity (Clay signal) + case study + authority** | usually **OMIT** (lead on the ICP-signal specificity) | High-level abstraction + Trigger |

> **The omit rule, said once more:** if the only honest mechanism line just restates the result ("we
> ranked them #1"), **omit the mechanism slot** and spend the words on specificity/relevance. SEO offers
> almost always omit. Template = **W9 (Velox/Dr Axe)**.

---

## Step 3 — Apply the two cross-cutting dials

These modify any row above:

**Sophistication** (how many similar pitches they've heard):
- **Low** → a plain strong result lands; casual interrupt ("bit random"); Helpful + guarantee work well.
- **High** → need specificity / a weird mechanism / permission opener ("feel free to ignore if…"); a plain
  result alone won't cut through.

**Case strength** (how impressive the result is on its own):
- **Strong / famous brand** → *fly high*: omit or abstract the mechanism, stack social proof + relevance.
  (W2, W13, W17)
- **Ordinary but solid** → *get specific*: the mechanism (if it carries) or a sharper, more specific
  result has to do the work. (most SEO/local rows)

---

## Worked routes

- **Big Leap (SEO/GEO for SaaS), mid sophistication, ordinary case** → SEO row → **OMIT mechanism**, lead
  Helpful/Curious, carry on **result + the {keyword}/niche specificity**, optional "without paid ads"
  wrapper. Pattern: Plain-English. *(This is the route v1 missed — it forced a unique mechanism.)*
- **Kynship (DTC seeding), high sophistication, strong case** → DTC row → **GENERATE mechanism**, lead
  Unique/Curious, Contrarian or High-level abstraction, fly high on the seeding mechanism + household-name
  proof (Grüns / Create Wellness).
- **Redo (DTC ecom)** → DTC row, but check case strength — if the result is ordinary, get specific and
  consider whether the mechanism actually carries or whether it's really a result/relevance play.

---

## How the wordsmith uses this

1. Classify the offer → get the row.
2. Take `mechanism: GENERATE / OMIT` as a hard instruction. **If OMIT, the wordsmith does not invent a
   mechanism — it returns "lead on result + specificity" and (optionally) wrapper variants.**
3. Apply the sophistication + case-strength dials.
4. Pass the lead lever + live patterns to the generation step.
