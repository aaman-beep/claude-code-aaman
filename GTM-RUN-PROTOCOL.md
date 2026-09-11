# GTM Run Protocol — the fill-in sheet for every copy run

> **STRAWMAN — redline me.** Copy this sheet at the start of **every** GTM/copy run and fill it as you go.
> The point isn't more process — it's that every run drops the **same shape of data**, so across a handful
> of runs we can see what's actually breaking, hand Hilal real numbers, and tweak from a fixed baseline.
> **Nothing in the system changes** — this is just the lane we agree to run in.
>
> Uses only what already exists: `sms-playbook/` (levers, FUNDAMENTALS, relevance-engine, enrichment-menu,
> winners.csv) + `sms-draft`'s `scoring-rubric.md` / `qa-checklist.md`. Don't improve the sheet mid-run — if a
> field feels wrong, note it in the margin and we fix the sheet *after*, so runs stay comparable.

---

## A · Lock the inputs BEFORE any copy  *(the consistent front door)*

Fill every line. A guess or a blank = mark it **GAP** — never skip it. A blank here IS the inconsistency we're killing.

- **Client / offer:**
- **Segment / persona** (one line):
- **Offer archetype** (pick one): `DTC creative-seeding` · `SEO/GEO/organic` · `PR/authority` · `Local/trigger` · `Agency/outbound`
- **Lead lever(s)** (1–3, from `levers.md`) + one-line why:
- **Mechanism — GENERATE or OMIT?** (see kernel below) · why:
- **Case study chosen:** brand · raw result · literal mechanism · tier (S–D) · result in the buyer's **native unit**? (Y/N)
- **Relevance plan:** the Clay var / enrichment + its **rung 0–3** (`relevance-engine.md`). *Floor check: not rung-0 unless the case is S-tier.*
- **Which bar is short here** (`FUNDAMENTALS.md` two bars): is **"this is real"** or **"this is for me"** the one that needs the words?
- **Closest logged winner(s)** this maps to (`winners.csv`):

→ If you can't fill A without inventing something, the run isn't ready. That's the signal — don't paper over it.

---

## B · Log the run AS IT HAPPENS  *(what only you supplied)*

- **Skills fired, in order:**
- **Rounds of back-and-forth:** ___  · **Wall-clock:** ___  · **vs your manual baseline:** ___
- **Every point you had to inject judgment a junior / your head of CX wouldn't have** *(the most important line — this is the backlog we're systematising):*
  1.
  2.
  3.
- **Anything the skill did off-script** (invented a taxonomy, padded thin, went generic, wrong unit, welded mechanism to T1…):

---

## C · Grade the shipped variant(s)  *(same scoring every time)*

Per variant, score 0–100 (`scoring-rubric.md`):

| Relevance /30 | Human /25 | Proof-fit /20 | USP-mechanism /15 | CTA /10 | **Total /100** |
|---|---|---|---|---|---|
|  |  |  |  |  |  |

- **QA gate** (`qa-checklist.md`): pass ≥ **11/13**? Any **auto-fail** (Q1 mechanism-coherence · Q2 no-overclaim · Q5 sender-credibility · Q6 anatomy · Q10 scam / speaks-to-them)?
- **Closest winner it's modelled on** — does it clear it? *(if not → rewrite or drop)*
- **Verdict vs launch bar:** ≥80 quality · materially faster than manual · 0–1 off-script → **PASS / NOT YET**

---

## D · One-line log  *(append one row per run — this is the data for Hilal + for us)*

| date | client | offer archetype | lever | score /100 | rounds | time | top failure | top thing YOU had to supply |
|---|---|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |  |  |

---

### Reference — the mechanism kernel (the de-bloated offer-matrix, for filling section A)

*Ammo / case-strength picks the lever; sophistication only flavours the tone. Match your case to the closest `winners.csv` row when unsure.*

| Offer archetype | Default lead lever | Mechanism? |
|---|---|---|
| DTC creative-seeding | Unique / Curious | **GENERATE** (it's genuinely distinctive) |
| SEO / GEO / organic | Helpful / Curious | **OMIT** (the tactic *is* the result → lead result + "without ads" wrapper) |
| PR / authority | Curious / Helpful | GENERATE (abstract — the *position*) |
| Local / trigger | Timely / Helpful | trigger → GENERATE · guarantee → OMIT |
| Agency / outbound | FOMO / Curious | usually OMIT (lead on the Clay ICP-signal) |
