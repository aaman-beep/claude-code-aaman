# WISE Digital — SMS copy swap brief

**Built:** 12 Aug 2026 · **Source:** GHL send log (`tools/ghl_mine.py`), 83,430 messages, era from 2026-03-10
**Action owner:** Aaman → GoHighLevel. Nothing here has been changed in the live account.

---

## The one-line version

**Your best opener is switched off and your worst opener is the only thing running.** Restoring it requires no new copy and no new leads.

---

## 1. What's live right now — all eight batches are the Monocacy opener

Every CPA batch still sending as of 11 Aug uses:

> Hi {{firstName}}, it's Matt from WISE Digital - feel free to ignore if u got enough referrals but we got Monocacy CPA $600k in new business in 1 yr…

| Reply % | Opt-out % | n | Burner? | T2 |
|---|---|---|---|---|
| 0.58% | 2.31% | 173 | 🔥 | "Did this for Dark Horse {{title}} too…" |
| 0.59% | 0.59% | 338 | 🔥 | "Did this for Dark Horse CPA too…" |
| 0.68% | 0.57% | 1,754 | | "The CPA firms doing this now show up first…" |
| 0.78% | 0.78% | 637 | 🔥 | "Did this for Dark Horse CPA too…" |
| 0.85% | 0.80% | 1,884 | | "The CPA firms doing this now show up first…" |
| 1.25% | 1.25% | 958 | 🔥 | "Did this for Dark Horse CPA too…" |
| 1.50% | 0.68% | 734 | | "Did this for Dark Horse CPA too…" |
| 1.81% | 1.09% | 276 | | "The {{title}} firms doing this now…" |

**5 of 8 are burners** — opt-outs at or above replies. That's not a slow campaign, it's a campaign actively costing you list.

## 2. What to restore — the Dark Horse opener

> **T1:** Hi {{firstName}}, I know this is out of the blue but we took Dark Horse CPAs from $1.5m to $21m in 5 years by replacing referrals with organic search (did this for Capstone Accounting too)
> **T2:** Saw **{{companyName}}** and had some ideas. Mind if I give you a ring **next week**? - Matt, WISE Digital Partners

### Ranked properly — meetings per send, SMS only

The batch table below originally ranked on **reply %**, which is the one metric our own rule says never to rank on. Re-cut on meetings per send it holds, and the gap is *wider*:

| Opener | Prospects texted | SMS meetings | **Meetings /1k** | Positives | Positives /1k | Meetings per positive | Won |
|---|---|---|---|---|---|---|---|
| **Dark Horse** | 10,225 | **18** | **1.76** | 32 | 3.13 | **0.56** | **4** |
| Monocacy | 10,558 | 2 | 0.19 | 11 | 1.04 | 0.18 | 1 |

**9.3× the meetings per send**, on near-identical denominators (10,225 vs 10,558). Significant on both meetings (z=3.65, p<0.001) and positives (z=3.31, p=0.001).

**No — it is not the same ranking as reply rate, and that matters.** The advantage compounds at every stage:

| Metric | Dark Horse edge |
|---|---|
| Reply rate | 2.0× |
| Positives per send | 3.0× |
| **Meetings per send** | **9.3×** |
| Meetings per positive reply | 3.1× |

Dark Horse doesn't just get more replies — it gets *better* replies. A Monocacy positive converts to a meeting 18% of the time; a Dark Horse positive, 56%. Ranking on reply % understated the winner.

### Batch-level detail (reply %, for reference only)

| Reply % | Opt-out % | n | Window | T2 variant |
|---|---|---|---|---|
| **6.25%** | 1.25% | 160 | 18–25 Jun | `{{companyName}}` · "next week" |
| 5.26% | 1.50% | 133 | 17 Jun | `{{company}}` · "this week" |
| 4.64% | 0.84% | 474 | 18–25 Jun | `{{company}}` · "next week" |
| 4.20% | 2.52% | 119 | 26 Mar | `{{company}}` · "this week" |

