# Scaletopia SMS autopsy — Mon 24 Aug – Fri 28 Aug 2026

**Question:** we sent ~1,800+ cold SMS and Evergreen showed zero positive responses. Is that real, and if so why?

**Short answer:** the "zero" is a reporting artifact, but the underlying result is close to true. SMS produced **eight replies with genuine interest and zero meetings**. Every meeting and every clean positive that week came from **EmailBison, not SMS**. The cause is not primarily the copy — it is that **a quarter of the leads were unreachable, roughly half of everyone who replied told us we had the wrong person, and every warm SMS reply was either unanswered or fumbled.**

**Confidence:** high on the mechanics (n = 5,111 texts, 79 repliers). Low on any copy verdict (n = 8 interested replies).

**Sources:** raw GoHighLevel `conversations/messages/export`, location `TYVYHj7lX8bamHkOKz4s`, PT day boundaries, pulled 2026-08-31. Evergreen `/stats`, `/report`, `/deals`. Cross-checked against `clients/_rollup/output/2026-08-24_to_2026-08-28-unbooked-replies.json` and a fresh `missed_replies_scan`.

---

## 1. The outcome, cross-footed

| source | sent | positives | why it differs |
|---|---|---|---|
| **GHL raw (headline)** | 2,681 leads / 5,111 texts / 4,045 delivered | **8 interested replies, 0 meetings** | the only source that counts messages and sees uncategorised replies |
| Evergreen `/stats` "This Week" | 1,845 → now 0 | 0 | **live-updating field.** It means *the current week*. Read on Aug 31 it shows this week; read mid-week it showed a partial Aug 24–28. It was never a fixed number for that week |
| Evergreen `/report` `weekly_trend` week `2026-08-24` | — | 3 positives, 1 booked | channel-blended: **all 3 are email** |
| `2026-08-28-pr-count-defect-log.md` | 3,250 leads | 5 PRs | keyword classifier, no channel split — overstates, and covers Aug 21–27 not 24–28 |

**Your instinct was right.** Evergreen in-window deals = **4: three email, one SMS — and the SMS one is `Disqualified`.**

| channel | leads/sends | interested replies | deals | meetings booked |
|---|---|---|---|---|
| **SMS** | 2,681 leads / 5,111 texts | 8 | 1 (Disqualified) | **0** |
| Email (BD Campaign Relaunch) | — | 3 | 3 | **1** (Ready Set, Aug 27) |

Nobody booked a meeting off SMS that week. The "5 PRs" figure that has been circulating is a keyword-classifier artifact — the same tool the Aug 28 defect log was written to correct.

---

## 2. The week, day by day — and the finding nobody has written down

**Two completely different campaigns ran inside this one week**, and they behaved nothing alike:

| day | campaign | leads | texts | delivery fail | unreachable leads | unique repliers | interested |
|---|---|---|---|---|---|---|---|
| Mon 24 | **Mel / Chamber Media** | 608 | 1,158 | **31.7%** | **207 (34%)** | 8 | 0 |
| Tue 25 | **Mel / Chamber Media** | 608 | 1,164 | **30.8%** | **201 (33%)** | 8 | 1 |
| Wed 26 | **Kylie / Wise Digital** | 720 | 1,384 | 10.1% | 98 (14%) | 38 | 5 |
| Thu 27 | **Kylie / Wise Digital** | 728 | 1,375 | 14.3% | 139 (19%) | 24 | 2 |
| Fri 28 | Kylie / Wise Digital | 17 | 30 | 13.3% | 4 (24%) | 2 | 0 |
| **week** | | **2,681** | **5,111** | **20.9%** | **649 (24.2%)** | **79** | **8** |

**Mon + Tue (ICP Hook / "Mel"): 1,216 leads → 16 repliers (1.3%) → 0 interested.**
**Wed–Fri (BD Agencies / "Kylie"): 1,465 leads → 63 repliers (4.3%) → all 8 interested.**

Monday and Tuesday were a write-off. A third of every text failed to deliver and a third of the leads never received a single message. That half of the week is not a copy result — it is a list that was one-third dead on arrival.

- **Reachable leads: 2,032 of 2,681 (75.8%).** 649 leads had *every* text fail.
- **One sending number all week** (`+18334970232`, toll-free). **No number-split problem this week** — that bug did not fire.
- **Zero merge-variable defects.** No unrendered `{{slots}}`, no `[object Object]`, no empty-slot artifacts. That regression is fixed.

