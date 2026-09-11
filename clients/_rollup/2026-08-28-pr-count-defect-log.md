# Defect log — the PR count was 4× overstated

**2026-08-28.** For the automation-engineer call. Covers why "4 positives yesterday" was wrong,
what the real number is, and the two data problems underneath it.

---

## 1 · The headline correction

| | reported | actual |
|---|---|---|
| Positive replies, Aug 27 | **4** | **1** |
| PR / lead | 0.55% (1 per 182) | **0.14% (1 per 726)** |
| Verdict I gave | *"best PR day in weeks, worth running"* | **below the 1-per-300 bar** |

One qualified positive: **Nancy O'Reilly, Strategis** — asked for a Friday call.
Everything else was a referral, a stale contact, a soft no, or an opt-out.

## 2 · The corrected week (Aug 21–27)

| day | leads | **PR** | opt-out | stale/wrong |
|---|---:|---:|---:|---:|
| Fri 21 | 599 | 1 | 11 | 0 |
| Mon 24 | 600 | **0** | 5 | 0 |
| Tue 25 | 605 | 1 | 5 | 0 |
| Wed 26 | 720 | 2 | 11 | 7 |
| Thu 27 | 726 | 1 | 11 | 9 |
| **week** | **3,250** | **5** | **43** | **16** |

**1 PR per 650 leads. 8.6 opt-outs per positive.** Target is 19 weekly positives; actual 5.

---

## 3 · The error chain — four defects, all in `tools/ghl_sms_daily.py`

**3.1 — Counted messages, not people.** `classify()` ran per message and the report printed
`len(cls["positive"])`. Nancy sent two replies; both matched; she scored as **two PRs**.
→ *Fixed: classification is now per contact over their whole thread.*

**3.2 — The keyword list matched almost anything.** `POSITIVE` included
`"ok"`, `"okay"`, `"time"`, `"works"`, `"sounds"`, `"send"`, `"info"`.
*"Ok give me a bit. I'm just on a zoom meeting"* scored positive on `"ok"`.
→ *Fixed: those tokens removed; now requires an actual intent phrase.*

**3.3 — No bucket for "I don't work there any more".** This is the big one.
*"Not with Veza anymore but interested"* matched `"interested"` → **POSITIVE**. A person who
left the company cannot buy for it. `SOFT_NO` had `"no longer with"` but not `"haven't worked"`,
`"not with"`, `"wrong person"`, `"my name is not"`, `"retired"`.
→ *Fixed: new `stale_or_wrong` bucket, ranked ABOVE positive in precedence.*

**3.4 — No referral bucket.** *"I can't make any of those decisions, I would suggest finding
Chris"* is a routing win, not a PR. → *Fixed: `referral` bucket.*

**Precedence now:** `opt_out` → `stale_or_wrong` → `referral` → `soft_no` → `positive` → `unclear`.
A stale contact who says "interested" is still stale.

---

## 4 · The real business problem this was hiding

**Half the people replying don't work there any more.**

Aug 27: of 24 unique repliers, **12 were wrong-person** — and 3 of those were angry enough to
opt out:

> *"I haven't worked there for 12 years. Take me off your list"*
> *"I haven't worked for Reid for six years."*
> *"No Christopher or Chris here for the past 8 yrs"*
> *"10 years too late Kylie"*
> *"My name is not Richard, please remove me from your list"*
> *"I'm retired now"* · *"I am happily Retired.! …No interest"*

Trend across the week: **0% → 0% → 19% → 43%** of replies. It is getting worse, not stable.

Delivery failures moved with it: **10.5% → 31.9% → 29.8% → 7.5% → 11.7%.** Two days near 30%
is high enough to put the toll-free number itself at risk.

**This is a lead-data problem, not a copy problem.** The list is being sold contacts who left
their roles up to a decade ago. Strip them out and the copy's true denominator is much smaller —
but we are paying full send cost and full reputation cost on every one.

---

## 5 · For the automation-engineer call

### Ask them to fix
1. **Phone-to-current-employer verification at list build.** A 43% stale day means the vendor
   feed is not being validated. This is the single highest-value fix on the page.
2. **Tag leads with vertical / segment / list-source.** Every one of the 8,044 August leads
   carries the identical tag, so "did PR firms convert better than general agencies?" is
   **impossible** to answer retrospectively — not hard, impossible.
3. **Store `copy_variant` / `cta_arm` on the send record.** Right now the only way to tell which
   CTA a lead received is regex over the message body.

### Evergreen bugs to raise
4. **`/stats` and `/report` disagree with each other for the same week.**
   `/stats` → `This Week sms_sent=1845, sms_pos=0`; `/report` → `this_week sent=4205, positives=3`.
   GHL says 3,250 leads / 6,190 texts. Three sources, three answers.
5. **Duplicate campaign rows.** `ICP Hook Enriched` returns **46 rows**, each stamped `pos=24`;
   `Sniper` returns 5. Naive `SUM` overstates by 46×.
6. **No day-level series.** `weekly_trend` is weekly only, which is why a mid-week cutover
   (the Aug 12 CTA change) was invisible until reconstructed by hand from GHL.
7. **Numbers returned as strings** (`power_rate` at minimum) — crashes consumers on first parse.

### Define this once, in writing
**What counts as a positive reply?** Nobody has written it down, which is how four different
things got counted as one. Proposed: *a reply from a person still at the target company
expressing interest or asking for more.* Everything else — referral, stale contact,
"send me an email", objection — gets its own bucket and does **not** hit the PR KPI.

---

## 6 · What I got wrong, plainly

I reported 4 positives, called it the best day in weeks, and recommended continuing on that
basis. The tooling defect was mine — I edited this script earlier the same week and did not
check that its classifier counted people rather than messages. The recommendation direction
happens to survive (the list is the problem, not the copy), but the number I built it on was
4× too high and should not have been quoted.
