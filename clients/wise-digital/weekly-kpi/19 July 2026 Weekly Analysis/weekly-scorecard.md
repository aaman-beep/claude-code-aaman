# Weekly Analysis — Wise Digital Partners — 19 July 2026

### Sunday 19 July 2026 → Saturday 25 July 2026
**Duration:** 7 days (Sun–Sat) · Sending days: Mon 20 → Fri 24 · Timezone `America/Denver`
**Generated:** Monday 27 July 2026 — week is **closed** (full 5 sending days elapsed).
**AM:** Aaman · **Client:** Wise Digital Partners (`recJjF0rXujlAHwaO`) · Client month start 2 Jul 2026 (this is week 3 of the client-month)
**Method:** Full KPI playbook — targets, replies & meetings from **Airtable** (canonical sources). Sends **could not** be pulled — see the blocker below.

**Status icons:** ✅ ≥100% · ⚠️ 70–99% · ❌ <70% of target.

> **⛔ Sends blocker (the real finding).** The playbook pulls sends from Email Bison (Step 1) and GoHighLevel (Step 2). **Wise Digital has neither MCP connector wired** — there is no `emailbison-wise-digital` and no `ghl-wise-digital` server, unlike your other clients. So the true Sun 19–Sat 25 send counts are **not measurable at source.** Airtable is never a valid sends source (its rollups run 3× off, per playbook §5). The only number available is Evergreen's **July month-to-date** aggregate, shown as context only. **Action: get Wise Digital's Bison + GHL connectors added** so sends can be scored like every other client.

---

## Master scorecard

| Client | SMS sends | Email sends | SMS PR | Email PR | Total PR | Meetings |
|--------|-----------|-------------|--------|----------|----------|----------|
| Wise Digital | ⛔ no connector (Jul MTD 5,439) / 1,500 | ⛔ no connector (Jul MTD 6,604) / 2,500 | **3 / 3 ✅**ᵃ | 0 / 2 ❌ᵇ | 3 / 4 ⚠️ᶜ | 0 / 2.0 ❌ᵈ |
| **ATTAINMENT** | — (unmeasurable) | — (unmeasurable) | 100% | 0% | 75% | 0% |
| **HIT RATE** | 1/4 measurable KPIs at ≥100% · 25% (SMS PR only) | | | | | |

ᵃ **SMS PR = 3** (High+Med), all GoHighLevel: 1 High (Power Request) + 2 Medium (Objection Handling + a thread-read Positive). Hits the weekly target of 3. **Downside risk:** the Positive (Majid Shah) is likely sarcasm — if excluded, SMS PR = **2/3 (67% ❌)**. See reconciliation.
ᵇ **Email PR = 0.** All 5 in-window EmailBison contacts were Not Interested (4) / Neutral (1). Genuinely zero positive email replies.
ᶜ **Total PR = 3/4 (75% ⚠️).** Note the target set is internally inconsistent: SMS PR target 3 + Email PR target 2 = 5, but Total PR target = 4. Flagged, not resolved — don't change targets without your say-so (playbook §6 known issue).
ᵈ **Meetings = 0.** Meeting target derived: monthly `KPI - Qualified Showed Meetings` 8 ÷ 4 = **2.0** (stored weekly Qualified Shows = 2, no rounding gap). **0 meeting-stage Deals created in-window** — the 3 deals created this week are all pre-meeting (2× "Maybe" + 1× Positive Reply) and don't count. No High-intent deal override fired.

```
Meetings booked

Hit: N/A

Missed:

- Wise Digital: 0/2.0

Positive replies

Hit: N/A

Missed:

- Wise Digital: 3/4

Email PR

Hit: N/A

Missed:

- Wise Digital: 0/2

SMS PR

Hit:

- Wise Digital: 3/3

Average Emails per PR: N/A (email sends unmeasurable — no connector; 0 email PRs regardless)

Average SMS per PR: N/A (SMS sends unmeasurable — no connector)
```

**Arithmetic (checkable):** SMS PR 1 High + 2 Med = 3 vs 3 → 100%. Email PR 0 vs 2 → 0%. Total PR 3 vs 4 → 75%. Meetings 0 vs 2.0 → 0%. Per-PR averages can't be computed — sends have no source connector.

---

<details>
<summary><b>Wise Digital Partners</b> — 1/4 measurable KPIs hit · SMS PR on target, email dead, 0 meetings, sends unmeasurable (no connector)</summary>

Client month start 2 Jul 2026 · AM Aaman · CPA/accounting cold outbound signed "Matt/Julia, WISE Digital" · the "$600k for Monocacy CPA / show up first when founders search" mechanism.

#### Sends — NOT MEASURABLE this run
| Channel | Weekly target | Source status |
|---|---|---|
| SMS | 1,500 | ⛔ No `ghl-wise-digital` connector. Evergreen July MTD = 5,439 (context, not weekly). |
| Email | 2,500 | ⛔ No `emailbison-wise-digital` connector. Evergreen July MTD = 6,604 (context, not weekly). |

Sends is the only metric the playbook sources from Bison/GHL rather than Airtable, so it's the only metric this connector gap breaks.

#### Positive replies — High + Medium only (Airtable Contacts, Sun 19–Sat 25)
| Channel | Actual | Target | Attainment |
|---|---|---|---|
| GHL (SMS) | 3 | 3 | 100% ✅ |
| Email Bison | 0 | 2 | 0% ❌ |
| **Total** | **3** | **4** | **75% ⚠️** |

