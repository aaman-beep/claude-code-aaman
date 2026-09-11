# Defect log — the PR count was 4× overstated

**2026-08-28.** For the automation-engineer call. Reported number was **4 positive replies on
2026-08-27**. True number is **1**. Below is every layer that broke, the fix, and what still needs
a decision.

---

## 1 · The error chain

Four independent defects stacked, all in the same direction (inflating PRs).

| # | Layer | Defect | Effect on Aug 27 |
|---|---|---|---|
| 1 | `tools/ghl_sms_daily.py` | Classified per **message**, reported `len(positives)` | Nancy O'Reilly sent 2 replies → counted as **2 PRs** |
| 2 | keyword list | `POSITIVE` contained `"ok"`, `"okay"`, `"time"`, `"works"`, `"sounds"`, `"send"`, `"info"` | *"Ok give me a bit, I'm on a zoom meeting"* matched `"ok"` |
| 3 | no stale bucket | Nothing caught "I don't work there any more" | *"Not with Veza anymore but **interested**"* matched `"interested"` → **POSITIVE**. A person who left cannot buy for that company |
| 4 | no referral bucket | Routing replies scored as interest | *"I can't make any of those decisions, I'd suggest finding Chris"* → counted |

**Then I compounded it in the analysis**: reported `4 PR / 726 leads = 1 per 182`, called it
"best day in weeks", and recommended continuing the campaign on that basis. That recommendation was
built on a number that was 4× wrong.

| metric | reported | actual | error |
|---|---|---|---|
| positives (Aug 27) | 4 | **1** | 4× |
| PR / lead | 0.55% | **0.14%** | 4× |
| leads per PR | 182 | **726** | 4× |
| verdict given | "beats your 1-per-300 bar" | **2.4× worse than the bar** | inverted |

## 2 · The fix (shipped)

`tools/ghl_sms_daily.py` — classification is now **per contact**, over that contact's whole thread,
with explicit precedence:

```
opt_out  >  stale_or_wrong  >  referral  >  soft_no  >  positive  >  unclear
```

Precedence is the important part: a stale contact who says "interested" resolves to **stale**, not
positive. `POSITIVE` tokens tightened to intent phrases only (`"give you a call"`, `"worth
exploring"`, `"pricing"`, `"let's do"`…). Output now prints `inbound msgs` **and** `unique people`
so the two can never be conflated again.

## 3 · The corrected week

| day | leads | **POS** | referral | stale/wrong | opt-out | delivery fail |
|---|---:|---:|---:|---:|---:|---:|
| Fri 21 | 599 | 1 | 0 | 0 | 11 | 10.4% |
| Mon 24 | 600 | **0** | 0 | 0 | 5 | **31.7%** |
| Tue 25 | 605 | 1 | 0 | 0 | 5 | **29.9%** |
| Wed 26 | 720 | 2 | 0 | 7 | 11 | 7.5% |
| Thu 27 | 726 | **1** | 1 | 9 | 11 | 11.7% |
| **week** | **3,250** | **5** | 1 | 16 | 43 | — |

**1 PR per 650 leads. 8.6 opt-outs per positive.** Against a 1-per-300 bar and a 19-weekly-positive
KPI, this is roughly **half rate**, not the "best day in weeks" I reported.

## 4 · Two more defects found, not yet fixed

**4.1 — Evergreen `/stats` and `/report` disagree with each other.** Same client, same week:

| source | sent | positives |
|---|---|---|
| `/api/clients/scaletopia/stats` → This Week | 1,845 | **0** |
| `/api/clients/scaletopia/report` → `kpi.this_week` | 4,205 | **3** |
| GHL raw (truth) | 3,250 leads / 6,190 texts | 5 |

Three sources, three answers. **Ask the engineer which one the dashboard reads.**

**4.2 — no day-level view in Evergreen.** `weekly_trend` is weekly only, so a mid-week change is
invisible. This is the same defect that let me mis-call the CTA test earlier — a hard cutover on
Aug 12 was hidden inside a weekly bucket.

## 5 · The business finding underneath

**Half of everyone who replies isn't at the company any more.**

Aug 26–27: 16 of 41 unique repliers were stale/wrong-person, plus 3 more inside the opt-out bucket
(*"I haven't worked there for 12 years"*, *"I haven't worked at Postcard Mania for a year"*,
*"My name is not Richard"*). Verbatims:

> *"10 years too late Kylie"* · *"I haven't worked for Reid for six years"* · *"No Christopher or
> Chris here for the past 8 yrs"* · *"I'm retired now"* · *"I no longer work at Boostability"* ·
> *"I am no longer at ThinkTech"* · *"I'm not at Velir"*

Trend: **0% (Fri) → 19% (Wed) → 43% (Thu)** of replies.

And **delivery failure hit 31.7% Monday and 29.9% Tuesday** — consistent with texting dead numbers,
and high enough to put the toll-free number itself at risk.

## 6 · Questions for the automation engineer

1. **Which source does the KPI dashboard read** — `/stats`, `/report`, or GHL? They disagree by 2×
   on sends and by 3 on positives for the same week.
2. **Is Evergreen's `positives` per contact or per message?** If per message, it carries the same
   defect as §1 and every historical PR figure is inflated.
3. **Where did this lead list come from, and when was it last verified?** A 43% stale day points at
   the data vendor, not targeting.
4. **Can we get phone→current-employer validation** before the next load? 1,495 SMS leads remain.
5. **Can `copy_variant` be written to the send record?** Still the top ask — variant performance is
   currently only recoverable by regex on message bodies.
6. **Day-level series** on the reporting endpoint, not weekly.

## 7 · What I'd change about the KPI itself

`positives` alone is not a safe KPI when half the list is unreachable — it silently rewards
volume. Track **positives per *reachable* lead**, and publish **opt-outs per positive** (currently
**8.6:1**) next to it. Yesterday's true read is 1 PR and 11 opt-outs from 726 leads: the list is
being consumed faster than it converts.
