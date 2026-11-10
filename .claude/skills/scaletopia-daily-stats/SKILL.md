---
name: scaletopia-daily-stats
description: Daily stats breakdown of Scaletopia's OWN outbound (cold SMS from GHL + cold email from EmailBison) for one send day - sends by campaign and copy, every human reply judged warm or not, how each warm reply was handled, bookings, and what to do today. Use whenever Aaman or the GTM engineer asks "run yesterday's stats", "stats report for yesterday", "daily breakdown", "how did yesterday go", "do Friday's stats", "stat breakdown for <day>", or says we sent more volume and wants to know if it worked. Scaletopia only (not client accounts). For the weekly artifact report use the weekly format instead.
---

# Scaletopia daily stats breakdown

One send day (US Pacific), replies counted up to today. GHL is the denominator. Evergreen is a cross-check only.
The script pulls everything; you judge the replies, check handling and the calendar, then write the report.

## Steps

**1. Pick the day.** "Yesterday" = the previous weekday (Monday's run covers Friday). A named day = that date.
Replies always run through today.

**2. Pull the data.** Run from the repo root (it reads the GHL/EmailBison keys from `~/.claude.json` and the
Evergreen key from `.env`; never print them. If keys are missing, run `bash tools/setup_scaletopia_stats.sh`):
```
python3 .claude/skills/scaletopia-daily-stats/scripts/daily_pull.py <YYYY-MM-DD>
```
Takes 1-3 minutes. Check the first line: "ours / GHL total" must match for every day. If a day shows 0 on a
weekday when you know texts went out, re-run (GHL's export returns empty days under load).
Read `references/data-gotchas.md` the first time in a session.

**3. Judge every human reply.** Use `references/judging.md`. Write one line per reply: warm / engaged /
referral / not a lead (left, wrong number, not the decision maker) / no. Quote the reply. Drop anyone on
anyone on `references/do-not-chase.md`. Count warm per 1,000 people by list.

**4. Check handling for every warm reply.** From "US AFTER": answered? times offered? booked? Flag any
"NO REPLY FROM US", any "I've sent the email" handoff with no times in the thread, and any booked call.
Then search the calendar for each booked or near-booked name (narrow `search_events` by name or company).
Flag a booking that isn't on the calendar, an invite not accepted, and anyone disqualified who is still booked.
If you have no access to Aaman's calendar, skip the calendar search and list the booked names for him to check.

**5. Compare.** Warm per 1k people against the previous few days of the same list and copy (use the
log in `local/daily-log.md` or re-run the script for an earlier day if needed). Note failed %, blank company count,
opt-outs, and anything new in the copy (a new text 2, a new list).

**6. Write the report** in the format in `references/report-format.md`. Short. Tables for sends and
replies, names and verbatim quotes for warm ones, a short "fix today" list. No em dashes, plain words.

**7. Check the pipeline board, then offer updates.** (Skip if you have no edit access to the board; list the new warm replies instead.) Since 2026-10-27 the master list is the pipeline board
artifact https://claude.ai/artifact/9dBpsP4DvtNwP58EHuya4A (db collection `deals`, stages 1 Decision pending,
2 Pilot, 3 Next stage, 4 Calls, 5 Warm replies, 6 Nurture). Read it with ArtifactData, say which new warm
replies are already on it, and offer to add the rest (stage 5, or 4 if booked). Aaman picks; write with
ArtifactData pinned to `if_version`, never by republishing. The attack list Google Sheet
(id `1Y8NB_c73RamwRfaLr7rpLmW53UjAAdHdh2OyC2VrQTw`) is the older list: update it only if he asks.

**8. Save one line** to `local/daily-log.md` in this skill folder (date, people, warm, what broke). That folder is gitignored: the repo is public, so prospect names never get committed.

**Side questions** (re-hits, emails sent, inbox health, which workflow sends what copy): see `references/side-questions.md`.

## Rules
- GHL counts are the truth for sends. Never quote Evergreen's "sent". Evergreen booked/positives are a cross-check.
- People, not texts, for rates ("warm per 1k people"). Texts and segments only for cost.
- A warm reply nobody answered goes at the top of the "fix today" list.
- Don't recommend chasing anyone Aaman removed or disqualified.
- Verbatim copy and replies, no claim-accuracy warnings on the copy (his call).
