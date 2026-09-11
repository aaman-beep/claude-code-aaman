# Email playbook

The cold-**email** counterpart to `sms-playbook/`. A cross-client, offer-blind store of email copy that **won** or **lost**, with a prose autopsy on each so future drafts QA against real outcomes — not vibes. This is the seed; it grows one A/B at a time.

**Started 2026-07-29** with the Kynship Health & Wellness UK A/B (first clean email A/B we've read). Deep record for that entry lives at `clients/kynship/output/2026-07-29-Kynship-email-AB-loss.md`.

## Files
- `winners.csv` — email variants that pulled replies. IDs `EW1, EW2 …`
- `losers.csv` — email variants that didn't. IDs `EL1, EL2 …`

## Columns (both files share these; last column differs)
| column | meaning |
|---|---|
| `id` | `EW#` (winners) / `EL#` (losers) |
| `client` | client name |
| `campaign` | EmailBison campaign (id + name) the variant ran in |
| `subject` | subject line (spintax rendered) |
| `body` | full email body, paragraphs separated by ` / ` |
| `offer` | what the client sells / the mechanism category |
| `niche/sub-niche` | target segment |
| `sophistication` | buyer market sophistication (low / mid / high) |
| `lever` | psychological lever(s) — Case, Unique, FOMO, Social proof, etc. |
| `mechanism_line` | the "how we did it" line — **the axis most A/Bs turn on** |
| `cta` | the ask |
| `sends` | emails sent (this arm) |
| `replies` | replies (this arm) |
| `reply_pct` | replies / sends |
| `why_it_worked` / `why_it_didnt_work` | prose autopsy — the richest field; always read it |

## Standing lesson (provisional — from EL1/EW1)
On **cold email**, a **higher-level / abstract mechanism** (buyer projects their own win onto it) + a natural secondary outcome tends to beat a **specific, granular / throughput mechanism** — the *opposite* of what often carries on **SMS**. Channel-dependent; re-test per campaign before treating as a rule. Sample size is small (~505/arm) — one round is a signal, not a law.

> Note: `sms-playbook/` never shipped a column README; this file is the convention going forward for both playbooks.
