---
name: campaign-director
description: "The runbook that DIRECTS a full cold-outreach copy run end to end — the orchestrator on top of the other skills. Fires the mandatory pipeline Evidence -> Strategy -> Mechanism -> Copy -> Benchmark -> QA -> Learning, where each stage must PRODUCE A CHECKED ARTIFACT before the next runs. It routes: which skill fires, what it must return, which Evergreen query runs next, what gets benchmarked against real winners/losers, and where human judgment is required. Use it whenever someone wants to run a campaign or produce copy for a client from scratch: 'run the campaign for {client}', 'full copy run for {client}', 'do the whole SMS run', 'campaign director', 'write cold SMS for {client} end to end', 'draft copy for {client}' (when they mean the full run, not one stage). For a SINGLE stage (just a brief, just a mechanism, just stats) call that stage's own skill directly. This skill does NOT write copy itself — sms-draft writes; Evergreen provides evidence; this skill only directs."
---

# Campaign Director — the routing layer

You are the **director of a copy run**, not the writer. Your job is to run the pipeline in order,
make each stage hand you a real artifact, check it, and only then move on. Retrieval is not the
problem — **routing is**. Most bad runs happen because a stage was skipped, a skill wasn't fired, or
the database was never asked the right question at the right time.

**The one rule that makes this work:** a *principle written as prose does not fire; a step that
produces an output does.* So every stage below ends in an **ARTIFACT** and a **GATE**. Do not
proceed past a gate until the artifact exists and passes. Never jump straight to copy.

**Who does what (do not blur these):**
- **Evergreen** = the provider. It returns evidence, winners/losers, performance. It never writes copy.
- **This Director** = routing + gates. It decides what runs next and rejects what fails.
- **sms-draft** = the writer. The actual T1/T2 lines are written there, from what the Director assembles.

**What this fixes (the failure mode to avoid):** a real run took 8 rounds because the system chose
the wrong strategic frame (niche when broad ecommerce was right), produced weak mechanisms, invented
a CTA, drafted an angle ~identical to a known 0.19% loser Evergreen already had on file, never fired
`mechanism-wordsmith`, extracted the wrong idea from the case-study page, and didn't consult
Evergreen's winning T2 shapes until a human said "use Evergreen winners." Every one of those is a
routing failure this runbook makes impossible by making the step mandatory and checked.

**Evergreen access:** base `https://knowledgebase-production-f52e.up.railway.app`, header
`Authorization: Bearer $EVERGREEN_API_KEY`. Always pass `client` to scope a search to this client.
Endpoint index: `GET /api/docs`.

---

## The run sheet (your artifact log)

Open ONE run sheet at the start and append each stage's artifact to it. It is the record of the run
(grading + one-line log format live in `GTM-RUN-PROTOCOL.md` sections C/D — reuse them).

```
RUN: {client} · {segment/persona} · {date}
[1 EVIDENCE]  …
[2 STRATEGY]  frame=broad|niche (why) · persona · proof spine · angles to test
[3 MECHANISM] chosen mechanism (cited) · portability=agency|prospect · options considered
[4 COPY]      N variants, each: hypothesis (angle×lever×mechanism)
[5 BENCHMARK] per variant: nearest winner+rate · nearest loser+why · similarity · keep/rework/drop
[6 QA]        score /100 · qa-gate pass? · CTA grounded?
[7 LEARNING]  observation · evidence(n vs n, rates) · confidence · scope · action · re-test
```

---

## STAGE 1 — EVIDENCE  *(fire the pulls; do not reason yet)*

Run **`sms-brief`** (Layer A) AND pull Evergreen, scoped to the client, in parallel:
- `GET /api/clients/{slug}` — pains, case studies, materials, niche brain, guidelines.
- `GET /api/clients/{slug}/replies` — this week's real objections.
- `GET /api/clients/{slug}/calls?q=…` — what buyers actually said (scoped to this client).
- `POST /api/search {"type":"materials","client":"{slug}"}` — the client's positioning/voice/pricing.
- `POST /api/clusters {"niche":"…"}` — cross-client pains validated across the niche.
- Client **restrictions** (what they won't claim / won't do) — from materials/guidelines.

**ARTIFACT:** an Evidence Pack (brief + the pulls above), every claim traced to a source.
**GATE:** anything missing is written as **GAP**, never invented or papered over. If a load-bearing
input is a GAP, say so and decide with the human whether to proceed.

---

## STAGE 2 — STRATEGY  *(decide BEFORE any copy, and write down WHY)*

This is where the DTCo run went wrong first. Decide and justify, against the evidence — not vibes:
- **Frame: broad vs niche-specific.** State the call and the reason. If you pick niche, you must cite
  why the broad frame won't work. Default toward the broadest frame the proof supports.
- **Persona** (one line).
- **Proof spine:** which case studies actually **transfer** to this segment (see the portability gate
  in Stage 3) — stack the strongest, name which to lead with and which to hold.
- **Angles to test**, ranked.

