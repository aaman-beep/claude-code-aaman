# QA Checklist — the pass/fail gate

> A pre-flight checklist. **Running it on every variant at Step 4 is NON-OPTIONAL** — it's the gate that kills
> shitty copy before it ships. The *standards* (tonality, banlist, anatomy) live in
> `sms-playbook/Cold-SMS-Voice-Profile-Scaletopia.md`; this checks against them, it doesn't restate them.
>
> **Score each item Y / N / Borderline, and SHOW IT** — output the filled grid item-by-item with a one-line
> piece of evidence per item. **A blanket "13/13 ✓ · banlist clean" is not acceptable** — that self-cert is
> exactly how shitty copy shipped before. If a line can't pass, **discard it and say why** ("dropped X —
> couldn't keep it on-script") — never ship a failing line silently.

---

## Logic layer — the argument

1. **Mechanism–result coherence:** does the *how* actually explain the result claimed? **Y / N / N-A**
   *(N/A if no mechanism is claimed — many SEO/commodity winners correctly have none. N/A passes.)* — **auto-fail**
   - **Unique-lever weirdness sub-gate:** if the variant runs the **Unique** lever or a "**weird approach**"
     disarmer (😂), the mechanism must pass the "*is this actually weird?*" test (`levers.md`). Category
     defaults — gifting/seeding product to creators, "we run your ads", ranking #1 on Google — are **not
     weird**; bolting "weird approach" onto them is an **auto-fail** here. Lean Curious/Helpful instead.
2. **No hallucinations / no overclaim stated as fact:** is every claim real and defensible word-for-word? Any
   **inferred or halo claim** ("it lifted their Amazon + DTC just as much") must be **flagged "defend on a call,"
   not stated as fact.** **Y / N** — **auto-fail**
3. **Specific proof:** a real number + unit + timeframe (or a real status fact)? **Y / N**
   - **Timeframe is load-bearing — do NOT drop it to thin out numbers.** "$100k → $1m/mo **in 3 months**"
     beats "$100k → $1m/mo." If `sms_qa.py` flags number-density, cut a `$`/volume figure, never the
     timeframe. (The script now excludes timeframes from the density count for this reason.)
