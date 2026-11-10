# Side questions: how to answer them fast

Run everything from the repo root. `SC` = `python3 .claude/skills/scaletopia-daily-stats/scripts/side_checks.py`.

| Question | How |
|---|---|
| Were people texted twice / re-hit? | `SC rehit <day>`. Shows per first-text copy how many were texted in the last 45 days, and who got two different first texts the same day. |
| How many emails went out? | `SC email <start> [end]`. GHL is not involved. Never quote Evergreen's "sent". |
| Are the inboxes OK? How many can we send? | `SC inboxes`. Capacity = sum of daily limit on connected inboxes. Outlook inboxes are dead. |
| What copy does a workflow send, from which number? | GHL MCP `ghl-scaletopia-legacy`: `search-workflows` (status published), then `get-workflow-definition` on the id. Text bodies are the `sms` actions; the number is `settings.senderAddress.from_number`. |
| Which campaigns are live in email and how many leads are left? | EmailBison MCP `emailbison-scaletopia`: `list_campaigns`, then `get_campaign_stats`. |
| What did a lead actually receive? | Look the contact up in GHL (`ghl-scaletopia-legacy`, search contacts by phone) and read the conversation. |

## Numbers and fields (Nov 2026)
- GHL legacy location `UqMcuYNiET94KiGWH5Ec` sends from 619 (+16194302534: old tech workflow + new lane), 314 (+13142750177: tech relaunch "Space Enriched", reminders), 479 (+14794580483: agencies).
- Custom fields: `EzxOaFAbB0O1mrs2t152` text 2 line / ICP signal (full SMS sentence, do not reuse in email), `Sy45XklJ5mBj6HsOOAEu` job title, `yde2YogBmy4QFwnwXp83` workflow/list name, `HcWJhqAl4SDL9d96Ca5b` variant.
- Two workflows reading the same tag will text the same person twice from two numbers. Before turning one on, check the other is off or excludes those contacts.

## Rules
- Rates are per 1,000 people, never per text.
- A warm reply nobody answered goes to the top of the fix list.
- Copy and replies are quoted exactly. No em dashes.