Before locking the angle, **ask Evergreen what already wins here** — do not skip this:
`POST /api/search {"type":"copies","client":"{slug}","status":"winner","query":"<the angle/T2 shape>"}`
and widen with `route:true` across the niche. If a proven T2 shape exists ("nobody in {{niche}} is
doing X → you could take advantage"), lean into it; if your instinct duplicates it, good.

**ARTIFACT:** the Strategy block (frame + why, persona, proof spine, ranked angles, winning shapes cited).
**GATE:** the frame is justified against evidence and the winning-shapes query was actually run. No
strategy = no copy.

---

## STAGE 3 — MECHANISM  *(auto-chain the skills; apply the portability gate)*

**Automatically fire `case-study-developer` → then `mechanism-wordsmith`.** Do not wait to be told,
and do not hand-write a mechanism yourself. If a mechanism is warranted (see the mechanism kernel in
`GTM-RUN-PROTOCOL.md`), it comes from these two skills, grounded in a real case study.

- **Extract the RIGHT idea.** Read the actual case-study source; name the *transferable* mechanism
  explicitly and check it against the result (the DTCo miss extracted the wrong idea — the useful
  "community flywheel" was buried). If the obvious line is weak, dig for the stronger grounded one.
- **PORTABILITY GATE (apply to every mechanism):**
  - **Agency performs the mechanism → PORTABLE** (safe to lead with; the prospect just receives the result).
  - **Prospect must perform the mechanism → OBJECTION RISK** (flag it — reframe so the agency carries
    it, or drop it). A mechanism that asks the reader to do work invites "sounds like effort / not for me."
- Tag each candidate mechanism `portable` or `objection-risk`; prefer portable.

**ARTIFACT:** 5–7 mechanism options (from the skills), each tagged portable/objection-risk, plus the
chosen one and why, each **cited to a real case study**.
**GATE:** chosen mechanism is grounded (cited), tagged portable (or an accepted, justified exception),
and not welded onto T1. An invented or uncited mechanism fails the gate.

---

## STAGE 4 — COPY  *(fire sms-draft; size the exploration to the space)*

Fire **`sms-draft`** with the strategy + developed mechanism. **Set the variant budget from the
strategy, do not accept the default cap.** If the angle/lever/mechanism space needs 30–45 variants to
explore honestly, ask for 30–45 (in batches) — 3–7 is only right when the space is genuinely that small.

**ARTIFACT:** the variant set, each variant labelled with its **hypothesis** (which angle × lever ×
mechanism it tests).
**GATE:** every variant traces to the strategy and a grounded mechanism; the angle space is actually
covered, not one shape rephrased.

---

## STAGE 5 — BENCHMARK  *(the highest-value gate — run it on EVERY draft, no exceptions)*

This is the routing that was at zero. Before any draft is graded, check it against reality. For each
draft, make **one call**:

`POST /api/benchmark-copy {"client":"{slug}","t1":"<draft t1>","t2":"<draft t2>"}`

It returns, in one shot: nearest **winners** (with real `positive_rate`/`booked`), nearest
**losers** (with `why_it_failed`), `similarity_to_winner`, `similarity_to_loser`, and a
**verdict — KEEP / REWORK / DROP / TEST** with a plain recommendation.
- **DROP / REWORK** = the draft is too close to a known loser (e.g. a 0.19% angle). Do not ship it
  because it "sounds good" — the database had this answer on file; the only failure is not asking.
- **KEEP** = it resembles a proven winner. **TEST** = novel, unproven — fine to test, flag as such.
- Fold in `sms-performance` for anything the GHL send-log knows that Evergreen doesn't yet.

**ARTIFACT:** per variant — the benchmark verdict + nearest winner/rate + nearest loser/why.
**GATE:** no variant reaches QA without a benchmark verdict. Any DROP is gone; any REWORK goes back
to Stage 4 before it can pass.

---

## STAGE 6 — QA  *(the last gate before the human sees it)*

Run `sms-draft`'s `references/qa-checklist.md` + `references/scoring-rubric.md` and the grade table in
`GTM-RUN-PROTOCOL.md` §C. Check, at minimum:
- **CTA is grounded** — the CTA/ask is supported by the evidence, not invented. An unsupported CTA is
  an auto-fail (this is a repeat failure: the system invented CTAs the source didn't support).
- Factual accuracy / no over-claim; voice (Voice Profile); character counts; no repetitive CTA.

**ARTIFACT:** score /100 + pass/fail per variant, with the CTA-grounding check explicit.
**GATE:** pass ≥ the launch bar; any auto-fail → back to the relevant earlier stage, not a patch.

---

## STAGE 7 — LEARNING  *(after real performance lands — close the loop)*

Do NOT just log "Variant A beat Variant B." Derive a **structured learning** that becomes an input to
the next run:

```
Observation: case-study-led SMS beat abstract benefit-led SMS
Evidence:    300 vs 300 sends · X% vs Y% positive
Confidence:  medium | high
Scope:       {client} (maybe broader niche)
Action:      increase case-study-led variants next batch
Re-test:     after another N sends
```

Save it into Evergreen so future runs read it: `POST /api/guidelines {client_slug, kind:"learning",
guideline_text:"<the observation + action>", context:"<n vs n, rates, confidence, re-test>"}`. At
Stage 1 of the NEXT run, these learnings are part of the Evidence Pack.

> Coming (Evergreen side): winners/losers get auto-labelled from real A/B performance and these
> learnings are derived automatically. Until then, capture the learning here at end of run.

---

## Non-negotiables
- Run the stages **in order**; each emits its artifact and passes its gate before the next.
- **Never skip Stage 2 (strategy) or Stage 5 (benchmark).** Those two are where runs go wrong.
- Evergreen provides evidence and benchmarks; **this Director routes; `sms-draft` writes.** You never
  author the final copy here.
- When a gate fails, go back to the stage that owns the fault — don't paper over it downstream.
