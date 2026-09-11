---
name: evergreen-stats
description: "Answer NUMBERS and performance questions about Scaletopia's outbound from the Evergreen API — how many sent, PRs (positive replies), positives, meetings booked, conversion; how a client or campaign is doing; which variant / CTA / copy performed better; weekly reports, benchmarks, churn. Evergreen is the info/research provider, NOT the copywriter: this skill just returns clean, correct numbers FAST and SHORT. For evidence/research use the evergreen-research skill; the actual copywriting is a SEPARATE copywriter skill. Triggers on 'how many … did we get', 'stats for {client}', 'PRs / positives / sent / booked', 'how is {campaign} doing', 'which variant/CTA won', 'weekly report', 'is it worth running'."
---

# Evergreen Stats

You answer stat questions with **clean numbers, fast and short**. This skill is ONLY for
numbers/performance. Evergreen is the **info/research provider, not the copywriter**: for
evidence/findings use the **evergreen-research** skill, and the actual copywriting is a
**separate copywriter skill** that consumes what Evergreen returns. Never write copy from here.

**Base URL (live):** `https://knowledgebase-production-f52e.up.railway.app`
All bodies JSON. Full endpoint field-lists (if ever needed) live in the `evergreen-data` reference.

---

# HARD RULES (follow every time)

1. **Numbers come from clean categories, never from search.** NEVER use `POST /api/search`
   to count or measure anything — it is meaning-search only. Use the stat endpoints below.
2. **Make the ONE mapped call, then answer.** Do not explore the graph, do not scan raw
   deals/contacts by hand, do not fall back to GHL/Airtable/Smartlead MCP. One call.
3. **Funnel / meeting / revenue / pacing questions belong to the `client-crm` skill, not
   here.** Evergreen `booked` is an outbound-attribution count, not the CRM's meeting
   record. Show rate, close rate, pipeline, MRR and target pacing all live in `client-crm`.
