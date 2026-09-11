---
name: sms-draft
description: Assembles a developed case study (the proof + mechanism handed over by case-study-developer) plus the Layer A brief into tight, ship-ready cold-SMS T1/T2 variants — the strategist picks 2-3 psychological levers and gets ~3 variants each — then cuts and QA's them to the Voice Profile. Use whenever a strategist is ready to write cold SMS copy and says "draft the SMS", "write SMS copy for [client/case study]", "turn this case study into texts", "make SMS variants", or "give me cold SMS drafts". Recommends the lever via an ammo-check; the strategist confirms direction and picks the winner. Does NOT invent a mechanism, does NOT fabricate a competitor name, does NOT pick a winner, does NOT send. Runs the same on any offer in any industry — all client-specific knowledge arrives as input.
---

# sms-draft — the cold-SMS copy engine

You've done the brief (Layer A) and the case study + mechanism are developed (case-study-developer / Layer
B). This skill turns that into **tight, on-voice T1/T2 variants** for the 2-3 levers you choose (~3 each) — cut
down, QA'd, and handed back with a remix bank so you ship in minutes.

**The one job of every text:** make the right person think *"tell me more."* Not explain. Not close. Worth
their attention, worth learning more. It's worth **testing, not guessing** — so you get a few variants, and
you + the market pick the winner.

## Who does what (read this first)

The skill is **strategist-led, skill-assisted.** Keeping this line clean is what stops it being a template-
filler.

| The strategist / upstream brings | The skill does | The strategist decides |
|---|---|---|
| Case study + the **proof menu & mechanism menu** (from case-study-developer) | Checks the winners, recommends the **2-3 levers** that fire | The **2-3 levers / direction** (confirm or override) |
| The **Layer A brief** (persona, pains, their words, niche) | **Borrows/mixes** the template that fits; assembles T1/T2 | How aggressive to chunk the proof |
| Optional: a lever steer, a `{{competitor}}`, a Clay/relevance signal | **Cuts + QA's**; outputs ~3 variants per lever + remix bank | The **final pick of which variant to ride** |

If you already know the lever, say it and the skill skips Step 1.

## Principles first — templates are scaffolds, never copy-paste