---

## 3. What actually caused it — ranked

### 🥇 The list, not the copy — HIGH confidence
**30 of 79 repliers (38%) explicitly said we had the wrong person**, by strict pattern match. Hand-reading the rest pushes it to **~37 (47%)**. Verbatim:

> "I have not worked at Spectrum in over 20 years." · "I have not been with Mudd in a decade. Maybe I should get you a better list to contact" · "Wrong number! No Christopher or Chris here for the past 8 yrs" · "I'm retired now" · "Take me off your list. I am a school teacher. I don't run or work at a company. I'm not the head of anything, except my students." · "10 years too late Kylie" · "I haven't worked for Reid for six years."

Combine that with 24% of leads being unreachable: **of 2,681 leads, roughly 2,000 were reachable and, extrapolating the replier signal, a large share of those were the wrong person.** The campaign never got a fair hearing. Opt-outs were 27 of 79 repliers (34%) — that is what a stale list does.

### 🥈 Every warm SMS reply was dropped or fumbled — HIGH confidence
Eight people showed genuine interest. Not one became a meeting.

| person | what they said | what we did |
|---|---|---|
| **Tyler Chesnicka** (Demand Local) | *"I'm interested in a demo. Ideally we'd like to focus on programmatic channels.. could you help there?"* | **never answered** |
| **Leslie Dean Fuller** (Brandefined) | *"3k per month after taxes, if so please continue"* | **never answered** |
| **Yannick Lorenz** (ex-Veza) | *"Kylie, good outreach. Not with Veza anymore but interested."* | **never answered, never categorised** |
| ex-Hyperquake replier | *"...working in another BD roll that could possibly be a fit"* + *"would you bill on a monthly retainer"* + *"do you do pay per perf"* | **filed as stale.** Two pricing questions, ignored |
| **Nancy O'Reilly** (Strategis) | *"it sounds very interested. Can I give you a call sometime Friday?"* | answered in 19 min — but **she offered a phone call and we countered with a calendar invite.** Thread died |
| **Simone Andes** (Rank Media) | *"Ok"* | answered in 3 min with the **stock template**. She replied with a different person's email (`tina@directroutedesign.com`) — likely wrong contact |
| Aug 25 replier | *"Sure! Let's chat"* | not in Evergreen at all |
| Aug 24 replier | *"Don't have the email. Mind re-sending it?"* | not in Evergreen at all |

Three High/Medium-tier replies were never answered at all. This is the same finding as `JULY-AUTOPSY.md` §6 item 2, unfixed six weeks later.

**Also, on the email side (noted, excluded from SMS numbers):** **Chad Gillen** (Above the Bar Marketing) replied *"I'd appreciate a 30 min demo, please"* **with a Google Calendar booking link — and was never answered.** That is a booked meeting left on the table.

### 🥉 The copy is not what killed the week — MEDIUM confidence
Details in §5. Both campaigns' T2 opens on the banned rung-0 construction, and the Wed–Fri pair ships at 2 SMS segments. But reply rate on the reachable Wed–Fri list was 4.3%, which is *above* July's 2.4–2.9%. **The hook was working. The week died downstream of it.**

---

## 4. Missed and miscategorised

`missed_replies_scan --client scaletopia --from 2026-08-24 --to 2026-08-28`:

> Scaletopia: 5,111 out / 86 in · **79 repliers = 54 categorised + 25 never categorised**

**25 of 79 replies (32%) never got a category in Airtable.** Breakdown: 14 wrong-number/left-company, 9 unclear, 1 negative, **1 positive**. Two of those 25 are live leads:

- **Yannick Lorenz** — *"Kylie, good outreach. Not with Veza anymore but interested."* Silent 3 days. Uncategorised, unanswered.
- **Sebastian Clemmons** — *"got laid off from PartnerCentric a few months ago and am now at another company."* Told us where he moved. Nobody followed up.

Three of the eight categorised SMS replies are flagged `mistagged=True` in the week artifact (two `Neutral` rows that are really wrong-person, one `Maybe` that is really a soft yes).

