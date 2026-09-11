---
name: client-crm
description: "Query the Scaletopia client CRM dashboard (meetings booked, shows, funnel, pipeline, revenue/MRR, target pacing, outreach volume) via its read-only insights API. Use when asked about client performance, appointments booked, show rates, close rates, revenue or MRR, pipeline health, which clients are under target, funnel drop-off, or any question about leads and deals across clients. Triggers on 'how many meetings did {client} book', 'pull {client}'s numbers', 'show rate', 'close rate', 'what's our pipeline', 'who is behind target', 'revenue this month', 'funnel for {client}'. This is the CRM dashboard — it is NOT the Airtable 'Master Inbox & CRM' base and NOT Evergreen. Read-only; never mutates data."
---

# Client CRM — insights API

Read-only access to the Scaletopia clients-kpis dashboard. Every endpoint is a GET,
returns JSON, and never mutates data — safe to call freely.

**This is the system of record for booked / showed / next stage / proposal / won.**
Do not answer those questions from Airtable or Evergreen — see [Not this system](#not-this-system).

## Access

Base URL: `https://clients.scaletopia.online/api/insights`

The token is a live credential and **must not be committed** — this repo has a public
remote. It lives in `.env` (gitignored) as `INSIGHTS_TOKEN`. Load it, don't inline it:

```bash
set -a; . ./.env; set +a
curl -s -H "Authorization: Bearer $INSIGHTS_TOKEN" \
  "https://clients.scaletopia.online/api/insights/clients?client=big-leap"
```

`?token=<token>` also works if setting a header is awkward.

**`GET /api/insights` self-documents** every endpoint, filter and enum. Call it if you're
unsure of a field name rather than guessing.

## Endpoints

| Endpoint | Use it for |
|---|---|
| `/api/insights` | Index — endpoints, enums, caveats. Start here if unsure. |
| `/api/insights/clients` | One row per client: booked, shows, won, revenue, target pacing. **Best overview.** |
| `/api/insights/kpis` | Headline metrics. `groupBy=month\|client\|status` |
| `/api/insights/leads` | Individual lead rows. `status=`, `category=`, `q=` search, `fields=slim`, `limit=` (default 200, max 2000), `offset=` |
| `/api/insights/funnel` | Stage-by-stage conversion + drop-off. `groupBy=client` |
| `/api/insights/revenue` | Won deals, totals, averages. `groupBy=month\|client` |
| `/api/insights/marketing` | Email/SMS sent and positive replies. `granularity=month\|day` |

## Shared filters

Every endpoint accepts:

- `client=` — slug, name or uuid; comma-separated for several. Omit for all clients.

> **Slug trap — verify the slug first.** An unrecognised `client=` does **not** error. The
> API returns `clientIds: []` and a full response of zeros, which reads exactly like a real
> client with no activity. Always check `filters.clientIds` is non-empty before believing a
> zero. CRM slugs are **not** the same as `clients/registry.json` slugs — e.g. registry
> `gofish` is CRM `go-fish-digital`, `strike-tax` is `strike-tax-advisory`, `wise-digital`
> is `wise-digital-partners`. Get the real list with:
>
> ```bash
> curl -s -H "Authorization: Bearer $INSIGHTS_TOKEN" \
>   "https://clients.scaletopia.online/api/insights/clients" \
>   | python3 -c "import sys,json;[print(c['slug']) for c in json.load(sys.stdin)['clients']]"
> ```
- `from=` / `to=` — ISO dates. `from` inclusive, `to` exclusive.
- `dateField=` — which date the range filters on: `date_of_meeting` (default),
  `created_date`, or `call_scheduled_for`.

```bash
# One client, one quarter, month by month
".../api/insights/kpis?client=chamber-media&from=2026-05-01&to=2026-08-01&groupBy=month"

# Every won deal this year, biggest MRR first
".../api/insights/revenue?from=2026-01-01&groupBy=client"

# Where is the funnel leaking, per client?
".../api/insights/funnel?groupBy=client"
```

## How the metrics are defined

Read this before interpreting numbers — several statuses behave unintuitively.

- `meetingsBooked` = every lead **EXCEPT** status `lost`. A plain "Lost" is treated as
  never having become a real meeting.
- `post_meeting_lost` counts as booked **and** as a show (the call happened, the deal
  died afterwards).
- `rescheduled` counts as booked but **not** as a show (hasn't happened yet).
- `shows` = `show`, `not closed`, `next stage`, `proposal sent`, `verbal agreement`,
  `won`, `post_meeting_lost`.
- Revenue is only counted on status `won` (`upfront_collected`, `mrr_collected`).
- The status `not closed` is labelled **"Unqualified"** in the UI.
- `closingRate` = won ÷ proposalsSent (**not** ÷ booked). `showRate` = shows ÷ booked.
- `targetAttainment` on `/clients` = **all-time** booked ÷ **monthly** target. It is only
  meaningful when the date range is a single month. Unfiltered it inflates every
  multi-month client (Big Leap showed 167% while actually booking 2 against a target of
  9 that month). **To judge pacing, always pass `from`/`to` for one month**, or bucket
  `/leads` by `date_of_meeting[:7]` and compare each month to `monthlyTarget` yourself.

### `monthlyTarget` is a SHOWS target, not a booked target

Verified 2026-09-01 across all three systems. One Airtable field — Clients table,
**`KPI - Qualified Showed Meetings`** (`fldc6F26Y8A3CojbF`) — feeds both downstream
dashboards, and **both rename it to a booked target**:

- CRM `monthlyTarget` = that field verbatim for 9 of 13 active clients (Growth Lab 10,
  Redo 12, Big Leap 9, Go Fish 9, Kynship 8, Wise 8, Seedx 8, Acceler8 10, Leadgenix 12).
- Evergreen `kpi.targets.monthlyBooked` = the same field (Scaletopia: Airtable 38 →
  Evergreen 38). Evergreen's weekly figures are just monthly ÷ 4.

No show-rate haircut is applied anywhere — it is the same integer, relabelled.

**So comparing `meetingsBooked` to `monthlyTarget` measures booked against a shows bar
and overstates attainment.** Judge pacing on **shows vs target**. To convert to a booked
bar, divide by the client's actual `showRate` (a 9-show target at 73% needs ~12 booked).

**CRM has drifted from Airtable** for 4 clients — Scaletopia 10 vs 38, Strike Tax 15 vs
24, Chamber Media 20 vs 24, Taktical 8 vs 4. Airtable is the source of truth; re-check it
before quoting a target for these.

**Statuses:** `meeting booked`, `rescheduled`, `show`, `no show`, `not closed`,
`next stage`, `proposal sent`, `verbal agreement`, `won`, `lost`, `post_meeting_lost`,
`future`.

**Categories:** `meeting` (sales calls) and `pr` (positive replies). KPI endpoints count
`meeting` only; use `/leads?category=pr` for outreach replies.

**Sources:** `email`, `sms`.

## Answering questions well

1. Start with `/clients` to see the landscape, then drill into one client.
2. Quote the concrete numbers and name the clients — never generalise vaguely.
3. When something looks wrong, pull the underlying rows with `/leads` and check before
   concluding. Counts and raw rows should agree.
4. `targetAttainment` on `/clients` is booked ÷ monthly target — the quickest read on
   who is behind.
5. Data flows from Airtable, so a very recent change may not have synced yet. If a
   figure looks stale, say so rather than treating it as final.

## Not this system

Three different things are called "CRM" around here. Getting them confused wastes real
time — it has already happened once.

| System | What it is | Use it for |
|---|---|---|
| **This insights API** | The clients-kpis dashboard | Booked / showed / next stage / proposal / won, revenue, target pacing. **The funnel numbers.** |
| Airtable `Master Inbox & CRM` (`appgezzL6Uqr0xgBa`) | Reply/inbox management, hand-marked stages, per-deal Notes | Reading a specific deal's notes or a rep's commentary. **Its stage column is current-state only — never build a funnel from it, and its counts will not match this API.** |
| Evergreen | Copy, pains, proof, campaign stats | Copywriting evidence. See `evergreen-research` (evidence) / `evergreen-stats` (numbers). |

If the question is "how many meetings / what's the show rate / how much revenue" —
it's this API, first call, no exploration needed.
