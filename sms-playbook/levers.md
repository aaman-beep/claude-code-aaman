# The 5 Psychological Levers

> The **emotional frame** a cold text leans on — *why this person, reading on their phone, would care
> enough to reply.* This is the single source of truth for the levers. Don't redefine them anywhere else.
>
> A strategist picks **2-3 levers** for a given case study and writes ~3 variants each — because it's worth
> testing, not guessing. Each text **leads with one** lever; they often compound (Curious + Helpful), but
> one drives.
>
> Separate axis: the lever is the *feeling*. **What carries the bite** (the case study, the mechanism, the
> relevance) is a different question — a strong FOMO text and a strong Curious text can both be carried by
> the same case study. Don't collapse the two.
>
> **Before picking a lever, go to the winners first** — pull them from **Evergreen** (`POST /api/search
> {"type":"copies","status":"winner"}`, filtered by offer/niche) so you see which lever actually worked
> **with its real results** (positive_rate), and `/variant-performance` for which arm won. The local
> `winners.csv` / `winner-structure.md` are the seed underneath. Familiarity first, invention second.

---

## FOMO — "I'm leaving something on the table"

**The feeling:** everyone but me is getting this; there's money/growth that should be mine and I'm not
capturing it; I'll be left behind. It's loss, not gain.

**What makes it fire (any one of these — it is NOT just "name a competitor"):**
- **Their own uncaptured result** — revenue, deductions, demos, pipeline that's rightfully theirs and
  they're not getting. *(This is the most-missed one.)*
- **Rivals/peers pulling ahead** — a named `{{competitor}}`, or "brands/firms like yours are already…".
- **A market shift they haven't moved on** — "the way [category] is being done now is X, most haven't switched."
- **Scarcity / exclusivity** — "only taking 2 more [niche] brands," "looking for one firm per city to trial this."

**How it shows up:** the text frames a gap between where they are and what's being left on the table, then
the case study proves it's real and capturable.

**Examples across offers:**
- *Tax/accounting:* "most [niche] businesses are overpaying tax by a chunk they never see — we found
  [client] $340k they were leaving on the table."
- *DTC ecom (e.g. returns/retention):* "you're likely leaking revenue on returns you could be recapturing —
  we turned that into $X/mo for [brand]."
- *Marketing agency / SaaS (GEO):* "your competitors are the ones ChatGPT recommends for [keyword] — you're
  not in the conversation yet."
- *DTC paid (market shift):* "brands your size are scaling Meta profitably on creator content right now —
  most still aren't."

**When it doesn't fit:** there's nothing they're credibly missing, and you'd have to manufacture a rival or
a fake scarcity. Don't.

---

## Unique — "wait, that's different"

**The feeling:** I've heard every pitch — but not *that* one. For the jaded, sophisticated buyer who
pattern-matches and dismisses in a second.

**What makes it fire:** a genuinely **unorthodox mechanism** — it passes the "is this actually weird?" test.
If the how is a category default, this lever is off; don't bolt a "weird approach" frame onto a normal tactic.

**The weirdness gate (be honest — this is where it goes wrong).** Ask: *would the buyer's peers raise an
eyebrow at the HOW, or just nod?* If they'd nod, it's not Unique. Things that **feel** novel but are
**category defaults** (the buyer has heard them) — so they do NOT earn Unique or a "weird approach" disarm:
- **DTC/creative:** gifting/seeding free product to creators, UGC, "creator content as ads", running paid social.
- **SEO/organic:** ranking #1 on Google, content, backlinks. **PR:** getting press. **Local:** Google Ads.
What *is* weird: an inversion or a counter-intuitive constraint the category doesn't do — "customers make
their *own* ads", "humor as the growth driver", "PR + AI-search as one play", "we *paused* paid and grew."
If your mechanism isn't in that league, run **Curious** (let the result/number carry) or **Helpful** — and
say the tactic plainly; don't dress a normal tactic as weird (it reads try-hard and the disarm misfires).

**How it shows up:** the mechanism *is* the hook — said as a picture, often with a light "bit of a weird
approach" disarm.

**Examples across offers:**
- *DTC paid:* "by letting their customers make their own ads" (vs polished brand creative).
- *Marketing/creative:* "using humor as the actual growth driver — ads people don't skip."
- *SaaS (GEO+PR):* "by combining PR and AI-search instead of running them as two separate plays."

**When it doesn't fit:** the mechanism is ordinary, or it's already been handed to you as "omit." Lean
Curious or Helpful instead — never invent weirdness.

---

## Curious — "huh, how did that happen?"

**The feeling:** an open loop I want closed. A number too big to ignore, or an angle I can't immediately explain.

**What makes it fire:** a **sharp/outlier result** said plainly, OR a **strange angle** that begs a "how."

**How it shows up:** a striking number or a loop-opener ("I think I cracked the code to…"), with the reveal
held just out of reach so the reply *is* the curiosity.

**Examples across offers:**
- *DTC:* "took [brand] from $8m to $85m in under 4 years."
- *SaaS:* "got [client] ranked #1 in ChatGPT for [keyword] in 3 months."
- *Agency/ecom:* "I think I cracked the code to scaling Meta profitably."

**When it doesn't fit:** an ordinary number with no intriguing angle — then the result has to carry on
sheer specificity (lean Helpful/FOMO), don't fake intrigue.

---

## Timely — "this is relevant *right now*"

**The feeling:** the timing makes this land — there's a moment, a trigger, a thing that just happened.

**What makes it fire:** real **trigger / signal / event data** — recently funded, just hired a CMO with no
agency, a seasonal window, a live problem (water damage, a launch, a price change). Usually Clay-driven.

**How it shows up:** anchor to the moment, not the offer — "we [do X] the exact moment [trigger]," or "saw
you just [signal]."

**Examples across offers:**
- *Local services:* "we run ads the exact moment someone in your area gets [problem]."
- *B2B/agency:* "saw you just brought on a CMO but don't have an agency of record yet."
- *Seasonal/ecom:* "with [season] coming, the brands that prep their [thing] now are the ones that win it."

**When it doesn't fit:** steady-state offer, no discrete trigger. Don't invent urgency — it reads fake.

---

## Helpful — "this person isn't pushing me"

**The feeling:** low guard. They're not selling me; they're offering. Disarming for the overworked,
high-ticket, or guard-up buyer where a hard ask kills it.

**What makes it fire:** always available — it's a **posture**, not ammo. But it's weakest naked: pair it
with a **specific relevance hook** or it reads generic.

**How it shows up:** a permission opener ("feel free to ignore if not a priority"), a capacity question, or
the generous CTA — "not asking for your business, but could I show you how [company] could do this in [their
space]?"

**Examples across offers:**
- *High-ticket agency:* "not asking for your business, but could I show you how [company] could do this in
  the [niche] space?"
- *Any:* "feel free to ignore if this isn't on your radar — but…"
- *Capacity flavor:* "we've got room for one more [niche] brand this quarter."

**When it doesn't fit:** it always fits as a *flavor* (often on the CTA). It just can't be the whole reason
to reply — back it with relevance or a strong case study.

---

## How they compound

Real winners often run two — lead with the primary, let the second flavor the opener or the CTA:
- **Curious + Helpful** — the loop pulls them in, the soft CTA makes replying easy.
- **FOMO + Curious** — "you're missing out on X" + "and here's the how you'll want."
- **Unique + Curious** — the weird mechanism *is* the open loop.

**Sophistication nudge:** low-sophistication buyers respond to Helpful + a plain strong result; high-
sophistication buyers need Unique/Curious + specificity, and a permission opener ("feel free to ignore")
lands better than a casual "bit random."
