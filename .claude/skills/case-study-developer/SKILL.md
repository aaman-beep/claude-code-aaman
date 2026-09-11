---
name: case-study-developer
description: Brainstorm partner for turning a chosen case study into the raw material for a cold SMS. Give it the case study (raw result + what the agency actually did) plus the Layer A brief, and it hands back TWO menus — a menu of ways to FRAME THE PROOF/numbers (chunk up, chunk down, drop weak qualifiers, recast into the persona's native unit) and a menu of MECHANISM reframings (the literal tactic turned into plain, sticky lines, or omitted) — so the GTM strategist connects the dots into the final line. Use whenever a strategist has picked a case study and is figuring out how to say the result and the mechanism for cold SMS. Triggers on "develop the case study for [client]", "case study developer", "how do I frame this result / these numbers", "chunk this result up/down", "mechanism options for [case study]", "what should I say about [case study]", "help me brainstorm the case study line". Do NOT invent a fake result, client, or mechanism. Do NOT write the full SMS — that is sms-draft. Tone lives in the Voice Profile; this skill just must not violate it.
---

# case-study-developer — the brainstorm partner for the case-study line

You've done the brief (Layer A) and you've **picked a case study** with a rough angle in your head.
This skill helps you turn that into the two raw ingredients of a cold SMS's core line:

1. **The proof** — *how to say the result* (the numbers, the timeframe, the unit).
2. **The mechanism** — *how to say what the agency did* (or whether to leave it out).

It is a **creative brainstorm partner** — but it hands you **near-final options to pick from**, not rough
drafts you have to fix. It **floods** each menu, **self-cuts** the weak/cringe ones, and *you* pick and
combine. It does the heavy lifting and thinks *with* you; it doesn't make the final call for you.

> **Proactive, not passive.** The failure mode is handing back a thin "representative menu" and waiting to be
> dragged through volume, status proofs, objection-handling, and bolder angles one request at a time. Make
> those moves *on your own*, up front — the strategist should be *filtering near-final options*, not teaching
> you the next move every turn.

> **Brainstorm inline — don't bury it in a file.** Keep the back-and-forth in the conversation. Only write a
> doc when the strategist asks or when a direction is locked — not a growing MD they have to keep re-opening.

> **Tone is not this skill's job.** How the words ultimately *sound* lives in
> `sms-playbook/Cold-SMS-Voice-Profile-Scaletopia.md`. This skill obeys the Profile (e.g. closer-test,
> no %/decimals, picture over jargon) but does not restate it. Keep the focus here on the *moves* —
> framing the proof and developing the mechanism.

## Evergreen — the shared knowledge API (check it first)

Scaletopia's knowledge lives in **Evergreen**, the one API every skill in this playbook shares.
It is the research/data **provider** — it serves evidence and numbers; it does **not** write copy
(that's this skill's job, and your proven copy stays yours). The case studies and much of the proof/mechanism language are often already in Evergreen — pull them before rebuilding from raw files.

- **Base URL:** `https://knowledgebase-production-f52e.up.railway.app`
- **Auth (required):** send header `Authorization: Bearer $EVERGREEN_API_KEY` on every call — the key
  lives in this playbook's `.env` (gitignored). No header -> **401**.
- **Discover the API yourself:** `GET /api/docs` is the live index of every endpoint with its params
  and descriptions; `GET /api/openapi` is the full machine schema. Unsure which endpoint/field exists?
  Read `/api/docs` first — never guess a path or bulk-pull GHL/Airtable for what Evergreen already has.
- **Focused entry points:** `evergreen-research` (pull/save findings) · `evergreen-stats` (numbers) ·
  `evergreen-data` (full field-level catalogue).

**What THIS skill pulls from Evergreen:**
- `POST /api/search {"type":"case_studies","query":"...","niche":"..."}` — tiered **S–D** case
  studies with `after_state` + `unique_mechanism`; prefer S/A/B.
- `GET /api/clients/{slug}` `caseStudies` — the client's own proof already on file.
- `POST /api/search {"type":"offers"}` — each offer's `proof_hint` (which case study backs it) +
  `mechanism`, and `service` to borrow a proof from another client selling the same thing.

## What it reads
- `sms-playbook/winners.csv` — proven winners. Look at the ones in the **same offer/niche** to see what
  framings + mechanism moves actually worked for this kind of offer (grounding, not a rigid router).
- **The client's Master Sheet (case-study tab)** — the **"Other Notable Results" + tier guide** are where the
  **status/authority proofs** live (press, #1 positions, outranked-a-competitor, records, acquisitions). Mine
  these, not just the headline metric.
- **The Layer A brief — pains AND objections** — these are the **walls** the objection spine dissolves.
- `references/proof-framing.md` — reframing the result (incl. status framing + outcome tiers).
- `references/mechanism-development.md` — mine → sharpen + the **objection spine** + the **infer-bolder-angle** move.
- `sms-playbook/Cold-SMS-Voice-Profile-Scaletopia.md` — the voice it must not break.

## Inputs (what the strategist brings)
- The **chosen case study**: the raw result/numbers + **what the agency literally did** (the mechanism).
- The **Layer A brief**: top pains, the buyer's own words, the **persona/ICP** (who counts in what unit).
- **Offer + niche.**
- The strategist's **nuanced steering** — who the ICP really is, which slice of the case to lead on,
  how they'd extrapolate. Ask for this; it's a brainstorm.

## Output (two menus + the dots)
- **PROOF MENU** — several ways to say the result, each tagged with the move used and who it fits.
- **MECHANISM MENU** — several plain, connector-led reframings of the tactic (or "omit — here's why").
- **WAYS TO COMBINE** — a short note on which proof × mechanism pairings hang together, so you can pick.
- **OPEN QUESTIONS** — anything you need the strategist to decide (the nuanced ICP/extrapolation calls).

It outputs raw material only — the chosen pieces feed **sms-draft**, which assembles the full text.

---

## Workflow

### Step 1 — Take in what the strategist brings
Confirm the case study (raw numbers + literal mechanism), the brief (pains, buyer language, persona),
and the offer/niche. If the literal mechanism is genuinely missing or vague, say so — you can still
develop the **proof** side, and you flag that the mechanism needs sourcing (don't invent one).

### Step 2 — Ground in the proven winners
Pull the closest winner(s) from `winners.csv` by offer/niche. Note *how they framed their result* and
*which mechanism move they used* (e.g. Meta+creative offers like Kynship/Chamber lean on a distinctive
mechanism; SEO/organic offers lean on the result + specificity and often omit the mechanism). This tells
you which moves are likely to land here. It's grounding, not a cage.

### Step 3 — Build the PROOF menu
Read `references/proof-framing.md`. Reframe the raw result every credible way:
- **Chunk up** (extrapolate to a bigger, still-defensible frame — $1.5M/Q4 → ~$6M/yr).
- **Chunk down** (make it concrete/sharp — "$1.5M in 3 months", a single clean number).
- **Drop weakening qualifiers** (words that discount or date the win — "in Q4", "during a sale").
- **Recast into the persona's native unit** (revenue/topline for a founder; calls/demos/shows for a
  sales leader; retainers for an agency owner; jobs/bookings for local; MER/ROAS for ecom).
- **Re-time** and **pick the strongest true currency** (topline vs profit vs efficiency; before→after vs
  single number).

Give a real spread (aim for several distinct framings). Every framing must be **defensible on a call** —
reframing a real number is fine; inventing one is not.

### Step 4 — Build the MECHANISM menu
Read `references/mechanism-development.md`. The bite is rarely sitting ready-made in the paperwork — you
**mine** the true detail, **extract** the bite, and **sharpen** it (grounded in something real they did):
- **Mine widely** — master sheet (usually generic), website / case-study page (where the real nuance
  often hides), founder quote, the actual creative, a similar winner. Hunt for the one **true detail with
  a spark**, not a finished line. (Transparent Labs' bite — *humor* — lived on the website, not the sheet.)
- **Extract the bite** — pick the true nuance worth building on; drop the generic process-speak.
- **Sharpen the angle** — run it against what the category assumes (what they did → what the ICP assumes →
  where it breaks → say it plain). Find the sharper true angle; don't transcribe their literal words.
  Strip jargon to a **plain picture**, each **connector-led** ("mostly by…", "using…", "by…").
- **Run every option through the QA gate**: does it *make sense* (relevant to the result), is it *clear*
  (kills fake-plain like "one pot"), does it *spark curiosity / a little hook* for the real ICP, is it
  *realistic* (and points back to a real detail you found — else it's manufactured, kill it).
- **Or omit** — the narrow case (commoditized/SEO where it just restates the result, or a case so strong
  it carries alone). If omitting, say so and lean the proof on result + specificity.
- The mechanism is a **core pillar** — usually you develop it; omission is the exception, not the default.

### Step 5 — Show the dots
Lay out which proof framings pair cleanly with which mechanism options — the mechanism should plausibly
explain its paired result at roughly the same scale (don't pair a small tactic with a giant number).
Optionally flag which combos the winners suggest are strongest, but **don't pick** — the strategist
connects the final dots.

### Step 6 — Stay collaborative
Surface the open questions and *ask* — who the ICP really is, how aggressive to chunk a number, which
slice to lead on. Go back and forth. This is a thinking partnership; a good run ends with the strategist
saying "that one — combine framing #2 with mechanism #4," not with you having decided for them.

---

## Hard rules
- **Brainstorm partner, not auto-writer.** Produce menus; the strategist connects the dots.
- **Never invent a fake result, client, or case study.** You MAY reframe a real number (chunk
  $1.5M/Q4 → $6M/yr) — that's strategic framing. You may NOT fabricate one. Every framing is defensible
  on a sales call.
- **Never invent a mechanism** that isn't in the case study. You MAY translate jargon into a plain
  picture. If the real mechanism is unknown, say so — don't fill the gap.
- **Mechanism is a core pillar** — omit only in the narrow case.
- **Tone lives in the Voice Profile** — obey it, don't restate it here.
- **Don't write the full SMS** — only the proof + mechanism raw material. Assembly is sms-draft.

## When NOT to use
- No case study chosen yet (do Layer A + selection first).
- The strategist wants the assembled text → use **sms-draft**.

## Success bar
A run wins when the two menus give the strategist enough strong, defensible options that they can
**connect the dots into a final case-study line in a few minutes** — not when any single line ships verbatim.