**Structural blind spot:** Evergreen's `/contacts` endpoint cannot return `Wrong Number`, `Retired`, `Disqualified`, `AI Automated` or `AI Error`. For this window those tags hold **87 / 55 / 9 / 6 / 1** records. So any stale-rate computed from Evergreen is **zero by construction** — it structurally cannot see the thing that broke this week. Stale rate must come from GHL.

---

## 5. Copy QA

Run against `.claude/skills/sms-draft/references/qa-checklist.md` and `scripts/sms_qa.py`.

### Mechanical

| | Mon–Tue T1 | Mon–Tue T2 | Wed–Fri T1 | Wed–Fri T2 | July winner T1 | July winner T2 |
|---|---|---|---|---|---|---|
| chars | 145 | 160 | **211** | **162** | 157 | 133 |
| segments | 1 | 1 | **2** | **2** | 1 | 1 |
| flags | clean | clean | ⚠BULK ⚠MULTI-SEG | ⚠BULK ⚠MULTI-SEG | rung-0 risk | clean |

**42.9% of all texts sent that week (2,191 of 5,111) were over 160 characters.** The Wed–Fri campaign shipped both halves as 2-segment messages. This is the exact defect that flagged the July *loser* (211-char T2) in `JULY-AUTOPSY.md` §4.

### The 13-item gate

**Wed–Fri (BD Agencies, "Kylie") — the CTA is proven; the format is not.**

> T1: `Hi {name}, I know you head up sales at {Company} so wanted to run an idea by you.. just helped Wise Digital Partners close 8 retainers ($42k mrr) over the summer by combining text outreach with calling.`
> T2: `think we could do the same to connect you with {ICP_signal}.. could I show u how? - Kylie, Scaletopia`

- **Q4 relevance — the gate says auto-fail. The send log says otherwise.** The checklist calls `think we could do the same to…` a rung-0 opener and fails it automatically. August contradicts the gate. On 2026-08-10 a prospect named Tyler received `think we could do the same to help you sign hvac firms spending $3k/month on google with no conversion tracking.. could I show u how? (on a performance basis)`, answered `How?`, and booked on 2026-08-11. **That line booked a meeting.** The `{ICP_signal}` slot carries real account-level specificity, so the line is not generic in practice. I withdraw the auto-fail. The rule needs a change, not the copy.
- T1's *"I know you head up sales at {Company}"* is a weaker claim. It restates the title and the company. It broke twice this week: John Condit answered *"you would need to begin your journey with cox media groups headquarters in atlanta"*, and Howard Bomstein answered *"only a consultant, not active in day to day operations."* Both are targeting errors, not copy errors.
- Q3 proof ✓ (8 retainers / $42k mrr / "over the summer" — number, unit and timeframe all present).
- Q6 anatomy ✓ (the mechanism *"combining text outreach with calling"* sits on T1).
- Q7 length ✗ — both halves ship at 2 SMS segments.
- **Verdict: the length and the sender name fail. The CTA does not.**

**Mon–Tue (ICP Hook, "Mel") — mechanically clean, but sent into a dead list.**
Same T2 construction, and this is the exact variant that booked Tyler on Aug 11. No disarmer — `lol` is doing that job and reads as a tic. It is a degraded copy of logged winner W6: it kept *"max capacity"* but dropped the discovery source, so scarcity stopped being a reason for the text and became a boast. Mechanically clean (1 segment each). 

### Sender identity — a real defect
SMS signs **"Kylie"**. Nancy O'Reilly replied *"Hi Kyle"*. Another replier just wrote *"Kylie?"*. The email arm the same week ran **"Molly"** *and* **"Alex"**. That is **three sender personas across two channels in one week**, and prospects are visibly confused by the name.

### Loser gate
Live pull from Evergreen `POST /api/search {"type":"copies","status":"loser"}` returned **0 rows**. The gate could not be run — the loser corpus has no Scaletopia entries despite 30k+ documented sends. Stating this rather than skipping it.

### The honest part
As in July: **the QA does not explain the result.** Wed–Fri pulled a 4.3% replier rate on reachable leads — better than the July winner's week. Fixing the copy alone would not have produced a meeting. It would have produced more of the same replies, still unanswered.

---

## 6. Logistics verdict

