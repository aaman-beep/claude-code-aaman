# Wise Digital Partners — SMS performance autopsy

**Built:** 11 Aug 2026 · **AM:** Aaman · **Retainer:** $4,000 · **Onboarded:** 2 Mar 2026
**Question:** why did meetings go 17 (Jun) → 6 (Jul) → 0 (Aug)?
**Sources:** Evergreen API only — raw pulls saved in `clients/wise-digital/output/` (`PULLED-AT.txt` = 2026-08-11T15:29Z). No GHL or EmailBison connector exists for this client; see §7 for what that costs us.

---

## 1. Headline

**Three separate things happened, and only one of them is a copy problem.**

1. **June was inflated by a one-time conference campaign.** 10 of June's 17 meetings came from ENGAGE — a trade-show play ("I'll be at #705"). Cold SMS produced 6. The 17→6 "collapse" is mostly an event rolling off.
2. **August's zero is a volume failure, not a copy failure.** The CPA list — the only segment that has ever worked — is spent. 528 leads remain, ~7 days at current burn. Last week shipped **341 sends against a 1,500 target (23%)**.
3. **The retarget pass is genuinely tired.** Reply rate fell from 2.25% (July) to 0.72% (August) on the 4th retarget of an already-worked list. Volume and efficiency dropped together, which is why the result is exactly zero rather than merely low.

Reply handling is **not** the problem here — unlike the Scaletopia July case, this team works 83–100% of positives with a 21–67 min median. Don't spend effort there.

---

## 2. Reconciliation — the numbers cross-footed three ways

| Month | `meeting_booked_at` | meeting-stage @ created | `/report` weekly_trend |
|---|---|---|---|
| Mar | 11 | 12 | — |
| Apr | 6 | 7 | — |
| May | 8 | 6 | — |
| **Jun** | **17** | 14 | 5 |
| **Jul** | **6** | 15 | 15 |
| **Aug** | **0** | 0 | 0 |
| Total | **48** | 54 | — |

**Use the `meeting_booked_at` column.** It matches Aaman's recollection exactly (17 / 6 / 0) and is the only one keyed to when the meeting actually happened.

**Why the other two disagree — this is the ENGAGE artifact.** All 21 ENGAGE deals were *recorded* across June (12) and July (9), but all 10 bookings carry a **June** `meeting_booked_at`. The conference happened in June; the deals were entered retroactively into early July. Any view that buckets on record-creation date (`weekly_trend`, stage-at-created) pushes ~9 June meetings into July — which is why `weekly_trend` shows the trend *backwards* (Jun 5, Jul 15).

The 9 late-entered ENGAGE deals also carry `channel: null`, so any channel split that trusts the `channel` field will drop them.

---

## 3. What June's 17 actually was

| Source | Meetings | Note |
|---|---|---|
| **ENGAGE conference campaign** | **10** | 9 with `channel: null` + 1 SMS. One-time event. |
| Cold SMS — CPA | 5 | V2 ×3, Retargeting T4 ×1, V4 Retargeting ×1 |
| Cold SMS — unattributed | 1 | |
| Email — Plumbing/Clay | 1 | |
| **Total** | **17** | |

Restating the trend on cold SMS alone:

| | Mar | Apr | May | Jun | Jul | Aug |
|---|---|---|---|---|---|---|
| **Cold SMS meetings** | 9 | 3 | 6 | 6 | 4 | **0** |

Cold SMS has been flat at 3–6/month all year. It did not collapse in July — it went to zero in August. **That is the event to explain, and it is an August event, not a June→July one.**

---

## 4. Hypotheses — confirmed and killed

### ✅ CONFIRMED — Volume collapse from list exhaustion (HIGH confidence)

