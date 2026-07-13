# Quality Filters

Every variant produced by the skill must run through four filters before it enters the menu. The first two are disqualifying (a variant that fails either is dropped, not scored). The second two are scoring (a variant that fails still appears but with a lower score).

---

## Filter 1: Jargon Test (DISQUALIFYING)

**Question:** Would a smart person outside the industry (e.g., a CFO, a generalist VC, the strategist's mom) understand this sentence without Googling any term?

**How to run it:**

Read the variant out loud. Flag every term that requires industry knowledge to parse. If even one flagged term cannot be replaced with plain English without losing the variant's meaning, the variant fails the jargon test and is dropped from the menu.

**Common jargon to flag (DTC/ecom):**

| Jargon term | Plain English replacement |
|---|---|
| Cost Cap / Cost Cap per SKU | "a hard ceiling on what we'd pay per sale" |
| Cactuar / cost-controlled campaigns | "campaigns that won't overspend per result" |
| CAC / blended CAC | "cost to acquire a customer" |
| ROAS / blended ROAS | "ad spend efficiency" |
| Contribution margin | "profit per sale after variable costs" |
| NCR / new customer revenue | "revenue from first-time buyers" |
| AOV | "average order size" |
| MER / marketing efficiency ratio | "every $1 of ad spend earning $X back" |
| LTV | "what a customer is worth over time" |
| iOS 14 / SKAdNetwork | "attribution since the privacy changes" |
| Lookalikes | "audiences that match your best customers" |
| UGC | "real-customer content" |
| Influencer seeding | "sending product to creators in bulk and using their content" |
| Pixel data / first-party data | "your own customer data" |
| Conversion API / CAPI | "server-side tracking" |
| Whitelisting / spark ads | "running ads through a creator's account" |

**Common jargon to flag (B2B/SaaS):**

| Jargon term | Plain English replacement |
|---|---|
| Signal-based | "triggered by specific events" |
| Intent data | "buying signals" |
| ICP | "ideal customer" |
| PQS / product-qualified signals | "behavior that says they're ready to buy" |
| MQL / SQL | "qualified leads" |
| TAM / SAM / SOM | "market size" |
| Outbound motion | "outbound process" |

**Exception:** Industry-native terms that the target buyer uses casually in their own speech (verified from transcripts in the brief) are OK. If Founders in the brief are saying "CAC" and "NCR" in transcripts without explaining, those terms are NOT jargon for that audience and can stay. Verify against the brief's "Words they use casually" section before approving any borderline term.

**Pass criteria:** Zero unflagged jargon terms after running through this list AND the brief's language section.

---

## Filter 2: Length Test (DISQUALIFYING)

**Question:** Is the variant ≤ 25 words?

**Target range:** 8–18 words.

**How to count:** Count words in the variant text only — not the case study client name, not the outcome, not the surrounding template scaffolding. Count only what would slot into `{{unique_mechanism}}`.

**Why:** Cold SMS is constrained. The full Text 1 is typically 25–45 words. The mechanism portion gets ~10–15 of those. A 30-word mechanism crowds out the case study, the human bridge, the CTA.

**Tight examples (good):**
- "humor to make their ads actually entertaining" — 7 words
- "making their CEO the go-to voice for AI defense" — 9 words
- "ranking them first on Google for terms like {keyword} — without spending on ads" — 13 words

**Bloated examples (bad):**
- "by combining unpaid micro-influencer content with branded creative production in a flywheel system that ran 150 ads per month" — 19 words but reads as 30 because of clause-stacking

**Pass criteria:** ≤ 25 words. Bonus points internally for 8–15 words but no scoring delta.

---

## Filter 3: Sticky Anchor Test (SCORING)

**Question:** Does the variant have at least ONE of the following anchors?

- **Specific number** — "1,000 micros", "150 creatives", "$234K in 53 days"
- **Named tactic** — "viral seeding", "signal-based outbound", "humor in ads"
- **Contrarian word** — "actually entertaining", "without paying", "instead of polishing"
- **"Without X" clause** — "without burning ad spend", "without referrals"
- **Named position** — "the go-to voice", "the only [thing]", "the default for [category]"
- **Sketchable image** — "redirect competitors' traffic", "intercept water-damage signals"

**Why:** Without an anchor, the variant fades from memory three seconds after the buyer reads it. Anchors are what the buyer remembers when they decide whether to reply.

**Pass criteria:** At least 1 anchor present.

**Score impact:**
- Pass: +1 point
- Fail: 0 points (variant still ships if it passes Filters 1 and 2)

---

## Filter 4: Pain-Dissolution Test (SCORING)

**Question:** If pain hierarchy from the brief is provided, does this variant answer at least ONE named pain?

**How to run it:**

For each of the brief's top 3–5 pains, ask: would a reader experiencing this pain see this variant and think "they GET it" or "they're talking about my problem"?

**Worked example — Kynship Founder/CEO brief:**

Top pains (illustrative):
1. Creative engine is the bottleneck — can't produce enough variants
2. CAC keeps creeping up at scale
3. Burned by previous agencies who couldn't sustain results
4. Don't know what's actually scalable vs. one-hit-wonder

A Supergut variant: "by using 1,000 unpaid micro-influencer videos as paid creative on meta"
- Dissolves Pain #1 (creative engine bottleneck — solved by mass customer-sourced creative) ✓
- Does NOT dissolve Pain #2 directly (CAC isn't mentioned)
- Does NOT dissolve Pain #3 (agency-burn isn't addressed)

Score: +1 (dissolves at least one pain).

A different Supergut variant: "by training meta CPA models on first-time buyers, not site visitors"
- Does NOT dissolve Pain #1 (creative engine — irrelevant)
- Dissolves Pain #2 partially (improves CAC efficiency via better targeting) ✓
- Does NOT dissolve Pain #3
- Indirectly addresses Pain #4 (shows what's actually scalable) ✓

Score: +1 (dissolves Pain #2 at minimum).

**Pass criteria:** Dissolves ≥ 1 brief pain.

**Score impact:**
- Pass: +1 point
- Fail: 0 points (variant still ships)

**If no pain hierarchy is provided:** This filter is skipped and every variant gets +1 default. Flag in the output that pain-dissolution wasn't checked.

---

## Filter ordering (canonical)

When scoring, always apply in this order:

1. Jargon Test — drop if fail
2. Length Test — drop if fail
3. Sticky Anchor Test — score +1 if pass
4. Pain-Dissolution Test — score +1 if pass

This means surviving variants start at +2 (passing 1 and 2) and can earn up to +2 more, for a maximum score of 4.

---

## Anti-patterns to never produce

The skill must NEVER produce a variant that contains any of the following — these have been observed in losing drafts and are filtered at generation time, not just at scoring:

- **"Unique mechanism"** as literal text — meta-language about having a mechanism is not a mechanism
- **"Proprietary"** — empty word, signals defensiveness not novelty
- **"AI-powered"** unless the literal mechanism IS AI-powered AND the brief verifies the buyer cares
- **"World-class" / "best-in-class"** — empty
- **"Solution"** as a noun — "our solution does X" reads as agency speak
- **Multiple "ands"** — "X and Y and Z" reads as a list, not a mechanism
- **Parentheticals over 8 words** — they break SMS rhythm
- **Anything Bryan Phelps's actual on-call language wouldn't survive** — read it back as if Bryan said it on a sales call. If it would sound rehearsed, rewrite.

---

## Quick reference card (for in-flow use)

```
DROP IF: jargon survives OR > 25 words
SCORE: +1 anchor present, +1 dissolves brief pain
MAX SCORE: 4
TARGET: 3+ variants at score 4
```