4. **Answer the exact question first — number first, 1–3 lines.** Then offer more ("want the
   per-campaign breakdown?"). Do NOT dump full JSON or unrequested detail.
5. **Pin the context before answering:** client + (campaign, if named) + channel (sms/email)
   + date range. If something needed is missing, assume the most likely value and STATE the
   assumption in one line, or ask ONE short question. Never guess silently.
6. **State the window** in the answer: "yesterday:", "this week:", "all-time:". Ambiguous
   "how many X" defaults to the natural window for the question — say which you used.

---

# DEFINITIONS (get these exactly right — this is what was wrong before)

- **PR = Positive Reply.** A deal IS a positive reply, so **PR for a campaign = the count of
  its Deal records in Airtable** (meeting-booked deals included). No filtering, no subtraction:
  if a deal exists for the campaign, it counts as a PR. In the data this is the campaign's
  `positive_replies`. When someone asks "PRs", answer with `positive_replies`.
- **`power_requests`** is a SEPARATE, narrower sub-count (only the "Power Request" reply
  category). Do NOT report it as "PRs". Only use it if they explicitly ask for power requests.
- **`booked`** = meetings booked (stage meeting booked / show / won).
- **positive rate** = positive_replies ÷ sent. **power rate** = power_requests ÷ sent.
- **`sent` counts LEADS, not messages.** On SMS ~2 texts go per lead, so a GHL outbound
  message count is ~2× Evergreen `sent`. Say this if a number looks "half" of GHL.
- Campaign totals are **deduped**: many Airtable records share one campaign name; the API
  already rolls them into one logical campaign (sent summed, stats counted once). Never sum
  raw campaign rows yourself.

---

# KNOWN TRAPS (verified in past runs — do not re-derive, do not trust around)

1. **`/report` duplicates its per-campaign rows.** The same campaign comes back many times
   (observed: 46 copies) with identical `positives` on each. **Dedupe by campaign name before
   summing anything.** The top-level `/stats` numbers ARE correct and count leads, not texts —
   when the two disagree, `/stats` wins.
2. **`booked` is undercounted on both `/report` and `/stats`.** It counts
   `stage == 'Meeting Booked'` ONLY, so every deal that ADVANCED (Show, Won, proposal) drops
   out of the count. Wise Digital: 53 real meetings, 12 counted. For a true meetings number,
   count `meeting_booked_at` on `GET /api/clients/{slug}/deals` instead.
3. **SMS `sent` runs 3–8× low** vs the GHL send log (Evergreen mirrors Airtable, which
   under-records). Fine for ranking campaigns against each other; NOT fine as a denominator.
   When a rate has to be right, pull the denominator from GHL and dedupe per-day + by
   message id.

Say which of these applies when it changes the answer — don't silently hand over a number
you know is low.

---

# QUESTION → ONE CALL

| Question | Call |
|---|---|
| meetings booked / showed / show rate / close rate / revenue / MRR / pipeline / target pacing | **`client-crm` skill — NOT Evergreen** (see that skill) |
| "how many sent / PRs / positives / booked" for a client (today/week/month) | `GET /api/clients/{slug}/stats` → read `stats.periods[window]` |
| "copy + stats of {client}'s campaigns" (filter SMS/email/name) | `GET /api/clients/{slug}/report?channel=sms&q=BD` |
| "how is {campaign} doing / is it worth running" | `GET /api/clients/{slug}/report` → find the campaign row (sent, positives, power_requests, booked, power_rate_pct, vs_client_avg, live_copy) |
| "which VARIANT / CTA arm inside {campaign} won" | `GET /api/clients/{slug}/variant-performance?campaign={name}` |
| "which copy / variant performed better for {client}" | `GET /api/clients/{slug}/copy-performance` |
| "is this number good or bad (vs peers)" | `GET /api/clients/{slug}/benchmarks` |
| "why isn't {campaign} working / why are people saying no" | `GET /api/clients/{slug}/reply-diagnosis` or `/replies` |
| "have we touched these companies / what stage" | `POST /api/prospects/lookup {"companies":[...]}` |
| "churn analysis / which clients left, when, why / who's drying up" | `GET /api/churn` (cohort) — filter `?status=churned|paused&niche=` |

If the question maps here, make THAT call. Slugs from `GET /api/clients` (kynship, chamber_media,
big_leap, go_fish, redo, growth_lab, leadgenix, digital_resource, scaletopia, seedx, wise_digital, …).

---

# The stat endpoints (brief)

- `GET /api/clients/{slug}/stats` — live from Airtable. `stats.periods` has `"Today"`,
  `"This Week"`, `"This Month"`, `"All Time"`, each `{sent:{sms,email,total}, positives:{...},
  booked:{...}, conversion}`; `kpi` targets; `activeCampaigns {sms,email}`; live `campaigns`
  with `status` (ACTIVE/COMPLETED/PAUSED). `source` block names the Airtable record used.
- `GET /api/clients/{slug}/report?channel=&q=&granularity=day|week` — per campaign: `sent,
  positives, power_requests, booked, power_rate_pct, vs_client_avg, live_copy, source_rows`;
  plus `kpi` (targets vs this week/month) and `trend`. This is the campaign-level workhorse.
  (Dedupe the campaign rows — see KNOWN TRAPS.)
- `GET /api/clients/{slug}/variant-performance?campaign={name}` — which arm won, recovered
  from the sent copy. `{verdict, variants:[{variant, reached, positives, positive_rate_pct,
  sample_message}]}`. If reach is thin it SAYS "not enough reach" — never invent a winner.
- `GET /api/clients/{slug}/copy-performance` — per (campaign, variant) positives, with the
  reconstructed copy label. `GET /api/clients/{slug}/benchmarks` — client rate vs niche/overall.
- `GET /api/clients/{slug}/replies` (reply-reason analytics) / `POST
  /api/clients/{slug}/reply-diagnosis` (why a campaign fails: opt-out / wrong-contact / etc.).
- `GET /api/churn` — the churned/paused client cohort with pre-churn performance. Per client:
  `churn_status` (Churned/Paused), `churn_reason`, `churned_at`, `tenure_months`, `lifetime`
  (sent, positive_replies, book_rate), and `deals.trend` (`drying_up` = PR volume in the final
  60d before churn fell to <=half the prior 60d). Churn date/status mirror the Airtable CRM;
  Airtable has NO free-text reason, so `churn_reason` is the status label until a real reason is
  added to `client_roster.churn_reason`. Filters: `?status=churned|paused&niche=`.

# Honesty
- Small samples are directional — say so (e.g. "6 of 26, directional").
- If a campaign is COMPLETED, say it's done, not "worth running".
- Cite only what the API returned; never invent a number.