Reconstructed from two Evergreen snapshots (27 Jul scorecard vs today's pull):

| | July | August 1–11 | This week |
|---|---|---|---|
| SMS sends | ~7,069 (~228/day) | 1,958 (~178/day) | **341** |
| vs weekly target 1,500 | — | — | **23%** |

SMS **leads remaining: 1,729 (27 Jul) → 528 (today)** — 1,201 consumed in 15 days. At that burn there are **~7 days of list left.**

### ✅ CONFIRMED — Retarget fatigue (HIGH confidence)

| Month | Sends | Replies | Reply rate | Positives | Meetings |
|---|---|---|---|---|---|
| July | ~7,069 | 159 | **2.25%** | 15 | 6 |
| Aug 1–11 | 1,958 | 14 | **0.72%** | 3 | 0 |

A **3× reply-rate drop**. The only campaign generating August deals is `Retargeting T4` — the fourth retarget pass over the same CPA list.

**Counterfactual:** at July's efficiency (1,178 sends/meeting) August's 1,958 sends should have produced ~1.7 meetings. It produced 0. So volume explains most of the gap, but not all — efficiency fell too. To hit the 2 meetings/week target at July's rate, they'd need ~2,356 sends/week. They shipped 341.

### ✅ CONFIRMED — Merge-field defect (MED confidence, small blast radius)

**21 of 355 conversations (5.9%)** contain a literal empty-`{company}` render — texts that went out as:

> "Saw  and had some ideas. Mind if I give you a ring this week?"

Clustered **30 Jun – 1 Jul**, i.e. the launch batch of `Retargeting T4`. Same defect class flagged in their email copy ("Put together a couple ideas for ."). Real, cheap to fix, but too small to explain August.

### ❌ RULED OUT — Reply handling

| Month | Positives | Worked | Work % | Median response |
|---|---|---|---|---|
| Mar | 11 | 10 | 91% | 21 min |
| Apr | 11 | 10 | 91% | 24 min |
| May | 13 | 13 | 100% | 27 min |
| Jun | 18 | 15 | 83% | 67 min |
| Jul | 15 | 14 | 93% | 67 min |
| Aug | 3 | 3 | 100% | 45 min |

Response times roughly doubled after May (27 → 67 min) but stayed well inside the window that converted for Scaletopia. **When they answer, they answer fast** — the GHL-sourced register confirms a 17 min median across 66 human replies.

**But "worked %" was the wrong denominator — corrected 12 Aug.** It measured only positives that already had a *deal record*. Pulling every reply from the GHL log instead gives **35 people who engaged and were never answered at all**, median **64 days silent**. So: fast when they respond, but a third of the backlog never got a response. That's the follow-up list, not a reply-speed problem.

### ❌ RULED OUT — List decay getting worse

Dead contacts (wrong number / retired / disqualified) as a share of replies:

| Month | Threads | Dead | Dead % | Positive % |
|---|---|---|---|---|
| Jun | 27* | 7 | 25.9% | 3.7% |
| Jul | 159 | 40 | 25.2% | 8.8% |
| Aug | 14 | 3 | 21.4% | 21.4% |

\*June truncated — Evergreen caps the thread list at 200.

A ~25% dead rate is **chronically bad but flat.** It is not deteriorating, so it doesn't explain August. Worth fixing on its own merits: one in four people who reply is the wrong person.

### ✅ CONFIRMED — Copy regression (HIGH confidence) — *corrected 12 Aug, see §9*

**This section previously said copy was ruled out. That was wrong**, and the GHL connector is what showed it. Evergreen reconstructed copy for only 12 of 30 campaigns and its per-campaign positives are a broken join, so the comparison that matters was invisible.

All eight CPA batches sending today use the **Monocacy** opener, at 0.58–1.81% reply — **5 of the 8 are burners** (opt-outs ≥ replies). The **Dark Horse** opener, which pulled **6.25% / 5.26% / 4.64%**, is switched off. The two ran *concurrently* 17–25 June — same list, same weeks — so this is not seasonal drift. **4–7× the reply rate, at a lower opt-out rate.**

Dark Horse is also `W16`/`W17` in `sms-playbook/winners.csv` and produced all 5 CPA closed-won deals.

Full detail and the execution steps: [COPY-SWAP.md](COPY-SWAP.md).

---

## 5. The SMS copy that produced meetings

All 28 CPA meetings and all 5 CPA closed-won deals trace to one proof: **Dark Horse CPAs, $1.5m → $21m in 5 years via organic search.** Already logged as `W16`/`W17` in `sms-playbook/winners.csv`; still running as `Retargeting T4`.

> **T1:** Hi {first_name}, sorry to text out of the blue but we took Dark Horse CPAs from $1.5m to $21m in 5 years by replacing referrals with organic search (did this for Capstone Accounting too)
> **T2:** Saw {company} and had some ideas. Mind if I give you a ring this week? - Matt, WISE Digital

Seasonal T2 alt (`W17`, "slow at first then booked 3"):
> Thought I'd reach out now tax season's over - when referrals dry up it's tough to stay selective with clients. Mind if I give you a ring? - Matt, WISE Digital

A second live variant leads with a different case:
> "it's Matt from WISE Digital - feel free to ignore if u got enough referrals but we got Monocacy CPA $600k in new business in 1 yr by showing up first when startup founders searched for a CPA"

**Meetings by CPA campaign × A/B variant:** Accounting/CPA firms A=7, B=1, none=4 · V2 A=3, B=2, none=2 · Retargeting T4 B=3 · T3 (Fahad's) B=2, A=1 · V4 Retargeting A=1 · Google+Other ESPs=2.

**Closed-won (8):** Gurian CPA · Rise Financial Solutions · Rock Solid Financials · Seamless · Core Business Advisors · Han Group (×2, ENGAGE) · 1 unattributed.

**Note on `$21M` vs `$20M`** — the Dark Horse figure is written inconsistently across SMS ($1.5m→$21m) and email ($1.5m/yr→$20m/yr). Pick one and make it uniform.

---

## 6. Segment economics — reported, not recommended

All-time, all channels:

| Segment | Sends | Meetings | Won | Sends/meeting |
|---|---|---|---|---|
| **ENGAGE (event)** | 1,268 | 10 | 2 | **127** |
| **CPA/Accounting** | 19,814 | 28 | 5 | **708** |
| Wealth Mgmt | 5,877 | 2 | 0 | 2,938 |
| Plumbing/HVAC | 33,420 | 7 | 0 | 4,774 |
| **Total** | 60,379 | 48 | 8 | |

Plumbing/HVAC is the largest volume block in the account and has produced **zero closed deals**. `Plumbing Only | Clay` alone: 11,926 sends → 1 positive.

**Plumbing/HVAC is a client mandate — this is stated as cost, not as a recommendation.** At the CPA rate of 708 sends/meeting, the 33,420 sends spent there represent roughly **47 meetings' worth of send capacity**. That is the number to put in front of the client; the call is theirs.

The ENGAGE line is the one to look at hardest: **127 sends/meeting, 5.6× better than cold CPA**, and it produced 2 of the 8 closed-won deals off 1,268 sends. It is the highest-yield thing this account has ever run.

---

## 7. Data limits — what we could not measure

No `ghl-wise-digital` and no `emailbison-wise-digital` connector exists. No locationId, PIT, or Bison key anywhere in the repo or config. Four things are therefore out of reach, and no number above depends on them:

1. **True weekly send counts.** Evergreen has no date filter on sends — July's ~7,069 is *reconstructed* by differencing two month-to-date snapshots, not measured.
2. **Real opt-out rates.** Evergreen excludes hard opt-outs, so every reply rate here is a **floor**. (Go Fish precedent: undercounted 30×.)
3. **Copy for 18 of 30 campaigns** was never reconstructed — a losing variant could be invisible to this analysis.
4. **Number-split check** — the rotation bug that stalled warm Scaletopia leads cannot be run.

Also flagged:
- **Evergreen `/report` per-campaign `positives` and `power_requests` are broken** — `pos=17, pow=7` repeats verbatim across four unrelated campaigns. Do not reuse those fields. Only `sent` and `booked` are trustworthy there; positives in this doc are derived from `/deals` and `/contacts`.
- **Three conflicting Airtable record IDs**: `recQQkheKwE77cFn8` (Evergreen skill doc), `recJjF0rXujlAHwaO` (AM Aaman — the targets used in KPI runs), `rectON75BxGzXttGz` (AM Khizar, different targets: SMS PR 7 / Email PR 5 / 24 monthly meetings). An automated pull can silently grab the wrong one.
- **Target set is internally inconsistent**: SMS PR 3 + Email PR 2 = 5, but Total PR target is 4.
- Evergreen caps `/contacts` threads at 200 of 433, so June's thread-level counts are truncated. July and August are complete.

### To close these gaps
- **GHL:** sub-account locationId + Private Integration Token (Settings → Private Integrations, read-only scopes)
- **EmailBison:** wise-digital workspace API key from `send.scaletopia.io`
- Add a `wise-digital` block to `clients/registry.json` (absent — so is `seedx`), then `python tools/ghl_mine.py --client wise-digital`

---

## 8. Open items

1. **Was ENGAGE a conference booth?** The copy says #705 and it is the best-performing campaign in the account by 5.6×. If another event is on the calendar, that's the highest-leverage item here.
2. **Fresh CPA leads are the binding constraint.** ~7 days of list left. Everything else is second-order until that's solved.
3. **Fix the empty-`{company}` render** before the next batch ships.
4. **~25% of repliers are the wrong person** (wrong number / retired). Chronic, flat, and separate from the August problem — but it's a quarter of the reply volume.
5. **Confirm which Airtable client record is canonical** before the next KPI run.

---

## 9. Correction log — 12 Aug 2026, after the GHL connector was wired

The original autopsy ran Evergreen-only. `ghl-wise-digital` is now live (locationId `zZnyFj8m8JxFUF3XJWJB`, registry entry added), and the mine pulled **83,430 messages / 30,421 contacts / 155 real copy variants**. Three things changed:

1. **"Copy quality ruled out" was wrong.** §4 now carries the reverse finding — the winning opener is switched off and 5 of 8 live batches are burners. Evergreen could not see this.
2. **"Reply handling ruled out" was half wrong.** Response *speed* is fine (17 min median). But 35 engaged people were never answered at all, median 64 days silent — invisible in Evergreen because they never became deals.
3. **Number split, now measurable:** 3,722 threads open from `855-684-0852` and follow up from `844-780-3466` — 15.4% of repliers, 9 warm unbooked leads mid-split. See `output/number-split.csv`.

**Still standing unchanged:** the ENGAGE decomposition of June's 17, the list-exhaustion diagnosis, the segment economics, and the reconciliation in §2.

**One limit closed, one opened.** Real opt-out rates are now visible, so §7's "reply rates are floors" no longer applies to anything sourced from `batches.json`. Still open: no EmailBison connector, so email remains Evergreen-only.

New artifacts: [COPY-SWAP.md](COPY-SWAP.md) · `output/2026-03-01_to_2026-08-12-sms-followup.html` · `output/batches.json` · `output/number-split.csv`

---

## Appendix — method

Follows `clients/scaletopia/JULY-AUTOPSY.md`: cross-foot the outcome three ways → decompose the headline → test each hypothesis against a number that can kill it → rule out the losers explicitly so they don't get re-litigated → size with a counterfactual → state the limits.

Raw pulls in `clients/wise-digital/output/`: `evergreen-{stats,report,replies,deals,copies,contacts,client}.json`. Every figure recomputes from those files.