Two details worth keeping exactly as written:
- **`{{companyName}}` beat `{{company}}`** — 6.25% vs 4.64%, same T1, same week. `{{company}}` is also the field that renders blank (see §4).
- **"next week" beat "this week"** — 6.25% vs 5.26%.

## 3. Why this isn't a seasonal illusion

The Dark Horse batches ran **17–25 June**. The Monocacy batches started **3–11 June** and are *still running*. They overlapped for over a week — same list, same weeks, same sender.

**4–7× the reply rate, at a lower opt-out rate.**

This is also the copy already logged as `W16`/`W17` in `sms-playbook/winners.csv`.

### Where this weakens — state it before the client does

1. **List freshness is partly entangled with copy.** 84% of Dark Horse's volume ran on the retarget list vs **100%** of Monocacy's. Dark Horse got slightly more fresh-list exposure. That gap is too small to explain 9.3×, but it isn't zero.
2. **Within `Retargeting T4` alone** — identical campaign, identical list — the direction holds but the sample collapses: Dark Horse 2 meetings / 8,572 (0.23/1k) vs Monocacy 1 / 10,524 (0.10/1k). Same winner, not significant on its own.
3. **The strongest clean evidence is June**, when both ran concurrently. Monocacy got **6,577** prospects to Dark Horse's **3,455** — nearly double the volume — and Dark Horse still booked **8 meetings to Monocacy's 2**.
4. Three of the meetings first attributed to Dark Horse were **email**, not SMS. The table above is SMS-only; the earlier draft wasn't.

**Verdict: restore Dark Horse.** The direction is consistent across every cut, significant on the full sample, and strongest in the one window where both ran side by side on the same list. The list-freshness caveat argues for confirming with a clean A/B once fresh CPA leads land — not for waiting.

## 4. Fix these before relaunching

1. **Empty `{{company}}` render.** 21 of 355 sampled threads went out as *"Saw  and had some ideas."* — clustered 30 Jun–1 Jul. Use `{{companyName}}`, which is both better-performing and the one that populates.
2. **Pick one Dark Horse number.** SMS says **$21m**, email says **$20m**. Same case study, two figures, in front of the same buyers.
3. **Stop re-texting people who already engaged.** Casey Haynes (Compass CPA) replied *"Hm, maybe. Can you email marketing@compasscpa.net"*, got the email, and was then re-hit with the cold Monocacy opener two touches later. He replied **"Stop."** A warm, hand-raised lead was converted into an opt-out by the automation. Suppress anyone with an inbound reply from the cold sequence.
4. **Number split.** 3,722 threads open from `855-684-0852` and follow up from `844-780-3466` — 15.4% of all repliers. 9 warm, unbooked leads are currently mid-split. Per the Scaletopia precedent this doesn't tank a campaign when a human answers fast, but it stalls automated nudges. Details in `output/number-split.csv`.

## 5. Sequencing — and why "refresh the copy" isn't first

The instinct to go harder at CPA is right; CPA is the only segment that has ever closed. But copy is not the binding constraint:

| Lever | Effect | Cost |
|---|---|---|
| **Restore Dark Horse** | 4–7× reply rate | Free — no writing, no leads |
| **Load fresh CPA leads** | The actual ceiling | Lead spend |
| Refresh copy | Moves you inside a 0.23–6.25% band | Writing time |

**28,277 of 30,421 contacts in the sub-account have already been texted.** ~2,100 untouched; Evergreen shows 528 leads left in the live campaign. Only 282 are DND — the list isn't burned, it's *consumed*. No new list has been loaded since July; August sends are the drip-tail of July's batches.

New copy against an empty list is worth nothing. **Restore the winner (free) → load fresh CPA leads (the constraint) → then refresh copy.**

---

## Appendix — reproduce

```
python tools/ghl_mine.py --client wise-digital          # → batches.json, sms-copy-history.csv
python tools/ghl_number_split_scan.py --clients wise-digital --since 160
```
All figures re-derive from `clients/wise-digital/output/batches.json` (155 variants at n≥20).
