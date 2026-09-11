# ICP Hook Enriched — refreshed angles

**STRAWMAN — redline me.** 2026-08-25. Campaign `Scaletopia - ICP Hook Enriched | 25-500E | NA`,
GHL loc `TYVYHj7lX8bamHkOKz4s`.

## Why the running copy draws STOPs

Baseline, Aug 3–25 (GHL truth): **8,044 leads · 15,502 texts · 190 replies · ~14 true positives
· 116 opt-outs.** That's **1 positive per ~575 leads** and **7.2 opt-outs per positive**.

```
T1: Hi {name}, it's Mel from Scaletopia - we just helped Chamber Media sign 18 retainers
    in 8 months from outbound but now they're at max capacity lol
T2: think we could do the same to help you sign {hook}.. could I show u how? (on a performance basis)
```

Three defects against our own playbook:

1. **T2 opens on the banned rung-0 line.** `relevance-engine.md` grades relevance on 4 rungs and
   marks rung 0 banned, quoting the exact failure: *"could do the same for {{company}}"*. T2 opens
   **"think we could do the same to help you sign…"** — verbatim, on all 8,044 sends. The enriched
   hook that follows is rung 1–3, but the generic frame lands first.
2. **No disarmer.** Voice Profile: *"Disarmer is near-mandatory"*, with a decision table
   prescribing *"feel free to ignore if…"* for skeptical agency buyers. **18 of our 20 winners**
   open with one. This has none — `lol` is doing that job and reads as a tic, not a lowered guard.
3. **It's a degraded [W6].** W6 = *"found {{company}} on AgencyVista, bit of a weird situation …
   but they're maxed for client capacity."* The current copy kept "maxed" and dropped the
   discovery source — so "max capacity" stopped being a reason for the text and became a boast.

**The antidote is already logged.** [W18] Go Fish won because *"T1 opens on a manual-looking
observation… reads hand-written, not blasted"*, with T2 *"not asking for your business but could I
at least share a few ideas"* — that shipped human replies instead of STOPs.

---

## The angles

QA'd: disarmer present · no `AI-timed` · no `could do the same` · no email-handoff CTA ·
native unit = retainers/clients · T1+T2 ≤ 310 chars.

> Note on structure: the ask *"I think we could help {company} sign 3-4 clients"* lives in **T2**,
> not T1. Voice Profile: the opener *"is not the place to lead with heavy relevance — that spikes
> the guard on a stranger's text."* T1 disarms, T2 aims. That's how [W13] works.

### A · Named-target — RUN THIS (W13 · Curious+Helpful · carries: ICP-signal specificity)
```
T1: Hi {first_name}, feel free to ignore if outbound's already handled - Mel at Scaletopia.
    We run the texting side for 26 marketing agencies.

T2: for {company} I'd go straight at {ICP_signal} and text them the week they start shopping.
    that's how Chamber Media signed 18 retainers in 8 months. worth 10 mins?
```
Mechanism in plain English — *"text them the week they start shopping"* — says what "AI-timed"
meant without the burnt phrase a prospect already threw back at us
(*"is this one of your ai-timed text outreach campaigns?"* — 702 Pros).

### B · Value-give — RUN THIS (W18 · Helpful · carries: relevance + a real give)
```
T1: Hi {first_name}, bit random - Mel at Scaletopia. The {n} domains pointing at {company}
    tell me you already run cold email.

T2: not asking for your business, but I pulled the {ICP_signal} we'd be texting for you
    this month. want the list? yours either way.
```
Rung-3 relevance we can actually pay for — the WHOis redirect detector produces `{n}`.
Gives before asking. **The direct STOP antidote.**

### C · Restored capacity (W6 · FOMO · carries: case + discovery source)
```
T1: Hi {first_name}, found {company} on {directory} - bit of a weird situation. We run outbound
    for 26 agencies and one just went maxed on {ICP} they can't take.

T2: rather than sit on it I'd point it at {company} - we'd be texting {ICP_signal} on your
    behalf. Chamber signed 18 retainers this way. want the details?
```

### D · Capacity reframe (W4/W10 · Helpful · carries: the question)
```
T1: Hi {first_name}, know this is random - Mel at Scaletopia. could {company} take on
    3-4 more clients this quarter?

T2: asking bc that's about what we add for the 26 agencies we run texting for - by reaching
    {ICP_signal} before they start shopping around. worth a look?
```
⚠️ Two question marks — drop the second for strict one-ask.

### E · The bandwidth truth (peer · Curious · carries: a true observation)
```
T1: Hi {first_name}, feel free to ignore - Mel at Scaletopia. most agencies we meet have the
    list and the copy, just nobody whose only job is working the replies.

T2: we're that bit for 26 of them. for {company} we'd be texting {ICP_signal}. Chamber got
    18 retainers out of it in 8 months. worth 10 mins?
```
Built on the Evergreen research quote — *"We just don't have someone to do it, frankly."* Doesn't
claim to be better at outbound than they are, which is this audience's actual objection.

---

## Lock before sending

1. **The Chamber number.** These use **18 retainers / 8 months**. [W13] says *14 in 5 months*;
   Sniper shipped *14 in 6 months, $72k mrr*. Three versions are live — pick one.
2. **Fix the hook generator.** One send went out as *"healthcare providers spending **$0/month on
   meta**"*. 657 distinct hooks over ~1,700 messages, some pitching $3–5k/mo clients to agencies
   whose floor is far higher (*"Need to be bigger than $10k/mo"*, *"Our minimum is significantly
   higher than that"*). Put a floor on the dollar figures; drop hooks with no number.

## How to run

- **A vs B, 50/50**, one week, ~600 leads/day. Five arms at 20% teaches nothing at this volume.
- **Tag the list by vertical before sending** — every one of the 8,044 leads carries the same tag,
  which is why "did PR firms do better?" is currently unanswerable.
- Read on **opt-outs per positive**. Baseline **7.2:1** is the number to beat.
- **Restore `could I show you how?`** alongside `(on a performance basis)`. In the only true
  head-to-head (Aug 6–11, both arms live) it was **3× more efficient** — 1 PR per 289 leads vs
  863 — and it's been off since the Aug 12 workflow edit.

## Open

- Whether A/B beats baseline is untested. Nothing here is a winner until the numbers say so.
- The PLAIN>PERF finding has a possible confound: all 6 PLAIN winners carried a concrete $ figure,
  3 of 7 PERF winners had none. Could be "concrete $ hooks win" rather than "PLAIN wins".