This skill encodes the **engine**, not any client. Never hardcode an industry, jargon, or example into it —
all of that arrives as input. When an offer has no comparable winner (a SaaS GEO+PR play; seeding before
we'd done seeding), **do not force a template onto it.** Find the closest analog even across industries,
**mix-and-match the pieces** that fit (the #1-ranking piece + the PR-valuation piece), and build the rest
from the anatomy + `FUNDAMENTALS`. **Lean to what's worked first → ship that as V1 → deviate after.** A
genuinely unique combo *becomes* the angle.

## What it reads (the reading contract)

On every run — **reference these, never restate them:**
- **`sms-playbook/winner-structure.md` + `sms-playbook/winners.csv` FIRST.** Find the closest offer/niche
  and see what actually worked — which lever, which structure. Familiarity before invention; the winners are
  your anchor, not an afterthought.
- `sms-playbook/levers.md` — the 5 psychological levers. **The single source for the lever logic — it lives
  there, not here.**
- `sms-playbook/FUNDAMENTALS.md` — the two bars ("this is real" + "this is for me"; build the short bar,
  never prop the standing one) + the one job.
- `sms-playbook/Cold-SMS-Voice-Profile-Scaletopia.md` — voice, the T1/T2 anatomy + never-cut spine, the
  banlist. **The tone source of truth.**
- `sms-playbook/relevance-engine.md` — **how to GENERATE relevance** (the ladder + the bridge move). The
  source for the relevance logic — it lives there, not here. Relevance is the weak spot; this is the fix.
- `sms-playbook/enrichment-menu.md` — which Clay enrichment buys which relevance rung / lever, how to weave
  it, when not to. The supply chain `relevance-engine.md` draws on.
- **Live losers from Evergreen** — pulled fresh EVERY run via the `evergreen-research` skill
  (`POST /api/search {type:"copies", status:"loser", ...}`), never from a static local list. Feeds the
  **loser gate** in `references/qa-checklist.md`: drafts are checked against each loser's `why_it_failed`
  *reason*, not its surface text. The pool grows with every campaign, so this QA tightens over time.

(Not `pattern-library.md` — that's mechanism patterns, and the mechanism is already developed upstream by
case-study-developer.)

## Inputs

**REQUIRED:** the developed case study (proof menu + mechanism decision from case-study-developer) · the
Layer A brief (persona, pains, their language, niche). If the brief is missing, run `sms-brief` first.
**OPTIONAL:** a lever steer · a `{{competitor}}` · ticket size + sales motion (sets CTA softness) · a
Clay/relevance signal for the specific prospect · already-tried drafts to avoid repeating.

---

## Workflow — 4 steps, confirm before moving on

### Step 1 — Direction: pick the levers
Go to the winners first (closest offer/niche) to see what's worked there. Then read `sms-playbook/levers.md`
and run the 5 levers against what's actually available — the case study, the mechanism, the brief, any
competitor/signal data. Report **which levers fire and why** (the firing logic lives in `levers.md` — don't
restate it here), and recommend the **2-3 worth writing**. **The strategist picks the 2-3** (or overrides);
each gets ~3 variants in Step 4.

**Before you recommend Unique, run the weirdness gate** (`levers.md` → Unique): is the mechanism *actually*
unorthodox, or a category default the buyer has already heard (gifting/seeding product, UGC, ranking on
Google, running paid social)? Category defaults do **not** earn Unique or a "weird approach" disarm — it
misfires as try-hard. If the how is ordinary, say it plainly and run **Curious** (let the number carry) or
**Helpful** instead. (QA Q1 auto-fails a Unique/"weird approach" variant built on a non-weird mechanism.)

Reminder on FOMO so it's never narrowed again: it is **not** just "name a competitor" — it's *anything
they're missing out on* (uncaptured revenue/deductions/demos, rivals ahead, a market shift, scarcity), per
`levers.md`. For a named rival use a `{{competitor}}` placeholder — never fabricate a name; suggest
candidates flagged "verify before sending," or use the no-name FOMO frames.

### Step 2 — Lock the core case-study line (T1's spine)
The proof + mechanism arrive developed. Confirm the exact T1 spine: the **proof in the persona's native
unit** (pick from the proof menu — "$8m → $85m/yr", not "+962%"), and **mechanism in or out** as decided
upstream. **Never re-introduce or invent a mechanism here.** If the case study is S-tier, you can keep the
mechanism vague and lean on a social-proof stack instead (fly high); ordinary case → get specific.

**Pick the RIGHT case, not just the strongest** (the Momofuku rule, `relevance-engine.md` §2b): lead with an
**on-niche** case. If the strongest proof is off-niche (e.g. a CPG/food brand for a Health & Wellness buyer),
either **bridge it** (§2) or demote it to a short authority-stack tail behind an on-niche lead — a famous
logo proves "this is real," never "this is for me." An off-niche case as the main proof with no bridge fails
QA Q4 even when it's S-tier. Keep the **timeframe** in the proof line — it's load-bearing; never cut it to
satisfy number-density (cut a `$`/volume figure instead).

### Step 3 — Build the T1/T2
Assemble to the **Voice Profile** anatomy (`sms-playbook/Cold-SMS-Voice-Profile-Scaletopia.md` — the T1/T2
anatomy + never-cut spine: disarmer → identity → case study; relevance bridge → soft CTA) and pull
**disarmers** from it. Borrow the structure from `sms-playbook/winner-structure.md` — pick the closest
offer/lever, note *why that winner worked*, and map that reason onto **this** client's ICP. Pull **soft-CTAs
+ slots** from `references/variable-schema.md`.

**Anatomy is non-negotiable: the mechanism is welded to the case study in T1** — never split onto T2 (that's
an auto-fail). T2 = the relevance bridge + soft CTA only.

**Propose the strongest opener — don't default to "bit random."** Pull the proven hooks from
`references/variable-schema.md` (cracked-the-code, permission, capacity, credibility) and pick the best fit
for the lever + persona; reach higher than the floor when the case allows.

**The language comes from Layer A, not a generic persona file.** Shape vocabulary, tonality, and which proof
you lead on from the **brief's ICP** — their actual words, their pains, the sales-call language. Then check
back: *does this read like Layer A — the ICP's own world — or like us?* If it sounds like us, it's not done.

**Build the relevance — don't leave it to chance** (it's the weak spot, the tie-breaker, and the heaviest
scored dimension). Run the relevance engine (`sms-playbook/relevance-engine.md` + `sms-playbook/enrichment-menu.md`):

1. **Inventory the enrichments** actually available for this segment — from the Layer A brief and the Clay
   vars in play. Don't assume a signal you don't have.
2. **Climb the ladder to the highest rung those enrichments honestly support** (rung 1 niche → rung 2
   account → rung 3 individualised). Say it at **human altitude** — the level a real person would notice
   ("just hired Jack"), not scraped/nerdy ("traffic was 87.2k").
3. **If the case study's world ≠ the prospect's world** (a soup brand's case for a baby buyer), run the
   **bridge move**: abstract the case to the *mechanic* that drove it → re-instantiate it in the prospect's
   world via *their* enrichment (`{{relevant_search_term}}`, `{{product_category}}`…) → lead T2 with the
   prospect's own uncaptured opportunity. **Never fake a category match** ("same baby space as {{company}}").
4. **Per-prospect relevance is a Clay slot** — leave `{{relevant_search_term}}` / `{{ICP_signal}}` /
   `{{competitor}}` as merge vars and write the sentence around them (the W13 pattern). Build the line, don't
   invent the value.
5. Produce **2-3 relevance bridges as candidate T2 openers, each tagged with the enrichment + rung used** —
   so the variants differ on relevance, not just proof.

**The floor (enforced at Step 4): no variant ships at rung 0** — generic "could do the same for {{company}}"
/ "had a few ideas for you" / a bare-`{{niche}}` T2 — **unless the case study is S-tier.** Below the floor:
climb a rung, or discard with a one-line reason. **Never climb a rung you can't pay for** — an honest rung 1
beats a fabricated rung 3.

Identity can sit at the top of T1 or as a "– Name, Co" signature at the bottom — move it to a signature when
the top is bulky. Keep one main number. **Wordsmith fresh — don't slot.** Vary the relevance bridge and CTA
per variant (not the same "could do the same for {{company}}" every time). Never repeat the CTA across
T1/T2, and **never two question marks in one text.**

### Step 4 — Output: ~3 variants per chosen lever, cut + QA'd
For each of the strategist's 2-3 chosen levers, spin **~3 tight variants**, differing by which detail T2
features (mechanism / the number / relevance / a social-proof stack). For each:
- Run `python3 scripts/sms_qa.py "T1" "T2"` for the mechanical read (chars, segments, number-density,
  absolute-claim, **generic-relevance, and banlist flags**). Then run it once more with **all the variants'
  T2s together** (`sms_qa.py "<v1 T2>" "<v2 T2>" …`) to catch **repeated-CTA sameness** across the set.
- **Mandatory — run the QA checklist gate** (`references/qa-checklist.md`) on every variant; it is **not
  optional**, and neither is reading the Voice Profile. **Show the work: output the filled grid item-by-item
  with one-line evidence — a blanket "13/13 ✓" is not acceptable.** A variant that doesn't clear **11/13**
  (or hits any auto-fail: coherence · no-hallucination/overclaim · sender-credibility · anatomy · scam-test)
  is **discarded with a one-line reason** ("dropped X — couldn't keep it on-script") — never shipped, and
  never silently changed off the strategist's direction.
- **Relevance floor (enforced):** every surviving variant must **name the enrichment + rung its relevance
  uses** (`relevance-engine.md`). No variant ships at **rung 0** unless the case study is S-tier — below the
  floor it's rewritten or discarded.
- **Winner benchmark:** for each surviving variant, name the **closest logged winner** (`winners.csv` /
  `winner-structure.md`) and state whether it clears that winner's bar on **relevance · sounds-human ·
  proof-fit**. If it doesn't clear the winner it's modelled on, it isn't winner-grade yet — rewrite or drop.
- **Loser gate (evergreen):** pull the losers for this angle/lever **live** from the Evergreen API
  (`evergreen-research` skill — never a cached list) and run every surviving variant through the loser gate in
  `references/qa-checklist.md`. A variant fails **only if it repeats a logged `why_it_failed` reason** (same
  failing component, same mode) — resemblance to a loser's *good* parts is not a fail; a loser's strong
  mechanism killed by rung-0 relevance leaves the mechanism live and the relevance as the tripwire. Show the
  work: loser (client + id) → its `why_it_failed` in one line → which draft component does/doesn't repeat it.
- Among the variants that pass, rank by **perceived likelihood the ICP responds** (`references/scoring-rubric.md`).
- Add a light tag (*leans on mechanism / number / relevance*) — nothing more; no hypothesis narration.

Then a **remix / ingredient bank**: the disarmers, proof phrasings, CTAs, and the relevance variable used,
so the strategist remixes. The skill never marks a winner and never sends.

---

## Hard rules
- **Never invent a mechanism** the case study doesn't have. If it's not there, lead on proof/relevance.
- **Never fabricate a competitor** — use a `{{competitor}}` placeholder or verified/suggested-for-review name.
- **Never invent a number.** Use the case study's real figures (reframing is fine — that's the proof menu).
- **Never pick a winner or send.** Output 2-3 variants + remix bank; the strategist + market decide.
- **Templates are optional scaffolds.** Principles first; never copy-paste a template onto an offer it
  doesn't fit.
- **Jargon is judged against the brief**, not a fixed banlist — but the Voice Profile banlist (percentages/
  decimals, "it's not just X — it's Y", triadic lists, empty verbs, hard CTAs) always applies.
- **The two-finger test is the master gate:** does it read like a person thumbing it out, not a marketing
  line blasted on a keyboard? If not, cut or bin.
- **Mechanism stays welded to the case study in T1** — never split it onto T2.
- **Relevance has a floor.** No variant ships at rung 0 (generic "could do the same for {{company}}") unless
  the case is S-tier; climb the ladder with a real enrichment (`relevance-engine.md`) or discard. Never climb
  a rung you can't pay for — an honest rung 1 beats a fabricated rung 3.
- **Run the QA gate + Voice Profile on every variant — non-negotiable.** Show the filled grid (no blanket
  "13/13 ✓"), discard fails with a one-line reason; never ship a broken line or silently deviate from the
  strategist's direction.
- **Losers are checked by REASON, from the live API.** The loser gate pulls `status:"loser"` copies fresh
  from Evergreen every run and judges drafts against each loser's `why_it_failed` — never against its surface
  text, and never from a stale local list. A hit means rewrite *that component*; the loser's good parts stay
  usable.

## When NOT to use
- No case study developed yet → run case-study-developer first. No brief → run `sms-brief` first.

## What to do next (the review loop)
Don't end on a wall of variants — **open a feedback loop with the GTM strategist.** After handing over the
ranked variants:
- Ask a **specific** question: *"which of these resonates / which do you want to go with?"* — and *why*.
- Offer to **dive deeper** on the one they pick — more variants on that line, a sharper relevance hook, a
  different disarmer or CTA.
- Brainstorm **back and forth**: take their reaction ("the mechanism one's too clever", "this relevance
  isn't quite right") and regenerate. Each round should make the copy *and* the next ideation stronger.

The strategist picks the winner to test; the loop is how the copy gets to 9/10. Then: paste the chosen
variant into the SMS preview / Messages for the final phone-thumb test, and ship to test — the market picks
the real winner.

## Quality bar
A run wins when it hands the strategist **~3 tight, on-voice variants they'd actually text** (+ a remix
bank) for each of their chosen 2-3 levers — each passing the two-finger test and the banlist — not when any
single line ships verbatim. Better copy than a human GTM strategist, in a tenth of the time.
