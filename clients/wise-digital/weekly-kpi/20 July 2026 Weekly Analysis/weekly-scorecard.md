# Weekly Analysis — Wise Digital Partners — week of 20 July 2026

### Monday 20 July 2026 → Sunday 26 July 2026  (Evergreen "last week", Mon-start)
**Duration:** 7 days · Sending days: Mon 20 → Fri 24 · Timezone `America/Denver`
**Generated:** Monday 27 July 2026 — week is **closed**.
**AM:** Aaman · **Client:** Wise Digital Partners (`wise_digital`) · Retainer $4,000 · Onboarded 2 Mar 2026
**Source:** Evergreen-native run (no GHL/Bison/Airtable pull). Wise Digital has **no GHL connector**, so this is the only route to its numbers.

**Status icons:** ✅ ≥100% · ⚠️ 70–99% · ❌ <70% of target.

> **Read the window carefully.** Evergreen buckets weeks **Monday-start**, so this is Mon 20 → Sun 26 Jul, ~1 day offset from the playbook's canonical Sun–Sat. Evergreen has **no last-week sends** (its `This Week` counter is empty and there's no date filter), and **no send-volume target**, so **sends are shown as July month-to-date context, not a scored weekly KPI.** The two scored KPIs — positive replies and booked — come from the `/replies` weekly series.

---

## Master scorecard

| Client | SMS sends (Jul MTD)ᵃ | Email sends (Jul MTD)ᵃ | Positive replies (wk)ᵇ | Booked (wk) |
|--------|-----------|-------------|-------------|----------|
| Wise Digital | 5,439 (MTD, unscored) | 6,604 (MTD, unscored) | 1 / 4 ❌ | 0 / 2 ❌ |
| **ATTAINMENT** | — | — | 25% | 0% |
| **HIT RATE** | 0/2 scored KPIs · 0% | | | |

ᵃ **Sends = July month-to-date, NOT the week.** Evergreen can't isolate last week's sends and carries no send target, so these are context only. All-time volume: 33,652 SMS / 38,455 email.
ᵇ **Positive replies (wk) = 1** uses Evergreen's `power` (high-intent requests) count for week_start 2026-07-20 as the High-intent proxy. Total replies that week = **3** (0 marked Not Interested). This is Evergreen's granularity, not a hand-tiered High+Med thread read — a human audit of the 3 threads could move it to 2–3.

```
Booked

Hit: N/A

Missed:

- Wise Digital: 0/2

Positive replies

Hit: N/A

Missed:

- Wise Digital: 1/4
```

**Arithmetic (checkable):** Booked wk = `/replies weekly[week_start=2026-07-20].booked` = 0 vs target 2 → 0%. Positive replies wk = `.power` = 1 vs target 4 → 25%.

---

<details>
<summary><b>Wise Digital Partners</b> — 0/2 scored KPIs hit · quiet week (3 replies, 0 bookings); pipeline lumpy — 6 bookings the week of Jul 6</summary>

Client month start 2 Mar 2026 · AM Aaman · CPA / wealth-mgmt / HVAC-plumbing home-services outbound · **No GHL connector — Evergreen-only.**

#### Sends — July month-to-date (no weekly figure available, no target)
| Channel | Jul MTD | All-time | Active campaigns now | Leads remaining |
|---|---|---|---|---|
| SMS | 5,439 | 33,652 | 1 | 1,729 |
| Email | 6,604 | 38,455 | 1 | 2,641 |
| **Total** | **12,043** | **72,107** | 2 | — |

#### Positive replies & booked — last week (week_start 2026-07-20)
| Metric | Actual | Target | Attainment |
|---|---|---|---|
| Positive replies (`power` proxy) | 1 | 4 (`weeklyPositives`) | 25% ❌ |
| Booked | 0 | 2 (`weeklyBooked`) | 0% ❌ |
| Total replies (all, context) | 3 | — | — |

**4-week trend** (Evergreen `/replies weekly`, Mon-start): Jul 20 → 3 replies / 1 power / **0 booked** · Jul 13 → 5 / 2 / **1** · Jul 6 → 16 / 1 / **6** · Jun 29 → 4 / 2 / **0**. Bookings are lumpy — the Jul 6 week carried the month; last two weeks are quiet.

#### Intent breakdown (recent window — broader than one week, context only)
| Category | n |
|---|---|
| Power Request | 6 |
| More Info Request | 4 |
| Referral Request | 3 |
| Email Me Request | 2 |
| Custom Response | 2 |
| Objection Handling | 1 |
| Neutral | 1 |
| (uncategorized) | 9 |

#### Live copy running now — Evergreen inventory (fast; no body text)
`activeCampaigns` = 1 SMS + 1 email. Campaigns currently **PROCESSING** (actively sending), ranked by power_rate:

| Campaign | Channel | Status | Sent | Pos. replies | Power req. | Booked | Power rate |
|---|---|---|---|---|---|---|---|
| Accounting/CPA — Google + Other ESPs V2 | email | PROCESSING | 1,673 | 2 | 1 | 1 | 0.060% |
| Accounting/CPA — T3 (Fahad's copy) | sms | PROCESSING | 1,686 | 7 | 1 | 2 | 0.059% |
| Accounting/CPA — Outlook | email | PROCESSING | 2,884 | — | — | — | — |
| Plumbing Only — Clay / google | email | PROCESSING | 4,252 | — | — | — | — |

Paused-but-live (can resume): Accounting/CPA V2 (email+sms), Accounting/CPA Google+Other ESPs (email). Everything else is COMPLETED or CANCELLED.

> **Copy bodies not available from Evergreen** (the `copies` search isn't client-scoped and campaign records carry no message text). For actual sent SMS/email copy per variant you'd need the source connector — and Wise Digital has no GHL connector wired, so SMS bodies specifically can't be mined without adding one.

</details>

---

## Flags & data-quality notes

1. **Mon-start window.** Evergreen's weekly series starts weeks on Monday (Jul 20 → Sun 26), ~1 day off the playbook's Sun–Sat. Consistent across clients; just not identical to the canonical window.
2. **Sends are July MTD, not weekly, and unscored.** Evergreen's `This Week` bucket is empty and it has no date filter or send target. Real weekly sends would need a GHL/Bison pull.
3. **Positives = `power` proxy.** Last-week High-intent is taken as Evergreen's `power` count (1); total replies were 3, none Not Interested. Not a thread-level High+Med audit — flagged rather than presented as exact.
4. **No GHL connector for Wise Digital.** SMS copy bodies and true send-event counts can't be mined; Evergreen aggregates are the ceiling of fidelity here.
5. **Lumpy bookings.** 0 booked last week reads as ❌, but the client booked 6 the week of Jul 6 and 1 the week of Jul 13 — pipeline is live, last week was just quiet. July MTD booked = 4 vs monthly target 8.
6. **Multiple PROCESSING campaigns vs `activeCampaigns`=1/channel.** Evergreen's campaign `notes` mark 4 as PROCESSING while the summary counts 1 active per channel — reported both; the summary likely dedupes to the primary live variant per channel.