| check | result | threshold | verdict |
|---|---|---|---|
| Delivery failure (week) | 20.9% | >20% = carrier risk | 🔴 **FAIL** — Mon/Tue at ~31% |
| Reachable leads | 75.8% | >95% | 🔴 **FAIL** |
| Wrong-person share of repliers | 38–47% | >25% | 🔴 **FAIL** — list is the primary defect |
| Opt-out per lead | 1.0% | <1.5% | 🟢 pass |
| Opt-out per interested reply | 27:8 ≈ 3.4:1 | >5:1 kill | 🟡 watch |
| Interested per lead | 1 per 335 | ≥1 per 300 | 🟡 borderline — **but 0 converted** |
| Merge-var rendering | 0 defects | any = stop | 🟢 pass |
| Sending numbers | 1 | >1 = split risk | 🟢 pass |
| Sender personas | **3** across channels | 1 | 🔴 **FAIL** |
| Texts >160 chars | 42.9% | 0 | 🔴 **FAIL** |
| High-tier replies unanswered | **3 SMS + 1 email** | any = sev-1 | 🔴 **FAIL** |
| Replies never categorised | 25 of 79 (32%) | <10% | 🔴 **FAIL** |

---

## 7. Strawman — redline this

Ordered by expected meetings per unit of effort.

1. **Go answer the four people still waiting.** Tyler Chesnicka, Leslie Dean Fuller, Yannick Lorenz, and — on email — Chad Gillen, who sent a calendar link. Answer the question they actually asked, in the channel they used. Nancy O'Reilly asked for a *phone call*; call her. Cost: one hour. This is the only item that can produce a meeting from work already paid for.
2. **Stop sending to this list.** 24% unreachable and ~45% wrong-person is not a copy problem you can write your way out of. Re-verify or replace before the next send. The toll-free number is carrying two days at ~31% failure — that is reputation risk.
3. **Make "answer every reply within the hour, in-channel" an owned job with a name on it.** 32% of replies got no category at all. The standing benchmark is <1h books 43% vs >1h 28%. This has now been the #1 or #2 finding in three consecutive audits.
4. **Keep the T2 CTA. Change the QA rule instead.** `think we could do the same to… could I show u how?` booked a meeting on Aug 11. The rung-0 rule in `qa-checklist.md` fails a line that converts, because the rule cannot see that `{ICP_signal}` carries the specificity. Fix the rule to test the rendered text, not the template.
5. **Get both texts back to one segment.** T1 211 → ≤160. The July winner ran 157/133.
6. **One sender name.** Pick it, use it on SMS and email, stop rotating. Prospects are replying to the wrong name.
7. **Promote the July winner into `sms-playbook/winners.csv`.** Our best-evidenced copy still is not in the file every skill QAs against, so the gate cannot benchmark against it.

**What I would deliberately NOT do:**
- Don't rewrite the hook. Wed–Fri's reply rate beat July's. The hook is not the problem.
- Don't chase volume. More sends into this list buys more opt-outs.
- Don't touch the number-split bug. It did not fire this week — one number, all week.
- Don't conclude anything causal about copy from n=8.

---

## 8. Caveats and tooling defects found

- **n = 8 interested replies.** No copy verdict is statistically supportable at this n. The mechanics (5,111 texts, 79 repliers) are.
- The week artifact was built **2026-08-28 16:14Z** — mid-Friday. Friday afternoon replies are absent from it. The GHL pull here supersedes it.
- `ghl_sms_daily.py` "leads texted" (2,668) counts workflow-source only; the raw outbound count is 2,681. Both are quoted where used.
- **Classifier defects** (append to `clients/_rollup/2026-08-28-pr-count-defect-log.md`):
  - `POSITIVE` matched *"Hey Kylie, not sure how you got my number but I got laid off from PartnerCentric"* — a stale record scored as a positive. `STALE` precedence is not catching "laid off".
  - `HARD_OPTOUT` lacks `don't contact`; `REFERRAL` contains the token `contact `, so *"please don't contact me again"* would classify as a referral.
  - 22 replies landed in `unclear` on Aug 26 alone, most of which are plainly wrong-person.
  - `ghl_sms_daily.py` does not load `clients/scaletopia/reply-overrides.csv`, so any positive count it prints is unfiltered.
- `PT_OFFSET` is hardcoded `-7` (PDT). Correct for August, wrong after Nov 1.
- Evergreen `/report` returned 132 campaign rows, 132 distinct names — the 46× duplicate-row bug did **not** reproduce on this pull. `replies` came back as 0 on every row, so campaign-level reply data remains unusable.
