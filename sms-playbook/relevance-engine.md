# The Relevance Engine — how to GENERATE "why them, why now"

> Relevance is the heaviest scored dimension (`scoring-rubric.md` = 30/100), a QA gate
> (`qa-checklist.md` Q4), one of the two bars in `FUNDAMENTALS.md` ("this is for me"), and the
> Voice Profile's "aimed, not blasted." Every other doc *assesses* relevance — tells you when it's
> good and penalises generic. **None of them tell you how to build it.** This one does.
>
> The default failure without this page: the model falls back to the only relevance it can produce
> unaided — "could do the same for {{company}} in {{niche}}." That's rung 0. It's the generic V1,
> and it's the ceiling we're breaking. Built on the 17 winners; plain language, no buzzwords.
> Pair it with `enrichment-menu.md` (which enrichment feeds which move).
>
> **Feed the ladder from Evergreen:** rung-1/2 relevance comes from mined `pains`/`lingo`/`objections`
> and the niche brain (`GET /api/clients/{slug}`, `POST /api/search`, `POST /api/clusters`), and the
> on-niche case pick from tiered `case_studies` — not from guessing. See FUNDAMENTALS → "Reaching Evergreen".

---

## 1. The relevance ladder — climb as high as the data honestly allows

The same case study can be made relevant at four altitudes. **Push to the highest rung the
available enrichments support, then say it at human altitude** — the level a real person would
notice and text. ("saw you just hired Jack" = human; "saw your traffic was 87.2k" = scraped and
nerdy, reads automated even though it's *more* specific.)

| Rung | What it sounds like | Logged in | Enrichments that get you there |
|---|---|---|---|
| **0 · Generic** *(banned, see §4)* | "could do the same for {{company}}" · "had a few ideas for you" | W11, W15 — survive **only** on an S-tier case | none |
| **1 · Niche-level** | speaks their world / their native unit / their vocabulary | W9 (`{keyword}`), W14 ("contested probate billables") | `product_category`, `subniche`, `niche`, `top_service`, `main_expertise`, `speciality`, `saas_type`, `main_product` |
| **2 · Account-level** | true about *their* account: city/service, a directory they're on, a named rival, a niche authority stack | W6 ("found you on AgencyVista"), W8 ("Daniel Defense & 4 Patriots"), W10 (`{{city}}`) | `city`, `directory`, `competitor_1/2/3`, `dream_client`, `ideal_segment`, `what_they_build` |
| **3 · Individualised** *(the 26–30 band)* | a real per-prospect signal or moment — a recent hire, their own work, a search they'd actually chase | W13 ("recently hired a CMO with no agency of record"), W6 ("saw your work with {case}"), W3 ("the exact moment commercial properties have water damage") | `ICP_signal`/`dream_icp`, `relevant_search_term`, `relevance`, `reason_1/2`, role/trigger signals |

**The move at draft time:**
1. **Inventory** which enrichments are actually available for this segment — from the Layer A
   brief and the Clay vars in play. (Don't assume a signal you don't have.)
2. **Write the relevance bridge at the highest rung those enrichments honestly support.** If the
   only thing you have is the niche, you're at rung 1 — that's fine, but reach for 2–3 whenever the
   data is there.
3. **Where the rung-2/3 piece is a per-prospect merge var** (`{{relevant_search_term}}`,
   `{{ICP_signal}}`, `{{competitor}}`…), **leave it as a slot for Clay to fill at list scale** and
   write the line around it. Per-prospect relevance as a Clay variable is the top performer
   (the W13 pattern) — you're not inventing the value, you're building the sentence that uses it.
4. **Never climb a rung you can't pay for.** A rung-3 line on invented data is worse than an honest
   rung-1 line — it reads fake and it's a hallucination. Honesty over altitude.

---

## 2. The bridge move — when the case study's world ≠ the prospect's world

This is the hard case the system had no answer for. The case study is in one world (Spoonful of
Comfort = soup / get-well gift baskets); the prospect is in another (a baby/family CPG brand).
**Do not assert a fake category match** ("same baby space as {{company}}") — it's untrue and it
reads like a blast. Bridge instead, in three steps:

1. **Abstract the win.** Strip the case down to the *mechanic* that actually drove the result —
   not the surface category. *Spoonful: high-intent **gift/occasion searches**, captured via
   **bottom-funnel organic content**, converting buyers at purchase intent with no paid.*
2. **Re-instantiate it in the prospect's world** using *their* enrichment — their own equivalent
   of that mechanic. *A baby brand has the same thing: high-intent gift/registry searches it cedes
   to the big retailers — "baby shower gift", "newborn gift set", "new-mom care package" — i.e.
   their `{{relevant_search_term}}` in their `{{product_category}}`.*
3. **Lead T2 with the prospect's uncaptured opportunity, proven by the case mechanic** — never
   with the surface category.

**Worked example — Spoonful → baby buyer (the proof of the method):**

> **T1:** hey {{first_name}}, it's Mia at Big Leap - bit random, but we got Spoonful of Comfort to
> $462k in organic revenue by ranking their blog for the gift searches people actually buy from,
> like "get well care package"
> **T2:** {{company}} has the baby version of that - "{{relevant_search_term}}" searches going
> straight to the big retailers. want me to show you the ones you could own?

Why it's strong: it never pretends Spoonful is a baby brand — it **transfers the mechanic** and
lands on the prospect's *own* uncaptured searches, climbing to rung 2–3 via
`{{relevant_search_term}}` instead of the rung-0 "same baby space."

**The bridge formula, said once:** *Case mechanic → abstract to the underlying principle →
re-instantiate in the prospect's world via their enrichment.* It generalises to any
case-doesn't-match-prospect situation, not just Spoonful.

### 2b · The case-niche rule (the "Momofuku rule")
Picking the *strongest* case is not the same as picking the *right* case. A case in a **different niche**
(a CPG/food brand for a Health & Wellness buyer) doesn't read "for me" no matter how big the number —
**a famous logo proves "this is real," never "this is for me."** So, in order of preference:
1. **Lead with an on-niche case** when you have one (the data usually offers several — use them).
2. If the strongest case is off-niche, **bridge it** (§2: abstract the mechanic → re-instantiate in their
   world) and lead T2 with *their* version of the win — never assert a fake category match.
3. Only drop in an off-niche famous logo **raw** (no bridge) as a short **authority-stack tail** behind an
   on-niche lead — not as the main proof.
An off-niche case used as the main proof with **no bridge** is a relevance fail at the QA gate
(`qa-checklist.md` Q4), even if it's S-tier.

---

## 3. Why-now (the timing half of relevance)

"Why them" is who they are; "why now" is what makes this land *today*. It only fires on a real
trigger — don't manufacture urgency (it reads fake; see `levers.md` → Timely). Sources of a true
why-now: a `reason_1/2` or `ICP_signal` (recently funded, just hired, no agency of record), a
seasonal/occasion window the `relevant_search_term` implies ("baby-shower season"), or a live
market shift in their `subniche`. If there's no real trigger, drop why-now and carry on why-them —
a forced "right now" is a tell.

---

## 4. The rung-0 floor (the enforced rule)

A variant **may not ship at rung 0** ("could do the same for {{company}}", "had a few ideas for
{{company}}", a bare-`{{niche}}` T2 with nothing else) **unless the case study is S-tier** (a
famous brand or an outlier number that carries the text on proof alone — W11/W15). Below the floor:
climb a rung using an available enrichment, or discard the variant with a one-line reason. Every
shipped variant must be able to **name the enrichment + rung its relevance uses.** This is checked
at the Step 4 gate (`qa-checklist.md`) — it is not optional.

**The S-tier exception is narrow:** it relaxes the *relevance-phrasing* floor (an outlier number can carry
"this is real" without a rung-2/3 hook). It does **not** license an **off-niche case** — a famous brand in
the wrong niche still fails the case-niche rule (§2b). S-tier buys slack on phrasing, not on whether the
proof is in their world.

---

## The non-negotiables

- Climb to the highest rung the data honestly supports; say it at **human altitude**, not scraped.
- When the case ≠ the prospect's world, **bridge the mechanic** — never fake a category match.
- **Lead with an on-niche case**; if the strongest is off-niche, bridge it or demote it to an authority
  tail — a famous logo proves "this is real," never "this is for me" (§2b, the Momofuku rule).
- Per-prospect relevance lives in a **Clay slot** (`{{relevant_search_term}}`, `{{ICP_signal}}`…);
  build the sentence, don't invent the value.
- **Never climb a rung you can't pay for** — an honest rung 1 beats a fabricated rung 3.
- No variant ships at rung 0 unless the case is S-tier; every variant names its rung + enrichment.
