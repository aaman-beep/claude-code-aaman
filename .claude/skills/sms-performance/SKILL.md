---
name: sms-performance
description: Pulls what a client's cold SMS ACTUALLY did — every copy variant ever sent, with reply and opt-out rates — by mining the GoHighLevel send log. Use whenever someone asks what copy a client has run or tested, which SMS is winning or losing, what the reply/opt-out rate is, "show me the copy history for [client]", "what's working for [client]", "which variant should we scale", "has this angle been tried", or wants evidence before drafting new copy. Also use to promote proven copy into sms-playbook/winners.csv (as a strawman for the strategist). Runs on any client in clients/registry.json. Does NOT write copy (that's sms-draft), does NOT send, does NOT pick the winner.
---

# sms-performance — what the copy actually did

Every other skill in this repo reasons about copy that *should* work. This one is the
only source of what **did** work: the real texts that went out, and what came back.

## Evergreen — the shared knowledge API (check it first)

Scaletopia's knowledge lives in **Evergreen**, the one API every skill in this playbook shares.
It is the research/data **provider** — it serves evidence and numbers; it does **not** write copy
(that's this skill's job, and your proven copy stays yours). GHL's send log stays the deepest mine of raw copy history — keep using it. But for the aggregates, the RECONSTRUCTED live copy per campaign, and correct period numbers, Evergreen is faster and already fixed the counting bugs (period sent from the ops daily feed; booked from `meeting_booked_at`).

- **Base URL:** `https://knowledgebase-production-f52e.up.railway.app`
- **Auth (required):** send header `Authorization: Bearer $EVERGREEN_API_KEY` on every call — the key
  lives in this playbook's `.env` (gitignored). No header -> **401**.
- **Discover the API yourself:** `GET /api/docs` is the live index of every endpoint with its params
  and descriptions; `GET /api/openapi` is the full machine schema. Unsure which endpoint/field exists?
  Read `/api/docs` first — never guess a path or bulk-pull GHL/Airtable for what Evergreen already has.
- **Focused entry points:** `evergreen-research` (pull/save findings) · `evergreen-stats` (numbers) ·
  `evergreen-data` (full field-level catalogue).

**What THIS skill pulls from Evergreen:**
- `GET /api/clients/{slug}/report?channel=sms` — per campaign `sent, positives, power_requests,
  booked, power_rate_pct`, **reconstructed `live_copy`**, and `vs_client_avg`.
- `GET /api/clients/{slug}/variant-performance?campaign={name}` — which **arm / CTA won** (recovered
  from the sent copy); honors `confidence` (won't invent a winner on thin reach).
- `GET /api/clients/{slug}/period?window=this_week&channel=sms` (one client) and
  `GET /api/period?window=last_week&channel=sms` (agency-wide) — correct **period sent** + PR-per-SMS.
  Never derive a window by arithmetic.
- `GET /api/clients/{slug}/monthly` — month-by-month trend + `peaks`.
- Promoting proven copy into `sms-playbook/winners.csv` stays your call; Evergreen stores copy as
  `draft` and lets real metrics decide winner/loser.

## The one thing you must understand first

**GoHighLevel does not store copy history.** Copy is edited **in place** inside a workflow,
so the workflow holds only its *current* text — every variant ever overwritten is gone from
it. And GHL's Workflows API exposes **no message content at all** (verified against their
OpenAPI spec, v2 and v3: `GET /workflows/` returns only `id/name/status/version/dates`).

So the **sent-message log is the only surviving record of what was tested.** Do not go
looking for copy in workflows, campaigns, or templates. It is not there. It never will be.

## Run it

```bash
python tools/ghl_mine.py --client digital-resource       # ~3 min, no questions asked
```

Credentials and location IDs come from `clients/registry.json` (which reads tokens from the
MCP servers in `~/.claude.json` — no secrets in the repo). If a client's `sms.locationId` is
`null`, it needs a read-only Private Integration Token first; the script prints the exact
command.

Writes to that client's `output/`:
- `sms-copy-history.csv` — every copy unit, incl. the long tail of one-off manual texts
- `batches.json` — the real variants (≥20 prospects), ready to render or promote

## The five rules (violate any one and the numbers lie)

| # | Rule | What breaks if you don't |
|---|---|---|
| 1 | **T1 + T2 are ONE unit.** Two texts ship together, ~13s apart. The *batch* is the atom — same as `winners.csv` (`raw_T1`, `raw_T2`). | Score them separately and a reply gets credited to the last text sent, so **T1 shows ~0% reply**. You'd rewrite the wrong message. |
| 2 | **Judge reply % against opt-out %.** Never rank on reply alone. | A variant with opt-outs ≥ replies is a **list-burner**, not a winner. The miner flags these; Digital Resource was scaling one. |
| 3 | **Era-scope every sub-account.** GHL sub-accounts get reused between clients. | Digital Resource's location previously held another business — 104k of its 155k messages weren't theirs. Mixing them in poisons everything. |
| 4 | **De-merge exactly, never fuzzily.** Substitute each contact's *own* field values back out. | Fuzzy similarity can't tell `Hi Cindy`/`Hi Bartholomew` (same copy) from `could I`/`can I` (**a real test**) — it silently merges two experiments into one. |
| 5 | **Batch #2 is retargeting**, median ~54 days later — a genuine sequence step, not part of the initial send. | Fold it into batch #1 and you'll blame the copy for a follow-up's numbers. |

## Reading the output

- `send` — `initial` (the first batch) or `retarget` (a second batch, weeks later)
- `T1` / `T2` — the structural copy, merge fields restored to `{{slots}}`
- `prospects` — people who got this exact copy unit (**not** texts sent)
- `reply_pct` — genuine human replies. STOP/unsubscribe is counted separately as `optout_pct`.
- `burner` — **true = opt-outs ≥ replies. Kill it, don't scale it.**
- Ignore variants under ~20 prospects — those are reps' one-off manual texts, not campaign copy.

A high-volume variant with a mediocre reply rate is the most expensive thing in the file:
it means the client is **scaling the wrong copy**. Look for that first — it's usually the
single most actionable finding, and it's what the strategist actually wants to know.

## What you do with it

- **Before drafting** — check whether an angle has already been tried, and how it did. Feed
  the winners into `sms-draft` as evidence instead of guessing.
- **Promote to the playbook** — a proven unit can go into `sms-playbook/winners.csv`. The data
  columns map 1:1 (`raw_T1`, `raw_T2`, `char_T1`, `char_T2`). The **judgment** columns
  (`lever`, `pattern`, `what_carries`, `mechanism_line`, `pattern_interrupt`, `why_it_worked`)
  are the strategist's — draft them as a **strawman to redline, never as fact**.
- **Losers too.** A burner belongs in `losers.csv` with the real `why_it_failed`.

## What this skill does not do

Does **not** write copy (that's `sms-draft`). Does **not** send anything — every token is
read-only by design. Does **not** pick the winner: it hands over evidence, the strategist
decides. Does **not** invent a `why_it_worked` — that's judgment, and it's the strategist's.

See `references/platform-notes.md` for the GHL API landmines (they will cost you an hour each
if you rediscover them).
