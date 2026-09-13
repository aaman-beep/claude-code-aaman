# SMS Fundamentals — the spine

> The shared mental model behind every cold SMS we write. Plain language, no buzzwords.
> Both skills (mechanism-wordsmith, sms-draft) are built on this. If a rule here is wrong,
> fix it here first — everything downstream inherits from this page.

---

## Reaching Evergreen (the shared knowledge — pull from it first)

Before you write, most of the evidence you need already exists in **Evergreen**, Scaletopia's
shared research/data provider. It is not the writer — it serves the facts you write FROM: mined
**pains / lingo / objections** per client, tiered **case studies (S–D)**, **winner & loser copies
with why-it-worked/failed AND real results** (sent, positives, booked, positive_rate), swipeable
**components** with verdicts, **offers** (mechanism + proof_hint), real **reply threads**, client
**materials** (voice/positioning), and saved **guidelines**.

- **Reach it:** base URL `https://knowledgebase-production-f52e.up.railway.app`, header
  `Authorization: Bearer $EVERGREEN_API_KEY` (the key is in this playbook's `.env`; no header → 401).
- **Discover every endpoint yourself:** `GET /api/docs` (index + descriptions), `GET /api/openapi`
  (schema). Don't guess a path or bulk-pull GHL/Airtable for what Evergreen already has.
- **Skills that drive it:** `evergreen-research` (pull/save findings), `evergreen-stats` (numbers).
- **Rule of thumb:** Evergreen is the live source of truth. The local `winners.csv` / `losers.csv` /
  Master Sheet are the *seed* it was built from — read Evergreen first; treat local files as fallback.

Everywhere below that says "winners", "case study", "pains", or "master sheet", that evidence
should come from Evergreen when it has it. Your craft — voice, levers, structure — stays yours.

---

## 1. The job of a first text

Make the right person think **"tell me more."** That's it.

Not explain everything. Not close the deal. Not prove you're smart. One job: earn the reply.
Every word either helps earn the bite or gets cut.

---

## 2. The two bars every text has to clear

A cold text only works if the reader believes **both** of these in the first read:

1. **"This is real."** — the result is believable. (A named brand + a specific number + a
   timeframe usually carries this.)
2. **"This is for me."** — it's relevant to *them*, not a blast. (Something specific about their
   world, their niche, or a pain they actually have.)

**The rule: build the bar that's short. Never prop up the one that's already standing.**

- If your result already screams "this is real" (huge number, famous brand), you don't need to
  pile on more proof — spend the words making it feel "for me" instead.
- If "this is real" is shaky (ordinary result, unknown brand), that's where the work goes — a
  sharper number, or a *mechanism* that makes them curious enough to overlook the modest result.

This is the single most important idea. Most bad texts fail because they prop up the bar that was
already standing (e.g. cramming three proof-numbers into one line) and ignore the short one.

---

## 3. Mechanism = the bite, not more proof

The **mechanism** is the "how we did it" line ("by giving product to 1,471 creators without ever
asking for a post", "mostly by making their CEO the go-to voice for AI defense").

Its job is **curiosity** — the "wait, how does that work?" feeling. The *result* already did the
proving. So a mechanism stuffed with proof-numbers is doing the wrong job: it reads robotic and
soulless. **The mechanism should make them lean in, not re-prove the result.**

The biggest v1 mistake was treating the mechanism as a second proof slot. It's not. It's the hook.

**Dissolve the objection implicitly — don't name it.** When the mechanism also answers a buyer fear, let
the *picture* carry the dissolve rather than stating the contrast. "creator content that doesn't even feel
like an ad" dissolves "my ads look like ads / agency creative isn't converting" **without saying it** —
stronger than the explicit "instead of polished agency creative," which names the objection and reads like
a pitch. Show the better world; don't argue against the worse one. (The "without X" wrapper is the one
sanctioned explicit form — a compressed pain, not an argument.) Implicit > explicit wherever it still lands.

---

## 4. You can only run the frame your case study can pay for

A "frame" (FOMO, curiosity, timing, etc.) needs specific ammo to fire. If you don't have the
ammo, that frame is off the table — don't fake it:

- No competitor to name → you can't run a "your rivals are doing this" (FOMO) frame.
- No timing/trigger signal → you can't run a "we hit them at the exact moment X happens" frame.
- No genuinely unusual method → you can't run a curiosity/weird-approach frame. Lead with the
  plain result instead.

This is why the same engine writes for any client: the *frames* are universal, but **which ones
fire is decided by what this specific case study actually gives you.**

---

## 5. Strong case → fly high. Ordinary case → get specific.

How hard the mechanism has to work depends on how strong the result is on its own:

- **Strong / outlier / famous-brand case** → the number does the convincing. You can keep the
  mechanism vague or even leave it out, and spend the words on stacked proof + relevance.
  ("Took them $0 → $2M in 2 months, now a $500M brand" needs no clever mechanism line.)
- **Ordinary-but-solid case** → the number won't stop them on its own, so a **sharp specific
  result or a curious mechanism has to carry it.** Get concrete.

(This is the real idea some earlier notes called "altitude." We don't use that word — just:
*strong case, fly high; ordinary case, get specific.*)

---

## 6. The offer changes what carries the text

Different offers give you different ammo, so the same rules produce different texts:

- **DTC creative / seeding** (e.g. Kynship): usually has a genuinely unusual *mechanism* → the
  mechanism can carry the bite.
- **SEO / GEO / organic** (e.g. Big Leap, Velox): the "mechanism" basically *is* the result
  ("ranking #1 on Google"). There's no weird method to be curious about → **don't force a fake
  unique mechanism.** Lead with the plain result + a "without X" wrapper + relevance.
- **PR / authority**: the bite is the *position* you engineered ("the go-to voice for X").
- **Local / home services**: the bite is usually *timing* ("at the exact moment a property floods").

The `offer-matrix.md` turns this into a lookup so a strategist doesn't have to hold it in their
head. **Forcing a DTC-style unique mechanism onto an SEO offer is exactly why v1 broke on Big Leap.**

---

## 7. What this means in practice (the order of moves)

1. Start from the **brief** (who they are, real pains, their own words) and the **chosen case study**.
2. Read the offer type → the **matrix** tells you which frame to lead with and whether the
   **mechanism, the result, or relevance** carries the bite.
3. If the mechanism carries: **mechanism-wordsmith** turns the literal "what we did" into a few
   sticky, curious, on-tone lines (or correctly tells you the mechanism should be omitted).
4. **sms-draft** assembles the full text(s) around the chosen frame, runs them through the
   tone guide, and hands you a spread to pick from.
5. A human always does the final taste pass. The skills get you 8/10 fast; you take it to 9–10.

---

## The non-negotiables (carry these into every skill)

- One job: earn "tell me more."
- Build the short bar; never prop up the standing one.
- Mechanism = curiosity, not extra proof.
- Only run frames the case study can pay for; never fake ammo.
- Strong case → fly high; ordinary case → get specific.
- Never force a unique mechanism onto an offer that doesn't have one (the Big Leap rule).
- Nothing gets invented — every claim traces to the brief, case study, master sheet, or winners
  (pulled from **Evergreen** first — see "Reaching Evergreen" above; local files are the seed).
- A human takes the last 8→9.