4. **Why them, why now — and at what rung:** a clear, relevant reason we're texting *this* person *now* —
   not just "saw your company"? **Name the enrichment + rung** the relevance uses (`relevance-engine.md`).
   **Rung 0 (generic "could do the same for {{company}}" / bare-`{{niche}}` T2) auto-fails unless the case is
   S-tier.** **Y / N** — **auto-fail at rung 0 (non-S-tier)**
   - **Variety never costs aimedness:** when you vary a T2 across variants, the new line must still
     speak to *their world* (a niche/account/signal hook). **Reacting to the case** ("wild what that
     volume does") instead of speaking to them is rung-0 even though it's "different." A reused strong
     relevance hook ("haven't seen many {{niche}} brands run it this way") beats a fresh generic one.
   - **Case-relevance / bridge sub-gate:** is the **case study itself** in the prospect's world? If the
     case is off-niche (e.g. a CPG/food brand for a Health & Wellness buyer), you must have run the
     **bridge move** (`relevance-engine.md` §2: abstract the mechanic → re-instantiate in their world) or
     swapped to an on-niche case. An off-niche case with **no bridge** is an **auto-fail** (a famous logo
     doesn't make it "for them"). Name the bridge or the on-niche swap.
5. **Sender credibility:** could we (or the client we represent) make this claim with a straight face? **Y / N** — **auto-fail**

## Form layer — the mechanics

6. **Anatomy — mechanism welded to the case study on T1:** is the mechanism in the **same bubble as the result
   (T1)**, never split onto T2? (T2 = relevance bridge + CTA only.) **Y / N** — **auto-fail**
7. **Length (characters):** T1 ≤ ~200 and T2 ≤ ~150? **Y / N**
   *(Target, not a hard cap — winners ran T1 110–292 / T2 46–248. Over the target must read clean; balance the
   pair, long T1 → short T2. Hard stop ~290 on T1. Readability beats the count.)*
8. **Language match (Layer A):** uses the ICP's actual words / tonality from the brief + calls — sounds like *their* world? **Y / N**
9. **Reads naturally out loud:** breathes, human-ish, free-flowing, not congested? **Y / N**
10. **Scam / bot test + speaks-TO-them (two-finger test):** do the first 5–7 words avoid sounding like a
    scam, sales bot, or AI — **and does the text (esp. T2) speak TO the prospect rather than declare a thesis
    about their market?** This is the most-missed T2 crime. The line:
    - ✅ **Aimed (passes)** — a *first-person observation* or a line about *them*: "haven't seen many do this
      yet — could I show u how it'd work for you?" · "you're probably leaving X on the table." The subject is
      *I/you*; it invites a reply.
    - ❌ **Statement (fails)** — a *third-person market thesis* with the category as subject of a state verb:
      "most {{niche}} brands are still all-in on X" · "{{niche}} brands can't scale creative fast enough" ·
      "food brands are quietly pulling ahead." Reads like an email intro / podium voice, not a text.
    Rule of thumb: if you could paste it into a LinkedIn post unchanged, it's a statement — rewrite it as
    something one person would *text* the other. (Borderline cases: `sms_qa.py` STATEMENT-LEAD flag nudges;
    you make the call.) **Y / N** — **auto-fail**
11. **No AI-overused words or cringe constructions:** clean of the banlist (empty verbs, "it's not just X — it's
    Y", triadic lists, %/decimals) **and** the **"no X, no Y" tell** ("no luck, no lottery", "no fluff, no
    filler") **and** the **brag-superlative flourish** ("biggest in their history", "best month ever",
    "record-breaking", "of all time") — a closer states the number; the flourish is the AI tell. Cut it.
    **Y / N**
12. **One question per text:** no two question marks in a single text. **Y / N**

## Negative-priming layer — the opener

13. **No defensive / self-defeating opener:** does it avoid apologising or pre-empting refusal — AND avoid the
    **self-defeating conditional**? *"Feel free to ignore if X"* is fine when **X is a graceful fit/priority out**
    ("if TikTok Shop isn't a priority"). It's **self-defeating** when **X is the prospect's actual pain/problem**
    ("if affiliates haven't worked for you") — that tells the exact person you want to talk to that they should
    dismiss you. **Y / N**

---

## Scoring

- **Pass:** Y on at least **11 / 13**.
- **Automatic fail** — any **N** on **mechanism-coherence (Q1), no-hallucination/overclaim (Q2),
  sender-credibility (Q5), anatomy (Q6), or the scam/bot + speaks-TO-them test (Q10)** — or **rung-0 relevance
  on a non-S-tier case (Q4)** — fails the variant regardless of total. The sub-gates inherit the auto-fail:
  **Unique lever on a non-weird mechanism (Q1)**, **off-niche case with no bridge (Q4)**, and a **statement-T2
  market thesis (Q10)** are all dead on arrival. These are the exact misses from the Kynship run.
- A failed variant goes back to **rewrite, or gets discarded with a one-line reason** — never shipped or
  silently changed off your direction.

## Winner benchmark (the last gate before ranking)

Passing 11/13 isn't enough — the bar is **winner-grade**. For each variant that clears the grid, **name the
closest logged winner** (`winners.csv` / `winner-structure.md`, matched by offer/niche) and state plainly
whether it clears that winner's bar on the three that decide replies: **relevance · sounds-human ·
proof-fit**. If it doesn't clear the winner it's modelled on, it isn't winner-grade yet — **rewrite or drop**,
don't pass it through to ranking.

> Cross-checked against the 17 winners: every logged winner clears the bar with no auto-fails. If a new draft
> can't clear it, it isn't winner-grade yet.

## Loser gate (evergreen) — judged by the REASON, never by resemblance

Winners set the bar; losers set the tripwires. Two non-negotiables about how this gate works:

1. **The loser pool is LIVE, never a local list.** Pull it fresh every run via the `evergreen-research` skill:
   `POST /api/search {type:"copies", status:"loser", query:"<this angle/offer/lever>", route:true, limit:5}`
   (a second pull pinned to the client's `niche` if routing looks off). The pool grows with every campaign
   that reports back — which is the point: **this gate gets stricter as the system learns.** A static list
   would freeze the QA at today's mistakes.
2. **The check is against `why_it_failed`, NOT the loser's surface text.** A loser is a whole text that
   usually died for ONE reason. Reduce each loser's `why_it_failed` to its **failing component** (relevance
   rung · opener · proof framing · CTA · mechanism clarity · tone/phrasing) and check the draft against
   *that*. A variant fails this gate only when it **repeats a logged failure reason** — same component, same
   failure mode, comparable persona/offer.

**Corollary — never bin a loser's good parts.** The loser's *other* components are still live ammo. Canonical
case (go_fish, logged): a differentiated mechanism + sexy case study that died because "the whole text is
about US, with zero relevance hook tying it to THIS recipient." The mechanism is reusable; the rung-0
relevance is the tripwire. Blanket-avoiding everything that resembles a loser would throw away its best
material *and* miss the actual lesson.

**Run it per surviving variant, and show the work:**
- Name each relevant loser (client + id), quote its `why_it_failed` in one line, and state which component
  of the draft does / doesn't repeat it.
- "No losers returned for this angle" is a valid outcome — **say it**; never skip the pull silently.
- `aged: true` losers: the lesson usually holds, the phrasing/offer context may not — weigh accordingly.
- A hit = **rewrite the failing component** (the rest of the variant stands), or discard with the one-line
  reason. A near-miss ("adjacent failure mode, different rung") is a Borderline — flag it to the strategist,
  don't silently pass or kill.
