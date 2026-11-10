# Data gotchas (all learned the hard way, Oct 2026)

**GHL**
- Two accounts. `ghl-scaletopia-legacy` (UqMcuYNiET94KiGWH5Ec) sends from A2P local numbers (619, 479, 559...). `ghl-scaletopia` (TYVYHj7lX8bamHkOKz4s) is toll-free and was shared with Velox before Aug 3 2026. Always pull both.
- The message export silently returns empty or short days when hit in parallel, and can even report `total` 0 for a busy day (Oct 27 2026: 0 twice, then 3,806). The script compares against GHL's own `total`, retries, and only accepts an empty day after 5 empty tries. If a weekday still shows 0 texts while Evergreen has SMS replies that day, re-run.
- Speed (Oct 29 2026): the old script took ~6.5 min, 4 of it sleeping on empty weekend/today/toll-free days. Now the two accounts pull in parallel (one worker each), finished non-empty days and weekends are cached in /tmp/scaletopia-daily/ghl_cache, and only past weekdays get the 5 slow retries when empty. ~40s with cache, ~75s cold. Running both accounts at once can glitch the toll-free day to 0, which is why weekday empties still retry on both accounts.
- Follow-up batches: check how many went to people who already replied (Oct 27: 16 of 749, incl. 4 unbooked warm) and blank {company} in the follow-up text too, not only text 1. If you call it yourself: `limit` must be 10 or more (limit=1 gives 422).
- Each lead gets text 1 + text 2 about 1 minute apart. Batches = workflow texts to one contact within 5 minutes. Follow-ups are a later batch.
- `source` = "workflow" for campaign sends, "app" for Kylie's manual replies. Every message has a userId, so don't use that.
- Company merge field: blank company shows as "been looking at , had an idea". Count it every day.
- Text 1 over 160 characters (or with a non-breaking space) bills as 2 segments. Cost is ~2.3c a text, ~5c a person.

**EmailBison**
- Campaign stats: `POST /api/campaigns/{id}/stats` with start/end date. Workspace day stats: `GET /api/workspaces/v1.1/stats`.
- `interested` is always 0 (nobody tags replies). Read the replies.
- Most replies are out-of-office. The script filters the common ones; read what's left.
- Sender inboxes: 111 Google inboxes live (Sep 29 batch 51, Oct 15 batch 30, Scaletopia-branded 30). The 150 Outlook inboxes are dead.

**Evergreen**
- `/period?window=yesterday` lags a day and its "sent" is far below GHL. Never quote it.
- `/deals` needs `?limit=5000`. Booked = `meeting_booked_at`, not the stage. Some warm replies are missing or labelled oddly.

**Calendar**
- Calls booked on the prospect's own link (OnceHub, Teams, Calendly) may not be on Aaman's calendar. Search by name and check Gmail for the invite.
- UK time: BST until the last Sunday of October, then GMT. US clocks change a week later, so ET is 4 hours behind UK for that week.