#### Meetings booked (Deals pipeline)
| Metric | Value |
|---|---|
| Meeting-stage Deals created in-window | 0 |
| In-window Deals (all pre-meeting) | 3 — "Maybe" ×2 · Positive Reply ×1 |
| Monthly KPI (Qualified Showed Meetings) | 8 |
| Weekly target (÷4) | 2.0 |
| Attainment | 0% ❌ |

#### Intent breakdown (in-window replies)
| Tier | Count | Categories |
|---|---|---|
| High | 1 | Power Request ×1 (SMS) |
| Medium | 2 | Objection Handling ×1 · Positive (thread-read) ×1 — both SMS |
| **Not replies / excluded** | (34) | Not Interested ×27 · Neutral ×3 · Wrong Number ×3 · Retired ×1 |

37 Wise Digital contacts replied in-window; 3 land in High+Med, all SMS. Email produced 5 contacts, all negative.

**Thread evidence (the 3 SMS positives):**
- **High — Henry Aldana (Power Request):** replied *"I'm listening to!"* to the Monocacy-CPA hook; rep offered Thu 1pm / Fri 2pm. Genuine engagement.
- **Medium — Alissa Grimm (Objection Handling):** *"How expensive is this?"* → pricing question, rep quoted ~$1–3k/mo + audit offer. Info-seeking = Medium.
- **Medium (borderline) — Majid Shah (Positive):** *"Guarantee $500 **million** in new revenue… in writing with legal binding contracts and we will sign up!"* → almost certainly sarcasm (impossible ask for a CPA SEO retainer). Tag rule says Positive is never Low, so scored Medium — **but a human read would likely exclude it as a brush-off**, dropping SMS PR to 2/3.

</details>

---

## 🔍 Difference vs the quick Evergreen run (why the first version was misleading)

You asked to see the gap. Same client, same rough week:

| Metric | Evergreen quick-run (`power`/`replies` proxy) | Full playbook (Airtable, tiered) | Why it moved |
|---|---|---|---|
| **Positive replies** | **1 / 4 ❌ (25%)** | **3 / 4 ⚠️ (75%)**, and **SMS PR 3/3 ✅** | Evergreen's `power` field counts only *Power Requests* (1). It **missed the Objection Handling (Medium) and the Positive** — both real High+Med replies. The client looked like a near-total miss but actually **hit its SMS PR target.** |
| **Channel split** | Blended; no per-channel target | SMS 3/3 ✅ vs Email 0/2 ❌ | Evergreen had no SMS-vs-email PR targets. Airtable does — and they tell opposite stories (SMS healthy, email dead). |
| **Send targets** | None in Evergreen | SMS 1,500 · Email 2,500 (Airtable) | Evergreen carries no send-volume target at all. |
| **Meetings** | 0 (weekly booked) | 0 (0 meeting-stage deals) | Agree — but the playbook shows *why* (3 pre-meeting deals, no override). |
| **Window** | Mon 20 → Sun 26 (Evergreen Mon-start) | Sun 19 → Sat 25 (canonical) | Evergreen can't do Sun–Sat. |

**Bottom line:** the Evergreen quick-run understated this client badly — it read `power`=1 as "positive replies" and called a 25% miss, when a proper High+Med thread-read shows **SMS PR hitting target (3/3)** and total PR at 75%. Evergreen is fine for orientation and booked-meeting counts, but **not** for scoring positive replies — the tiering and channel split only exist in Airtable.

---

## Flags & data-quality notes

1. **⛔ No Bison/GHL connector for Wise Digital** — sends unmeasurable at source. This is the single biggest gap; wiring the two connectors makes Wise Digital fully scorable like the rest of the roster.
2. **Two "Wise Digital Partners" client records exist** in the Clients table — one AM **Aaman** (`recJjF0rXujlAHwaO`, month start 2 Jul, used here), one AM **Khizar** (`rectON75BxGzXttGz`, month start 23 Jul, different targets: SMS PR 7 / Email PR 5 / monthly meetings 24). All in-window contacts and deals link to Aaman's record. Worth confirming the Khizar duplicate is intentional.
3. **Target set internally inconsistent:** SMS PR 3 + Email PR 2 = 5 ≠ Total PR 4. Reported as-is; flagged per playbook §6.
4. **Majid Shah "Positive" is likely sarcasm** — scored Medium under the "Positive never Low" rule, but flagged. Excluding it → SMS PR 2/3 (67% ❌), Total PR 2/4 (50% ❌).
5. **Email is genuinely at zero** for positives — 5 in-window email contacts, all Not Interested/Neutral. Clean, not a data gap.
6. **Meetings clock:** 0 meeting-stage deals *created* in-window. A meeting booked later for a lead who replied this week would count toward a future week's meetings, not this one.

---

## Reconciliation

- **Replies pull:** 37 in-window Wise Digital contacts (Airtable Contacts, `Date created` Sun 19 00:00 → Sat 25 23:59 America/Denver). High+Med = 3 (all GHL/SMS); email = 5, all negative; 34 not-replies excluded. 3 + 34 = 37 ✅
- **Thread-read tiers:** Power Request → High (call offered, "I'm listening"). Objection Handling → Medium (pricing ask). Positive → Medium, flagged sarcasm (would exclude on human read).
- **Meetings:** 0 meeting-stage Deals; 3 in-window Deals all pre-meeting (2 "Maybe" + 1 Positive Reply). Deal-stage High override evaluated, none applied.
- **Sends:** not reconciled — no source connector; Evergreen July-MTD figures are month aggregates, not the week.
